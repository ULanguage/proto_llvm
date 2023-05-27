#############################################################
# S: Utils ##################################################

import os
from pathlib import Path

UDOConfig = {
  'version': (1, 3, 0)
}

SRCD = 'src'
EXPD = 'example'
BUILDD = 'build'

BIN = os.path.join(BUILDD, 'kaleido')

def filesWithExtension(d, extension):
  return [ str(fpath) for fpath in list(Path(d).rglob(f'*{extension}')) ]

CSRC = filesWithExtension(SRCD, '.cpp')
CHEADS = filesWithExtension(SRCD, '.h')

ESCRIPT = os.path.join(EXPD, 'script.k')

def TaskKaleido():
  return {
    'name': 'kaleido',
    'deps': CSRC + CHEADS,
    'outs': [BUILDD, BIN],

    'actions': [
      f'mkdir -p {BUILDD}',
      f'clang++ -g -O3 {" ".join(CSRC)} `llvm-config --cxxflags --ldflags --system-libs --libs all` -o {BIN}',
    ],
  }

def TaskExample():
  return {
    'name': 'example',
    'deps': [TaskKaleido, ESCRIPT],

    'capture': 1,
    'actions': [
      f'{BIN} < {ESCRIPT}',
    ],
  }
