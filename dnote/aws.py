import boto3
from botocore import exceptions

from .config import config


# TODO: streamline config settings
try:
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=config.dynamodb_endpoint)
except exceptions.NoRegionError:
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=config.dynamodb_endpoint,
        region_name=config.dynamodb_region)
