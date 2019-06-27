import subprocess
from pathlib import Path

import pypeline.default_paths as default


def peptide3d(input_file,
		   	  output_dir,
		   	  write_xml=True,
		   	  write_binary=False,
		   	  write_csv=False,
		   	  write_binning=False,
		   	  min_LEMHPlus=0,
			  path_to_peptide3d=default.peptide3Dpath,
			  **kwds):
	"""A wrapper around the infamous Peptide3D.
	
	Args:
		input_file (Path or str): a path to the file containing Apex3D's outcomes.
		output_dir (Path or str): Path to where to place the output.
		write_xml (boolean): Write the output in an xml in the output folder.
		write_binary (boolean): Write the binary output in an xml in the output folder.
		write_csv (boolean): Write the ions to csv file.
		write_binning (boolean): Write binning file.
		min_LEMHPlus (int): The minimal (M)ass of the (L)ow (E)nergy precursor with a single charge (H+).
		path_to_peptide3d (Path or str): Path to the "Peptide3D.exe" executable.
		**kwds: other parameters for 'subprocess.run'.
	Returns:
        tuple: the completed process and the path to the outcome (preference of xml over bin).
	"""
	algo = str(Path(path_to_peptide3d))
	input_file = Path(input_file)
	output_dir = Path(output_dir)
	process = subprocess.run([	"powershell.exe", algo,
				                "-inputFileName {}".format(input_file),
				                "-outputDirName {}".format(output_dir),
				                "-WriteXML {}".format(int(write_xml)),
				                "-WriteBinary {}".format(int(write_binary)),
				                "-WriteAllIonsToCSV {}".format(int(write_csv)),
				                "-WriteBinningFile {}".format(int(write_binning)),
				                "-minLEMHPlus {}".format(min_LEMHPlus)  ],
				             **kwds)
	if '_Apex3D' in input_file.stem:
		out = input_file.parent/input_file.stem.replace('_Apex3D','_Pep3D_Spectrum')
	else:
		out = input_file.stem + "_Pep3D_Spectrum"
		out = input_file.parent/out
	out_bin = out.with_suffix('.bin')
	out_xml = out.with_suffix('.xml')
	if not out_bin.exists() and not out_xml.exists():
    	raise RuntimeError("The output is missing: Peptide3D failed us!!!")
	if kwds.get('capture_output', False):# otherwise no input was caught.
        log = output_dir/"peptide3d.log"
        log.write_bytes(process.stdout)
    if write_xml and out_xml.exists():
        return out_xml, process
    if out_bin.exists():
        return out_bin, process


def test_peptide3d():
	"""Test the stupid Peptide3D."""
	peptide3d(Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput/O190302_01_Apex3D.bin"),
	       	  Path("C:/ms_soft/MasterOfPipelines/test/apex3doutput"))
