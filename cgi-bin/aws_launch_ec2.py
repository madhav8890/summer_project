#!/usr/bin/python3

print("content-type: text/html")
print()

import boto3
import os
import cgi

# Set up your AWS login credentials
aws_access_key_id = 'AKIAXCJPOLASDLP5KSOH'
aws_secret_access_key = 'Fbx9PpzHnDNi7IXlKePIdjCRRoE9/0IjfriuW8XU'
region_name = 'ap-south-1'

form = cgi.FieldStorage()

instance_name = form.getvalue("name")
instance_type = form.getvalue("instype")
image_id = form.getvalue("imgid")
key_name = form.getvalue("key")

# Create a session
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Create an EC2 resource and client
ec2_resource = session.resource('ec2')
ec2_client = session.client('ec2')

def create_key_pair(key_name):
    response = ec2_client.create_key_pair(KeyName=key_name)

    # Save the private key to a file
    private_key = response['KeyMaterial']
    key_file_path = f"{key_name}.pem"
    with open(key_file_path, 'w') as f:
        f.write(private_key)

    # Change the permissions of the key file to be readable only by the owner
    os.chmod(key_file_path, 0o400)

    return key_file_path

# Function to launch a new EC2 instance
def launch_instance():
    instance_name = form.getvalue("name")
    instance_type = form.getvalue("instype")
    image_id = form.getvalue("imgid")
    key_name = form.getvalue("key")

    # Create the key pair and save the private key to a file
    key_file_path = create_key_pair(key_name)

    # Launch the EC2 instance
    instance = ec2_resource.create_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        KeyName=key_name,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    },
                ]
            },
        ]
    )[0]

    print(f"Launched instance with name '{instance_name}' and ID: {instance.id}")
    print(f"The private key has been saved to '{key_file_path}'")

# Prompt user to launch an instance


while True:

        launch_instance()
        break
