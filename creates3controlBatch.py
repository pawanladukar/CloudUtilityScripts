import boto3
import json

# Configure the AWS credentials and region
session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
    region_name='YOUR_REGION'
)

# Create an S3 Batch client
s3batch_client = session.client('s3control', region_name='YOUR_REGION')

# Define the parameters for the batch job
account_id = 'YOUR_AWS_ACCOUNT_ID'
job_name = 'YOUR_JOB_NAME'
bucket_name = 'YOUR_BUCKET_NAME'
report_prefix = 'YOUR_REPORT_PREFIX/'
existing_job_role_arn = 'arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/YOUR_EXISTING_ROLE'
existing_report_arn = f'arn:aws:s3:::{bucket_name}/{report_prefix}'

# Generate S3 manifest using manifestGenerator method
manifest_file = 'manifest.json'
manifest_generator = {
    'spec': {
        'fields': ['Bucket', 'Key'],
        'format': 'S3BatchOperations_CSV_20180820',
        'recordDelimiter': '\n',
        'recordFormat': 'JSON',
    },
    'entries': [
        {'url': f's3://{bucket_name}/file1.txt'},
        {'url': f's3://{bucket_name}/file2.txt'}
    ]
}

# Create the manifest file
with open(manifest_file, 'w') as f:
    json.dump(manifest_generator, f)

# Create the S3 Batch job
response = s3batch_client.create_job(
    AccountId=account_id,
    ConfirmationRequired=False,
    Operation={
        'S3PutObjectCopy': {
            'TargetResource': existing_report_arn,
            'CannedAccessControlList': 'bucket-owner-full-control'
        }
    },
    Priority=1,
    Report={
        'Bucket': bucket_name,
        'Prefix': report_prefix,
        'Format': 'Report_CSV_20180820',
        'Enabled': True,
        'ReportScope': 'AllTasks'
    },
    RoleArn=existing_job_role_arn,
    Manifest={
        'Spec': {
            'Location': {
                'S3Location': {
                    'BucketArn': f'arn:aws:s3:::{bucket_name}',
                    'Key': manifest_file
                }
            },
            'ManifestGenerator': {
                'RoleArn': existing_job_role_arn,
                'JobTemplate': {
                    'Name': 'S3BatchOperations_CSV_20180820',
                    'Version': '1.0'
                }
            }
        }
    }
)

# Print the response from the create_job API
print(response)
