import re


class ExactMatch:

    def __init__(self, value):
        self.value = value

    def __call__(self, record):
        return self.value == record

    def __str__(self):
        return 'Matches: {}'.format(self.value)


class RegexMatch:

    def __init__(self, value):
        self.value = value

    def __call__(self, record):
        return self.value == record

    def __str__(self):
        return 'Regex: {}'.format(self.value)


class SubstringMatch:

    def __init__(self, value):
        self.value = value

    def __call__(self, record):
        return bool(re.search(self.value, record))

    def __str__(self):
        return 'Substring: {}'.format(self.value)


MAPPING = {
    'exact': ExactMatch,
    'regex': RegexMatch,
    'substring': SubstringMatch,
}


def load(config):
    """
    C
    """
    klass = MAPPING[config['method']]
    return klass(config['value'])
