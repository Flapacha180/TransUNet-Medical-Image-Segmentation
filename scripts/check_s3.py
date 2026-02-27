import boto3
s3 = boto3.client('s3', region_name='us-east-2')
r = s3.list_objects_v2(Bucket='lab-sagemaker-bucket-879654127886', Prefix='transunet/data/test_vol_h5', MaxKeys=5)
items = r.get('Contents', [])
if items:
    for o in items:
        print(o['Key'])
else:
    print('EMPTY - test data not uploaded yet')
