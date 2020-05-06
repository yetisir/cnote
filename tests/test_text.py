from dnote import notes


def test_preprocessing():
    test_input = (
        '\n\n\t     This is a text string that has extra whitespace      \n\n')
    test_output = 'This is a text string that has extra whitespace'

    text = notes.Text(test_input)
    assert text.raw == test_output


def test_tokenize():
    test_input = (
        'This is a text string that requires tokenizing with some CRAZY !@#$')
    test_output = {
        '0cc175b9c0f1b6a831c399e269772661': 'a',
        '1cb251ec0d568de6a929b520c4aed8d1': 'text',
        '1df9f64fc9d0c3e4ea2b1546cc216572': 'requir',
        '21582c6c30be1217322cdb9aebaf4a59': 'that',
        '94a08da1fecbb6e8b46990538c7b50b2': 'token',
        'a2a551a6458a8de22446cc76d639a9e9': 'is',
        'b45cffe084dd3d20d928bee85e7b0f21': 'string',
        'd9aebf7d5a83db9709fe0af7b92ab73a': 'thi',
        '01abfc750a0c942167651c40d088531d': '#',
        '03d59e663c1af9ac33a9949d1193505a': 'some',
        '23a58bf9274bedb19375e527a0744fa9': 'with',
        '518ed29525738cebdac49c49e60ea9d3': '@',
        '6755872b84c93260ff7149cd2ef5572c': 'crazi',
        '9033e0e305f247c0c3c80d0c7848c8b3': '!',
        'c3e97dd6e97fb5125688c97f36720cbe': '$',
    }

    text = notes.Text(test_input)
    assert text.tokens == test_output
