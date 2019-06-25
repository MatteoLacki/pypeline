import subprocess
from pathlib import Path


def get_coresNo():
	import multiprocessing
	return multiprocessing.cpu_count()

def apex3d(raw_folder,
		   output_dir,
		   lock_mass_z2=785.8426,
		   lock_mass_tol_amu=.25,
		   low_energy_thr=300,
		   high_energy_thr=30,
		   lowest_intensity_thr=750,
		   write_xml=True,
		   write_binary=True,
		   write_raw_csv=True,
		   max_used_cores=get_coresNo(),
		   apex64=True,
		   path_to_apex=Path("C:/Symphony/PLGS")):
	"""A wrapper around the infamous Apex3d.
	
	Args:
		raw_folder (Path or str): a path to the input folder with raw Waters data.
		output_dir (Path or str): Path to where to place the output.
		lock_mass_z2 (float): The lock mass for doubly charged ion (which one, dunno, but I guess a very important one).
		lock_mass_tol (float): Tolerance around lock mass (in atomic mass units, amu).
		apex64 (boolean): Use 'Apex3D64.exe' rather than 'Apex3D.exe'.
	"""
	algo = path_to_apex/("Apex3D64.exe" if apex64 else "Apex3D.exe")
	subprocess.call(["powershell.exe", str(algo)])
	# set apx3dCmd=%apx3d% -pRawDirName "%rawFile%" -outputDirName "%processingFolder%" -lockmassZ2 785.8426 -lockmassToleranceAMU 0.25 -leThresholdCounts %leThreshold% -heThresholdCounts %heThreshold% -binIntenThreshold %inThreshold% -writeXML 1 -PLGS 1
