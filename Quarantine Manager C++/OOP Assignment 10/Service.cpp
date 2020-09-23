#include "Service.h"
#include <iostream>
#include <algorithm>
#include "DomainValidator.h"

Service::Service(unique_ptr<Repository> r) {
	this->repo = move(r);
}

void Service::set_path(string new_path) {
	this->repo->set_path(new_path);
	this->buffer = this->repo->get_all();
	this->buffer_index = 0;
}

void Service::update_stack() {
	if (this->stack_index == this->unredo_stack.size()) return;
	while (this->stack_index != this->unredo_stack.size()) this->unredo_stack.pop_back();
}

void Service::undo() {
	if (this->stack_index == 0) throw CustomException("No more actions to undo");
	this->unredo_stack[--this->stack_index]->executeUndo();
}

void Service::redo() {
	if (this->stack_index == this->unredo_stack.size()) throw CustomException("No more actions to redo");
	this->unredo_stack[this->stack_index++]->executeRedo();
}

void Service::add(string name, string proffesion, int age, string photo) {
	DomainValidator val = DomainValidator();
	if (!val.valid(name, proffesion, age, photo)) throw CustomException("Invalid input!\n");
	Profile to_add = Profile(name, proffesion, age, photo);
	this->repo->add(to_add);

	this->update_stack();
	std::unique_ptr<Action> p = std::make_unique<ActionAdd>(to_add, this->repo);
	this->unredo_stack.push_back(std::move(p));
	this->stack_index++;
}

void Service::remove(string name) {
	Profile to_remove = Profile(name, "", 0, "");

	for (auto it : this->get_all()) {
		if (it.get_name() == name) {
			to_remove = it;
			break;
		}
	}

	this->repo->remove(to_remove);

	this->update_stack();
	std::unique_ptr<Action> p = std::make_unique<ActionRemove>(to_remove, this->repo);
	this->unredo_stack.push_back(std::move(p));
	this->stack_index++;
}

void Service::update(string name, string proffesion, int age, string photo) {
	DomainValidator val = DomainValidator();
	if (!val.valid(name, proffesion, age, photo)) throw CustomException("Invalid input!\n");

	Profile to_add = Profile(name, proffesion, age, photo);
	Profile to_remove = Profile(name, "", 0, "");

	for (auto it : this->get_all()) {
		if (it.get_name() == name) {
			to_remove = it;
			break;
		}
	}

	this->repo->remove(to_remove);
	this->repo->add(to_add);

	this->update_stack();
	unique_ptr<Action> p = std::make_unique<ActionUpdate>(to_add, to_remove, this->repo);
	this->unredo_stack.push_back(std::move(p));
	this->stack_index++;
}

vector<Profile> Service::get_all() {
	this->buffer = this->repo->get_all();
	this->buffer_index = 0;
	return this->repo->get_all();
}

void Service::save(string name) {
	//if (this->quaranteen_passed.search(Profile(name)) != -1) throw CustomException("Profile already passed quarantine!\n");
	//if (this->buffer.search(Profile(name)) == -1) throw CustomException("Profile is not in current list!\n");
	//quaranteen_passed.add(this->buffer[this->buffer.search(Profile(name))]);

	if (vector_search(this->quaranteen_passed, Profile(name))) throw CustomException("Profile already passed quarantine!\n");
	if (!vector_search(this->buffer, Profile(name))) throw CustomException("Profile is not in current list!\n");

	for (auto it : this->buffer) {
		if (it == Profile(name)) {
			quaranteen_passed.push_back(it);
			break;
		}
	}
}

Profile& Service::next() {
	if (this->buffer.size() == 0) throw CustomException("No elements selected!\n");
	Profile& aux = this->buffer[buffer_index];
	this->buffer_index = (this->buffer_index + 1) % (this->buffer.size());
	return aux;
}

vector<Profile>& Service::filter(int age, string prof) {
	/*
	this->buffer = DynVectorT<Profile>();
	
	DynVectorT<Profile> elems = repo.get_all();
	for (DynVectorT<Profile>::Iterator it = elems.begin(); it != elems.end(); it++) {
		if (( (*it).get_proffesion() == prof || prof == "*") && (*it).get_age() <= age) buffer.add(*it);
	}
	this->buffer_index = 0;
	return this->buffer;
	*/
	
	vector<Profile> elems = repo->get_all();
	this->buffer = vector<Profile>(elems.size());

	auto it = std::copy_if(elems.begin(), elems.end(), buffer.begin(), [age, prof](Profile& t) {return (t.get_age() <= age && (t.get_proffesion() == prof || prof == "*")); });
	this->buffer.resize(std::distance(this->buffer.begin(), it));

	return this->buffer;
}

vector<Profile>& Service::get_passed() {
	return this->quaranteen_passed;
}