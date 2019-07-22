import boto3
import json 
import argparse

ec2 = boto3.client('ec2')
images = {
    'aws-linux'  : 'ami-0bbc25e23a7640b9b',
    'centos' : 'ami-0ff760d16d9497662',
}

parser = argparse.ArgumentParser(description='Script to manager EC2 instances.')
arguments = parser.add_argument_group('Arguments')
# required = parser.add_argument_group('required group')
# required.add_argument('-n', '--name', help='Please provide image name for ec2 instances.', required=False)
# notrequired = parser.add_argument_group('not required group')
# notrequired.add_argument('-g', '--get', help='Please provide image id', required=False)
arguments.add_argument('-n', '--name', help='Image name to be used for the instance', required=False)
arguments.add_argument('-l', '--list', help='List running instances', action='store_true', required=False)
arguments.add_argument('-k', '--key', help='Key name', required=False)
arguments.add_argument('-t', '--type', help='Instance type', required=False)
arguments.add_argument('-d', '--delete', nargs='+', help='ID of the instance to delete', required=False)
args = parser.parse_args()


args = parser.parse_args()



def get_instances():
    data = ec2.describe_instances()
    for item in data['Reservations']:
        if item['Instances'][0]['State']['Name'].lower() == 'running':
            print('InstanceId', item['Instances'][0]['InstanceId'])
            print('SubnetId', item['Instances'][0]['SubnetId'])

def create_instance(name):
    image_id = None 
    
    if name in images.keys():
        image_id =  images[name]
    else:
        print('Image not found ')

    if image_id:
        ec2 = boto3.resource('ec2')
        ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType='t2.micro')

def deleteInstance(instances):
    ec2 = boto3.client('ec2')
    response = ec2.terminate_instances(
        InstanceIds=instances,
        #DryRun=True|False
    )
def main():
    if args.get:
        get_instances()
        exit()
        
    if args.name in images.keys():
        key = args.key if args.key else 'deployer-key1'
        instancetype = args.type if args.type else 't2.nano'
        create_instance(args.name, 1, 1, instancetype, key)
        exit()

        create_instance(args.name)
    else:
        print('Image name is not supported.')
        exit()
    else:
        print("Script requires at least one argument")
        print(parser.print_help())
        exit()
    
    if(args.delete):
        deleteInstance(args.delete)
        exit()
    
    
    

if __name__ == "__main__" :
    main()

