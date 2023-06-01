import boto3

def copy_s3_objects(source_bucket, source_prefix, destination_bucket, destination_prefix):
    s3 = boto3.client('s3')

    # Get the list of objects in the source folder
    response = s3.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix)

    # Iterate through the objects
    for obj in response['Contents']:
        # Get the object's key (filename)
        key = obj['Key']

        # Get all versions of the object
        versions = s3.list_object_versions(Bucket=source_bucket, Prefix=key)['Versions']

        # Iterate through the versions
        for version in versions:
            # Get the version ID
            version_id = version['VersionId']

            # Copy the object to the destination bucket with the same key and version ID
            s3.copy_object(
                Bucket=destination_bucket,
                Key=key,
                CopySource={
                    'Bucket': source_bucket,
                    'Key': key,
                    'VersionId': version_id
                },
                MetadataDirective='COPY'
            )

    print('S3 objects copied successfully!')

# Usage example
source_bucket = 'your-source-bucket'
source_prefix = 'folder-x/'
destination_bucket = 'your-destination-bucket'
destination_prefix = 'folder-y/'

copy_s3_objects(source_bucket, source_prefix, destination_bucket, destination_prefix)
