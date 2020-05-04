import configurator


def get_config(config_dir='~/.dnote.yml'):
    default_config = configurator.Config({
        'dynamodb_endpoint': None,
    })

    user_config = configurator.Config.from_path(config_dir, optional=True)

    return default_config + user_config

config = get_config()
