from pathlib import Path

from vodkas.fs import check_algo
from vodkas.subproc import run_win_proc


def peptide3d(input_file,
              output_dir,
              min_LEMHPlus=0,
              write_xml=True,
              write_binary=True,
              write_csv=False,
              write_binning=False,
              path_to_peptide3d="C:/SYMPHONY_VODKAS/plgs/Peptide3D.exe",
              timeout_peptide3d=60,
              make_log=True,
              verbose=False,
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
        timeout_peptide3d (float): Timeout in minutes.
        make_log (boolean): Make log.
        verbose (boolean): Make output verbose.
        kwds: other parameters.
    Returns:
        tuple: the completed process and the path to the outcome (preference of xml over bin).
    """
    algo = check_algo(path_to_peptide3d, verbose)
    input_file = Path(input_file)
    output_dir = Path(output_dir)
    if input_file.suffix != '.bin':
        raise RuntimeError("Peptide3D failed: it accepts 'bin' input files only.")
    log_path = output_dir/"peptide3d.log" if make_log else ""

    cmd = ["powershell.exe",
            str(algo),
            f"-inputFileName {input_file}",
            f"-outputDirName {output_dir}",
            f"-WriteXML {int(write_xml)}",
            f"-WriteBinary {int(write_binary)}",
            f"-WriteAllIonsToCSV {int(write_csv)}",
            f"-WriteBinningFile {int(write_binning)}",
            f"-minLEMHPlus {min_LEMHPlus}"]

    pr, runtime = run_win_proc(cmd,
                               timeout_peptide3d,
                               log_path)

    if '_Apex3D' in input_file.stem:
        out = input_file.parent/input_file.stem.replace('_Apex3D','_Pep3D_Spectrum')
    else:
        out = input_file.stem + "_Pep3D_Spectrum"
        out = input_file.parent/out
    out_bin = out.with_suffix('.bin')
    out_xml = out.with_suffix('.xml')

    if not out_bin.exists() and not out_xml.exists():
        raise RuntimeError("Peptide3D's output missing.")

    if verbose:
        print(f'Peptide3D finished in {runtime} minutes.')

    return out_bin.with_suffix(''), pr, runtime


def test_peptide3d():
    """Test the stupid Peptide3D."""
    peptide3d(Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput/O190302_01_Apex3D.bin"),
              Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput"))
