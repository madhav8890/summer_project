#!/usr/bin/python3

print("content-type: text/html")
print()

import boto3
import subprocess as sp
import cgi

form = cgi.FieldStorage()
instance_id  = form.getvalue("detail")

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

# Function to print instance details
def print_instance_details(instance):
    instance_id = instance['InstanceId']
    state = instance['State']['Name']

    # Get instance name if available
    name = ''
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            name = tag['Value']
            break

    print(f"Instance ID: {instance_id}")
    print(f"State: {state}")
    print(f"Name: {name}")
    print('---')

# Describe EC2 instances
response = ec2_client.describe_instances()

# Get the instance ID from user input

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        if instance['InstanceId'] == instance_id:
            print_instance_details(instance)
            # Get security, networking, storage, and monitoring details
            security_groups = instance.get('SecurityGroups', [])
            network_interfaces = instance.get('NetworkInterfaces', [])
            block_device_mappings = instance.get('BlockDeviceMappings', [])
            monitoring = instance.get('Monitoring', {})

            # Print security group details
            print("Security Groups:")
            for security_group in security_groups:
                group_id = security_group['GroupId']
                group_name = security_group['GroupName']
                print(f"  Group ID: {group_id}")
                print(f"  Group Name: {group_name}")
                print('---')

            # Print network interface details
            print("Network Interfaces:")
            for network_interface in network_interfaces:
                interface_id = network_interface['NetworkInterfaceId']
                private_ip = network_interface['PrivateIpAddress']
                public_ip = network_interface.get('Association', {}).get('PublicIp')
                print(f"  Interface ID: {interface_id}")
                print(f"  Private IP: {private_ip}")
                print(f"  Public IP: {public_ip}")
                print('---')

            # Print block device mapping details
            print("Block Device Mappings:")
            for block_device_mapping in block_device_mappings:
                device_name = block_device_mapping['DeviceName']
                volume_id = block_device_mapping['Ebs']['VolumeId']
                print(f"  Device Name: {device_name}")
                print(f"  Volume ID: {volume_id}")
                print('---')

            # Print monitoring details
            state = monitoring.get('State', '')
            print("Monitoring:")
            print(f"  State: {state}")
            print('---')

            break
    else:
        continue
    break
else:
    print(f"No instance found with ID: {instance_id}")
