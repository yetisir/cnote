# dNote

[![Build Status](https://travis-ci.com/yetisir/dnote.svg?branch=master)](https://travis-ci.com/yetisir/dnote)
[![Coverage Status](https://coveralls.io/repos/github/yetisir/dnote/badge.svg?branch=master)](https://coveralls.io/github/yetisir/dnote?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/9188bb54d74247ab039e/maintainability)](https://codeclimate.com/github/yetisir/dnote/maintainability)
[![Documentation Status](https://readthedocs.org/projects/dnote/badge/?version=latest)](https://dnote.readthedocs.io/en/latest/?badge=latest)

 # dNote
  
 dNote is a simple Python based CLI utility for managing notes across independent systems in real-time using AWS (free-tier) cloud infrastructure. This project has been inspired by similar CLI note taking utilities ([notes](https://github.com/pimterry/notes)   and [notes-cli](https://github.com/rhysd/notes-cli)), but distinguishes itself by using AWS DynamoDB   as a storage back-end natively instead of the local filesystem. This approach has two major advantages:
 * Notes are available across devices instantly without relying on third party syncing tools like DropBox.
 * 
 However,  avoiding the local filesystem in favor of the cloud does come with limitation that the notes are only accessible with an internet connection (a local caching solution might be included in a future release though).
 
 ## Installation

 The latest release of dNote can be installed with [pip](https://pip.pypa.io/en/stable/).
 
 ```bash
python -m pip install dnote
 ```

 ### Configuring the DynamoDB back-end
 Two options exists for 
 In order to set up the DynamoDB backend
 
 ## Usage
 
 ```bash
 dnote add 'this is a new note!'
 dnote add 'this is another new note.'
 dnote add 'this is an old note'
 dnote find 'new'
 ```
 
 ## Contributing
 Pull requests are welcome. For major changes, please open an issue first to discuss what you would   like to change.
 
 Please make sure to update tests as appropriate.
 
 ## License
 [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

