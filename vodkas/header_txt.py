import json
from pathlib import Path

from .logging import get_logger


logger = get_logger(__name__)


# TODO this should be mostly used by a script for Folder Synchronization.
def parse_header_txt(path, 
                     valid_keys = ('Acquired Name', 'Acquired Date', 'Acquired Time',
                  'Sample Description', 'Bottle Number',
                  'Inlet Method', 'MS Method', 'Tune Method')):
    """Parse the _HEADER.TXT file."""
    logger.info('Parsing _HEADER.TXT')

    path = Path(path)
    assert path.name == '_HEADER.TXT', "Wrong path."
    params = {}
    with open(path, 'r') as f:
        for l in f:
            l = l.strip()
            k = l.split(':')[0]
            v = l[len(k)+2:]
            k = k[3:]
            if k in valid_keys:
                params[k] = v

    logger.info(json.dumps(params))

    return params


