import platform
import socket

from .apex3d import apex3d
from .exceptions import StdErr
from .peptide3d import peptide3d
from .iadbs import iadbs
from .wx2csv import wx2csv
from .plgs import plgs


on_windows = platform.system() == 'Windows'
currentIP = socket.gethostbyname(socket.gethostname())