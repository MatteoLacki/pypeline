from pathlib import Path
from platform import system

from .fs import check_algo
from .subproc import run_win_proc

from .xml_parser import print_parameters_file


def iadbs(input_file,
          output_dir,
          fasta_file,
          parameters_file="X:/SYMPHONY_VODKAS/search/215.xml" if system()=='Windows' else "~/SYMPHONY_VODKAS/search/215.xml",
          write_xml=True,
          write_binary=False,
          write_csv=False,
          exe_path="C:/SYMPHONY_VODKAS/plgs/iaDBs.exe" if system()=='Windows' else 'none',
          timeout=180):
    """Run iaDBs.
    
    Args:
        input_file (str): a path to the pep3D spectrum file, with an extesion like .xml or .bin. Warning, .bin might not produce an output.
        output_dir (str): Path to where to place the output.
        fasta_file (str): Path to the fasta file used for search.
        parameters_file (str): Path to the search xml.
        write_xml (boolean): Write the output in an xml in the output folder.
        write_binary (boolean): Write the binary output in an xml in the output folder.
        write_csv (boolean): Write the ions to csv file.
        exe_path (str): Path to the "iaDBs.exe" executable.
        timeout (float): Timeout in minutes. Passing 0 will mock the process. Passing negative value will not run the process.

    Returns:
        pathlib.Path: path to the outcome xml file.
    """
    if timeout >= 0:
        input_file = Path(input_file)
        output_dir = Path(output_dir)
        fasta_file = Path(fasta_file)
        parameters_file = Path(parameters_file)
        iadbs_stdout = output_dir/'iadbs.log'

        algo = check_algo(exe_path)
        cmd = [ "powershell.exe", algo,
                f"-paraXMLFileName '{parameters_file}'",
                f"-pep3DFileName '{input_file}'",
                f"-proteinFASTAFileName '{fasta_file}'",
                f"-outputDirName '{output_dir}'",
                f"-WriteXML {int(write_xml)}",
                f"-WriteBinary {int(write_binary)}",
                f"-bDeveloperCSVOutput {int(write_csv)}" ]
        run_win_proc(cmd, timeout, iadbs_stdout)

        if '_Pep3D_Spectrum' in input_file.stem:
            out = output_dir/input_file.stem.replace('_Pep3D_Spectrum','_IA_workflow')
        else:
            out = output_dir/(input_file.stem+"_IA_workflow")
        out_bin = out.with_suffix('.bin')
        out_xml = out.with_suffix('.xml')

        if not out_bin.exists() and not out_xml.exists():
            raise RuntimeError("iaDBs' output missing.")

        return out_xml
    else:
        return None



def parameters_gui(parameters_file):
    print(f'Default search parameters {parameters_file}:')
    print_parameters_file(parameters_file)
    out = input(f'OK? ENTER. Not OK? Provide path here and hit ENTER: ') or parameters_file
    print()
    return out


#TODO: this could be done rather with the XML module
def write_params_xml_file(path, 
                          fasta_db='UNIPROT', 
                          fasta_format='DEF',
                          min_by_per_peptide=2,
                          min_peptides_per_protein=1,
                          min_by_per_protein=5,
                          max_prot_mass=2500000,
                          FDR_rate=1,
                          workflow_template_title='new workflow',
                          workflow_template_id='000'):
    """Write the file with xml parameters needed for iaDBs analysis.

    Args:
        path (Path or str): path to where to write the xml file.
        fasta_db (str): Name of used protein database.
        fasta_format (str): Format of fastas (check Symphony Pipeline manual).
        min_by_per_peptide (int): Minimal number of B and Y ions per peptide.
        min_peptides_per_protein (int): Minimal number of peptides per protein.
        min_by_per_protein (int): Minimal number of B and Y ions per protein.
        max_prot_mass (float): Maximal acceptable mass of protein.
        FDR_rate (float): FDR used by iaDBs.
    """
    params_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <WORKFLOW_TEMPLATE TITLE="{}" UUID="f499a2d3-22f0-4ab6-b0d9-0999d01e543f" WORKFLOW_TEMPLATE_ID="{}">
        <PROTEINLYNX_QUERY TYPE="Databank-search">
            <DATABANK_SEARCH_QUERY_PARAMETERS>
                <SEARCH_ENGINE_TYPE VALUE="PLGS"/>
                <SEARCH_DATABASE NAME="{}"/>
                <SEARCH_TYPE NAME="Electrospray-Shotgun"/>
                <IA_PARAMS>
                    <FASTA_FORMAT VALUE="{}"/>
                    <PRECURSOR_MHP_WINDOW_PPM VALUE="-1"/>
                    <PRODUCT_MHP_WINDOW_PPM VALUE="-1"/>
                    <NUM_BY_MATCH_FOR_PEPTIDE_MINIMUM VALUE="{}"/>
                    <NUM_PEPTIDE_FOR_PROTEIN_MINIMUM VALUE="{}"/>
                    <NUM_BY_MATCH_FOR_PROTEIN_MINIMUM VALUE="{}"/>
                    <PROTEIN_MASS_MAXIMUM_AMU VALUE="{}"/>
                    <FALSE_POSITIVE_RATE VALUE="{}"/>
                    <AQ_PROTEIN_ACCESSION VALUE=""/>
                    <AQ_PROTEIN_MOLES VALUE="-1"/>
                    <MANUAL_RESPONSE_FACTOR VALUE="1000"/>
                    <DIGESTS>
                        <ANALYSIS_DIGESTOR MISSED_CLEAVAGES="2">
                            <AMINO_ACID_SEQUENCE_DIGESTOR NAME="Trypsin" UUID="50466de0-ff04-4be2-a02f-6ccc7b5fd1f5">
                                <CLEAVES_AT AMINO_ACID="K" POSITION="C-TERM">
                                    <EXCLUDES AMINO_ACID="P" POSITION="N-TERM"/>
                                </CLEAVES_AT>
                                <CLEAVES_AT AMINO_ACID="R" POSITION="C-TERM">
                                    <EXCLUDES AMINO_ACID="P" POSITION="N-TERM"/>
                                </CLEAVES_AT>
                            </AMINO_ACID_SEQUENCE_DIGESTOR>
                        </ANALYSIS_DIGESTOR>
                    </DIGESTS>
                    <MODIFICATIONS>
                        <ANALYSIS_MODIFIER STATUS="FIXED">
                            <MODIFIER MCAT_REAGENT="No" NAME="Carbamidomethyl+C">
                                <MODIFIES APPLIES_TO="C" DELTA_MASS="57.0215" TYPE="SIDECHAIN"/>
                            </MODIFIER>
                        </ANALYSIS_MODIFIER>
                        <ANALYSIS_MODIFIER ENRICHED="FALSE" STATUS="VARIABLE">
                            <MODIFIER MCAT_REAGENT="No" NAME="Oxidation+M">
                                <MODIFIES APPLIES_TO="M" DELTA_MASS="15.9949" TYPE="SIDECHAIN"/>
                            </MODIFIER>
                        </ANALYSIS_MODIFIER>
                    </MODIFICATIONS>
                </IA_PARAMS>
            </DATABANK_SEARCH_QUERY_PARAMETERS>
        </PROTEINLYNX_QUERY>
    </WORKFLOW_TEMPLATE>""".format(workflow_template_title, workflow_template_id,
                                   fasta_db, fasta_format,
                                   min_by_per_peptide, min_peptides_per_protein,
                                   min_by_per_protein, max_prot_mass, FDR_rate)
    with open(Path(path), 'w') as f:
        f.write(params_xml)