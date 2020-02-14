#!/usr/bin/env python3
import argparse
import json
import pandas as pd
from pathlib import Path


debug = False
if debug:
    from pprint import pprint

parser = argparse.ArgumentParser(description='Update the PLGS.csv file with all runs of the bloody.')

parser.add_argument("-PLGS", "--PLGS_csv_path",
    type=Path,
    help="peptide report path",
    default="C:/SYMPHONY_VODKAS/PLGS.csv")

parser.add_argument("-temp", "--temporary_logs_folder",
    type=Path,
    help="peptide report path",
    default="C:/SYMPHONY_VODKAS/temp_logs")

args = parser.parse_args()
if debug:
    pprint(args.__dict__)

def unlist(d):
    assert all(len(v)==1 for v in d.values()), "A function was called more than once."
    return {f"{f} {a}":v for f,A in d.items() for a,v in A[0].items()}

def pop_update(temp_fold):
    temp_fold = Path(temp_fold)
    for f in temp_fold.glob('*.json'):
        with open(f, 'r') as h:
            yield unlist(json.load(h))
        f.unlink()


if __name__ == "__main__":
    try:
        D = pd.read_csv(args.PLGS_csv_path)
    except FileNotFoundError:
        D = pd.DataFrame()
    X = pd.DataFrame(pop_update(args.temporary_logs_folder))
    if X.empty:
        raise FileNotFoundError("There are no logs to append! Run some more PLGS :)")
    else:
        D = D.append(X, ignore_index=True, sort=False)
        D = D[sorted(D.columns)]
        D.to_csv(args.PLGS_csv_path, index=False)
        print('PLGS.csv updated.')