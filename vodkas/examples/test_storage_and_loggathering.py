from vodkas.misc import store_wrap

def foo(a, b, c=10, **kwds):
    """abc"""
    return a+b+c

def foo2(a, b, c=10, **kwds):
    """abc"""
    return a*b*c

_foo, _foo2, storage = store_wrap(foo, foo2)
_foo(2120, 34, 34)
_foo2(210, 34, 344230)

fold = Path('C:/SYMPHONY_VODKAS')
temp_fold = fold/'temp_logs'
storage.json(temp_fold)

_foo, _foo2, storage = store_wrap(foo, foo2)
_foo(2120, 34, 34)
_foo2(210, 34, 343, e=190)
storage.json(temp_fold)

_foo, _foo2, storage = store_wrap(foo, foo2)
_foo(2120, 34, 34, f='ava')
_foo2(210, 34, 343, e='dd')
storage.json(temp_fold)

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
