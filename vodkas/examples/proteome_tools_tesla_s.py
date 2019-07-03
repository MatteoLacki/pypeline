"""Run the pipeline for the Proteome Tools project."""
from pathlib import Path
import json

from vodkas import apex3d, peptide3d, iadbs, wx2csv

debug = True
proj_folder = Path(r"//MSSERVER/restoredData/proteome_tools")
parameters_file = proj_folder/"params/515.xml"
with open(proj_folder/"plate1.json", 'r') as f:
    settings = json.load(f)

# rawdatapath, fastapath = next(iter(settings))
for rawdatapath, fastapath in settings:
    rawdatapath= Path(rawdatapath)
    fastapath  = Path(fastapath)
    raw_folder = rawdatapath.stem
    out_folder = Path("D:/projects/proteome_tools/RES")/raw_folder[0:5]/raw_folder
    if debug:
        print('rawdatapath',    '\n\t', rawdatapath,    '\n\t', str(rawdatapath))
        print('fastapath',      '\n\t', fastapath,      '\n\t', str(fastapath))
        print('raw_folder',     '\n\t', raw_folder)
        print('out_folder',     '\n\t', out_folder)
        print('parameters_file','\n\t', parameters_file)

    apexOut, apex_proc = apex3d(rawdatapath, out_folder,
                                write_binary=True,
                                capture_output=True,
                                debug=True)
    if debug:
        print(apexOut, apex_proc)

    pep3dOut, pep_proc = peptide3d(apexOut.with_suffix('.bin'),
                                   out_folder,
                                   write_binary=True,
                                   min_LEMHPlus=350.0,
                                   capture_output=True,
                                   debug=True)
    if debug:
        print(pep3dOut, pep_proc)

    iadbsOut, iadbs_proc = iadbs(pep3dOut.with_suffix('.xml'),
                                 out_folder, 
                                 fasta_file=fastapath,
                                 parameters_file=parameters_file,
                                 capture_output=True,
                                 debug=True)
    if debug:
        print(iadbsOut, iadbs_proc)

    report, wx2csv_proc = wx2csv(iadbsOut.with_suffix('.xml'),
                                 temp_folder/parameters_file.stem/"report.csv",
                                 debug=debug)
    if debug:
        print(report, wx2csv_proc)
        print("Finished")
