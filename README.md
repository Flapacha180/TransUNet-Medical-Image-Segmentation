# TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation

PyTorch reproduction of the paper [TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation](https://arxiv.org/abs/2102.04306) (Chen et al., 2021), trained and evaluated on the **Synapse multi-organ segmentation** dataset.

This repository reproduces the key results from the original paper, achieving **77.29% mean Dice score** and **30.71 mean HD95** on the Synapse dataset (paper reports 77.48% / 31.69).

---

## Table of Contents

- [Introduction](#introduction)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Data Preparation](#data-preparation)
- [Pre-trained Models](#pre-trained-models)
- [Training](#training)
- [Evaluation](#evaluation)
- [Results](#results)
- [AWS SageMaker](#aws-sagemaker)
- [Citation](#citation)
- [Acknowledgments](#acknowledgments)
- [License](#license)

---

## Introduction

TransUNet combines the strengths of Transformers and U-Net for medical image segmentation. It uses a Vision Transformer (ViT) as the encoder to capture global context, while leveraging a CNN-based decoder with skip connections to recover fine-grained spatial details. The hybrid ResNet-ViT encoder (R50-ViT-B/16) first extracts feature maps through a ResNet-50 backbone, then feeds them into a Transformer for self-attention modeling.

---

## Architecture

TransUNet follows an encoder-decoder design:

1. **Encoder**: Images are split into patches and processed by a hybrid ResNet-50 + ViT-B/16 backbone pre-trained on ImageNet-21k. The Transformer layers model long-range dependencies across patches.
2. **Decoder**: A cascaded upsampler progressively recovers the spatial resolution, guided by skip connections from the CNN encoder stages.
3. **Segmentation Head**: A 1x1 convolution produces per-pixel class predictions.

---

## Requirements

- Python >= 3.7
- PyTorch >= 1.9
- CUDA-compatible GPU (recommended)

Install dependencies:

```bash
pip install -r requirements.txt
```

Or use the provided setup script (requires [uv](https://docs.astral.sh/uv/)):

```bash
scripts\setup_env.bat
```

---

## Data Preparation

This project uses the **Synapse multi-organ segmentation** dataset (BTCV). The preprocessed data is publicly available:

- [BTCV preprocessed data](https://drive.google.com/drive/folders/1ACJEoTp-uqfFJ73qS3eUObQh52nGuzCd?usp=sharing)
- [ACDC data](https://drive.google.com/drive/folders/1KQcrci7aKsYZi1hQoZ3T3QUtcy7b--n4?usp=drive_link)

Download and place the data under `data/Synapse/`:

```
data/
  Synapse/
    train_npz/
      case0005_slice000.npz
      ...
    test_vol_h5/
      case0001.npy.h5
      ...
```

Alternatively, use the download script:

```bash
python scripts/download_data.py --dataset Synapse
```

---

## Pre-trained Models

Download Google pre-trained ViT models from [this link](https://console.cloud.google.com/storage/vit_models/) (R50-ViT-B_16 recommended):

```bash
wget https://storage.googleapis.com/vit_models/imagenet21k/R50+ViT-B_16.npz
mkdir -p model/vit_checkpoint/imagenet21k
mv R50+ViT-B_16.npz model/vit_checkpoint/imagenet21k/R50+ViT-B_16.npz
```

Or use the download script:

```bash
python scripts/download_weights.py
```

---

## Training

Train on the Synapse dataset with the default configuration (R50-ViT-B/16, batch size 24, 150 epochs):

```bash
CUDA_VISIBLE_DEVICES=0 python train.py --dataset Synapse --vit_name R50-ViT-B_16
```

Key hyperparameters can be adjusted via command-line arguments:

| Argument | Default | Description |
|---|---|---|
| `--batch_size` | 24 | Batch size per GPU |
| `--max_epochs` | 150 | Number of training epochs |
| `--base_lr` | 0.01 | Initial learning rate |
| `--img_size` | 224 | Input image resolution |
| `--n_skip` | 3 | Number of skip connections |

The batch size can be reduced to 12 or 6 to save memory (decrease `base_lr` linearly).

On Windows, you can use the provided script:

```bash
scripts\run_train.bat
```

---

## Evaluation

Run evaluation on the Synapse test set:

```bash
python test.py --dataset Synapse --vit_name R50-ViT-B_16
```

To save segmentation predictions as NIfTI files:

```bash
python test.py --dataset Synapse --vit_name R50-ViT-B_16 --is_savenii
```

On Windows:

```bash
scripts\run_test.bat
```

---

## Results

Reproduction results on the Synapse multi-organ segmentation dataset compared with the original paper:

| Method | Mean Dice (%) | Mean HD95 (mm) |
|---|---|---|
| TransUNet (paper) | 77.48 | 31.69 |
| **This reproduction** | **77.29** | **30.71** |

**Configuration**: R50-ViT-B/16, image size 224x224, batch size 24, 150 epochs, learning rate 0.01.

---

## AWS SageMaker

This repository includes scripts for training on AWS SageMaker. See the `scripts/` directory:

- `scripts/sagemaker_run.py` -- Submit a SageMaker training job
- `scripts/sagemaker_test.py` -- Submit a SageMaker evaluation job
- `scripts/sagemaker_trust_policy.json` -- IAM trust policy for the SageMaker execution role

Additional SageMaker utilities:

- `scripts/check_s3.py` -- Verify S3 bucket contents
- `scripts/delete_job.py` -- Delete a SageMaker training job
- `scripts/delete_s3_output.py` -- Clean up S3 output artifacts
- `scripts/get_logs.py` -- Fetch CloudWatch logs for a training job
- `scripts/get_results.py` -- Download results from a completed job

Hyperparameter configuration for SageMaker is stored in `config.yaml`.

---

## Citation

If you find this work useful, please cite the original paper:

```bibtex
@article{chen2024transunet,
  title={TransUNet: Rethinking the U-Net architecture design for medical image segmentation through the lens of transformers},
  author={Chen, Jieneng and Mei, Jieru and Li, Xianhang and Lu, Yongyi and Yu, Qihang and Wei, Qingyue and Luo, Xiangde and Xie, Yutong and Adeli, Ehsan and Wang, Yan and others},
  journal={Medical Image Analysis},
  pages={103280},
  year={2024},
  publisher={Elsevier}
}
```

```bibtex
@article{chen2021transunet,
  title={TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation},
  author={Chen, Jieneng and Lu, Yongyi and Yu, Qihang and Luo, Xiangde and Adeli, Ehsan and Wang, Yan and Lu, Le and Yuille, Alan L. and Zhou, Yuyin},
  journal={arXiv preprint arXiv:2102.04306},
  year={2021}
}
```

---

## Acknowledgments

- [Google ViT](https://github.com/google-research/vision_transformer)
- [ViT-pytorch](https://github.com/jeonsworld/ViT-pytorch)
- [segmentation_models.pytorch](https://github.com/qubvel/segmentation_models.pytorch)

---

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
