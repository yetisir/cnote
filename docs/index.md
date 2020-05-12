
# dNote
[![Build Status](https://travis-ci.com/yetisir/dnote.svg?branch=master)](https://travis-ci.co/yetisir/dnote) [![Coverage Status](https://coveralls.io/repos/github/yetisir/dnote/badge.svg?branch=master)](https://coveralls.io/github/yetisir/dnote?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/9188bb54d74247ab039e/maintainability)](https://codeclimate.com/github/yetisir/dnote/maintainability) [![Documentation Status](https://readthedocs.org/projects/dnote/badge/?version=latest)](https://dnote.readthedocs.io/en/latest/?badge=latest)
  
dNote is a simple Python based CLI utility for managing notes across independent systems in real-time using AWS (free-tier) cloud infrastructure. This project has been inspired by similar CLI note taking utilities ([notes](https://github.com/pimterry/notes)   and [notes-cli](https://github.com/rhysd/notes-cli)), but distinguishes itself by using AWS DynamoDB   as a storage back-end natively instead of the local filesystem. This approach has the advantage that notes are inherently backed-up and also become available across devices instantly without relying on third party syncing tools like Dropbox. That being said, avoiding the local filesystem in favor of the cloud does come with limitation that the notes are only accessible with an internet connection (a local caching solution might be included in a future release though), and some search implications as well (see search section)
 
# Installation

The latest release of dNote can be installed with [pip](https://pip.pypa.io/en/stable/).
 
```bash
python -m pip install dnote
```

## Configuring the DynamoDB Back-End
 ******more details to come 
  
Two options exists for accessing DynamoDB
1) Create a free AWS account and create a user with access to DynamoDB (recommended).
2) Host an instance of DynamoDB yourself with Docker (useful for  development and testing).
 
By default, dNote tries to connect to AWS servers, but you can specify the location of your local instance as an environment variable:
```bash
DNOTE_DYNAMODB_ENDPOINT = 'http://localhost:8000'
```

or in ~/.dnote.yml

```yaml
dynamodb_endpoint: 'http://localhost:8000'
```
 
# Usage
dNote uses the default text editor for creating notes. If no system editor is specified this will default to Vim, though this can be configured (see configuration section). The syntax has been inspired by the other tools mentioned at the top of this document, with modifications where appropriate.

## Basic Usage
 The simplest way to create a note with dNote is to use the `new` command:
```bash
 dnote new
```
The new command will open up a text editor in which you can type your notes. dNotes will grab the contents of the file and save it directly to the configured DynamoDB database. 
 
## Options for Creating Notes
By default, a name is assigned to the note based on your username, but this can be overridden with the `--name` (or `-n`) flag. The name does not have to be unique, but is used as  a high level description of the note contents (like a file name).
 
We can also tag notes so they may be easier to find in the future. Tagging is accomplished with the `--tag`  (or `-t`) flag  and takes a list of any number of tags.
 
Finally,  the `--file` (or `-f`) flag can be used to specify a file to be used as the starting point for a note.

## Piping Into `dnote new`
We may find ourselves wanting to use the output of another program as a note. Although dNote will accept piped input, there is a weird combination of reading from stdin and opening Vim from the same process that renders the terminal in an unusable state afterwards. This is a known bug in dNote and PRs or any direction on how to handle this would gladly be accepted. The workaround for now is to issue a `reset` command afterwards to get the terminal functional again, or just use a different editor.

## Finding Notes
dNote indexes all notes as they are written. The index is written to a separate table and used to lookup the specified search terms. To limit the number of index entries and maximize the likelihood of a search returning the intended result, a stemming algorithm from [NLTK](https://www.nltk.org/) is used to group similar words into the same search token (e.g. 'run', 'runs', 'runner', and 'running' would all return the same search results). This stemming approach makes the search experience more natural than regex approaches. That being said, the `--exact` (or `-e`) flag will ignore the stem token matches and yield only exact matches. 

Finding notes can be accomplished with the `find` command. To search the content of the note we can We can specify a time range with the `--range` (or `-r`) flag and include up to four text fields in the search: 

* `--name` (or `-n`) - name of the note
* `--body` (or `-b`) - content of the note
* `--host` (or `-h`) - computer name on which the note was written
* `--tags` (or `-t`) - any specified tags

For example, we can query all notes that contain mentions of words that share the stem of 'test' (e.g. 'tests', 'testing', 'tester', etc.).:
```bash
dnote find -b test
```

We can also specify multiple search terms in a single field. This will return notes that have mentions of both 'test' and 'note':
```bash
dnote find -b test note
```

To query multiple fields, we just add them to the search query. If we were only interested in the test notes that were written from a system called 'homecomputer', we could update the previous command to be as follows:
```bash
dnote find -b test note -h homecomputer
```

With respect to more advanced queries, the decision to use a predefined text index limits us from more sophisticated pattern matching like regex since those approaches require iteration through the contents of the file and can't be done exclusively with an index. This can be accomplished in a future release however, by integrating AWS Elasticsearch or using local caching. That being said, Elasticsearch is not currently included in the AWS free-tier which makes it a bit inaccessible. 

## Removing Notes
Support for removing notes is currently being implemented. Please check back soon.

## Updating Notes
Support for updating notes is currently being implemented. Please check back soon.

#Configuration
Coming soon

# Contributing
Bugs? Missing features? Issues and pull requests are more than welcome.
 
# License
dNote is licensed under the  [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

