# dNote

dNote is a simple Python based CLI utility for managing notes across independent systems in real-time using AWS (free-tier) cloud infrastructure. This project has been inspired by similar CLI note taking utilities ([notes](https://github.com/pimterry/notes) and [notes-cli](https://github.com/rhysd/notes-cli)), but distinguishes itself by using AWS DynamoDB as a storage back-end natively instead of the local file system. This approach has the advantage that notes are inherently backed-up and also become available across devices instantly without relying on third party syncing tools like Dropbox. That being said, avoiding the local file system in favor of the cloud does come with limitation that the notes are only accessible with an internet connection (a local caching solution might be included in a future release though). There are some search implications associated with moving away from a local file system which are detailed in the search section.

## Quickstart

The following is a summary of installation requirements. More installation details are [here](installation.md)

- Install [Python](https://www.python.org/) >=3.6
- Install dNote: `python -m pip install dnote`
- Configure [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

Once dNote is installed and AWS is configured, we are ready to start making notes!

```bash
dnote new
```

The `new` command will open up a text editor in which you can type your notes. dNote will grab the contents of the file and save it directly to the configured DynamoDB database. Please refer to the [documentation](https://dnote.readthedocs.io/en/latest/?badge=latest) for complete functionality and examples.

## Testing

Testing is facilitated with the pytest framework.

```bash
python -m pytest --flake8 --cov=dnote
```

Dependencies can be installed with the dev option.

```bash
python -m pip install dnote[dev]
```

## Contributing

Bugs? Missing features? Issues and pull requests are more than welcome.

## License

dNote is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License
