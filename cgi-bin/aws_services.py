#!/usr/bin/python3

import cgi
import boto3

# Set up your AWS login credentials
aws_access_key_id = 'AKIAVQKPBMJSVIIIFP6X'
aws_secret_access_key = 'MdGImkDAfjmx/tOCtgl2DHVjLfh49BdTWnbx9idU'
region_name = 'ap-south-1'

# Create a session
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Create an EC2 client
ec2_client = session.client('ec2')

# Create an IAM client
iam_client = session.client('iam')

# Create an S3 client
s3_client = session.client('s3')

# Create a Lambda client
lambda_client = session.client('lambda')

# Create API Gateway client
api_gateway_client = session.client('apigateway')

# Function to start an EC2 instance
def start_ec2_instance(instance_id):
    try:
        ec2_client.start_instances(InstanceIds=[instance_id])
        return f"Started instance with ID: {instance_id}"
    except Exception as e:
        return f"Failed to start instance with ID: {instance_id}. Error: {e}"

# Function to stop an EC2 instance
def stop_ec2_instance(instance_id):
    try:
        ec2_client.stop_instances(InstanceIds=[instance_id])
        return f"Stopped instance with ID: {instance_id}"
    except Exception as e:
        return f"Failed to stop instance with ID: {instance_id}. Error: {e}"

# Function to describe EC2 instances
def describe_ec2_instances():
    response = ec2_client.describe_instances()
    instances_info = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            name = ""
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    name = tag['Value']
                    break
            instance_info = {
                'Instance ID': instance_id,
                'State': state,
                'Name': name
            }
            instances_info.append(instance_info)

    return instances_info


# Function to create a new IAM user
def create_iam_user(username):
    try:
        response = iam_client.create_user(UserName=username)
        return f"Created IAM user: {username}"
    except Exception as e:
        return f"Failed to create IAM user: {username}. Error: {e}"

# Function to list existing IAM users
def list_iam_users():
    response = iam_client.list_users()
    users_info = ""
    for user in response['Users']:
        username = user['UserName']
        users_info += f"IAM User: {username}<br>"
    return users_info

# Function to create a new S3 bucket
def create_s3_bucket(bucket_name):
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        return f"Created S3 bucket: {bucket_name}"
    except Exception as e:
        return f"Failed to create S3 bucket: {bucket_name}. Error: {e}"

# Function to list existing S3 buckets
def list_s3_buckets():
    response = s3_client.list_buckets()
    buckets_info = ""
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        buckets_info += f"S3 Bucket: {bucket_name}<br>"
    return buckets_info

# Function to create a new Lambda function
def create_lambda_function(function_name, runtime='python3.10', handler='lambda_function.lambda_handler', role_arn='YOUR_DEFAULT_ROLE_ARN', code_path='YOUR_DEFAULT_CODE_PATH'):
    # Use default values if not provided by the user
    if role_arn == 'YOUR_DEFAULT_ROLE_ARN':
        # Provide the ARN of the IAM role with Lambda execution permissions
        role_arn = 'arn:aws:iam::378659758693:user/iamuser'
    
    if code_path == 'YOUR_DEFAULT_CODE_PATH':
        # Provide the path to your Lambda function code ZIP file
        code_path = '/path/to/your/lambda_function.zip'

    with open(code_path, 'rb') as f:
        code_content = f.read()
    
    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler,
            Code={'ZipFile': code_content},
        )
        return f"Created Lambda function: {function_name}"
    except Exception as e:
        return f"Failed to create Lambda function: {function_name}. Error: {e}"

# Function to list existing Lambda functions
def list_lambda_functions():
    response = lambda_client.list_functions()
    functions_info = ""
    for function in response['Functions']:
        function_name = function['FunctionName']
        functions_info += f"Lambda Function: {function_name}<br>"
    return functions_info

# Function to create a new API in API Gateway
def create_api_gateway(api_name):
    try:
        response = api_gateway_client.create_rest_api(name=api_name)
        api_id = response['id']
        return f"Created API Gateway API: {api_name}, API ID: {api_id}"
    except Exception as e:
        return f"Failed to create API Gateway API: {api_name}. Error: {e}"

# Function to list existing APIs in API Gateway
def list_api_gateways():
    response = api_gateway_client.get_rest_apis()
    apis_info = ""
    for api in response['items']:
        api_name = api['name']
        api_id = api['id']
        apis_info += f"API Gateway API: {api_name}, API ID: {api_id}<br>"
    return apis_info
# ... (existing imports and functions)

