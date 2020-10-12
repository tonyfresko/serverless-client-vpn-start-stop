import subprocess
import boto3
from os import getenv
from logging import getLogger
from sys import exit


logger = getLogger(__name__)
client = boto3.client("ec2")

def get_subnet_list():
    subnet_list = []
    for n in range(11):
        subnet_n = getenv(f"SUBNET_{n}")
        if subnet_n:
            subnet_list.append(subnet_n)
    if not subnet_list:
        logger.error("""No SUBNET_ environment variables found! 
        These must be set (e.g. SUBNET_1) to run the function""")
        exit(1)
    return subnet_list


def lambda_handler(event, context):
    client_vpn_endpoint_id = getenv("CLIENT_VPN_ENDPOINT_ID")
    if not client_vpn_endpoint_id:
        logger.error(
        """Environment variable CLIENT_VPN_ENDPOINT_ID is not set!
        This variable must be set for the program to work"""
        )
        exit(1)
    subnet_id_list = get_subnet_list()
   
    start_or_stop = event['start_or_stop']
    if start_or_stop == "start":
        start_client_vpn(client_vpn_endpoint_id, subnet_id_list)
        message = "VPN is associated"
    elif start_or_stop == "stop":
        stop_client_vpn(client_vpn_endpoint_id)
        message = "VPN is disassociated"
    else:
        message = "message type is unknown."
    print(message)


def start_client_vpn(client_vpn_endpoint_id, subnet_id_list):
    for subnet_id in subnet_id_list :
        response = client.associate_client_vpn_target_network(
            ClientVpnEndpointId=client_vpn_endpoint_id,
            SubnetId=subnet_id,
        )
        logger.info(response)


def stop_client_vpn(client_vpn_endpoint_id):
    description = client.describe_client_vpn_target_networks(
        ClientVpnEndpointId=client_vpn_endpoint_id
    )
    endpoints = description['ClientVpnTargetNetworks']
    for endpoint in endpoints:
        association_id = endpoint['AssociationId']
        response = client.disassociate_client_vpn_target_network(
            ClientVpnEndpointId=client_vpn_endpoint_id,
            AssociationId=association_id,
        )
        logger.info(response)