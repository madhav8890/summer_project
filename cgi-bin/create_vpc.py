#!/usr/bin/python3

print("content-type: text/html")
print()

import cgi
import boto3

ACCESS_KEY = 'AKIAXCJPOLASN6RFGU4M'
SECRET_KEY = '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'
REGION = 'ap-south-1'


form = cgi.FieldStorage()
cidr_block = form.getvalue("cidr")
vpc_name = form.getvalue("vpcname")

def create_vpc():
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
    )

    ec2 = session.resource('ec2')

    # Get user input for CIDR block and VPC name
#     cidr_block = input("Enter the CIDR block for the VPC (e.g., 10.0.0.0/16): ")
#     vpc_name = input("Enter the name for the VPC: ")

    # Create VPC
    vpc = ec2.create_vpc(CidrBlock=cidr_block)

    # Enable DNS support and hostname
    vpc.modify_attribute(EnableDnsSupport={'Value': True})
    vpc.modify_attribute(EnableDnsHostnames={'Value': True})

    # Create a name tag for the VPC
    vpc.create_tags(Tags=[{'Key': 'Name', 'Value': vpc_name}])

    return vpc

def describe_vpc(vpc):
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
    )
    ec2_client = session.client('ec2')

    # Describe the VPC
    response = ec2_client.describe_vpcs(VpcIds=[vpc.id])
    vpc_details = response['Vpcs'][0]

    # Display VPC details
    print("VPC Details:")
    print(f"VPC ID: {vpc_details['VpcId']}")
    print(f"VPC CIDR Block: {vpc_details['CidrBlock']}")
    print(f"Is Default VPC?: {vpc_details['IsDefault']}")
    print(f"State: {vpc_details['State']}")
    print(f"Tenancy: {vpc_details['InstanceTenancy']}")

    # Describe the VPC's CIDR blocks
    print("\nCIDR Blocks:")
    for cidr in vpc_details['CidrBlockAssociationSet']:
        print(f"  - {cidr['CidrBlock']}")

    # Describe the VPC's Flow Logs
    print("\nFlow Logs:")
    flow_logs = ec2_client.describe_flow_logs(Filters=[{'Name': 'resource-id', 'Values': [vpc.id]}])
    for log in flow_logs['FlowLogs']:
        print(f"  - Log Group: {log['LogGroupName']}")
        print(f"    Resource ID: {log['ResourceId']}")
        print(f"    Traffic Type: {log['TrafficType']}")
        print(f"    Status: {log['FlowLogStatus']}")
        print(f"    ARN: {log['FlowLogId']}")
        print()

    # Describe the VPC's Tags
    print("\nTags:")
    tags_response = ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [vpc.id]}])
    for tag in tags_response['Tags']:
        print(f"  - Key: {tag['Key']}")
        print(f"    Value: {tag['Value']}")
        print()

if __name__ == '__main__':
    vpc = create_vpc()
    describe_vpc(vpc)
