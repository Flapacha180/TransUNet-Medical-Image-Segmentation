import boto3

JOB_NAME = 'lab-transunet-test-v1'
region = 'us-east-2'
logs = boto3.client('logs', region_name=region)

log_group = '/aws/sagemaker/TrainingJobs'
streams = logs.describe_log_streams(logGroupName=log_group, logStreamNamePrefix=JOB_NAME)

for stream in streams['logStreams']:
    print(f"=== {stream['logStreamName']} ===")
    token = None
    while True:
        kwargs = dict(logGroupName=log_group, logStreamName=stream['logStreamName'], startFromHead=True)
        if token:
            kwargs['nextToken'] = token
        resp = logs.get_log_events(**kwargs)
        for e in resp['events']:
            msg = e['message']
            if any(k in msg for k in ['Mean class', 'mean_dice', 'mean_hd95', 'Testing performance', 'idx ']):
                print(msg)
        if resp['nextForwardToken'] == token:
            break
        token = resp['nextForwardToken']
