import configparser
import collections

from .google_doc_string_parser import parse_google



def get_config_values(foo, config):
    """Get configuration values for given function.

    Args:
        foo (function): function with a google-scheme docstring.
        config (configparser.ConfigParser): configuration.
    Returns:
        dict: Foo's argument to value mapping.
    """
    type2configMethod = collections.defaultdict(lambda:'get')
    type2configMethod['boolean'] = 'getboolean'
    type2configMethod['int']     = 'getint'
    type2configMethod['float']   = 'getfloat'

    assert foo.__name__ in config, f"Function '{foo.__name__}' is not documented in the config."

    fooArg2type = {a_name: a_type 
                   for a_name, a_type, a_help 
                   in parse_google(foo.__doc__)['Args']}

    foo_args = {}
    for arg in config[foo.__name__]:
        parser = getattr(config,
                         type2configMethod[fooArg2type[arg]])
        foo_args[arg] = parser(foo.__name__, arg)

    return foo_args