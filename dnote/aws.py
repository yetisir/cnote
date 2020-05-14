import boto3
from botocore import exceptions

from .config import settings


# TODO: streamline config settings
try:
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=settings.aws_endpoint)
except exceptions.NoRegionError:
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=settings.aws_endpoint,
        region_name=settings.aws_region)
