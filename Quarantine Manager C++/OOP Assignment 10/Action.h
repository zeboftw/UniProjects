#pragma once

#include <memory>
#include "Domain.h"
#include "Repository.h"

class Action {
public:
	virtual void executeUndo() = 0;
	virtual void executeRedo() = 0;
};

class ActionAdd : public Action {
private:
	std::unique_ptr<Profile> addedProfile;
	std::shared_ptr<Repository> repo_ptr;
public:
	ActionAdd(Profile& s, shared_ptr<Repository>& r) : addedProfile{ std::make_unique<Profile>(s) }, repo_ptr{ r }{};
	void executeUndo() override {
		this->repo_ptr->remove(*this->addedProfile);
	}
	void executeRedo() override {
		this->repo_ptr->add(*this->addedProfile);
	}
};

class ActionRemove : public Action {
public:
	ActionRemove(Profile& s, shared_ptr<Repository>& r) : removedProfile{ std::make_unique<Profile>(s) }, repo_ptr{ r }{};
	void executeUndo() override {
		this->repo_ptr->add(*this->removedProfile);
	}
	void executeRedo() override {
		this->repo_ptr->remove(*this->removedProfile);
	}
private:
	std::unique_ptr<Profile> removedProfile;
	shared_ptr<Repository> repo_ptr;

};

class ActionUpdate : public Action {
public:
	ActionUpdate(Profile& s_add, Profile& s_remove, shared_ptr<Repository>& r) : addedProfile{ std::make_unique<Profile>(s_add) }, removedProfile{ std::make_unique<Profile>(s_remove) }, repo_ptr{ r }{};
	void executeUndo() override {
		this->repo_ptr->remove(*this->addedProfile);
		this->repo_ptr->add(*this->removedProfile);
	}
	void executeRedo() override {
		this->repo_ptr->remove(*this->removedProfile);
		this->repo_ptr->add(*this->addedProfile);
	}
private:
	std::unique_ptr<Profile> removedProfile;
	std::unique_ptr<Profile> addedProfile;
	shared_ptr<Repository> repo_ptr;

};