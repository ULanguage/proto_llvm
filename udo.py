#############################################################
# S: Utils ##################################################

import os
from pathlib import Path

UDOConfig = {
  'version': (1, 3, 0)
}

SRCD = 'src'
INCLUDED = os.path.join(SRCD, 'include')
EXPD = 'example'
BUILDD = 'build'

BIN = os.path.join(BUILDD, 'kaleido')

def filesWithExtension(d, extension):
  return [ str(fpath) for fpath in list(Path(d).rglob(f'*{extension}')) ]

CSRC = filesWithExtension(SRCD, '.cpp')
CHPPS = filesWithExtension(SRCD, '.hpp')
CHEADS = filesWithExtension(SRCD, '.h')
CFLAGS = ' '.join([
  '-g -O3',
  '`llvm-config --cxxflags --ldflags --system-libs --libs core orcjit native`',
  f'-I{INCLUDED}',
  '-rdynamic',
])

TSCRIPT = os.path.join(EXPD, 'test_jit.k')
ESCRIPT = os.path.join(EXPD, 'script.k')
MSCRIPT = os.path.join(EXPD, 'mandel.k')

def genTaskRun(name, script, *, skipRun = False):
 return {
    'name': name,
    'deps': [TaskKaleido, script],
    'skipRun': skipRun,

    'capture': 1,
    'actions': [
      f'{BIN} < {script}',
    ],
  }

def genTaskCompile(fpath, opath):
  return {
    'name': fpath,
    'deps': [fpath],
    'outs': [opath],

    'actions': [
      f'mkdir -p {BUILDD}',
      f'clang++ -c -o {opath} {CFLAGS} {fpath}',
    ],
  }

def TaskKaleido():
  objects = [os.path.join(BUILDD, os.path.basename(fpath) + '.o') for fpath in CSRC]

  return {
    'name': 'kaleido',
    'deps': CSRC + CHEADS + CHPPS,
    'outs': [BUILDD, BIN],

    'subtasks': [genTaskCompile(*args) for args in zip(CSRC, objects)],
    'actions': [
      f'clang++ -o {BIN} {CFLAGS} {" ".join(objects)}',
      # TODO: Link
    ],
  }

def TaskTest():
  return genTaskRun('test', TSCRIPT)

def TaskExample():
  return genTaskRun('example', ESCRIPT, skipRun = True)

def TaskMandel():
  return genTaskRun('mandel', MSCRIPT, skipRun = True)
