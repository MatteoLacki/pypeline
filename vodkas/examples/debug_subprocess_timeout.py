import subprocess
from pathlib import Path

from vodkas.misc import get_coresNo

out_stout = Path("C:/SYMPHONY_VODKAS/temp/subproc_test/apex.loglog")
raw_folder = "C:/ms_soft/MasterOfPipelines/Data/O190302_01.raw"
output_dir = "C:/SYMPHONY_VODKAS/temp/subproc_test"

lock_mass_z2=785.8426
lock_mass_tol_amu=.25
low_energy_thr=300
high_energy_thr=30
lowest_intensity_thr=750
write_xml=True
write_binary=True
write_csv=False
max_used_cores=get_coresNo()
path_to_apex3d="C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe"
PLGS=True
cuda=True
unsupported_gpu=True
debug=False

raw_folder = Path(raw_folder)
output_dir = Path(output_dir)
cmd = ["powershell.exe",
    str(Path("C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe")),
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

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
proc.poll()
proc.kill()
proc.wait(1)
output, error = proc.communicate()
proc.terminate()
try:
    with open(out_stout, 'w') as fh:
        proc = subprocess.Popen(cmd,
                                stdout=fh)
        proc.communicate(timeout=4)
except subprocess.TimeoutExpired:
    _ = subprocess.run("Taskkill /IM Apex3D64.exe /F")


proc = subprocess.Popen(cmd, 
                        stdout=subprocess.PIPE)

subprocess.Popen("Taskkill /IM Apex3D64.exe /F")


from pathlib import Path
from vodkas import apex3d
from subprocess import TimeoutExpired
raw_folder = "C:/ms_soft/MasterOfPipelines/Data/O190302_01.raw"
output_dir = "C:/SYMPHONY_VODKAS/temp/subproc_test"

try:
    apex3d(raw_folder, output_dir, timeout=2, make_log=True)
except TimeoutExpired as e:
    print(e)




try:
    outs, errs = proc.communicate(timeout=15)
except TimeoutExpired:
    proc.kill()
    outs, errs = proc.communicate()

if make_log:
        log = output_dir/"apex3d.log"
        kill = "Taskkill /IM {} /F".format(algo.name)
        try:
            with open(log, 'w') as h:    
                T0 = time()
                pr = Popen(cmd, stdout=h)
                pr.communicate(timeout=timeout)
                runtime = time() - T0
        except TimeoutExpired:
            _ = run(kill, capture_output=True)
            raise TimeoutExpired(" ".join(cmd), timeout)
    else:
        try:
            T0 = time()
            pr = Popen(cmd, stdout=PIPE)
            pr.communicate(timeout=timeout)
            runtime = time() - T0
        except TimeoutExpired:
            _ = run(kill, capture_output=True)
            raise TimeoutExpired(" ".join(cmd), timeout)
