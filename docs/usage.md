# dNote Usage
dNote uses your default text editor for creating notes. If no system editor is specified this will default to Vim, though this can be configured (see configuration section). The command syntax has been inspired by similar CLI note taking utilities ([notes](https://github.com/pimterry/notes) and [notes-cli](https://github.com/rhysd/notes-cli)), with modifications where appropriate.

## Note Attributes

Each note created in dNote has the following attributes that can be specified:

* body - the main text of the note.
* name - a few words to describe the body of the note
* tags - metatext that can be used to help group and search

And two other attributes that are automatically determined

* host - the hostname of the system used to create the note
* timestamp - the timestamp (in UTC) when the note was created


## Creating Notes
Notes are added to the dNote database with the `dnote new` command:

```bash
dnote new [--body(-b) BODY] [--name(-n) NAME] [--tags(-t) [TAGS ...]]
```

All the arguments for this command are optional. If no arguments are specified, dNote will open up a command line text editor in which you can type your notes. dNotes will grab the contents of the file and save it directly to the configured DynamoDB database.

```bash
dnote new
```

The text of this note can also be specified using the `--body` flag:

```bash
dnote new -b "this is a note"
```

Alternatively, we can pipe in a note. Piped input on the `new` command is always interpereted as the `--body` argument. When a pipe is used, the text editor is still launched so that the note can be edited before saving. Note that use of the `--body` flag will override any piped input.

```bash
echo "this is a piped note" | dnote new
```

We can use this feature to pipe in the contents of a file.

```bash
cat note.txt | dnote new
```

By default, a name is assigned to the note based on your username, but this can be overridden with the `--name` flag. The note name does not have to be unique, but should be a high level description of the note contents (like a file name).

```bash
dnote new -b "this note has a custom name" -n "custom note name"
```

We can also tag notes so they may be easier to find in the future. Tagging is accomplished with the `--tag` flag  and takes a list of any number of relavent tags.

```bash
dnote new -b "this note has custom tags" -t "custom tag 1" "custom tag 2"
```

## Finding Notes
The dNote database searched for notes with the `dnote find` command:

```bash
dnote find [--range(-r) [RANGE ...]] [--name(-n) [NAME ...]] [--body(-b) [BODY ...]] [--tags(-t) [TAGS ...]] [--host(-h) [HOST ...]] [--exact(-e)] [--quiet(-e)]
```

All arguments for this command ar optional. If not arguments are specified, dNote will return up to 100 notes from the dNote database.

```
dnote find
```

dNote allows searching of all four text fields (i.e. name, body, tags, and host) as well as the timestamp field. We can specify a time range with the `--range` flag and include any of the four text fields with their corresponding flags: 

For example, we can query all notes that contain mentions of words that share the stem of 'test' (e.g. 'tests', 'testing', 'tester', etc.).

```bash
dnote find -b "test"
```

We can also specify multiple search terms in a single field. This query will return notes that have mentions of both 'test' and 'note'.

```bash
dnote find -b "test" "note"
```

To query multiple fields, we just add them to the search query. If we were only interested in the test notes that were written from a system called 'testserver', we could update the previous command to be as follows:

```bash
dnote find -b "test" note -h "testserver"
```

Querying the time range takes one or two arguments representing the bounding times of the range. If only one argument is given, the second argument is assumed to be "now". A unique feature of dNote is that it supports relative human time references to find all the notes written in the last day we can just write:

```bash
dnote find -r "one day ago"
```

Which is equivalent to:

```bash
dnote find -r "now" "one day ago"
```

By default, the search engine compares the stems of the search words - this allows for near matches (e.g. runner and running would match) which makes the search a more human experience. That being said, we can specify an exact search by using the '--exact' flag.

```bash
dnote find -b 'runner' --exact
```

If we only want the note ids, we can use the `--quiet` flag

```bash
dnote find --quiet
```

By default, we can only return up to 100 notes in a single search. The returned notes will only print the first 10 lines - to show the full notes we can use the `dnote show` command described below.

## Showing Notes

Notes from the dNote database can be shown in their entirety with the `dnote show` command:

```bash
dnote show [[--ids(-i) [IDS ...]] [--max(-m) MAX]
```

The `--id` flag is mandatory, but all other arguments for this command are optional.

The easiest way get note ids into `dnote show` is with a pipe from the `dnote find` command.

```bash
dnote find -q | dnote show
```

## Removing Notes

Notes from the dNote database can be shown in their entirety with the `dnote rm` command:

```bash
dnote rm [[--ids(-i) [IDS ...]]
```

All arguments for this command are mandatory. The easiest way get note ids into `dnote rm` is with a pipe from the `dnote find` command.

```bash
dnote find -q | dnote rm
```


## Updating Notes
Notes can be updated with the `dnote edit` command:

```bash
dnote new [[--id(-i) ID] [--body(-b) BODY] [--name(-n) NAME] [--tags(-t) [TAGS ...]]
```

This is functionally equivalent to a `dnote rm` followed by a `dnote new`. Note that this will give the note a new id.