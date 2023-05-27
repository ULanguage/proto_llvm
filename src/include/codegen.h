#pragma once

#include "ast.h"
#include "utils.h"

extern std::unique_ptr<LLVMContext> TheContext;
extern std::unique_ptr<Module> TheModule;
extern std::unique_ptr<IRBuilder<>> Builder;
extern std::map<std::string, AllocaInst *> NamedValues;
extern std::unique_ptr<legacy::FunctionPassManager> TheFPM;
extern std::unique_ptr<KaleidoscopeJIT> TheJIT;
extern std::map<std::string, std::unique_ptr<PrototypeAST>> FunctionProtos;
extern ExitOnError ExitOnErr;

Value *LogErrorV(const char *Str);

Function *getFunction(std::string Name); 

/// CreateEntryBlockAlloca - Create an alloca instruction in the entry block of
/// the function.  This is used for mutable variables etc.
AllocaInst *CreateEntryBlockAlloca(Function *TheFunction, StringRef VarName);
