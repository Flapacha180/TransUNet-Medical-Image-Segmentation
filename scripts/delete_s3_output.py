import boto3

s3 = boto3.resource('s3', region_name='us-east-2')
bucket = s3.Bucket('lab-sagemaker-bucket-879654127886')
deleted = bucket.objects.filter(Prefix='transunet/test_output/lab-transunet-test-v1/').delete()
print("Deleted S3 output for lab-transunet-test-v1")
