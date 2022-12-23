import boto3

def update_lambda_function(function_name, source_zip_file, lib_zip_file, runtime='nodejs12.x', handler='app.handler'):
    client = boto3.client('lambda')

    # Check if the function exists
    functions = client.list_functions()
    function_exists = any(f['FunctionName'] == function_name for f in functions['Functions'])

    # If the function does not exist, create it
    if not function_exists:

        with open(lib_zip_file, 'rb') as f:
            libs = f.read()

            response = client.publish_layer_version(
                LayerName='my-layer',
                Description='My layer',
                CompatibleRuntimes=[runtime],
                Content={
                    'ZipFile': libs
                }
            )
            # client.create_function(
            #     FunctionName=function_name,
            #     Runtime=runtime,
            #     Role='arn:aws:iam::682749323867:role/lambda-twitch-node',
            #     Handler=handler,
            #     Code={'ZipFile': libs}
            # )

        with open(source_zip_file, 'rb') as f:
            code = f.read()
            client.create_function(
                FunctionName=function_name,
                Runtime=runtime,
                Role='arn:aws:iam::682749323867:role/lambda-twitch-node',
                Handler=handler,
                Code={'ZipFile': code},
                Layers=[response['LayerVersionArn']]
            )
        
    # If the function exists, update the code
    else:
        with open(zip_file, 'rb') as f:
            code = f.read()
        client.update_function_code(FunctionName=function_name, ZipFile=code)
