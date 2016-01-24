PYTHON=`which python`
DESTDIR=/
BUILDIR=$(CURDIR)/debian/myprojectname
PROJECT=py-daemon-skeleton
VERSION=0.1.0

all:
        @echo "make source - Create source package"
        @echo "make builddeb - Generate a deb package"
        @echo "make clean - Get rid of scratch and byte files"

source:
        $(PYTHON) setup.py sdist $(COMPILE)

builddeb:
        # build the source package in the parent directory
        # then rename it to project_version.orig.tar.gz
        $(PYTHON) setup.py sdist $(COMPILE) --dist-dir=../ --prune
        rename -f 's/$(PROJECT)-(.*)\.tar\.gz/$(PROJECT)_$$1\.orig\.tar\.gz/' ../*
        # build the package
        dpkg-buildpackage -i -I -rfakeroot

clean:
        $(PYTHON) setup.py clean
        $(MAKE) -f $(CURDIR)/debian/rules clean
        rm -rf build/ MANIFEST
        find . -name '*.pyc' -delete
