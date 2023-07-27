#!/usr/bin/python3

print("content-type: text/html")
print()

import boto3
import subprocess as sp
import cgi

form = cgi.FieldStorage()
instance_id  = form.getvalue("launch")
#instance_id  = "i-075bf7f41e5097097"

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

# Function to start an EC2 instance
def start_ec2_instance(instance_id):
    try:
        ec2_client.start_instances(InstanceIds=[instance_id])
        print(f"Started instance with ID: {instance_id}")
    except Exception as e:
        print(f"Failed to start instance with ID: {instance_id}. Error: {e}")

# Prompt user to enter the instance ID to start

# Check if the instance exists and is stopped before starting it
found_instance = False
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        if instance['InstanceId'] == instance_id:
            state = instance['State']['Name']
            if state == 'stopped':
                start_ec2_instance(instance_id)
            else:
                print(f"The instance with ID {instance_id} is already running.")
            found_instance = True
            break

if not found_instance:
    print(f"No stopped instance found with ID: {instance_id}")
