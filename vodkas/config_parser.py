import collections
import configparser
import pathlib

from furious_fastas.protogui import fasta_file

from .google_doc_string_parser import parse_google


class AdvConfigParser(configparser.ConfigParser):
    def __init__(self, path, *args, **kwds):
        super().__init__(*args, **kwds)
        out = self.read(path)    
        assert len(out) == 1, "Something is fishy about the config."

    def get_foo_args(self, foo):
        """Get configuration values for given function.

        Args:
            foo (function): function with a google-scheme docstring.
        Returns:
            dict: Foo's argument to value mapping.
        """
        type2configMethod = collections.defaultdict(lambda:'get')
        type2configMethod['boolean'] = 'getboolean'
        type2configMethod['int']     = 'getint'
        type2configMethod['float']   = 'getfloat'

        assert foo.__name__ in self, f"Function '{foo.__name__}' is not documented in the config."

        fooArg2type = {a_name: a_type 
                       for a_name, a_type, a_help 
                       in parse_google(foo.__doc__)['Args']}

        foo_args = {}
        for arg in self[foo.__name__]:
            parser = getattr(self, type2configMethod[fooArg2type[arg]])
            foo_args[arg] = parser(foo.__name__, arg)

        return foo_args

    def get_ip_port(self):
        ip, port = self['logging']['log_server_ip_port'].split(':', 1)
        port = int(port)
        return ip, port

    def get_log_file(self):
        log_file = pathlib.Path(self['logging']['log_file']).expanduser().resolve()
        log_file.parent.mkdir(parents=True, exist_ok=True)
        return log_file

    def get_fasta_path(self, verbose=False):
        fasta_file_kwds = self.get_foo_args(fasta_file)
        return fasta_file(**fasta_file_kwds)
