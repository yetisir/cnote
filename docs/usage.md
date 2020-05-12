# Usage
dNote uses your default text editor for creating notes. If no system editor is specified this will default to Vim, though this can be configured (see configuration section). The command syntax has been inspired by the other tools mentioned at the top of this document, with modifications where appropriate.
 
## Options for Creating Notes
By default, a name is assigned to the note based on your username, but this can be overridden with the `--name` (or `-n`) flag. The name does not have to be unique, but is used as  a high level description of the note contents (like a file name).
 
We can also tag notes so they may be easier to find in the future. Tagging is accomplished with the `--tag`  (or `-t`) flag  and takes a list of any number of tags.
 
Finally,  the `--file` (or `-f`) flag can be used to specify a file to be used as the starting point for a note.

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

Notes can be removed from the database with the `dnote rm` command and specifying a range of ids. These ids can be piped in from a dnote search or just listed with the `--id` flag.

```bash
dnote find -b 'test' 'note' | dnote rm
```

## Updating Notes
Notes can be updated with the `dnote edit` command.
