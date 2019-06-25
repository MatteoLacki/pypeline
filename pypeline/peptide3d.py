import subprocess
from pathlib import Path


def peptide3d(input_file,
		   	  output_dir,
		   	  write_xml=True,
		   	  write_binary=True,
		   	  write_csv=False,
		   	  write_binning=False,
			  path_to_peptide3d=Path("C:/Symphony/PLGS/Peptide3D.exe")):
	"""A wrapper around the infamous Peptide3D.
	
	Args:
		input_file (Path or str): a path to the file containing Apex3D's outcomes.
		output_dir (Path or str): Path to where to place the output.
		write_xml (boolean): Write the output in an xml in the output folder.
		write_binary (boolean): Write the binary output in an xml in the output folder.
		write_csv (boolean): Write the ions to csv file.
		write_binning (boolean): Write binning file.
		path_to_peptide3d (Path or str): Path to the "Peptide3D.exe" executable.
	"""
	algo = str(Path(path_to_peptide3d))
	process = subprocess.call([	
	                          	"powershell.exe", algo,
				                "-inputFileName {}".format(input_file),
				                "-outputDirName {}".format(output_dir),
				                "-WriteXML {}".format(int(write_xml)),
				                "-WriteBinary {}".format(int(write_binary)),
				                "-WriteAllIonsToCSV {}".format(int(write_csv)),
				                "-WriteBinningFile {}".format(int(write_binning))
				              ])
	return process


def test_peptide3d():
	"""Test the stupid Peptide3D."""
	peptide3d(Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput/O190302_01_Apex3D.bin"),
	       	  Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput"))
