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


def test_token_hashing():
    test_tokens = ['these', 'are', 'test', 'tokens']
    test_ids = [
        'bd4c4ea1b44a8ff2afa18dfd261ec2c8',
        '098f6bcd4621d373cade4e832627b4f6',
        '4015e9ce43edfb0668ddaa973ebc7e87',
        '25d7186fe598a394919623186ca325e2',
    ]
    assert set(test_ids) == set(notes.NoteTable.token_ids(test_tokens))


def test_note_display(capfd):
    test_notes = [
        {
            'id': '987654321',
            'host': 'test-computer',
            'timestamp': 12345678,
            'text': 'This is a note',
        },
        {
            'id': '123456789',
            'host': 'computer-test',
            'timestamp': 12345698,
            'text': 'This is also a note',
        },
    ]

    notes.NoteTable.show_notes(test_notes)
    out, _ = capfd.readouterr()
    assert out
