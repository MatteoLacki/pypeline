from pathlib import Path
import re
import json
import csv
from os import walk

sample_set = re.compile("(\d{4}-\d{3}|[^[Hh]*[Hh][Ee][Ll][Aa].*)$")
raw_file = re.compile("[TSIO]+\d{6}_(BM){0,1}\d{2,3}$")


def read_line(path, n):
    """Read a line in a file.

    Args:
        f (str or pathlib.Path): Path to the csv with data.
        n (int): number of line to output.
    """
    with open(path, "r") as f:
        for i in range(n+1):
            x = f.readline()
    return x


def parse_stats(path):
    """Parse the _stat.csv file in the output of the pipeline.

    Args:
        f (str or pathlib.Path): Path to the folder with csv.
    """
    x = ('stat:sample','stat:mode','stat:queries','stat:peptides','stat:proteins')
    y = read_line(path, 1).replace('\n','').split(",")[1:]
    yield from zip(x,y)


def parse_xml_params(path, prefix=""):
    """A quicker XML parser.

    Args:
        path (str or pathlib.Path): path to the xml file.
        prefix (str): prefix to the name of the parameter.
    Yields:
        tuples (parameter, value).
    """
    with open(path, 'r') as f:
        for l in f:
            if "PARAM NAME" in l:
                w = l.split('"')
                k = w[1]
                v = w[3]
                try:
                    v = v.replace(',','.')
                    v = float(v)
                except ValueError:
                    pass
                yield "{}{}".format(prefix, k), v
            if "</PARAMS>" in l:
                break


def parse_folder(f):
    """Parse the contents of a folder.

    Only if the folder contains one of files matching the patter,
    will it ever output anything. Matches include:
        *_Apex3D.xml
        *_Pep3D_Spectrum.xml
        *_workflow.xml

    Args:
        f (str or pathlib.Path): Path to the folder with data.
    """
    f = Path(f)
    for prefix, suffix in (("apex:","*_Apex3D.xml"),
                           ("spec:","*_Pep3D_Spectrum.xml"),
                           ("work:","*_workflow.xml")):
        for file in f.glob(suffix):
            for param in parse_xml_params(file, prefix):
                yield param


def iter_input_folders(fps, recursive=False):
    """Iterate over the input folders all subfolders (if recursive).

    Args:
        fps (list of strings or pathlib paths): paths to where to recursively look into.
    Yields:
        A sequence of paths to the folders with data.
    """
    for fp in fps: # iterate over potentially multiple folders
        fp = Path(fp)
        fp.resolve()
        if recursive: # iter into the folders
            for x in walk(fp):
                yield Path(x[0])
        else:
            yield fp


def dump_params_to_jsons(file_paths, verbose=True):
    for p in file_paths:
        p = Path(p)
        param_dict = dict(parse_folder(p))
        if param_dict:
            try:
                with (p/"params.json").open('w') as h:
                    json.dump(param_dict, h, indent=3)
                if verbose:
                    print("dumped {}".format(p))
            except Exception as e:
                print(e)
                print(p)
    if verbose:
        print('Thank you for patience.')


def dump_to_csv(path, rows, header=None):
    """Dump rows to a csv.

    Args:
        path (str or pathlib.Path): Path to where to store the csv.
        rows (iterable): rows to dump.
        header (list/tuple of str): Strings to put as header.
    """
    path = Path(path)
    assert path.suffix == '.csv', "Writing only to csv."
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        if header is not None:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)

class MissingInfoForIsoquant(Exception):
    pass


def parse_raw_folder(path):
    """Parse a particular Waters raw folder as needed for IsoQuant project."""
    p = Path(path)
    try:
        with open(p/"params.json", 'r') as f:
            sample_desc = json.load(f)['work:SampleDescription']
    except KeyError:
        print("'work:SampleDescription' missing in params.json")
        raise MissingInfoForIsoquant
    except FileNotFoundError:
        print("'params.json' missing. Run 'xmls2jsons' on this folder, or think.")
        raise MissingInfoForIsoquant
    try:
        pep3dspec = next(p.glob("*_Pep3D_Spectrum.xml"))
    except StopIteration as e:
        print("Attention: File {} was not analysed as '*_Pep3D_Spectrum.xml' was (most likely) missing.".format(p.name))
        raise MissingInfoForIsoquant
    try:
        workflow = next(p.glob("*_workflow.xml"))
    except RuntimeError as e:
        print("Attention: File {} was not analysed as '*_workflow.xml' was (most likely) missing.".format(p.name))
        raise MissingInfoForIsoquant
    return p.name, pep3dspec, workflow, sample_desc


