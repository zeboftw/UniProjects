#include "Domain.h"
#include <unordered_map>
#include <stdio.h>
#include <sstream>

Profile::Profile(string t_name, string t_proffesion, int t_age, string t_link) : name{ t_name }, proffesion{ t_proffesion }, age{ t_age }, photograph{ t_link } {}

string Profile::get_name() const {
	return this->name;
}

int Profile::get_age() const {
	return this->age;
}

string Profile::get_proffesion() const {
	return this->proffesion;
}

string Profile::get_photo() const {
	return this->photograph;
}

bool Profile::operator==(const Profile& target) const {
	return this->name == target.name;
}

bool Profile::operator!=(const Profile& target) const {
	return this->name != target.name;
}

string Profile::to_string() const{
	std::stringstream result;
	
	result << "Name: " << this->name << "; Proffesion: " << this->proffesion << "; Age: " << this->age << "; Photograph: " << this->photograph << ";\n";

	return result.str();
}

Profile& Profile::operator=(const Profile& target) {
	this->name = target.name;
	this->proffesion = target.proffesion;
	this->age = target.age;
	this->photograph = target.photograph;
	return *this;
}

string Profile::to_text() const {
	std::stringstream txt;
	txt << this->name << ',' << this->proffesion << ',' << this->age << ',' << this->photograph << '\n';
	return txt.str();
}

vector<string> tokenize(string str, char delimiter)
{
	vector <string> result;
	stringstream ss(str);
	string token;
	while (getline(ss, token, delimiter))
		result.push_back(token);

	return result;
}

std::istream& operator>>(std::istream& is, Profile& target){
	string line;
	getline(is, line);

	vector<string> tokens = tokenize(line, ',');
	if (tokens.size() != 4) // make sure all the starship data was valid
		return is;
	Profile s{ tokens[0], tokens[1], stoi(tokens[2]), tokens[3] };
	target = s;

	return is;
}

std::string Profile::to_html() const {
	string s = "<tr>";
	s += "<td>" + this->name + "</td>\n";
	s += "<td>" + this->proffesion + "</td>\n";
	s += "<td>" + std::to_string(this->age) + "</td>\n";
	s += "<td>" + this->photograph + "</td>\n";
	s += "</tr>";
	return s;
}

std::ostream& operator<<(std::ostream& os, Profile& target)
{
	os << target.to_text();
	return os;
}