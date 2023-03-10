

import boto3
import time


def tryLaunchGateway(functionName, accountId, region):
    # Create an AWS client for the API Gateway service
    apigateway = boto3.client('apigateway')

    # Get the list of REST APIs in the account
    response = apigateway.get_rest_apis()

    # Iterate through the list of REST APIs
    for api in response['items']:
        # Check if the API has the name we are looking for
        if api['name'] == 'MyAPI':
            # Return the ID of the matching REST API
            print("API Gateway API already created.")
            return

    print("Proceeding with API Gateway launch")
    
    # Create a new REST API
    response = apigateway.create_rest_api(
        name='MyAPI',
        description='This is my API'
    )
    api_id = response['id']

    time.sleep(20)  #6 mins + 100 sec


    # Get the list of resources for the API
    response = apigateway.get_resources(
        restApiId=api_id,  # Replace with the ID of your API
        limit=500
    )

    # Print the resource IDs
    firstResourceId = response['items'][0]['id']
        


    # Create a GET method on the root resource
    response = apigateway.put_method(
        restApiId=api_id,
        resourceId=firstResourceId,  # /
        httpMethod='GET',
        authorizationType='NONE'
    )

    # Create a Lambda function integration
    response = apigateway.put_integration(
        restApiId=api_id,
        resourceId=firstResourceId,
        httpMethod='GET',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f"arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/arn:aws:lambda:{region}:{accountId}:function:{functionName}/invocations"
    )


    #Deploy the REST API
    response = apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )