#include "OOPAssignment10.h"
#include <qdebug.h>
#include <QShortcut>

bool StringListModel::insertRows(int position, int rows, const QModelIndex& parent)
{
	beginInsertRows(QModelIndex(), position, position + rows - 1);

	for (int row = 0; row < rows; ++row) {
		stringList.insert(position, "");
	}

	endInsertRows();
	return true;

}

bool StringListModel::removeRows(int position, int rows, const QModelIndex& parent)
{
	beginRemoveRows(QModelIndex(), position, position + rows - 1);

	for (int row = 0; row < rows; ++row) {
		stringList.removeAt(position);
	}

	endRemoveRows();
	return true;

}

int StringListModel::rowCount(const QModelIndex& parent) const
{
	return stringList.count();
}

/*!
	Returns an appropriate value for the requested data.
	If the view requests an invalid index, an invalid variant is returned.
	Any valid index that corresponds to a string in the list causes that
	string to be returned.
*/
QVariant StringListModel::data(const QModelIndex& index, int role) const
{
	if (!index.isValid())
		return QVariant();

	if (index.row() >= stringList.size())
		return QVariant();

	if (role == Qt::DisplayRole)
		return stringList.at(index.row());
	else
		return QVariant();
}

OOPAssignment10::OOPAssignment10(Service* srv, QWidget* parent) : srv{ srv }, QWidget(parent) {
	this->initGUI();
	this->connectSignalsAndSlots();
	this->buffer = srv->get_all();
	this->populateProfilesList();
	this->populateQuarantineList();
}

void OOPAssignment10::initGUI() {
	this->listView = new QListView;

	QHBoxLayout* layout = new QHBoxLayout{ this };

	//left list widget
	this->profilesList = new QListWidget;

	//left input widget
	QWidget* inputLWidget = new QWidget;
	QFormLayout* inputLLayout = new QFormLayout;

	QLabel* l1 = new QLabel{ "Name: " };
	this->nameLE = new QLineEdit;
	l1->setBuddy(this->nameLE);
	QLabel* l2 = new QLabel{ "Proffesion: " };
	this->proffesionLE = new QLineEdit;
	l2->setBuddy(this->proffesionLE);
	QLabel* l3 = new QLabel{ "Age: " };
	this->ageLE = new QLineEdit;
	l3->setBuddy(this->ageLE);
	QLabel* l4 = new QLabel{ "Photo: " };
	this->photoLE = new QLineEdit;
	l4->setBuddy(this->photoLE);
	QLabel* l5 = new QLabel{ "Path: " };
	this->pathLE = new QLineEdit;
	l4->setBuddy(this->photoLE);
	inputLLayout->addRow(l1, this->nameLE);
	inputLLayout->addRow(l2, this->proffesionLE);
	inputLLayout->addRow(l3, this->ageLE);
	inputLLayout->addRow(l4, this->photoLE);
	inputLLayout->addRow(l5, this->pathLE);

	inputLWidget->setLayout(inputLLayout);

	//left buttons widget
	QWidget* buttonLWidget = new QWidget;
	QGridLayout* buttonLLayout = new QGridLayout{};

	this->addButton = new QPushButton{ "Add" };
	buttonLLayout->addWidget(this->addButton, 0, 0);
	this->removeButton = new QPushButton{ "Remove" };
	buttonLLayout->addWidget(this->removeButton, 0, 1);
	this->updateButton = new QPushButton{ "Update" };
	buttonLLayout->addWidget(this->updateButton, 0, 2);
	this->filterButton = new QPushButton{ "Filter" };
	buttonLLayout->addWidget(this->filterButton, 1, 0);
	this->listButton = new QPushButton{ "List" };
	buttonLLayout->addWidget(this->listButton, 1, 1);
	this->pathButton = new QPushButton{ "Path" };
	buttonLLayout->addWidget(this->pathButton, 1, 2);
	this->undoButton = new QPushButton{ "Undo" };
	buttonLLayout->addWidget(this->undoButton, 2, 0);
	this->redoButton = new QPushButton{ "Redo" };
	buttonLLayout->addWidget(this->redoButton, 2, 2);

	buttonLWidget->setLayout(buttonLLayout);

	//Left side widget
	QWidget* leftPane = new QWidget;
	QVBoxLayout* leftVLayout = new QVBoxLayout;
	leftVLayout->addWidget(new QLabel{ "All profiles" });
	leftVLayout->addWidget(this->profilesList);
	leftVLayout->addWidget(inputLWidget);
	leftVLayout->addWidget(buttonLWidget);
	leftPane->setLayout(leftVLayout);

	//middle pane with just a button
	this->saveButton = new QPushButton{ ">" };

	//right pane
	QWidget* rightPane = new QWidget;
	QVBoxLayout* rightVLayout = new QVBoxLayout;
	rightVLayout->addWidget(new QLabel{ "Profiles that passed the quarantine" });
	this->quarantinePassedList = new QListWidget;
	rightVLayout->addWidget(this->quarantinePassedList);
	rightPane->setLayout(rightVLayout);


	layout->addWidget(leftPane);
	layout->addWidget(this->saveButton);
	layout->addWidget(rightPane);
}

