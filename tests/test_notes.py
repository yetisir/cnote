from dnote import notes


def test_tokenize():
    test_notes = {
        'This is a note': [
            'this', 'thi', 'is', 'a', 'note'],
        'This is a note requiring stemming': [
            'this', 'thi', 'is', 'a', 'note', 'requiring', 'requir',
            'stemming', 'stem'],
    }

    for text, tokens in test_notes.items():
        assert set(tokens) == set(notes.NoteTable.tokenize(text))
