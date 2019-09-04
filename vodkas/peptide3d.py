import subprocess
from pathlib import Path
from time import time


def peptide3d(input_file,
              output_dir,
              min_LEMHPlus=0,
              write_xml=True,
              write_binary=True,
              write_csv=False,
              write_binning=False,
              path_to_peptide3d="C:/SYMPHONY_VODKAS/plgs/Peptide3D.exe",
              debug=False,
              run_kwds={},
              **kwds):
    """Run Peptide3D.
    
    Args:
        input_file (str): a path to the file containing Apex3D's outcomes (a binary file, with extension '.bin').
        output_dir (str): Path to where to place the output.
        write_xml (boolean): Write the output in an xml in the output folder.
        write_binary (boolean): Write the binary output in an xml in the output folder.
        write_csv (boolean): Write the ions to csv file.
        write_binning (boolean): Write binning file.
        min_LEMHPlus (int): The minimal (M)ass of the (L)ow (E)nergy precursor with a single charge (H+).
        path_to_peptide3d (str): Path to the "Peptide3D.exe" executable.
        debug (boolean): Debug mode.
        run_kwds (dict): arguments for the subprocess.run.
        kwds: other parameters for 'subprocess.run'.
    Returns:
        tuple: the completed process and the path to the outcome (preference of xml over bin).
    """
    algo = Path(path_to_peptide3d)
    assert algo.exists(), "Executable is missing! '{}' not found.".format(algo)
    input_file = Path(input_file)
    output_dir = Path(output_dir)
    if input_file.suffix != '.bin':
        raise RuntimeError("Peptide3D failed: it accepts 'bin' input files only.")
    cmd = ["powershell.exe",
            str(algo),
            "-inputFileName {}".format(input_file),
            "-outputDirName {}".format(output_dir),
            "-WriteXML {}".format(int(write_xml)),
            "-WriteBinary {}".format(int(write_binary)),
            "-WriteAllIonsToCSV {}".format(int(write_csv)),
            "-WriteBinningFile {}".format(int(write_binning)),
            "-minLEMHPlus {}".format(min_LEMHPlus) ]
    if debug:
        print('Peptide3D debug:')
        print(cmd)
    T0 = time()
    process = subprocess.run(cmd, **run_kwds)
    runtime = time() - T0
    if '_Apex3D' in input_file.stem:
        out = input_file.parent/input_file.stem.replace('_Apex3D','_Pep3D_Spectrum')
    else:
        out = input_file.stem + "_Pep3D_Spectrum"
        out = input_file.parent/out
    out_bin = out.with_suffix('.bin')
    out_xml = out.with_suffix('.xml')
    if subprocess_run_kwds.get('capture_output', False):# otherwise no input was caught.
        log = output_dir/"peptide3d.log"
        log.write_bytes(process.stdout)
    if not out_bin.exists() and not out_xml.exists():
        raise RuntimeError("Peptide3D failed: output is missing")
    if process.stderr:
        print(process.stderr)
        raise RuntimeError("Peptide3D failed: WTF")
    if debug:
        print(out_bin.with_suffix(''))
        print('peptide3D finished.')
    return out_bin.with_suffix(''), process, runtime


def test_peptide3d():
    """Test the stupid Peptide3D."""
    peptide3d(Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput/O190302_01_Apex3D.bin"),
              Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput"))
