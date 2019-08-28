from pathlib import Path
from vodkas.fs import fastas
from vodkas.misc import catch_arguments

get_fasta_path('human')
get_fasta_path('leishmania')
get_fasta_path('wheat')
get_fasta_path('mouse')
get_fasta_path('yeast')
get_fasta_path('hye')
get_fasta_path('ecoli')


def foo(a,b,c=1,d=20, **kwds):
    """Test."""
    return a+b, c+d

foo_with_args = catch_arguments(foo)
val = foo(a=2, b=3, c=24)
args, val = foo_with_args(3, b=2, c=24, d=194)
args, val = foo_with_args(3, 1, 5, 10, e=10)

