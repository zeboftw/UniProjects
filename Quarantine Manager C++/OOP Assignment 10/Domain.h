#pragma once
#include <string>
#include <fstream>

using namespace std;

class Profile {
private:
	string name;
	string proffesion;
	int age;
	string photograph;

public:

	//default constructor
	Profile(string t_name = "NULL", string proffesion = "NULL", int t_age = 0, string t_link = "NULL");

	string get_name() const;
	int get_age() const;
	string get_photo() const;
	string get_proffesion() const;

	bool operator==(const Profile&) const;
	bool operator!=(const Profile&) const;
	Profile& operator=(const Profile&);

	string to_string() const;
	string to_text() const;
	string to_html() const;

	friend istream& operator>>(istream& is, Profile& s);
	friend ostream& operator<<(ostream& os, Profile& s);
};