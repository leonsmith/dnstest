import pydig
import yaml
import cerberus


class InvalidConfig(Exception):

    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return 'Invalid Config: {}'.format(self.errors)


def _coerce_match(value):
    """
    Only a single match value was passed in, convert it to a list
    """
    if isinstance(value, list):
        return value

    return [value]


def _coerce_match_value(value):
    """
    If a match value was provided it's an exact match by default
    """
    if isinstance(value, dict):
        return value

    return {
        'value': value,
        'method': 'exact',
    }


def _coerce_record_domain(value):
    """
    Domains are always lowercase
    """
    return str(value).lower()


def _coerce_record_type(value):
    """
    Record types are always uppercase
    """
    return str(value).upper()


schema = {
    'nameservers': {
        'type': 'list',
        'required': False,
        'schema': {
            'type': 'string',
        }
    },
    'checks': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'name': {
                    'type': 'string',
                },
                'record': {
                    'required': True,
                    'type': 'dict',
                    'schema': {
                        'domain': {
                            'required': True,
                            'type': 'string',
                            'coerce': (_coerce_record_domain,),
                        },
                        'type': {
                            'required': True,
                            'type': 'string',
                            'coerce': (_coerce_record_type,),
                            'allowed': [query_type.name for query_type in pydig.QueryType]
                        }
                    }
                },
                'matches': {
                    'required': True,
                    'type': 'list',
                    'coerce': (_coerce_match,),
                    'schema': {
                        'type': 'dict',
                        'coerce': (_coerce_match_value,),
                        'schema': {
                            'value': {
                                'required': True,
                                'type': 'string',
                            },
                            'method': {
                                'required': True,
                                'type': 'string',
                                'allowed': ['exact', 'substring', 'regex'],
                            }
                        },
                    }
                }
            }
        }
    }
}


def load_validated_yaml(config):
    """
    Loads a yaml config file and runs it through the validator with our schema
    """

    # Create an instance of the validator with our schema
    validator = cerberus.Validator(schema=schema)

    # Load the yaml info a python dict
    with open(config, 'r') as stream:
        config = yaml.safe_load(stream)

    # Validate and normalized the provided config
    config = validator.validated(config)

    # Raise an exception if the config isn't valid
    if not config:
        raise InvalidConfig(errors=validator.errors)

    # Return our normalized config
    return config
