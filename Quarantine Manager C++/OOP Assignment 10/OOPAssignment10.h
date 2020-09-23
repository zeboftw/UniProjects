#pragma once

#include <QtWidgets/QMainWindow>
#include "Service.h"
#include <QLineEdit>
#include <QLabel>
#include <QFormLayout>
#include <QListWidget>
#include <QPushButton>
#include <QMessageBox>


class StringListModel : public QAbstractListModel
{
	Q_OBJECT

public:
	StringListModel(QStringList& strings, QObject* parent = Q_NULLPTR) : QAbstractListModel(parent), stringList(strings) {}
	bool insertRows(int position, int rows, const QModelIndex& index = QModelIndex());
	bool removeRows(int position, int rows, const QModelIndex& index = QModelIndex());
	int rowCount(const QModelIndex& parent = QModelIndex()) const;
	QVariant data(const QModelIndex& index, int role) const;

private:
	QStringList stringList;
};

class OOPAssignment10 : public QWidget
{
	Q_OBJECT

public:
	OOPAssignment10(Service*, QWidget *parent = Q_NULLPTR);

private:
	Service* srv;
	vector<Profile> buffer;

	QListWidget* profilesList;
	QListWidget* quarantinePassedList;
	QListView* listView;
	QAbstractItemModel* listModel;

	QLineEdit* nameLE;
	QLineEdit* proffesionLE;
	QLineEdit* ageLE;
	QLineEdit* photoLE;
	QLineEdit* pathLE;

	QPushButton* addButton;
	QPushButton* removeButton;
	QPushButton* updateButton;
	QPushButton* filterButton;
	QPushButton* saveButton;
	QPushButton* listButton;
	QPushButton* pathButton;
	QPushButton* undoButton;
	QPushButton* redoButton;

	void initGUI();
	void connectSignalsAndSlots();
	int getSelectedIndex();

	void populateProfilesList();
	void populateQuarantineList();
	void listItemChanged();

	void addProfile();
	void removeProfile();
	void updateProfile();
	void filter();
	void save();
	void list();
	void path();
	void undo();
	void redo();

signals:
	void profilesUpdatedSignal();
	void passedUpdatedSignal();
};
