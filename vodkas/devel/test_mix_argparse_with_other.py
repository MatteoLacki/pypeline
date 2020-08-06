import sys
import argparse

promptOK = False
try:
    promptOK = sys.argv[1] == 'prompt_me_and_i_will_tell_you_the_future'
    if promptOK:
        print('prompt')
        print(input('hit enter'))
except IndexError:
    pass

if not promptOK:
    ap = argparse.ArgumentParser(description='hahaha',
                                     epilog="hihi",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('dupa')
    ap.add_argument('chuj')
    ap.add_argument('--cipa')
    args = ap.parse_args()
    print(args.__dict__)




