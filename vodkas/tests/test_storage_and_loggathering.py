from vodkas.misc import monitor, now
from pathlib import Path
from pprint import pprint

def foo1(a, b, c=10, **kwds):
    """abc"""
    return a+b+c

def foo2(a, b, c=10, **kwds):
    """abc"""
    return a*b*c

_foo1, _foo2, fun_monitor = monitor(foo, foo2)
_foo1(2120, 34, 34)
_foo2(210, 34, 344230)
_foo2(210, 34, 344230, f=12)

pprint(fun_monitor)

fold = Path('C:/SYMPHONY_VODKAS')
temp_fold = fold/'temp_logs'
fun_monitor.json(temp_fold, prefix='human_')


# now the bloody parser
import json
import pandas as pd
from pathlib import Path


def unlist(d):
    assert all(len(v)==1 for v in d.values()), "A function was called more than once."
    return {f"{f} {a}":v for f,A in d.items() for a,v in A[0].items()}

def pop_update(temp_fold):
    temp_fold = Path(temp_fold)
    for f in temp_fold.glob('*.json'):
        with open(f, 'r') as h:
            yield unlist(json.load(h))
        f.unlink()

D = X

def update_PLGS_csv(PLGS_csv_path='C:/SYMPHONY_VODKAS/',
                    temp_fold='C:/SYMPHONY_VODKAS/temp_logs'):
    """Update the csv """

    D = pd.DataFrame.read_csv()
    X = pd.DataFrame(pop_update(temp_fold))
# X.index.name = 'idx'
# X.to_csv(path_or_buf=fold/"PLGS.cvs")
D = D.append(X, ignore_index=True)



if X.empty:
    print('h')

