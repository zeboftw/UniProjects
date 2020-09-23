#pragma once
#include "Domain.h"
#include "CustomException.h"
#include <vector>

class Repository {
protected:
	string file_path;
public:

	/*
	Setter for file_path variable
	*/
	virtual void set_path(string) = 0;

	/*
	Function that adds given element to the repository
	Throws CustomException if the element is already in in repository
	Returns void
	*/
	virtual void add(Profile) = 0;
	
	/*
	Function that removes given element from the repository
	Throws CustomException if the element is not in the repository
	Returns void
	*/
	virtual void remove(Profile) = 0;

	/*
	Function that provides acces to all elements in the repository
	Returns a DynamicVector of Profiles
	*/
	virtual std::vector<Profile> get_all() = 0;

	/*
	Function that returns the size of the repository
	Returns integer
	*/
	virtual int get_size() const = 0;

};

class RepositoryMemory : public Repository {
private:
	vector<Profile> array;
public:
	void set_path(string);

	void add(Profile);
	void remove(Profile);

	std::vector<Profile> get_all();
	int get_size() const;

};

class RepositoryCSV : public Repository {
public:
	RepositoryCSV(string s = "defaultInput.csv");

	void set_path(string);

	void add(Profile);
	void remove(Profile);

	std::vector<Profile> get_all();
	int get_size() const;

};

class RepositoryHTML : public Repository {
public:
	RepositoryHTML(string path =  "defaultInput.html");

	void set_path(string);

	void add(Profile);
	void remove(Profile);

	std::vector<Profile> get_all();
	int get_size() const;

};

bool vector_search(std::vector<Profile>, Profile);