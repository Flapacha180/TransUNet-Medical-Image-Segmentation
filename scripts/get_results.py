import boto3

JOB_NAME = 'lab-transunet-test-v1'
BUCKET = 'lab-sagemaker-bucket-879654127886'
region = 'us-east-2'

sm = boto3.client('sagemaker', region_name=region)
logs = boto3.client('logs', region_name=region)
s3 = boto3.client('s3', region_name=region)

# Get log stream
log_group = '/aws/sagemaker/TrainingJobs'
try:
    streams = logs.describe_log_streams(logGroupName=log_group, logStreamNamePrefix=JOB_NAME)
    for stream in streams['logStreams']:
        events = logs.get_log_events(logGroupName=log_group, logStreamNamePrefix=JOB_NAME,
                                     logStreamName=stream['logStreamName'], startFromHead=False)
        for e in events['events']:
            msg = e['message']
            if any(k in msg for k in ['Mean class', 'mean_dice', 'mean_hd95', 'Testing performance', 'idx']):
                print(msg)
except Exception as ex:
    print(f"Log error: {ex}")

# Also check output tar on S3
print("\n--- S3 output ---")
r = s3.list_objects_v2(Bucket=BUCKET, Prefix=f'transunet/test_output/{JOB_NAME}')
for o in r.get('Contents', []):
    print(o['Key'], f"({o['Size']//1024} KB)")

# Stop/delete job (SageMaker training jobs can't be deleted, only stopped if running)
try:
    info = sm.describe_training_job(TrainingJobName=JOB_NAME)
    status = info['TrainingJobStatus']
    print(f"\nJob status: {status}")
    if status in ('InProgress', 'Stopping'):
        sm.stop_training_job(TrainingJobName=JOB_NAME)
        print("Job stopped.")
    else:
        print("Job already completed — no action needed (SageMaker does not support deleting training jobs).")
except Exception as ex:
    print(f"Job error: {ex}")
