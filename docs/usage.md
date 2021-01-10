# cNote Usage
cNote uses your default text editor for creating notes. If no system editor is specified this will default to Vim, though this can be configured (see configuration section). The command syntax has been inspired by similar CLI note taking utilities ([notes](https://github.com/pimterry/notes) and [notes-cli](https://github.com/rhysd/notes-cli)), with modifications where appropriate.

## Note Attributes

Each note created in cNote has the following attributes that can be specified:

* body - the main text of the note.
* name - a few words to describe the body of the note
* tags - metatext that can be used to help group and search

And two other attributes that are automatically determined

* host - the hostname of the system used to create the note
* timestamp - the timestamp (in UTC) when the note was created


## Creating Notes
Notes are added to the cNote database with the `cnote new` command:

```bash
cnote new [--body(-b) BODY] [--name(-n) NAME] [--tags(-t) [TAGS ...]]
```

All the arguments for this command are optional. If no arguments are specified, cNote will open up a command line text editor in which you can type your notes. cNote will grab the contents of the file and save it directly to the configured DynamoDB database.

```bash
cnote new
```

The text of this note can also be specified using the `--body` flag:

```bash
cnote new -b "this is a note"
```

Alternatively, we can pipe in a note. Piped input on the `new` command is always interpereted as the `--body` argument. When a pipe is used, the text editor is still launched so that the note can be edited before saving. Note that use of the `--body` flag will override any piped input.

```bash
echo "this is a piped note" | cnote new
```

We can use this feature to pipe in the contents of a file.

```bash
cat note.txt | cnote new
```

By default, a name is assigned to the note based on your username, but this can be overridden with the `--name` flag. The note name does not have to be unique, but should be a high level description of the note contents (like a file name).

```bash
cnote new -b "this note has a custom name" -n "custom note name"
```

We can also tag notes so they may be easier to find in the future. Tagging is accomplished with the `--tag` flag  and takes a list of any number of relavent tags.

```bash
cnote new -b "this note has custom tags" -t "custom tag 1" "custom tag 2"
```

## Finding Notes
The cNote database searched for notes with the `cnote find` command:

```bash
cnote find [--range(-r) [RANGE ...]] [--name(-n) [NAME ...]] [--body(-b) [BODY ...]] [--tags(-t) [TAGS ...]] [--host(-h) [HOST ...]] [--exact(-e)] [--quiet(-e)]
```

All arguments for this command ar optional. If not arguments are specified, cNote will return up to 100 notes from the cNote database.

```
cnote find
```

cNote allows searching of all four text fields (i.e. name, body, tags, and host) as well as the timestamp field. We can specify a time range with the `--range` flag and include any of the four text fields with their corresponding flags: 

For example, we can query all notes that contain mentions of words that share the stem of 'test' (e.g. 'tests', 'testing', 'tester', etc.).

```bash
cnote find -b "test"
```

We can also specify multiple search terms in a single field. This query will return notes that have mentions of both 'test' and 'note'.

```bash
cnote find -b "test" "note"
```

To query multiple fields, we just add them to the search query. If we were only interested in the test notes that were written from a system called 'testserver', we could update the previous command to be as follows:

```bash
cnote find -b "test" note -h "testserver"
```

Querying the time range takes one or two arguments representing the bounding times of the range. If only one argument is given, the second argument is assumed to be "now". A unique feature of cNote is that it supports relative human time references to find all the notes written in the last day we can just write:

```bash
cnote find -r "one day ago"
```

Which is equivalent to:

```bash
cnote find -r "now" "one day ago"
```

By default, the search engine compares the stems of the search words - this allows for near matches (e.g. runner and running would match) which makes the search a more human experience. That being said, we can specify an exact search by using the '--exact' flag.

```bash
cnote find -b 'runner' --exact
```

If we only want the note ids, we can use the `--quiet` flag

```bash
cnote find --quiet
```

By default, we can only return up to 100 notes in a single search. The returned notes will only print the first 10 lines - to show the full notes we can use the `cnote show` command described below.

## Showing Notes

Notes from the cNote database can be shown in their entirety with the `cnote show` command:

```bash
cnote show [[--ids(-i) [IDS ...]] [--max(-m) MAX]
```

The `--id` flag is mandatory, but all other arguments for this command are optional.

The easiest way get note ids into `cnote show` is with a pipe from the `cnote find` command.

```bash
cnote find -q | cnote show
```

## Removing Notes

Notes from the cNote database can be shown in their entirety with the `cnote rm` command:

```bash
cnote rm [[--ids(-i) [IDS ...]]
```

All arguments for this command are mandatory. The easiest way get note ids into `cnote rm` is with a pipe from the `cnote find` command.

```bash
cnote find -q | cnote rm
```


## Updating Notes
Notes can be updated with the `cnote edit` command:

```bash
cnote new [[--id(-i) ID] [--body(-b) BODY] [--name(-n) NAME] [--tags(-t) [TAGS ...]]
```

This is functionally equivalent to a `cnote rm` followed by a `cnote new`. Note that this will give the note a new id.