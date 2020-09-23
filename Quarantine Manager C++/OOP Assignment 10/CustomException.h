#pragma once
#include <exception>

class CustomException : public std::exception {
public:
	CustomException(const char*);
};