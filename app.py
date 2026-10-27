import boto3
from botocore.exceptions import BotoCoreError, ClientError

def test_aws_credentials():
    try:
        sts = boto3.client('sts', region_name='us-east-1')

        identity = sts.get_caller_identity()

        print("AWS connection successful!")
        print(f"AWS Account: {identity['Account']}")
        print(f"Identity ARN: {identity['Arn']}")


    except (BotoCoreError, ClientError) as error:
        print(f"AWS connection failed. Error: {error}")

if __name__ == "__main__":
    test_aws_credentials()