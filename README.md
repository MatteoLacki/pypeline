# Rationale
Use Python to make your experience with Waters' Symphony Pipeline a much nicer experience.
Otherwise said, add some synthactic sugar to Waters.
In my country this results in Vodkas.

# Installation

```bash
    pip install git+https://github.com/MatteoLacki/vodkas
```

# Usage

Here is an examplary use.
Be sure to set up the remote disks before-hand and make sure that all
folders have proper, most lenient access privileges.
```Python
from pathlib import Path

from vodkas import apex3d, peptide3d, iadbs
from vodkas.fs import cp

raw = Path("C:/ms_soft/MasterOfPipelines/RAW/O1903/O190302_01.raw")
temp = Path("C:/Symphony/Temp/test")
apexOutPath, apex_proc = apex3d(raw, temp, write_binary=True, capture_output=True)
apexOutBIN = apexOutPath.with_suffix('.bin')
pep3dOutPath, pep_proc = peptide3d(apexOutBIN, temp,
                                   write_binary=True,
                                   min_LEMHPlus=350.0,
                                   capture_output=True)
pep3dOutXML = pep3dOutPath.with_suffix('.xml')
iadbsOutPath, iadbs_proc = iadbs(pep3dOutXML, temp, 
                                 fasta_file="C:/Symphony/Search/human.fasta",
                                 parameters_file="C:/Symphony/Search/251.xml",
                                 capture_output=True)
```

Best Regards,
Matteo Lacki
