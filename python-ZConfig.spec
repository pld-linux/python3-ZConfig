# TODO:
# - fix tests, needs: manuel and zope.testrunner
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		ZConfig
Summary:	Structured Configuration Library
Summary(pl.UTF-8):	Biblioteka ustrukturyzowanych plików konfiguracyjnych
Name:		python-%{module}
Version:	3.2.0
Release:	8
License:	ZPL 2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/Z/ZConfig/%{module}-%{version}.tar.gz
# Source0-md5:	1f7206c3efaaed21e492153156107e89
URL:		https://github.com/zopefoundation/ZConfig/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules >= 1:2.6
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

%package -n python3-%{module}
Summary:	Structured Configuration Library
Summary(pl.UTF-8):	Biblioteka ustrukturyzowanych plików konfiguracyjnych
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
ZConfig is a configuration library intended for general use. It
supports a hierarchical schema-driven configuration model that allows
a schema to specify data conversion routines written in Python.
ZConfig's model is very different from the model supported by the
ConfigParser module found in Python's standard library, and is more
suitable to configuration-intensive applications.

%description -n python3-%{module} -l pl.UTF-8
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
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%{py_sitescriptdir}/ZConfig
%{py_sitescriptdir}/ZConfig-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%attr(755,root,root) %{_bindir}/zconfig
%attr(755,root,root) %{_bindir}/zconfig_schema2html
%{py3_sitescriptdir}/ZConfig
%{py3_sitescriptdir}/ZConfig-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
