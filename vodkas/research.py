from tqdm import tqdm

from waters.parsers import iaDBsXMLparser
from fs_ops.csv import rows2csv

from .fastas import get_fastas
from .json import dump2json
from .remote.sender import Sender
from .xml_parser import create_params_file

MOCK = True


def research(xmls, fastas_path, iadbs_kwds, log, server_ip):
    try: # translate fastas to NCBIgeneralFastas and store it on the server.
        iadbs_kwds['fasta_file'] = get_fastas(fastas_path)
    except FileNotFoundError:
        log.error(f"Fastas unreachable: {fastas_path}")

    server = Sender('RESEARCH', server_ip)

    for xml in tqdm(xmls):
        log.info(f"researching: {str(xml)}")
        try:
            iadbs_kwds['input_file'] = xml
            iadbs_kwds['output_dir'] = xml.parent
            server.send_pair('iadbs_args', dump2json(iadbs_kwds))
            iadbs_out, _, runtime = iadbs(**iadbs_kwds)

            apex_out = iadbs_out.parent/iadbs_out.name.replace('_IA_workflow.xml', '_Apex3D.xml')
            create_params_file(apex_out, xml, iadbs_out) # for projectizer2.0

            search_stats = iaDBsXMLparser(iadbs_out).info()
            server.send_pair("stats", dump2json(search_stats))
            rows2csv(iadbs_out.parent/'stats.csv', [list(search_stats), list(search_stats.values())])
        except Exception as e:
            log.warning(repr(e))
    log.info("Search redone.")

# make it work without this stupid wrapping.
