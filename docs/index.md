
# dNote
[![Build Status](https://travis-ci.com/yetisir/dnote.svg?branch=master)](https://travis-ci.co/yetisir/dnote) [![Coverage Status](https://coveralls.io/repos/github/yetisir/dnote/badge.svg?branch=master)](https://coveralls.io/github/yetisir/dnote?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/9188bb54d74247ab039e/maintainability)](https://codeclimate.com/github/yetisir/dnote/maintainability) [![Documentation Status](https://readthedocs.org/projects/dnote/badge/?version=latest)](https://dnote.readthedocs.io/en/latest/?badge=latest)
  
dNote is a simple Python based CLI utility for managing notes across independent systems in real-time using AWS (free-tier) cloud infrastructure. This project has been inspired by similar CLI note taking utilities ([notes](https://github.com/pimterry/notes)   and [notes-cli](https://github.com/rhysd/notes-cli)), but distinguishes itself by using AWS DynamoDB   as a storage back-end natively instead of the local filesystem. This approach has the advantage that notes are inherently backed-up and also become available across devices instantly without relying on third party syncing tools like Dropbox. That being said, avoiding the local filesystem in favor of the cloud does come with limitation that the notes are only accessible with an internet connection (a local caching solution might be included in a future release though). There are some search implications associated with moving away from a locla filesystem which are detailed in the search section.
 

# Contributing
Bugs? Missing features? Issues and pull requests are more than welcome.
 
# License
dNote is licensed under the  [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

