# AWS IAM Access Keys for all Users with Threshold older than creation date.

import boto3
from datetime import datetime, timezone

# Threshold In Days
ThresholdInDays = 30

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def diff_dates(date1, date2):
    return abs(date2 - date1).days

resource = boto3.resource('iam')
client = boto3.client("iam")

KEY = 'LastUsedDate'

print("================================================================================")
print("IAM Access Keys List created than " + str(ThresholdInDays) + " Days...")
print("================================================================================")

for user in resource.users.all():
    Metadata = client.list_access_keys(UserName=user.user_name)
    if Metadata['AccessKeyMetadata']:
        for key in user.access_keys.all():

            AccessId = key.access_key_id
            Status = key.status
            CreatedDate = key.create_date

            numOfDays = diff_dates(utc_to_local(datetime.utcnow()), utc_to_local(CreatedDate))
            LastUsed = client.get_access_key_last_used(AccessKeyId=AccessId)

            if ( numOfDays > ThresholdInDays ):
                print("User:", user.user_name,  "Key:", AccessId, "Age of Key:", numOfDays, "Days")

print("================================================================================")
