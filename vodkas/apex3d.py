import subprocess
from pathlib import Path
from time import time

from vodkas.misc import get_coresNo
from vodkas.exceptions import StdErr


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
           path_to_apex3d="C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe",
           PLGS=True,
           cuda=True,
           unsupported_gpu=True,
           debug=False,
           run_kwds={},
           **kwds):
    """Analyze a Waters Raw Folder with Apex3D.
    
    Args:
        raw_folder (str): a path to the input folder with raw Waters data.
        output_dir (str): Path to where to place the output.
        lock_mass_z2 (float): The lock mass for doubly charged ion (which one, dunno, but I guess a very important one).
        lock_mass_tol_amu (float): Tolerance around lock mass (in atomic mass units, amu).
        low_energy_thr (int): The minimal intensity of a precursor ion so that it ain't a noise peak.
        high_energy_thr (int): The minimal intensity of a fragment ion so that it ain't a noise peak.
        lowest_intensity_thr (int): The minimal intensity of a peak to be analyzed.
        write_xml (boolean): Write the output in an xml in the output folder.
        write_binary (boolean): Write the binary output in an xml in the output folder.
        write_csv (boolean): Write the output in a csv in the output folder (doesn't work).
        max_used_cores (int): The maximal number of cores to use.
        path_to_apex3d (str): Path to the "Apex3D.exe" executable.
        PLGS (boolean): No idea what it is.
        cuda (boolean): Use CUDA.
        unsupported_gpu (boolean): Try using an unsupported GPU for calculations. If it doesn't work, the pipeline switches to CPU which is usually much slower.
        debug (boolean): Debug mode.
        run_kwds (dict): arguments for the subprocess.run.
        kwds: other parameters.
    Returns:
        tuple: the path to the outcome (no extension: choose it yourself and believe more in capitalism) and the completed process.
    """
    algo = Path(path_to_apex3d)
    assert algo.exists(), "Executable is missing! '{}' not found.".format(algo)
    raw_folder = Path(raw_folder)
    output_dir = Path(output_dir)
    cmd = ["powershell.exe",
        str(algo),
        "-pRawDirName {}".format(raw_folder),
        "-outputDirName {}".format(output_dir),
        "-lockMassZ2 {}".format(lock_mass_z2),
        "-lockmassToleranceAMU {}".format(lock_mass_tol_amu),
        "-leThresholdCounts {}".format(int(low_energy_thr)),
        "-heThresholdCounts {}".format(int(high_energy_thr)),
        "-binIntenThreshold {}".format(int(lowest_intensity_thr)),
        "-writeXML {}".format(int(write_xml)),
        "-writeBinary {}".format(int(write_binary)),
        "-bRawCSVOutput {}".format(int(write_csv)),
        "-maxCPUs {}".format(int(max_used_cores)),
        "-PLGS {}".format(int(PLGS)),
        "-bEnableCuda {}".format(int(cuda)),
        "-bEnableUnsupportedGPUs {}".format(int(unsupported_gpu))]
    if debug:
        print('Apex3D debug:')
        print(cmd)
    T0 = time()
    process = subprocess.run(cmd,**run_kwds)
    runtime = time() - T0
    out_bin = output_dir/(raw_folder.stem + "_Apex3D.bin")
    out_xml = out_bin.with_suffix('.xml')
    if subprocess_run_kwds.get('capture_output', False):# otherwise no input was caught.
        log = output_dir/"apex3d.log"
        log.write_bytes(process.stdout)
    if not out_bin.exists() and not out_xml.exists():
        raise RuntimeError("Apex3D failed: output is missing")
    if process.stderr:
        print(process.stderr)
        raise StdErr(process)
    if debug:
        print(out_bin.with_suffix(''))
        print('Apex3D finished.')
    return out_bin.with_suffix(''), process, runtime

def test_apex3d():
    """test the stupid Apex3D."""
    apex3d(Path("C:/ms_soft/MasterOfPipelines/RAW/O1903/O190302_01.raw"),
           Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput"))

if __name__ == "__main__":
    test_apex3d()