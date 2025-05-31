#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module		ZConfig
Summary:	Structured Configuration Library
Summary(pl.UTF-8):	Biblioteka ustrukturyzowanych plików konfiguracyjnych
Name:		python3-%{module}
Version:	4.2
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/Z/ZConfig/zconfig-%{version}.tar.gz
# Source0-md5:	93441a72f1598d0f39bf93fe6320f628
URL:		https://github.com/zopefoundation/ZConfig/
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-docutils
BuildRequires:	python3-manuel
BuildRequires:	python3-zope.exceptions
BuildRequires:	python3-zope.testrunner
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-sphinxcontrib-programoutput
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZConfig is a configuration library intended for general use. It
supports a hierarchical schema-driven configuration model that allows
a schema to specify data conversion routines written in Python.
ZConfig's model is very different from the model supported by the
ConfigParser module found in Python's standard library, and is more
suitable to configuration-intensive applications.

%description -l pl.UTF-8
ZConfig to biblioteka konfiguracji, przeznaczona do ogólnego użytku.
Obsługuje hierarchiczny, oparty na schematach model konfiguracji,
pozwalający na określanie w schematach napisanych w Pythonie procedur
konwersji danych. Model ZConfig różni się znacząco od modelu
obsługiwanego przez moduł ConfigParser z biblioteki standardowej
Pythona i bardziej odpowiada aplikacjon korzystającym intensywnie z
konfiguracji.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Pythona %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n zconfig-%{version}

mkdir -p stubs
cat >stubs/zconfig <<EOF
#!/bin/sh
%{__python} $(pwd)/src/ZConfig/validator.py "\$@"
EOF
cat >stubs/zconfig_schema2html <<EOF
#!/bin/sh
%{__python} $(pwd)/src/ZConfig/schema2html.py "\$@" 
EOF
chmod 755 stubs/zconfig*

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif

%if %{with doc}
PATH=$(pwd)/stubs:$PATH \
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/ZConfig/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/zconfig
%attr(755,root,root) %{_bindir}/zconfig_schema2html
%{py3_sitescriptdir}/ZConfig
%{py3_sitescriptdir}/ZConfig-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
