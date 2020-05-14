import configurator
import nltk
from dynaconf import settings, Validator


settings.validators.register(
    Validator(
        'DYNAMODB_ENPOINT',
        'DYNAMODB_NOTETABLE',
        'DYNAMODB_INDEXTABLE',
        'AWS_REGION',
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
))
# TODO: streamline config settings


def get_config(config_dir='~/.dnote.yml'):
    default_config = configurator.Config({
        'dynamodb_endpoint': None,
        # 'dynamodb_endpoint': 'http://localhost:8000',
        'dynamodb_region': 'us-west-2',
    })

    user_config = configurator.Config.from_path(config_dir, optional=True)

    return default_config + user_config


nltk.download('punkt', quiet=True)
config = get_config()
