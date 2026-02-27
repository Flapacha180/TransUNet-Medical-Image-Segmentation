#!/usr/bin/env python3
"""Download R50-ViT-B_16 pre-trained weights.
Requirements: 3.1, 3.2, 3.3

Usage:
    python download_weights.py
"""
import os
import sys

WEIGHT_DIR = os.path.join("model", "vit_checkpoint", "imagenet21k")
WEIGHT_FILE = os.path.join(WEIGHT_DIR, "R50-ViT-B_16.npz")


def main():
    print("=== Pre-trained ViT Weights Setup ===")

    os.makedirs(WEIGHT_DIR, exist_ok=True)

    if os.path.isfile(WEIGHT_FILE):
        size = os.path.getsize(WEIGHT_FILE)
        print(f"Weight file already exists: {WEIGHT_FILE} ({size:,} bytes)")
        return

    # Try gdown first (Google Drive mirror)
    try:
        import gdown
        print("Attempting download via gdown...")
        # Known Google Drive file ID for R50-ViT-B_16.npz
        gdown.download(
            id="1MIma5Iu0jMeFRzjVSKRcGRoGBq5XYkuV",
            output=WEIGHT_FILE,
            quiet=False,
        )
        if os.path.isfile(WEIGHT_FILE) and os.path.getsize(WEIGHT_FILE) > 1000:
            size = os.path.getsize(WEIGHT_FILE)
            print(f"Download complete: {WEIGHT_FILE} ({size:,} bytes)")
            return
    except Exception as e:
        print(f"gdown failed: {e}")
        if os.path.exists(WEIGHT_FILE):
            os.remove(WEIGHT_FILE)

    # Try direct URL
    import urllib.request
    urls = [
        "https://storage.googleapis.com/vit_models/imagenet21k/R50-ViT-B_16.npz",
    ]
    for url in urls:
        print(f"Trying: {url}")
        try:
            urllib.request.urlretrieve(url, WEIGHT_FILE)
            size = os.path.getsize(WEIGHT_FILE)
            print(f"Download complete: {WEIGHT_FILE} ({size:,} bytes)")
            return
        except Exception as e:
            print(f"  Failed: {e}")
            if os.path.exists(WEIGHT_FILE):
                os.remove(WEIGHT_FILE)

    print()
    print("=== Automatic download failed ===")
    print("Google Cloud Storage blocks anonymous access to ViT weights.")
    print()
    print("Please download R50-ViT-B_16.npz manually:")
    print("  1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install")
    print(f"  2. Run: gsutil cp gs://vit_models/imagenet21k/R50-ViT-B_16.npz {WEIGHT_DIR}\\")
    print()
    print(f"  Or place the file manually at: {os.path.abspath(WEIGHT_FILE)}")
    sys.exit(1)


if __name__ == "__main__":
    main()
