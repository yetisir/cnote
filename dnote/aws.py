import boto3

from .config import config

dynamodb = boto3.resource('dynamodb', endpoint_url=config.dynamodb_endpoint)

