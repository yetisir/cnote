
# dNote
[![Build Status](https://travis-ci.com/yetisir/dnote.svg?branch=master)](https://travis-ci.co/yetisir/dnote) [![Coverage Status](https://coveralls.io/repos/github/yetisir/dnote/badge.svg?branch=master)](https://coveralls.io/github/yetisir/dnote?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/9188bb54d74247ab039e/maintainability)](https://codeclimate.com/github/yetisir/dnote/maintainability) [![Documentation Status](https://readthedocs.org/projects/dnote/badge/?version=latest)](https://dnote.readthedocs.io/en/latest/?badge=latest)
  
dNote is a simple Python based CLI utility for managing notes across independent systems in real-time using AWS (free-tier) cloud infrastructure. This project has been inspired by similar CLI note taking utilities ([notes](https://github.com/pimterry/notes) and [notes-cli](https://github.com/rhysd/notes-cli)), but distinguishes itself by using AWS DynamoDB   as a storage back-end natively instead of the local filesystem. This approach has the advantage that notes are inherently backed-up and also become available across devices instantly without relying on third party syncing tools like Dropbox. That being said, avoiding the local filesystem in favor of the cloud does come with limitation that the notes are only accessible with an internet connection (a local caching solution might be included in a future release though). There are some search implications associated with moving away from a locla filesystem which are detailed in the search section.

## Quickstart
The following is a summary of installation requirements. More installation details are [here](installation.md)

* Install [Python](https://www.python.org/) >=3.6
* Intall dNote: `python -m pip install dnote`
* Configure [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

Once dNote is installed and AWS is configured, we are ready to start making notes!

```bash
dnote new
```

The new command will open up a text editor in which you can type your notes. dNotes will grab the contents of the file and save it directly to the configured DynamoDB database. 

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
dNote is licensed under the  [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

