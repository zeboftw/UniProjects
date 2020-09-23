#include "DomainValidator.h"

bool DomainValidator::valid(std::string name, std::string prof, int age, std::string photo) {
	if (name.size() < 4) return false;
	if (prof.size() < 4) return false;
	if (photo.size() < 4) return false;
	if (age < 1 || age > 110) return false;
	return true;
}