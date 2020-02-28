from pathlib import Path

from .fs import check_algo
from .misc import get_coresNo, call_info
from .subproc import run_win_proc


def apex3d(raw_folder,
           output_dir,
           lock_mass_z2=785.8426,
           lock_mass_tol_amu=.25,
           low_energy_thr=300,
           high_energy_thr=30,
           lowest_intensity_thr=750,
           write_xml=True,
           write_binary=True,
           write_csv=False,
           max_used_cores=get_coresNo(),
           path="C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe",
           PLGS=True,
           cuda=True,
           unsupported_gpu=True,
           timeout=60,
           mock=False):
    """Analyze a Waters Raw Folder with Apex3D.
    
    Args:
        raw_folder (str): a path to the input folder with raw Waters data.
        output_dir (str): Path to where to place the output (bin & xml).
        lock_mass_z2 (float): The lock mass for doubly charged ion.
        lock_mass_tol_amu (float): Tolerance around lock mass (in atomic mass units, amu).
        low_energy_thr (int): The minimal intensity of a precursor ion so that it ain't a noise peak.
        high_energy_thr (int): The minimal intensity of a fragment ion so that it ain't a noise peak.
        lowest_intensity_thr (int): The minimal intensity of a peak to be analyzed.
        write_xml (boolean): Write the output in an xml in the output folder.
        write_binary (boolean): Write the binary output in an xml in the output folder.
        write_csv (boolean): Write the output in a csv in the output folder (doesn't work).
        max_used_cores (int): The maximal number of cores to use.
        path (str): Path to the "Apex3D.exe" executable.
        PLGS (boolean): No idea what it is.
        cuda (boolean): Use CUDA.
        unsupported_gpu (boolean): Try using an unsupported GPU for calculations. If it doesn't work, the pipeline switches to CPU which is usually much slower.
        timeout (float): Timeout in minutes.
        mock (bool): Run without calling apex3D64.

    Returns:
        tuple: path to the outcome xml and the completed process (or None if mocking).
    """
    algo = check_algo(path)
    raw_folder = Path(raw_folder)
    output_dir = Path(output_dir)
    apex_stdout = output_dir/'apex3d.log'

    cmd = ["powershell.exe", algo,
          f"-pRawDirName '{raw_folder}'",
          f"-outputDirName '{output_dir}'",
          f"-lockMassZ2 {lock_mass_z2}",
          f"-lockmassToleranceAMU {lock_mass_tol_amu}",
          f"-leThresholdCounts {low_energy_thr}",
          f"-heThresholdCounts {high_energy_thr}",
          f"-binIntenThreshold {lowest_intensity_thr}",
          f"-writeXML {int(write_xml)}",
          f"-writeBinary {int(write_binary)}",
          f"-bRawCSVOutput {int(write_csv)}",
          f"-maxCPUs {int(max_used_cores)}",
          f"-PLGS {int(PLGS)}",
          f"-bEnableCuda {int(cuda)}",
          f"-bEnableUnsupportedGPUs {int(unsupported_gpu)}"]

    if mock:
        pr = None
    else:
        pr,_ = run_win_proc(cmd, timeout, apex_stdout)

    out_bin = output_dir/(raw_folder.stem + "_Apex3D.bin")
    out_xml = out_bin.with_suffix('.xml')

    if not out_bin.exists() and not out_xml.exists():
        raise RuntimeError("Apex3D's output missing.")

    return out_xml, pr


# def test_apex3d():
#     """test Apex3D."""
#     apex3d(Path("C:/ms_soft/MasterOfPipelines/RAW/O1903/O190302_01.raw"),
#            Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput"))

# if __name__ == "__main__":
#     test_apex3d()