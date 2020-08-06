from pathlib import Path
from platform import system

from .fs import check_algo
from .subproc import run_win_proc


def peptide3d(input_file,
              output_dir,
              min_LEMHPlus=0,
              write_xml=True,
              write_binary=False,
              write_csv=False,
              write_binning=False,
              exe_path="C:/SYMPHONY_VODKAS/plgs/Peptide3D.exe" if system()=='Windows' else 'none',
              timeout=180):
    """Run Peptide3D.
    
    Args:
        input_file (str): a path to the file containing Apex3D's outcomes (a binary file, with extension '.bin' preferentially).
        output_dir (str): Path to where to place the output.
        write_xml (boolean): Write the output in an xml in the output folder.
        write_binary (boolean): Write the binary output in an xml in the output folder.
        write_csv (boolean): Write the ions to csv file.
        write_binning (boolean): Write binning file.
        min_LEMHPlus (int): The minimal (M)ass of the (L)ow (E)nergy precursor with a single charge (H+).
        exe_path (str): Path to the "Peptide3D.exe" executable.
        timeout (float): Timeout in minutes. Passing 0 will mock the process. Passing negative value will not run the process.

    Returns:
        pathlib.Path: path to the outcome xml file.
    """
    if timeout >= 0:
        input_file = Path(input_file)
        output_dir = Path(output_dir)
        pep3d_stdout = output_dir/'pep3d.log'
        # if input_file.suffix != '.bin':
        #     raise RuntimeError("Peptide3D failed: it accepts 'bin' input files only.")

        algo = check_algo(exe_path)
        cmd = ["powershell.exe", algo,
                f"-inputFileName '{input_file}'",
                f"-outputDirName '{output_dir}'",
                f"-WriteXML {int(write_xml)}",
                f"-WriteBinary {int(write_binary)}",
                f"-WriteAllIonsToCSV {int(write_csv)}",
                f"-WriteBinningFile {int(write_binning)}",
                f"-minLEMHPlus {min_LEMHPlus}"]
        run_win_proc(cmd, timeout, pep3d_stdout)

        if '_Apex3D' in input_file.stem:
            out = input_file.parent/input_file.stem.replace('_Apex3D','_Pep3D_Spectrum')
        else:
            out = input_file.stem + "_Pep3D_Spectrum"
            out = input_file.parent/out
        
        out_bin = out.with_suffix('.bin')
        out_xml = out.with_suffix('.xml')

        if not out_bin.exists() and not out_xml.exists():
            raise RuntimeError("Peptide3D's output missing.")
        
        return out_xml
    else:
        return None

