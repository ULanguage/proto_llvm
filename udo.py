#############################################################
# S: Utils ##################################################

import os
from pathlib import Path

def filesWithExtension(d, extension):
  return [ str(fpath) for fpath in list(Path(d).rglob(f'*{extension}')) ]

def genTaskCCompile(fpath, opath):
  return {
    'name': fpath,
    'deps': [fpath],
    'outs': [opath],

    'actions': [
      f'mkdir -p {BUILDD}',
      f'clang++ -c -o {opath} {CFLAGS} {fpath}',
    ],
  }

def genTaskRun(name, script, *, skipRun = False):
 return {
    'name': name,
    'deps': [TaskKaleido, script],
    'skipRun': skipRun,

    'capture': 1,
    'actions': [
      f'{BIN} jit < {script}',
    ],
  }

def genTaskKCompile(fpath, opath):
  return {
    'name': fpath,
    'deps': [fpath],
    'outs': [opath],

    'actions': [
      f'{BIN} comp {opath} < {fpath}',
    ],
  }

#############################################################
# S: Config #################################################

UDOConfig = {
  'version': (1, 3, 0)
}

SRCD = 'src'
INCLUDED = os.path.join(SRCD, 'include')
EXPD = 'example'
BUILDD = 'build'

BIN = os.path.join(BUILDD, 'kaleido')

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

#############################################################
# S: Tasks ##################################################

def TaskKaleido():
  objects = [os.path.join(BUILDD, os.path.basename(fpath) + '.o') for fpath in CSRC]

  return {
    'name': 'kaleido',
    'deps': CSRC + CHEADS + CHPPS,
    'outs': [BUILDD, BIN],

    'subtasks': [genTaskCCompile(*args) for args in zip(CSRC, objects)],
    'actions': [
      f'clang++ -o {BIN} {CFLAGS} {" ".join(objects)}',
    ],
  }

def taskTestComp():
  return {
    'name': 'testComp',
    'deps': ['./example/main.cc'],
    'outs': ['./build/main'],
    
    'capture': 1,
    # 'subtasks': [genTaskKCompile('./example/test_comp.k', './build/output.o')],
    'actions': [
      f'{BIN} comp ./build/output.o < ./example/test_comp.k', # TODO: Parametize
      f'clang++ -o ./build/main ./build/output.o ./example/main.cc',
      f'./build/main',
    ],
  }

def TaskTest():
  return {
    'name': 'test',
    'deps': [TaskKaleido],

    'subtasks': [genTaskRun('test_jit', TSCRIPT), taskTestComp]
  }

def TaskExample():
  return genTaskRun('example', ESCRIPT, skipRun = True)

def TaskMandel():
  return genTaskRun('mandel', MSCRIPT, skipRun = True)
