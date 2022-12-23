

import deploy
import launch_api_gateway
import boto3

# Create an AWS client for the STS service
client = boto3.client('sts')

# Get the caller identity
response = client.get_caller_identity()

# Print the AWS account ID
accountId = (response['Account'])


deploy.update_lambda_function('my-api', 'app.zip', 'lib.zip')
launch_api_gateway.tryLaunchGateway('my-api', accountId, 'US-EAST-1')


print("Running deploy runner")