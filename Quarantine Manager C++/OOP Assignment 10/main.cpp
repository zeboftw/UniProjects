#include "OOPAssignment10.h"
#include <QtWidgets/QApplication>
#include <QLineEdit>
#include <QLabel>
#include <QFormLayout>
#include <qdebug.h>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	
	ifstream config{ "config.cfg" };
	unique_ptr<Repository> repo;

	string line;
	string path;

	while (config >> line) {
		if (line == "MODE=INMEMORY") {
			RepositoryMemory r;
			r.add(Profile("Filler1", "filter", 10, "asd"));
			r.add(Profile("Filler2", "filter", 20, "asd"));
			r.add(Profile("Filler3", "not filter", 30, "asd"));
			r.add(Profile("Filler4", "not filter", 40, "asd"));
			r.add(Profile("Filler5", "filter", 50, "asd"));
			r.add(Profile("Filler6", "filter", 60, "asd"));
			r.add(Profile("Filler7", "not filter", 70, "asd"));
			r.add(Profile("Filler8", "filter", 80, "asd"));
			repo = make_unique<RepositoryMemory>(r);
		}
		else if (line == "MODE=CSV") repo = make_unique<RepositoryCSV>(RepositoryCSV());
		else if (line == "MODE=HTML") repo = make_unique<RepositoryHTML>(RepositoryHTML());
		if (line.substr(0, 5) == "PATH=") path = line.substr(5, line.size());
	}

	try {
		repo->set_path(path);
	}
	catch (CustomException& e) {}

	Service* srv = new Service(move(repo));
	OOPAssignment10 w{ srv };
	w.show();


	return a.exec();
}