void OOPAssignment10::populateProfilesList() {
	vector<Profile> profiles = this->buffer;

	if (this->profilesList->count() > 0)
		this->profilesList->clear();

	for (auto it : profiles) {
		QString str = QString::fromStdString(it.get_name());
		this->profilesList->addItem(new QListWidgetItem{ str });
	}

	if (profiles.size() > 0)
		this->profilesList->setCurrentRow(0);

}

void OOPAssignment10::listItemChanged() {
	vector<Profile> profiles = this->buffer;
	int idx = this->getSelectedIndex();

	if (idx == -1) return;

	if (idx >= profiles.size()) return;

	Profile p = profiles[idx];
	this->nameLE->setText(QString::fromStdString(p.get_name()));
	this->proffesionLE->setText(QString::fromStdString(p.get_proffesion()));
	this->ageLE->setText(QString::fromStdString(std::to_string(p.get_age())));
	this->photoLE->setText(QString::fromStdString(p.get_photo()));
}

int OOPAssignment10::getSelectedIndex(){
	if (this->profilesList->count() == 0)
		return -1;

	// get selected index
	QModelIndexList index = this->profilesList->selectionModel()->selectedIndexes();
	if (index.size() == 0)
	{
		this->nameLE->clear();
		this->proffesionLE->clear();
		this->ageLE->clear();
		this->photoLE->clear();
		return -1;
	}

	int idx = index.at(0).row();
	return idx;
}

void OOPAssignment10::connectSignalsAndSlots()
{
	// when the vector of profiles is updated - re-populate the list
	QObject::connect(this, &OOPAssignment10::profilesUpdatedSignal, this, &OOPAssignment10::populateProfilesList);
	QObject::connect(this, &OOPAssignment10::passedUpdatedSignal, this, &OOPAssignment10::populateQuarantineList);

	// add a connection: function listItemChanged() will be called when an item in the list is selected
	QObject::connect(this->profilesList, &QListWidget::itemSelectionChanged, this, [this]() {this->listItemChanged(); });

	// add button connections
	QObject::connect(this->addButton, &QPushButton::clicked, this, &OOPAssignment10::addProfile);
	QObject::connect(this->removeButton, &QPushButton::clicked, this, &OOPAssignment10::removeProfile);
	QObject::connect(this->updateButton, &QPushButton::clicked, this, &OOPAssignment10::updateProfile);
	QObject::connect(this->filterButton, &QPushButton::clicked, this, &OOPAssignment10::filter);
	QObject::connect(this->saveButton, &QPushButton::clicked, this, &OOPAssignment10::save);
	QObject::connect(this->pathButton, &QPushButton::clicked, this, &OOPAssignment10::path);
	QObject::connect(this->undoButton, &QPushButton::clicked, this, &OOPAssignment10::undo);
	QObject::connect(this->redoButton, &QPushButton::clicked, this, &OOPAssignment10::redo);
	QObject::connect(this->listButton, &QPushButton::clicked, this, &OOPAssignment10::list);
	QShortcut* shortcut_undo = new QShortcut(QKeySequence("Ctrl+Z"), this);
	QShortcut* shortcut_redo = new QShortcut(QKeySequence("Ctrl+Y"), this);
	QObject::connect(shortcut_undo, &QShortcut::activated, this, &OOPAssignment10::undo);
	QObject::connect(shortcut_redo, &QShortcut::activated, this, &OOPAssignment10::redo);
	// connect the addGene signal to the addGene slot, which adds a gene to vector
}

