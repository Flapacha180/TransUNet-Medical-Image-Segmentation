#!/usr/bin/env python3
"""Download dataset files from Google Drive using gdown.

Requirements: 4.1, 4.2, 4.3, 4.4, 4.5

Usage:
    python download_data.py --dataset Synapse
    python download_data.py --dataset ACDC
"""
import argparse
import os
import sys

DATASET_CONFIG = {
    "Synapse": {
        "folder_url": "https://drive.google.com/drive/folders/1ACJEoTp-uqfFJ73qS3eUObQh52nGuzCd",
        "target_dir": os.path.join("data", "Synapse"),
    },
    "ACDC": {
        "folder_url": "https://drive.google.com/drive/folders/1KQcrci7aKsYZi1hQoZ3T3QUtcy7b--n4",
        "target_dir": os.path.join("data", "ACDC"),
    },
}


def create_data_directory(dataset_name: str) -> str:
    """Create the target data directory. Returns the path."""
    if dataset_name not in DATASET_CONFIG:
        raise ValueError(
            f"Unknown dataset '{dataset_name}'. Choose from: {list(DATASET_CONFIG.keys())}"
        )
    target_dir = DATASET_CONFIG[dataset_name]["target_dir"]
    os.makedirs(target_dir, exist_ok=True)
    return target_dir


def download_dataset(dataset_name: str) -> None:
    """Download a dataset from Google Drive using gdown."""
    config = DATASET_CONFIG[dataset_name]
    target_dir = create_data_directory(dataset_name)

    print(f"=== Downloading {dataset_name} Dataset ===")
    print(f"Target directory: {target_dir}")
    print(f"Google Drive folder: {config['folder_url']}")
    print()

    try:
        import gdown
    except ImportError:
        print("ERROR: gdown is not installed. Install it with: pip install gdown")
        sys.exit(1)

    try:
        gdown.download_folder(
            url=config["folder_url"],
            output=target_dir,
            quiet=False,
        )
        print(f"\nDownload complete. Files saved to: {target_dir}")
    except Exception as e:
        print(f"\nERROR: Download failed: {e}")
        print()
        print("=== Manual Download Instructions ===")
        print(f"1. Open this link in your browser:")
        print(f"   {config['folder_url']}")
        print(f"2. Download all files manually")
        print(f"3. Place them in: {os.path.abspath(target_dir)}")
        print()
        print("Common issues:")
        print("  - Google Drive download quota exceeded (wait 24h or use a different account)")
        print("  - Access restricted (request access from the dataset owner)")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Download TransUNet datasets from Google Drive")
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        choices=list(DATASET_CONFIG.keys()),
        help="Dataset to download (Synapse or ACDC)",
    )
    args = parser.parse_args()
    download_dataset(args.dataset)


if __name__ == "__main__":
    main()
