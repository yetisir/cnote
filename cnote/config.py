import configurator
import nltk


def get_settings(config_file='~/.cnote.yml'):
    """Get settings from config file

    Args:
        config_file (str, optional): [description]. Defaults to '~/.cnote.yml'.

    Returns:
        [type]: [description]
    """
    default_config = configurator.Config({
        'aws_endpoint': None,
        # 'aws_endpoint': 'http://localhost:8000',
        'aws_region': 'us-west-2',
        'dynamodb_note_table': 'cnote',
        'dynamodb_index_table': 'cnote_index',
    })

    user_config = configurator.Config.from_path(config_file, optional=True)

    return default_config + user_config


nltk.download('punkt', quiet=True)
settings = get_settings()
