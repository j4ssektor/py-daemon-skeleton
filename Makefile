PYTHON=`which python`
DESTDIR=/
BUILDIR=$(CURDIR)/debian/skeleton
PROJECT=skeleton
VERSION=0.1.0

all:
		@echo "make source - Create source package"
		@echo "make builddeb - Generate a deb package"
		@echo "make clean - Get rid of scratch and byte files"


source:
		$(PYTHON) setup.py sdist $(COMPILE)


builddeb:
		$(PYTHON) setup.py sdist $(COMPILE) --dist-dir=../ 
		rename -f 's/$(PROJECT)-(.*)\.tar\.gz/$(PROJECT)_$$1\.orig\.tar\.gz/' ../*
		dpkg-buildpackage -i -I -rfakeroot


clean:
		$(PYTHON) setup.py clean
		fakeroot $(MAKE) -f $(CURDIR)/debian/rules clean
		rm -rf $(CURDIR)/build
