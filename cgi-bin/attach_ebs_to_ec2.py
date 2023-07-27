#!/usr/bin/python3

print("content-type: text/html")
print()

import boto3
import cgi

form = cgi.FieldStorage()

instance_id = form.getvalue("id")
volume_size = form.getvalue("size")
volume_type = form.getvalue("type")


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

# Create an EC2 resource and client
ec2_resource = session.resource('ec2')
ec2_client = session.client('ec2')

# Function to add an EBS volume to an instance
def add_ebs_volume():

    # Create and attach the EBS volume to the instance
    response = ec2_client.create_volume(
        AvailabilityZone=region_name + 'a',  # Replace with your desired availability zone
        Size=volume_size,
        VolumeType=volume_type
    )

    volume_id = response['VolumeId']

    # Wait for the volume to be available
    waiter = ec2_client.get_waiter('volume_available')
    waiter.wait(VolumeIds=[volume_id])

    # Attach the volume to the instance
    response = ec2_client.attach_volume(
        Device='/dev/sde',  # Replace with the desired device name
        InstanceId=instance_id,
        VolumeId=volume_id
    )

    print(f"Added EBS volume with ID: {volume_id} to instance with ID: {instance_id}")

# Prompt user to add an EBS volume to an instance
add_ebs_volume()
