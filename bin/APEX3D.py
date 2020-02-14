from vodkas.cli import make_cli
from vodkas.apex3d import apex3d

if __name__ == '__main__':
    custom_kwds = {"--no_CUDA": 
        dict(dest="cuda",
             action='store_false',
             help="Don't use CUDA, Getruda (haha). [default = False]")}
    make_cli(apex3d, custom_kwds,
             ['--cuda', '--subprocess_run_kwds'])
