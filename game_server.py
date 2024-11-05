import boto3

from dataclasses import dataclass


@dataclass
class GameServerMetadata:
    instance_id: str
    instance_type: str
    instance_name: str
    public_ip: str
    availability_zone: str
    state: str

class GameServer:
    def __init__(self):
        # Initialize aws client
        session = boto3.Session()
        self.ec2 = session.client('ec2')
        self.instance_metadata: GameServerMetadata = GameServerMetadata(
            instance_id='',
            instance_type='',
            instance_name='',
            public_ip='',
            availability_zone='',
            state=''
        )

    def get_instance_metadata(self):
        instance = self.ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': ['SatisfactoryServer/SatisfactoryHostingServer']  # Parameterize this later
                },
            ],
        )
        instance_data = instance['Reservations'][0]['Instances'][0]
        self.instance_metadata = GameServerMetadata(
            instance_id=instance_data['InstanceId'],
            instance_type=instance_data['InstanceType'],
            instance_name=self._find_tag_by_name(instance_data['Tags'], 'Name'),
            public_ip=instance_data['PublicIpAddress'],
            availability_zone=instance_data['Placement']['AvailabilityZone'],
            state=instance_data['State']['Name']
        )
        return self.instance_metadata

    def start_server(self):
        self.ec2.start_instances(InstanceIds=[self.instance_metadata.instance_id])

    def stop_server(self):
        self.ec2.stop_instances(InstanceIds=[self.instance_metadata.instance_id])

    def restart_server(self):
        self.ec2.reboot_instances(InstanceIds=[self.instance_metadata.instance_id])

    @staticmethod
    def _find_tag_by_name(tags, tag_name):
        for tag in tags:
            if tag['Key'] == tag_name:
                return tag['Value']
        return None