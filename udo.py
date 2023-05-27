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
EBIN = os.path.join(BUILDD, 'main')

def filesWithExtension(d, extension):
  return [ str(fpath) for fpath in list(Path(d).rglob(f'*{extension}')) ]

CSRC = filesWithExtension(SRCD, '.cpp')
CHEADS = filesWithExtension(SRCD, '.h')

EOBJ = os.path.join(BUILDD, 'output.o')
ESCRIPT = os.path.join(EXPD, 'script.k')
ESRC = filesWithExtension(EXPD, '.cpp')
EHEADS = filesWithExtension(EXPD, '.h')

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

def TaskCompExample():
  return {
    'name': 'compExample',
    'deps': [TaskKaleido, ESCRIPT] + ESRC + EHEADS,
    'outs': [EOBJ, EBIN],

    'actions': [
      f'{BIN} < {ESCRIPT}',
      f'clang++ {" ".join(ESRC)} {EOBJ} -o {EBIN}',
    ],
  }

def TaskExample():
  return {
    'name': 'example',
    'deps': [TaskCompExample],

    'capture': 1,
    'actions': [
      EBIN,
    ],
  }
