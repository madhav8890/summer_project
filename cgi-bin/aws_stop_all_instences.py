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

# Function to stop all EC2 instances
def stop_all_ec2_instances():
    try:
        # Describe EC2 instances to get their IDs
        response = ec2_client.describe_instances()
        instance_ids = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] == 'running':
                    instance_ids.append(instance['InstanceId'])

        # Stop all running instances
        if instance_ids:
            ec2_client.stop_instances(InstanceIds=instance_ids)
            print("Stopping all running instances.")
        else:
            print("No running instances found to stop.")
    except Exception as e:
        print(f"Failed to stop instances. Error: {e}")

# Stop all EC2 instances
stop_all_ec2_instances()
