def read_description(filename):
    with open('commands/{}'.format(filename), 'r', encoding='utf-8') as f:
        return f.read()