def generate_html_page():
    form = cgi.FieldStorage()

    print("Content-type: text/html\n")
    print("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Boto3 Menu</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    margin: 20px;
                }
                h1 {
                    
                    text-align: center;
                }
                form {
                    margin-bottom: 20px;
                    text-align: center;
                }
                p {
                    margin-bottom: 5px;
                }
                label {
                    margin-right: 10px;
                }
                input[type="radio"] {
                    margin-right: 5px;
                }
                input[type="text"] {
                    padding: 5px;
                }
                input[type="submit"] {
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    border-radius: 4px;
                    cursor: pointer;
                }
                table {
                    border-collapse: collapse;
                    width: 100%;
                    border: 1px solid #ddd;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #f2f2f2;
                }
                .output {
                    margin-top: 20px;
                    background-color: #fff;
                    border: 1px solid #ddd;
                    padding: 10px;
                }
            </style>
        </head>
        <body>
            <h1>Boto3 Menu</h1>
            <form method="post" action="">
                <p>Select an option:</p>
                <label><input type="radio" name="option" value="start">Start EC2 Instance</label>
                <label><input type="radio" name="option" value="stop">Stop EC2 Instance</label>
                <label><input type="radio" name="option" value="describe">Describe EC2 Instances</label>
                <label><input type="radio" name="option" value="create_iam">Create IAM User</label>
                <label><input type="radio" name="option" value="list_iam">List IAM Users</label>
                <label><input type="radio" name="option" value="create_s3">Create S3 Bucket</label>
                <label><input type="radio" name="option" value="list_s3">List S3 Buckets</label>
                <label><input type="radio" name="option" value="create_lambda">Create Lambda Function</label>
                <label><input type="radio" name="option" value="list_lambda">List Lambda Functions</label>
                <label><input type="radio" name="option" value="create_api">Create API Gateway API</label>
                <label><input type="radio" name="option" value="list_api">List API Gateway APIs</label>
                <input type="submit" value="Submit">
            </form>
    """)

    if "option" in form:
        option = form.getvalue("option")
        if option == "start":
            print("""
                <div class="output">
                    <form method="post" action="">
                        <p>Enter the instance ID to start:</p>
                        <input type="text" name="instance_id" required>
                        <input type="hidden" name="option" value="start">
                        <input type="submit" value="Start Instance">
                    </form>
            """)
            instance_id = form.getvalue("instance_id")
            print(f"<p>{start_ec2_instance(instance_id)}</p></div>")

        elif option == "stop":
            print("""
                <div class="output">
                    <form method="post" action="">
                        <p>Enter the instance ID to stop:</p>
                        <input type="text" name="instance_id" required>
                        <input type="hidden" name="option" value="stop">
                        <input type="submit" value="Stop Instance">
                    </form>
            """)
            instance_id = form.getvalue("instance_id")
            print(f"<p>{stop_ec2_instance(instance_id)}</p></div>")
        elif option == "describe":
            instances_info = describe_ec2_instances()
            print("""
                <div class="output">
                    <h2>EC2 Instance Details</h2>
                    <table>
                        <tr>
                            <th>Instance ID</th>
                            <th>State</th>
                            <th>Name</th>
                        </tr>
            """)
            for instance in instances_info:
                print("<tr>")
                for key, value in instance.items():
                    print(f"<td>{value}</td>")
                print("</tr>")
            print("""
                    </table>
                </div>
            """)
        elif option == "create_iam":
            # Form for creating a new IAM user
            print("""
                <div class="output">
                    <form method="post" action="">
                        <p>Enter the IAM user name to create:</p>
                        <input type="text" name="username" required>
                        <input type="hidden" name="option" value="create_iam">
                        <input type="submit" value="Create IAM User">
                    </form>
            """)
            username = form.getvalue("username")
            print(f"<p>{create_iam_user(username)}</p></div>")

        elif option == "list_iam":
            iam_users_info = list_iam_users()
            print(f"""
                <div class="output">
                    <h2>IAM Users</h2>
                    {iam_users_info}
                </div>
            """)
        elif option == "create_s3":
            print("""
                <div class="output">
                    <form method="post" action="">
                        <p>Enter the S3 bucket name to create:</p>
                        <input type="text" name="bucket_name" required>
                        <input type="hidden" name="option" value="create_s3">
                        <input type="submit" value="Create S3 Bucket">
                    </form>
            """)
            bucket_name = form.getvalue("bucket_name")
            print(f"<p>{create_s3_bucket(bucket_name)}</p></div>")
        elif option == "list_s3":
            s3_buckets_info = list_s3_buckets()
            print(f"""
                <div class="output">
                    <h2>S3 Buckets</h2>
                    {s3_buckets_info}
                </div>
            """)
        elif option == "create_lambda":
            # Form for creating a new Lambda function
            print("""
                <div class="output">
                    <form method="post" action="">
                        <p>Enter the Lambda function name to create:</p>
                        <input type="text" name="function_name" required>
                        <input type="hidden" name="option" value="create_lambda">
                        <input type="submit" value="Create Lambda Function">
                    </form>
            """)
            function_name = form.getvalue("function_name")
            print(f"<p>{create_lambda_function(function_name)}</p></div>")

        elif option == "list_lambda":
            lambda_functions_info = list_lambda_functions()
            print(f"""
                <div class="output">
                    <h2>Lambda Functions</h2>
                    {lambda_functions_info}
                </div>
            """)
        elif option == "create_api":
            print("""
                <div class="output">
                    <form method="post" action="">
                        <p>Enter the API Gateway API name to create:</p>
                        <input type="text" name="api_name" required>
                        <input type="hidden" name="option" value="create_api">
                        <input type="submit" value="Create API Gateway API">
                    </form>
            """)
            api_name = form.getvalue("api_name")
            print(f"<p>{create_api_gateway(api_name)}</p></div>")
        elif option == "list_api":
            api_gateways_info = list_api_gateways()
            print(f"""
                <div class="output">
                    <h2>API Gateway APIs</h2>
                    {api_gateways_info}
                </div>
            """)

        else:
            print("<div class='output'><p>Invalid option. Please select a valid option from the menu.</p></div>")

    print("""
        </body>
        </html>
    """)

def main():
    generate_html_page()

if __name__ == "__main__":
    main()
