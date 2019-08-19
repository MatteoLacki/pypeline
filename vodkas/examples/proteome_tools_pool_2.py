"""Run the pipeline for the Proteome Tools project."""
from pathlib import Path
from pprint import pprint
import json
from collections import defaultdict

from vodkas import apex3d, StdErr, peptide3d, iadbs, wx2csv

debug = True
capture_output = True
proj_folder = Path(r"//MSSERVER/restoredData/proteome_tools")
parameters_file = proj_folder/"params/515.xml"
with open(proj_folder/"pool2.json", 'r') as f:
    settings = json.load(f)

if debug:
    print('Tasks:')
    pprint(settings)
    print()


exceptions = defaultdict(list)

# rawdatapath, fastapath = settings[2]
# data = settings[2:3]
# data = settings[2:]
data = settings[3:]
for rawdatapath, fastapath in data:    
    rawdatapath= Path(rawdatapath)
    fastapath  = Path(fastapath)
    raw_folder = rawdatapath.stem
    out_folder = Path("D:/projects/proteome_tools/RES/pool2")/raw_folder[0:5]/raw_folder    
    if debug:
        print('rawdatapath', '\n\t', rawdatapath, '\n\t', str(rawdatapath))
        print('fastapath', '\n\t', fastapath, '\n\t', str(fastapath))
        print('raw_folder', '\n\t', raw_folder)
        print('out_folder', '\n\t', out_folder)
        print('parameters_file','\n\t', parameters_file)
    try:
        apexOut, apex_proc = apex3d(rawdatapath,
                                    out_folder,
                                    write_binary=True,
                                    capture_output=capture_output,
                                    debug=debug)
        if debug:
            print(apexOut, apex_proc)
    except StdErr as e:
        print("Sometimes the errors are not reflected in the output.")
        print(e.err)
        apexOut = out_folder/(out_folder.name + "_Apex3D.bin")
        exceptions[rawdatapath].append(e)
    try:
        pep3dOut, pep_proc = peptide3d(apexOut.with_suffix('.bin'),
                                       out_folder,
                                       write_binary=True,
                                       min_LEMHPlus=350.0,
                                       capture_output=capture_output,
                                       debug=debug)
        if debug:
            print(pep3dOut, pep_proc)
    except Exception as e:
        print(e)
        exceptions[rawdatapath].append(e)
    try:
        iadbsOut, iadbs_proc = iadbs(pep3dOut.with_suffix('.xml'),
                                     out_folder, 
                                     fasta_file=fastapath,
                                     parameters_file=parameters_file,
                                     capture_output=capture_output,
                                     debug=debug)
        if debug:
            print(iadbsOut, iadbs_proc)
    except Exception as e:
        print(e)
        exceptions[rawdatapath].append(e)
    # iadbsOut = Path(r"D:/projects/proteome_tools/RES/T1707/T170722_03/T170722_03_IA_workflow")
    # out_folder= Path(r"D:/projects/proteome_tools/RES/T1707/T170722_03")
    try:
        report, wx2csv_proc = wx2csv(iadbsOut.with_suffix('.xml'),
                                     out_folder/"report.csv",
                                     debug=debug)
        if debug:
            print(report, wx2csv_proc)
            print("Finished")
    except Exception as e:
        print(e)
        exceptions.append(e)

print("And now all the exceptions:")
print(exceptions)