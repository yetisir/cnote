from abc import ABC, abstractmethod
import sys
import termios
import re
from datetime import datetime
import click
import dateparser
from . import aws


class EntryPoint(ABC):
    """Base class for CLI Entrypoints. This is an interface to
    help describe the commands and corresponding actions
    """

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

    @staticmethod
    def _validate_body(body, prompt=None):
        if body:
            return body.strip()

        stty_attrs = termios.tcgetattr(sys.stdout)

        if not sys.stdin.isatty():
            prompt = sys.stdin.read()
        elif not prompt:
            prompt = ''

        body = click.edit(prompt, require_save=False)

        termios.tcsetattr(sys.stdout, termios.TCSAFLUSH, stty_attrs)
        return body.strip()

    @staticmethod
    def _validate_ids(ids):
        piped_input = sys.stdin.read() if not sys.stdin.isatty() else ''
        ids = ids if ids else []

        regex = r'([a-fA-F\d]{32})'

        ids = [id for id in ids if re.match(regex, id)]
        for line in piped_input.split('\n'):
            if line.startswith('\t'):
                continue

            match = re.match(regex, line)
            if match:
                ids.append(match.group())

        return ids

    @staticmethod
    def _validate_range(datetime_range):
        now = datetime.utcnow()
        datetime_range = datetime_range if datetime_range else []
        dates = [
            dateparser.parse(date, settings={'TO_TIMEZONE': 'UTC'})
            for date in datetime_range]

        if datetime_range and len(datetime_range) > 2:
            raise ValueError('Number of range arguments exceeds 2 ...')
        elif None in dates:
            raise ValueError('Unable to parse date range')
        elif len(dates) == 0:
            return (datetime.fromtimestamp(0), now)
        elif len(dates) == 1:
            return (dates[0], now)
        elif len(dates) == 2:
            return (min(dates), max(dates))

    @staticmethod
    def _validate_search_fields(search_fields):
        return {
            field: searches for field, searches in search_fields.items()
            if searches}


class DynamoDBTable(ABC):
    """Base class for interfacing with DynamoDB tables

    Attributes:
        table_name (str): name of DynamoDB table
        table (aws.dynamodb.Table): Reference to the AWS DynamoDB table
    """

    def __init__(self, *args, **kwargs):
        self.table = aws.dynamodb.Table(self.table_name)

    @property
    @abstractmethod
    def table_name(self):
        raise NotImplementedError

    @property
    def exists(self):
        table_names = aws.dynamodb.meta.client.list_tables()['TableNames']
        return self.table_name in table_names

    def create_table(self):
        """Creates a DynamoDB Table if it doesnt already exist
        """

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
