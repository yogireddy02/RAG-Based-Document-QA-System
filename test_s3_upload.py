from pathlib import Path

from s3transfer import download

from src.s3_service import upload_document, s3_client, S3_BUCKET_NAME

LOCAL_FILE = Path("data/sample_document.txt")
OBJECT_KEY = "document-qa/uploads/sample_document.txt"

def main():
    if not LOCAL_FILE.exists():
        print(f"File not found: {LOCAL_FILE.resolve()}")
        return

    success = upload_document(
        file_path=str(LOCAL_FILE),
        object_key=OBJECT_KEY,
    )

    if not success:
        print("Upload failed.")
        return

    download_path = Path("data/downloaded_sample_document.txt")

    try:
        s3_client.download_file(
            S3_BUCKET_NAME,
            OBJECT_KEY,
            str(download_path),
        )

        print(f"Download successful: {download_path}")
        print("\nDownloaded content:\n")
        print(download_path.read_text(encoding="utf-8"))

    except Exception as error:
        print(f"Download failed: {error}")

if __name__ == "__main__":
    main()