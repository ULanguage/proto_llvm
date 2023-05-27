#pragma once

#include "utils.h"

void InitializeModuleAndPassManager();

void HandleDefinition();

void HandleExtern();

void HandleTopLevelExpression();

/// top ::= definition | external | expression | ';'
void MainLoop();
