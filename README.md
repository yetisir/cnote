<img align="left" height="120" src="docs/assets/logo.png">

# cNote - Cloud Based Note Management

[![Build Status](https://travis-ci.com/yetisir/cnote.svg?branch=main)](https://travis-ci.com/yetisir/cnote) [![Coverage Status](https://coveralls.io/repos/github/yetisir/cnote/badge.svg?branch=main)](https://coveralls.io/github/yetisir/cnote?branch=main) [![Maintainability](https://api.codeclimate.com/v1/badges/599a8ca1cb658c45f1c0/maintainability)](https://codeclimate.com/github/yetisir/cnote/maintainability) [![Documentation Status](https://readthedocs.org/projects/cnote/badge/?version=main)](https://cnote.readthedocs.io/en/main)


cNote is a simple Python based CLI utility for managing notes across independent systems in real-time using AWS (free-tier) cloud infrastructure. This project has been inspired by similar CLI note taking utilities ([notes](https://github.com/pimterry/notes) and [notes-cli](https://github.com/rhysd/notes-cli)), but distinguishes itself by using AWS DynamoDB as a storage back-end natively instead of the local file system. This approach has the advantage that notes are inherently backed-up and also available across devices instantly without relying on third party syncing tools like Dropbox. That being said, avoiding the local file system in favor of the cloud does mean that notes are only available with an internet connection (though a local caching solution could be implemented in a future release). There also are some search implications associated with moving away from a local file system which are detailed in the [documentation](https://cnote.readthedocs.io/en/latest/?badge=latest).

## Documentation

Complete documentation can be found [here](https://cnote.readthedocs.io/en/latest/?badge=latest).

## Quickstart

The following is a summary of installation requirements. More installation details are [here](https://cnote.readthedocs.io/en/latest/?badge=latest)

- Install [Python](https://www.python.org/) >=3.6
- Install cNote: `python -m pip install cnote`
- Configure [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

Once cNote is installed and AWS is configured, we are ready to start making notes!

```bash
cnote new
```

The `new` command will open up a text editor in which you can type your notes. cNote will grab the contents of the file and save it directly to the configured DynamoDB database. Please refer to the [documentation](https://cnote.readthedocs.io/en/latest/?badge=latest) for complete functionality and examples.

## Testing

Testing is facilitated with the pytest framework.

```bash
python -m pytest --flake8 --cov=cnote
```

Dependencies can be installed with the dev option.

```bash
python -m pip install cnote[dev]
```

## Contributing

Bugs? Missing features? Issues and pull requests are more than welcome.

## License

cNote is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License
