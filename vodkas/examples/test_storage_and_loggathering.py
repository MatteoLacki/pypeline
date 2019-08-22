from vodkas.misc import store_wrap

def foo(a, b, c=10, **kwds):
    """abc"""
    return a+b+c

def foo2(a, b, c=10, **kwds):
    """abc"""
    return a*b*c

_foo, _foo2, storage = store_wrap(foo, foo2)
_foo(210, 34, 34)
storage
_foo2(210, 34, 34)
storage

fold = Path('C:/SYMPHONY_VODKAS')
temp_fold = fold/'temp_logs'
storage.json(temp_fold)

# now the bloody parser
import json
import pandas as pd
from pathlib import Path


def unlist(d):
    assert all(len(v)==1 for v in d.values()), "A function was called more than once."
    return {f"{f} {a}":v for f,A in d.items() for a,v in A[0].items()}

def pop_update(temp_fold='C:/SYMPHONY_VODKAS/temp_logs'):
    temp_fold = Path(temp_fold)
    for f in temp_fold.glob('*.json'):
        with open(f, 'r') as h:
            yield unlist(json.load(h))
        f.unlink()

X = pd.DataFrame(pop_update())
# X.index.name = 'idx'
# X.to_csv(path_or_buf=fold/"PLGS.cvs")