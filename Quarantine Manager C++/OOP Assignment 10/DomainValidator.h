#pragma once
#include <string>
#include "Validator.h"

class DomainValidator : Validator {
public:
	bool valid(std::string, std::string, int, std::string);
};