#!/usr/bin/env python3
import cgi
import boto3

print("Content-type: text/html\n")

# Function to add an EBS volume to an instance
def add_ebs_volume(aws_access_key_id, aws_secret_access_key, region_name, instance_id, volume_size, volume_type):
    # Create a session
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    # Create an EC2 client
    ec2_client = session.client('ec2')

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
        Device='/dev/sdf',  # Replace with the desired device name
        InstanceId=instance_id,
        VolumeId=volume_id
    )

    return volume_id, instance_id

# Get user input from HTML form
form = cgi.FieldStorage()
if 'aws_access_key_id' in form and 'aws_secret_access_key' in form and 'region_name' in form and 'instance_id' in form and 'volume_size' in form and 'volume_type' in form:
    aws_access_key_id = form['aws_access_key_id'].value
    aws_secret_access_key = form['aws_secret_access_key'].value
    region_name = form['region_name'].value
    instance_id = form['instance_id'].value
    volume_size = int(form['volume_size'].value)
    volume_type = form['volume_type'].value

    # Call the function to add the EBS volume and get the result
    volume_id, instance_id = add_ebs_volume(aws_access_key_id, aws_secret_access_key, region_name, instance_id, volume_size, volume_type)

    # Display the result
    print(f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add EBS Volume</title>
    </head>
    <body>
        <h1>EBS Volume Added</h1>
        <p>Added EBS volume with ID: {volume_id} to instance with ID: {instance_id}</p>
    </body>
    </html>
    ''')
