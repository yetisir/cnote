import argparse
from abc import ABC, abstractmethod

from . import aws


class EntryPoint(ABC):
    aliases = []

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def build_parser(self, parser):
        raise NotImplementedError


class DynamoDBTable(ABC):

    def __init__(self, *args, **kwargs):
        self.table = aws.dynamodb.Table(self.table_name)

    @property
    @abstractmethod
    def table_name(self):
        raise NotImplementedError

    @property
    def exists(self):
        return self.table_name in aws.dynamodb.meta.client.list_tables()['TableNames']

    def create_table(self):
        aws.dynamodb.create_table(
            TableName=self.table_name,
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
            ],
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'},
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10,
            },
        )

        waiter = aws.dynamodb.meta.client.get_waiter('table_exists')
        waiter.wait(
            TableName=self.table_name,
            WaiterConfig={
                'Delay': 1,
            }
        )