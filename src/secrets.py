def get_secret(key):
    path = '/run/secrets/%s' % key
    with open(path, 'r') as f:
        return f.read()
