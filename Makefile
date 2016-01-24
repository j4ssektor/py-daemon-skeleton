PYTHON=`which python`
BUILDIR=$(CURDIR)/debian/skeleton
PROJECT=skeleton
VERSION=0.1.0

all:
		@echo "make source - Create source package"
		@echo "make builddeb - Generate a deb package"


source:
		$(PYTHON) setup.py sdist $(COMPILE)


builddeb:
		$(PYTHON) setup.py --command-packages=stdeb.command sdist_dsc $(COMPILE)
		dpkg-buildpackage -i -I -rfakeroot
