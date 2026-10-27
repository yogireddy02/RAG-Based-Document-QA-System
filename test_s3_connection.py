from src.s3_service import check_bucket_access

if __name__ == "__main__":
    success = check_bucket_access()

    if success:
        print("AWS S3 integration is ready!")
    else:
        print("Please check your AWS permissions and configuration.")