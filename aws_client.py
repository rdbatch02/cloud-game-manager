import boto3

class AwsClient():
    def __init__(self):
        # Initialize aws client
        session = boto3.Session()
        self.ec2 = session.client('ec2')

    def get_instance_metadata(self):
        # find instance by name
        instance = self.ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': ['SatisfactoryServer/SatisfactoryHostingServer'] # Parameterize this later
                },
            ],
        )
        instance_data = instance['Reservations'][0]['Instances'][0]
        return {
            'instance_id': instance_data['InstanceId'],
            'instance_type': instance_data['InstanceType'],
            'instance_name':  self._find_tag_by_name(instance_data['Tags'], 'Name'),
            'public_ip': instance_data['PublicIpAddress'],
            'availability_zone':  instance_data['Placement']['AvailabilityZone'],
            'state': instance_data['State']['Name'],
        }

    @staticmethod
    def _find_tag_by_name(tags, tag_name):
        for tag in tags:
            if tag['Key'] == tag_name:
                return tag['Value']
        return None