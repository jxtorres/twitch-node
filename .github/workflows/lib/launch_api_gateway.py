

import boto3


def tryLaunchGateway(functionName, accountId, region):
    # Create an AWS client for the API Gateway service
    client = boto3.client('apigateway')


    # Get the list of REST APIs in the account
    response = client.get_rest_apis()

    # Iterate through the list of REST APIs
    for api in response['items']:
        # Check if the API has the name we are looking for
        if api['name'] == 'My API':
            # Return the ID of the matching REST API
            print("API Gateway API already created.")
            return

    print("Proceeding with API Gateway launch")

    # Create the REST API
    response = client.create_rest_api(
        name='My API',
        description='This is my API'
    )

    # Get the ID of the newly created REST API
    api_id = response['id']

    # Create a resource in the REST API
    response = client.create_resource(
        restApiId=api_id,
        parentId=api_id,
        pathPart='myresource'
    )

    # Get the ID of the newly created resource
    resource_id = response['id']

    # Create a method for the resource
    response = client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='GET',
        authorizationType='NONE'
    )

    # Create an integration for the method
    response = client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='GET',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f"arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/arn:aws:lambda:{region}:{accountId}:function:{functionName}/invocations"
    )

    #Deploy the REST API
    response = client.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )