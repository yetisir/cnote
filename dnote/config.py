import configurator
import nltk


def get_settings(config_dir='~/.dnote.yml'):
    default_config = configurator.Config({
        'aws_endpoint': None,
        # 'aws_endpoint': 'http://localhost:8000',
        'aws_region': 'us-west-2',
        'dynamodb_note_table': 'dnote',
        'dynamodb_index_table': 'dnote_index',
    })

    user_config = configurator.Config.from_path(config_dir, optional=True)

    return default_config + user_config


nltk.download('punkt', quiet=True)
settings = get_settings()
