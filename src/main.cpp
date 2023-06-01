#include "lexer.h"
#include "parser.h"
#include "codegen.h"
#include "interpreter.h"
#include "utils.h"

CompMode_t CompMode;

void sharedSetup() {
  InitializeNativeTarget();
  InitializeNativeTargetAsmPrinter();
  InitializeNativeTargetAsmParser();

  // Install standard binary operators.
  // 1 is lowest precedence.
  BinopPrecedence['='] = 2;
  BinopPrecedence['<'] = 10;
  BinopPrecedence['+'] = 20;
  BinopPrecedence['-'] = 20;
  BinopPrecedence['*'] = 40; // highest.

  // Prime the first token.
  fprintf(stderr, "ready> ");
  getNextToken();
}

void startMainLoop() {
  InitializeModuleAndPassManager();

  // Run the main "interpreter loop" now.
  MainLoop();
}

int mainJIT(int argc, char* argv[]) {
  CompMode = JIT;

  sharedSetup();
  TheJIT = ExitOnErr(KaleidoscopeJIT::Create());
  startMainLoop();

  return 0;
}

int mainComp(int argc, char* argv[]) {
  CompMode = COMP;

  if (argc < 3) {
    fprintf(stderr, "Usage: kaleido comp {OPATH}");
    return 0;
  }

  auto opath = std::string(argv[2]);

  sharedSetup();
  startMainLoop();

  InitializeAllTargetInfos();
  InitializeAllTargets();
  InitializeAllTargetMCs();
  InitializeAllAsmParsers();
  InitializeAllAsmPrinters();

  auto TargetTriple = sys::getDefaultTargetTriple();
  TheModule->setTargetTriple(TargetTriple);

  std::string Error;
  auto Target = TargetRegistry::lookupTarget(TargetTriple, Error);

  // Print an error and exit if we couldn't find the requested target.
  // This generally occurs if we've forgotten to initialise the
  // TargetRegistry or we have a bogus target triple.
  if (!Target) {
    errs() << Error;
    return 1;
  }

  auto CPU = "generic";
  auto Features = "";

  TargetOptions opt;
  auto RM = Optional<Reloc::Model>();
  auto TheTargetMachine =
      Target->createTargetMachine(TargetTriple, CPU, Features, opt, RM);

  TheModule->setDataLayout(TheTargetMachine->createDataLayout());

  std::error_code EC;
  raw_fd_ostream dest(opath.c_str(), EC, sys::fs::OF_None);

  if (EC) {
    errs() << "Could not open file: " << EC.message();
    return 1;
  }

  legacy::PassManager pass;
  auto FileType = CGFT_ObjectFile;

  if (TheTargetMachine->addPassesToEmitFile(pass, dest, nullptr, FileType)) {
    errs() << "TheTargetMachine can't emit a file of this type";
    return 1;
  }

  pass.run(*TheModule);
  dest.flush();

  outs() << "Wrote " << opath << "\n";

  return 0;
}

int main(int argc, char* argv[]) {
  if (argc < 2) {
    fprintf(stderr, "Usage: kaleido [jit|comp]");
    return 0;
  }

  auto mode = std::string(argv[1]);
  if (mode == "jit")
    return mainJIT(argc, argv);
  else if (mode == "comp")
    return mainComp(argc, argv);
  else {
    fprintf(stderr, "Usage: kaleido [jit|comp]");
    return 1;
  }
}
