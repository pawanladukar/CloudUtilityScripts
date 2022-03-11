#!/bin/bash
# Script for Getting IAM User Access Keys List Older or Newer than ThresholdInDays provided.

IFS=$'\n'

# Number of Days listing older or newer IAM Access Keys
ThresholdInDays=30
OlderThan='yes'

cutoff=$(date -d "$ThresholdInDays days ago" +%s)

# Operand for Older or Newer (ThresholdInDays) listing.
Operand="older" # Choose older or newer - case sensitive. If entered wrong parameter it will display newer than keys.

if [[ $Operand == 'older' ]]
then
  Compare='<'
else
  Compare='>'
fi

echo "---------------------------------------------------------------------------------------------------------------------"
echo "IAM Access Keys List created $Operand than $ThresholdInDays Days..."
echo "---------------------------------------------------------------------------------------------------------------------"

# Iterating for Users in Account
for user in $(aws iam list-users --output text | cut -f7)
do
  # Iterating for Keys per users, this is required as a user can have multiple keys created/assgined.
  for keys in `aws iam list-access-keys --user-name $(echo $user) --output text`
  do
      UserCreateionDate=`echo $keys | cut -f3`
      UserCreateionCompareTimeStamp=`date --date=${UserCreateionDate} +%s`

      if (( $UserCreateionCompareTimeStamp $(echo $Compare) $cutoff ))
      then
        echo "User: ${user}"
        AccessKey=`echo $keys | cut -f2`
        CreationDays=$(( ($(date -d 'now' +%s)-$UserCreateionCompareTimeStamp)/60/60/24 ))
        Status=`echo $keys | cut -f4`
        echo "User: ${user}  AccessKey: ${AccessKey}  UserCreationDate: ${UserCreateionDate} AccountDaysOld: ${CreationDays} Status: ${Status}"
      fi
  done
done

echo "---------------------------------------------------------------------------------------------------------------------"
