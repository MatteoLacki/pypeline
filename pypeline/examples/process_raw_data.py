from pathlib import Path
from pypeline import apex3d, peptide3d, iadbs
from pypeline.fs import cp

# if __name__ == "__main__":
# raw = Path("//MSSERVER/restoredData/proteome_tools/net/idefix/WIRD_GESICHERT/T1707/T170722_03.raw")
# local file: nice small data-set
raw = Path("C:/ms_soft/MasterOfPipelines/RAW/O1903/O190302_01.raw")
temp = Path("C:/Symphony/Temp/test")
# what to do, if this file already existed? well, fuck it.
# no, need to add in some randomization!!!

temp.mkdir(exist_ok=True)
raw = Path("C:/ms_soft/MasterOfPipelines/RAW/O1903/O190302_01dsvsa.raw")
apex_out, process = apex3d(raw, temp, capture_output=True)

# apex_out = temp/(raw.stem + "_Apex3D.xml")
help(peptide3d)
# peptide3d(apex_out, temp)


# w = Path("C:/haha/dupa1.txt")
# z = w.parent/w.stem.replace('01','02')
# z
# g = z.with_suffix('.bin')
# g
# g.with_suffix('.xml')

# help(z.with_suffix)
# pep3d_out = temp/(raw.stem + "_Pep3D_Spectrum.bin")

# iadbs()
# help(iadbs)

