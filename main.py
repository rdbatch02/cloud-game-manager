import secrets

from fasthtml.common import *

from aws_client import AwsClient

app,rt = fast_app(
    secret_key=secrets.token_hex(32)
)

aws_client = AwsClient()

@rt('/')
def get():
    instance_metadata = aws_client.get_instance_metadata()
    server_running = instance_metadata['state'] == 'running'

    status_header = H2("Server Status")
    status = Div(
        P(f"Instance Name: {instance_metadata['instance_name']}"),
        P(f"Instance ID: {instance_metadata['instance_id']}"),
        P(f"Instance Type: {instance_metadata['instance_type']}"),
        P(f"Availability Zone: {instance_metadata['availability_zone']}"),
        P(f"Public IP: {instance_metadata['public_ip']}"),
        P(f"State: {instance_metadata['state']}")
    )
    status_card = Card(header=status_header, footer=status)

    server_control_header = H2("Server Controls")

    button_start_server = Button("Start Server")
    button_stop_server = Button("Stop Server", cls="secondary", disabled=not server_running)
    button_restart_server = Button("Restart Server", cls="secondary", disabled=not server_running)

    server_control_content = Div(Group(button_start_server, button_stop_server, button_restart_server))

    control_card = Card(header=server_control_header, footer=server_control_content)
    return Titled("Cloud Game Manager", status_card, control_card)

serve()