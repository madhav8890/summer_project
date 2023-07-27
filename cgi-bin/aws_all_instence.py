#!/usr/bin/python3

print("content-type: text/html")
print()

import boto3

# Set up your AWS login credentials
aws_access_key_id = 'AKIAXCJPOLASDLP5KSOH'
aws_secret_access_key = 'Fbx9PpzHnDNi7IXlKePIdjCRRoE9/0IjfriuW8XU'
region_name = 'ap-south-1'

# Create a session
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Create an EC2 client
ec2_client = session.client('ec2')

# Describe EC2 instances
response = ec2_client.describe_instances()

# Extract and print instance details
def print_instance_details(instance):
    instance_id = instance['InstanceId']
    state = instance['State']['Name']

    # Get instance name if available
    name = ''
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            name = tag['Value']
            break
    
    print("<pre>")
    print(f"Instance ID: {instance_id}")
    print(f"State: {state}")
    print(f"Name: {name}")
    print('---')
    print("</pre>")
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print_instance_details(instance)
