import boto3

# Configure the AWS credentials and region
session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
    region_name='YOUR_REGION'
)

# Create an S3 Batch client
s3batch_client = session.client('s3control')

# Define the parameters for the batch job
account_id = 'YOUR_AWS_ACCOUNT_ID'
job_name = 'YOUR_JOB_NAME'
manifest_location = 's3://YOUR_BUCKET_NAME/YOUR_MANIFEST_FILE.manifest'
existing_job_role_arn = 'arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/YOUR_EXISTING_ROLE'
existing_report_arn = 'arn:aws:s3:::YOUR_BUCKET_NAME/YOUR_REPORT_PREFIX/'

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
        'Bucket': 'YOUR_BUCKET_NAME',
        'Prefix': 'YOUR_REPORT_PREFIX/',
        'Format': 'Report_CSV_20180820',
        'Enabled': True,
        'ReportScope': 'AllTasks'
    },
    RoleArn=existing_job_role_arn,
    Manifest={
        'Spec': {
            'Format': 'S3BatchOperations_CSV_20180820',
            'Fields': ['Bucket', 'Key']
        },
        'Location': {
            'ObjectArn': manifest_location
        }
    },
    JobId=job_name
)

# Print the response from the create_job API
print(response)
