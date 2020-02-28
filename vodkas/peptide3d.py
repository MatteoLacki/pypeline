from pathlib import Path

from .fs import check_algo
from .subproc import run_win_proc


def peptide3d(input_file,
              output_dir,
              min_LEMHPlus=0,
              write_xml=True,
              write_binary=False,
              write_csv=False,
              write_binning=False,
              path="C:/SYMPHONY_VODKAS/plgs/Peptide3D.exe",
              timeout=60,
              mock=False):
    """Run Peptide3D.
    
    Args:
        input_file (str): a path to the file containing Apex3D's outcomes (a binary file, with extension '.bin').
        output_dir (str): Path to where to place the output.
        write_xml (boolean): Write the output in an xml in the output folder.
        write_binary (boolean): Write the binary output in an xml in the output folder.
        write_csv (boolean): Write the ions to csv file.
        write_binning (boolean): Write binning file.
        min_LEMHPlus (int): The minimal (M)ass of the (L)ow (E)nergy precursor with a single charge (H+).
        path (str): Path to the "Peptide3D.exe" executable.
        timeout (float): Timeout in minutes.
        mock (bool): Run without calling Peptide3D.

    Returns:
        tuple: path to the outcome xml file and the completed process (or None if mocking).
    """
    algo = check_algo(path)
    input_file = Path(input_file)
    output_dir = Path(output_dir)
    pep3d_stdout = output_dir/'pep3d.log'

    if input_file.suffix != '.bin':
        raise RuntimeError("Peptide3D failed: it accepts 'bin' input files only.")

    cmd = ["powershell.exe", algo,
            f"-inputFileName '{input_file}'",
            f"-outputDirName '{output_dir}'",
            f"-WriteXML {int(write_xml)}",
            f"-WriteBinary {int(write_binary)}",
            f"-WriteAllIonsToCSV {int(write_csv)}",
            f"-WriteBinningFile {int(write_binning)}",
            f"-minLEMHPlus {min_LEMHPlus}"]

    if mock:
        pr = None
    pr, runtime = run_win_proc(cmd, timeout, pep3d_stdout)

    if '_Apex3D' in input_file.stem:
        out = input_file.parent/input_file.stem.replace('_Apex3D','_Pep3D_Spectrum')
    else:
        out = input_file.stem + "_Pep3D_Spectrum"
        out = input_file.parent/out
    out_bin = out.with_suffix('.bin')
    out_xml = out.with_suffix('.xml')

    if not out_bin.exists() and not out_xml.exists():
        raise RuntimeError("Peptide3D's output missing.")
    
    return out_xml, pr


def peptide3d_mock(input_file,
                   output_dir,
                   min_LEMHPlus=0,
                   write_xml=True,
                   write_binary=False,
                   write_csv=False,
                   write_binning=False,
                   path="C:/SYMPHONY_VODKAS/plgs/Peptide3D.exe",
                   timeout=60):
    input_file = Path(input_file)
    output_dir = Path(output_dir)
    pep3d_stdout = output_dir/'pep3d.log'
    if '_Apex3D' in input_file.stem:
        out = input_file.parent/input_file.stem.replace('_Apex3D','_Pep3D_Spectrum')
    else:
        out = input_file.stem + "_Pep3D_Spectrum"
        out = input_file.parent/out
    out_bin = out.with_suffix('.bin')
    out_xml = out.with_suffix('.xml')
    return out_xml, True, 0.0

# def test_peptide3d():
#     """Test the stupid Peptide3D."""
#     peptide3d(Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput/O190302_01_Apex3D.bin"),
#               Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput"))
