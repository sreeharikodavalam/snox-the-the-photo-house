import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_s3(local_file_path, s3_file_name, bucket_name='snoxpro', extra_args=None):
    # AWS credentials (ensure your IAM user has the necessary permissions)
    access_key = 'AKIAQJETKX7INNXO2BDR'
    secret_key = 'nyyRg2sF64wfbaurfZ1HZOrfow2MDdlx/h3fPFYq'

    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    if extra_args is None:
        extra_args = {'error': 'No data'}
    try:
        # Upload the file
        s3.upload_file(local_file_path, bucket_name, s3_file_name)
        print(f"Upload successful: {s3_file_name}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

# Example usage
# local_file_path = 'path/to/local/file.jpg'
# bucket_name = 'your-s3-bucket-name'
# s3_file_name = 'path/in/s3/file.jpg'

# upload_to_s3(local_file_path, bucket_name, s3_file_name)
