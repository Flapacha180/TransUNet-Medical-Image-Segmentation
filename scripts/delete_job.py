import boto3
sm = boto3.client('sagemaker', region_name='us-east-2')
sm.delete_training_job(TrainingJobName='lab-transunet-test-v1')
print('Deleted lab-transunet-test-v1')
