import boto3

s3 = boto3.resource('s3')
bucket_tagging = s3.BucketTagging('san-s3-2019-22-11')
tags = bucket_tagging.tag_set
tags.append({'Key':'Owner', 'Value':"Sanket"})
Set_Tag = bucket_tagging.put(Tagging={'TagSet':tags})

#setup_bucket("s3","san-s3-2019-22-11","san")