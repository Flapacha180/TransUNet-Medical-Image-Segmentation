import boto3
import sagemaker
from sagemaker.pytorch import PyTorch

BUCKET = 'lab-sagemaker-bucket-879654127886'
ROLE   = 'arn:aws:iam::879654127886:role/lab-sagemaker-role'

session = sagemaker.Session(boto_session=boto3.Session(region_name='us-east-2'))

estimator = PyTorch(
    entry_point='test.py',
    source_dir='..',
    role=ROLE,
    instance_type='ml.g4dn.xlarge',
    instance_count=1,
    framework_version='1.13',
    py_version='py39',
    sagemaker_session=session,
    max_run=3600,
    hyperparameters={
        'dataset':    'Synapse',
        'vit_name':   'R50-ViT-B_16',
        'n_skip':     3,
        'max_epochs': 150,
        'batch_size': 24,
        'img_size':   224,
    },
    output_path=f's3://{BUCKET}/transunet/test_output',
)

estimator.fit(
    inputs={
        'data':  f's3://{BUCKET}/transunet/data/test_vol_h5',
        'model': f's3://{BUCKET}/transunet/trained_model',
    },
    job_name='lab-transunet-test-v1',
    wait=False,
)

print(f"Job submitted: {estimator.latest_training_job.name}")
print("Monitor: https://us-east-2.console.aws.amazon.com/sagemaker/home?region=us-east-2#/jobs")
