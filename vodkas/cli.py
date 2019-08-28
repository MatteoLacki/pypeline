from docstr2argparse import foo2parser, parse_arguments
from subprocess import TimeoutExpired

from .misc import monitor, FuncState


def make_cli(script, custom_args={}, custom_delete=[]):
    """Make a CLI for a given function.

    Args:
        script (function): the function to make the CLI for.
        custom_args (dict): custom modification to CLI.
    """
    script, fun_monitor = monitor(script)
    parser = foo2parser(script)
    K = dict(parse_arguments(script))
    del K['--write_xml'], K['--write_binary'], 
    for c in custom_delete:
        del K[c]
    K["--no_xml"] = dict(
        dest="write_xml",
        action='store_false',
        help="Don't dump the output to an xml file. [default = True]")
    K["--no_binary"] = dict(
        dest="write_binary",
        action='store_false',
        help="Don't dump the output into a binary format. [default = True]")
    K["--timeout"] = dict(
        default=24,
        type=lambda h: float(h)/3600,
        help="Timeout (in hours). [default = 24]")
    K.update(parse_arguments(FuncState.json))
    # K["--logs_folder"] = logs_folder_dict
    # K["--logs_server_folder"] = logs_server_folder_dict
    K["--show_less_output"] = dict(
        dest="capture_output",
        action='store_true',
        help="Don't show terminal output. [default = False]")
    K["--comment"] = dict(help="Your custom comment.", type=str, default="")
    K.update(custom_args)
    for name, kwds in K.items():
        parser.add_argument(name, **kwds)
    args = parser.parse_args()
    script_args = args.__dict__.copy()
    del script_args['logs_folder'], script_args['logs_server_folder'], script_args['comment']
    error = ""
    try:
        out_file, process = script(**script_args)
    except TimeoutExpired:
        error = 'Timeout of {} hour(s) reached.'.format(args.timeout)
        print(error)
    except (RuntimeError,FileNotFoundError) as e:
        error = "RuntimeError."
        print(error)
        print(e)
    fun_monitor[script.__name__][0]['__error__'] = error
    fun_monitor[script.__name__][0]['__comment__'] = args.comment
    fun_monitor.json(args.logs_folder, args.logs_server_folder, prefix='{}_'.format(script.__name__))

