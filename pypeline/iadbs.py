import subprocess
from pathlib import Path


def iadbs(input_file,
	   	  output_dir,
	   	  fasta_file,
	   	  parameters_file,
	   	  write_xml=True,
	   	  write_binary=True,
	   	  write_csv=False,
	   	  write_binning=False,
	   	  path_to_iadbs=Path("C:/Symphony/PLGS/iaDBs.exe"),
	   	  *args):
	"""A wrapper around the infamous iaDBs.
	
	Args:
		input_file (Path or str): a path to the pep3D spectrum file, xml or bin.
		output_dir (Path or str): Path to where to place the output.
		write_xml (boolean): Write the output in an xml in the output folder.
		write_binary (boolean): Write the binary output in an xml in the output folder.
		write_csv (boolean): Write the ions to csv file.
		write_binning (boolean): Write binning file.
		path_to_iadbs (Path or str): Path to the "iaDBs.exe" executable.
	"""
	algo = str(Path(path_to_iadbs))
	process = subprocess.call([	
	                          	"powershell.exe", algo,
				                "-pep3DFilename {}".format(input_file),
				                "-proteinFASTAFileName {}".format(fasta_file),
				                "-outputDirName {}".format(output_dir),
								"-paraXMLFileName {}".format(parameters_file),
				                "-WriteXML {}".format(int(write_xml)),
				                "-WriteBinary {}".format(int(write_binary)),
				                "-bDeveloperCSVOutput {}".format(int(write_csv))
				              ])
	return process


def test_iadbs():
	"""Test the stupid iaDBs."""
	iadbs(Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput/O190302_01_Pep3D_Spectrum.bin"),
	      Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput/"),
	      Path("C:/Symphony/Search/human.fasta"),
	      Path("C:/Symphony/Search/251.xml"))
