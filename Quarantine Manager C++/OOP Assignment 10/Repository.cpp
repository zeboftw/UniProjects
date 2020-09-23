#include "Repository.h"
#include <iostream>
#include <Windows.h>
#include <fstream>
#include <sstream>
#include <qdebug.h>

void RepositoryMemory::set_path(string s) {
	throw CustomException("In memory repository does not have a path!\n");
}

void RepositoryMemory::add(Profile target) {
	if (vector_search(this->array, target)) throw CustomException("Person already has profile!\n");
	this->array.push_back(target);
}

void RepositoryMemory::remove(Profile target) {
	if (!vector_search(this->array, target)) throw CustomException("Person does not have a profile!\n");

	for (auto it = this->array.begin(); it != this->array.end(); it++) {
		if (*it == target) {
			this->array.erase(it);
			break;
		}
	}

}

vector<Profile> RepositoryMemory::get_all() {
	return this->array;
}

int RepositoryMemory::get_size() const {
	return this->array.size();
}

void RepositoryCSV::set_path(string path) {
	this->file_path = path;
	qDebug() << QString::fromStdString("changed path!");
}

RepositoryCSV::RepositoryCSV(string path) {
	this->file_path = path;
}

void RepositoryCSV::add(Profile target) {
	std::vector<Profile> data;
	Profile current{};

	ifstream input(this->file_path);

	while (input >> current) {
		data.push_back(current);
	}
	input.close();

	if (vector_search(data, target)) throw CustomException("Person already has profile!\n");

	ofstream output(this->file_path, ios::app);
	output << target;
	output.close();
}

void RepositoryCSV::remove(Profile target) {
	std::vector<Profile> data;
	Profile current;

	ifstream input(this->file_path);
	while (input >> current) {
		data.push_back(current);
	}
	input.close();

	auto it = data.begin();
	while (it != data.end()) {
		if (*it == target) break;
		it++;
	}
	if (it == data.end()) throw CustomException("Person does not have a profile!\n");
	else (data.erase(it));

	ofstream output(this->file_path);
	for (auto it : data) {
		output << it;
	}
	output.close();

}

std::vector<Profile> RepositoryCSV::get_all() {
	std::vector<Profile> data;
	Profile current;
	ifstream input(this->file_path);

	while (input >> current) {
		data.push_back(current);
	}
	input.close();

	return data;
}

int RepositoryCSV::get_size() const {
	std::vector<Profile> data;
	Profile current;
	ifstream input(this->file_path);
	while (input >> current) {
		data.push_back(current);
	}
	input.close();
	return data.size();
}

void RepositoryHTML::set_path(string path) {
	this->file_path = path;
}

RepositoryHTML::RepositoryHTML(string path) {
	this->file_path = path;
}

void RepositoryHTML::add(Profile target) {
	std::vector<Profile> data;
	Profile current{};

	ifstream input(this->file_path + ".csv");

	while (input >> current) {
		data.push_back(current);
	}
	input.close();

	if (vector_search(data, target)) throw CustomException("Person already has profile!\n");

	data.push_back(target);
	ofstream output(this->file_path);

	output << "<!DOCTYPE html>\n";
	output << "<html>\n";
	output << "	<head>\n";
	output << "		<title>Profiles</title>\n";
	output << "	</head>\n";
	output << "	<body>\n";
	output << "		<table border=\"1\">\n";
	output << "		<tr>\n";
	output << "			<td>Name</td>\n";
	output << "			<td>Proffesion</td>\n";
	output << "			<td>Age</td>\n";
	output << "			<td>Photo</td>\n";
	output << "		</tr>\n";

	for (auto it : data) {
		output << it.to_html();
	}

	output << "		</table>\n";
	output << "	</body>\n";
	output << "</html>\n";

	output.close();

	ofstream output_csv(this->file_path + ".csv");
	for (auto it : data) {
		output_csv << it;
	}
	output_csv.close();
}

void RepositoryHTML::remove(Profile target) {
	std::vector<Profile> data;
	Profile current;

	ifstream input(this->file_path + ".csv");
	while (input >> current) {
		data.push_back(current);
	}
	input.close();


	auto it = data.begin();
	while (it != data.end()) {
		if (*it == target) break;
		it++;
	}
	if (it == data.end()) throw CustomException("Person does not have a profile!\n");
	else (data.erase(it));

	ofstream output(this->file_path);
	output << "<!DOCTYPE html>\n";
	output << "<html>\n";
	output << "	<head>\n";
	output << "		<title>Profiles</title>\n";
	output << "	</head>\n";
	output << "	<body>\n";
	output << "		<table border=\"1\">\n";
	output << "		<tr>\n";
	output << "			<td>Name</td>\n";
	output << "			<td>Proffesion</td>\n";
	output << "			<td>Age</td>\n";
	output << "			<td>Photo</td>\n";
	output << "		</tr>\n";

	for (auto it : data) {
		output << it.to_html();
	}

	output << "		</table>\n";
	output << "	</body>\n";
	output << "</html>\n";

	ofstream output_csv(this->file_path + ".csv");
	for (auto it : data) {
		output_csv << it;
	}
	output_csv.close();
	output.close();

}

std::vector<Profile> RepositoryHTML::get_all() {
	std::vector<Profile> data;
	Profile current;
	ifstream input(this->file_path + ".csv");

	while (input >> current) {
		data.push_back(current);
	}
	input.close();

	return data;
}

int RepositoryHTML::get_size() const {
	std::vector<Profile> data;
	Profile current;
	ifstream input(this->file_path + ".csv");
	while (input >> current) {
		data.push_back(current);
	}
	input.close();
	return data.size();
}

bool vector_search(std::vector<Profile> array, Profile target) {
	for (auto it : array) {
		if (it == target) return true;
	}
	return false;
}