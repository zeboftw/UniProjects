#pragma once
#include "Repository.h"
#include "Action.h"

class Service {
private:
	//Repository repo;
	shared_ptr<Repository> repo;
	vector<Profile> quaranteen_passed, buffer;
	vector<unique_ptr<Action>> unredo_stack;
	int buffer_index = 0;
	int stack_index = 0;

	void update_stack();
public:

	Service(unique_ptr<Repository>);

	void set_path(string);

	void undo();
	void redo();

	/*
	Function that creates a Profile object and adds it to the repository.
	Throws CustomException if the element is already in the repository.
	Returns void
	*/
	void add(string, string, int, string);

	/*
	Function that removes a specified element from the repository.
	Throws CustomException if the element is not found.
	Returns void
	*/
	void remove(string);

	/*
	Function that updates the information of a specified profile.
	Throws CustomExcception if the element is not found.
	Returns void.
	*/
	void update(string, string, int, string);

	/*
	Function that provides acces to the program's stored elements.
	Returns a DynamicVector of Profiles
	*/
	std::vector<Profile> get_all();

	/*
	Function that saves a profile to the quarantine passed folder.
	Throws CustomException if the given name is not found or already passed quaratine.
	Returns void
	*/
	void save(string);

	/*
	Function that gets the next profile in the list
	Returns a reference to a profile
	*/
	Profile& next();

	/*
	Function that creates a list of profiles with given age and proffesion
	Returns a DynamicVector of Profiles
	*/
	vector<Profile>& filter(int, string prof = "*");
	
	/*
	Function that returns a lits of all profiles that passed quarantine
	Returns a DynamicVector of Profiles
	*/
	vector<Profile>& get_passed();
};