void OOPAssignment10::list() {
	this->populateQuarantineList();
	this->listView->show();
}

void OOPAssignment10::undo() {
	try {
		this->srv->undo();
		this->buffer = srv->get_all();
		emit profilesUpdatedSignal();
	}
	catch (CustomException& e) {
		QMessageBox::information(this, "Error", e.what());
	}
}

void OOPAssignment10::redo() {
	try {
		this->srv->redo();
		this->buffer = srv->get_all();
		emit profilesUpdatedSignal();
	}
	catch (CustomException& e) {
		QMessageBox::information(this, "Error", e.what());
	}
}

void OOPAssignment10::path() {
	try {
		if (this->pathLE->text() != "") {
			this->srv->set_path(this->pathLE->text().toStdString());
			this->buffer = srv->get_all();
			emit profilesUpdatedSignal();
		}
	}
	catch (CustomException& e) {
		QMessageBox::information(this, "Error", e.what());
	}
}

void OOPAssignment10::filter() {
	if (this->ageLE->text() == "") {
		this->buffer = srv->get_all();
		emit profilesUpdatedSignal();
		return;
	}

	string proffesion = this->proffesionLE->text().toStdString();
	int age = stoi(this->ageLE->text().toStdString());

	try {
		if (this->proffesionLE->text() != "")
			this->buffer = this->srv->filter(age, proffesion);
		else
			this->buffer = this->srv->filter(age);
		emit profilesUpdatedSignal();
	}
	catch (CustomException& e) {
		QMessageBox::information(this, "Error", e.what());
	}
}

void OOPAssignment10::removeProfile() {
	string name = this->nameLE->text().toStdString();

	try {
		this->srv->remove(name);
		this->buffer = srv->get_all();
		emit profilesUpdatedSignal();
	}
	catch (CustomException& e) {
		QMessageBox::information(this, "Error", e.what());
	}
}

void OOPAssignment10::updateProfile() {
	string name = this->nameLE->text().toStdString();
	string proffesion = this->proffesionLE->text().toStdString();
	string photo = this->photoLE->text().toStdString();
	int age = stoi(this->ageLE->text().toStdString());

	try {
		this->srv->update(name, proffesion, age, photo);
		this->buffer = srv->get_all();
		emit profilesUpdatedSignal();
	}
	catch (CustomException& e) {
		QMessageBox::information(this, "Error", e.what());
	}
}

void OOPAssignment10::save() {
	string name = this->nameLE->text().toStdString();

	try {
		this->srv->save(name);
		emit passedUpdatedSignal();
	}
	catch (CustomException& e) {
		QMessageBox::information(this, "Error", e.what());
	}
}

void OOPAssignment10::addProfile() {
	string name = this->nameLE->text().toStdString();
	string proffesion = this->proffesionLE->text().toStdString();
	string photo = this->photoLE->text().toStdString();
	int age = stoi(this->ageLE->text().toStdString());

	try {
		this->srv->add(name, proffesion, age, photo);
		this->buffer = srv->get_all();
		emit profilesUpdatedSignal();
	}
	catch (CustomException& e) {
		QMessageBox::information(this, "Error", e.what());
	}
}

void OOPAssignment10::populateQuarantineList() {
	vector<Profile> q = this->srv->get_passed();
	QStringList list;
	for (auto it : q) {
		list << QString::fromStdString(it.get_name());
	}
	this->listModel = new StringListModel(list);
	this->listView->setModel(this->listModel);

	if (this->quarantinePassedList->count() > 0)
		this->quarantinePassedList->clear();

	for (auto it : q) {
		QString str = QString::fromStdString(it.get_name());
		this->quarantinePassedList->addItem(new QListWidgetItem{ str });
	}

	if (q.size() > 0)
		this->quarantinePassedList->setCurrentRow(0);

}