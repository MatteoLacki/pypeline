REM assuming git and python preinstalled
REM python and Scripts added to PATH

REM making python scripts executable
$env:Pathext += ";.py"

mkdir "C:\\SYMPHONY_VODKAS\" -Force

pip install numpy scipy networkx
pip install ipython

REM installing pipeline
cd C:\\SYMPHONY_VODKAS\
git clone https://github.com/MatteoLacki/fs_ops
git clone https://github.com/MatteoLacki/docstr2argparse
git clone https://github.com/MatteoLacki/waters
git clone https://github.com/MatteoLacki/vodkas

pip install -e fs_ops
pip install -e docstr2argparse
pip install -e waters
pip install -e vodkas

