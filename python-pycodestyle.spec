%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global with_python3 1

%if 0%{?fedora}
%{!?python3_pkgversion: %global python3_pkgversion 3}
%else
%{!?python3_pkgversion: %global python3_pkgversion 34}
%endif

%{!?python3_version: %global python3_version %(%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])")}

%global module_name pycodestyle

Name:           python-%{module_name}
Version:        2.0.0
Release:        2%{?dist}
Summary:        Python style guide checker

# License is held in the comments of pycodestyle.py
# setup.py claims license is Expat license, which is the same as MIT
License:        MIT
URL:            https://pypi.python.org/pypi/%{module_name}
Source0:        https://pypi.io/packages/source/p/%{module_name}/%{module_name}-%{version}.tar.gz

BuildArch:      noarch

%description
pycodestyle is a tool to check your Python code against some of the style
conventions in PEP 8. It has a plugin architecture, making new checks easy, and
its output is parseable, making it easy to jump to an error location in your
editor.

%package -n python2-%{module_name}
Summary:        Python style guide checker
%{?python_provide:%python_provide python2-%{module_name}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-sphinx_rtd_theme
Requires:       python-setuptools


%description -n python2-%{module_name}
pycodestyle is a tool to check your Python code against some of the style
conventions in PEP 8. It has a plugin architecture, making new checks easy, and
its output is parseable, making it easy to jump to an error location in your
editor.


%if %{with python3}
%package -n python3-pycodestyle
Summary:    Python style guide checker
%{?python_provide:%python_provide python%{python3_pkgversion}-%{module_name}}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-sphinx


Requires:  python%{python3_pkgversion}-setuptools
%description -n python%{python3_pkgversion}-pycodestyle
pycodestyle is a tool to check your Python code against some of the style
conventions in PEP 8. It has a plugin architecture, making new checks easy, and
its output is parseable, making it easy to jump to an error location in your
editor.

This is a version for Python %{python3_pkgversion}.

%endif


%prep
%autosetup -n %{module_name}-%{version}

# Remove #! from pycodestyle.py
sed --in-place "s:#!\s*/usr.*::" pycodestyle.py


%build
%py2_build
%py3_build

make -C docs man


%install
%py3_install
mv %{buildroot}%{_bindir}/pycodestyle %{buildroot}%{_bindir}/pycodestyle-%{python3_version}
ln -s ./pycodestyle-%{python3_version} %{buildroot}%{_bindir}/pycodestyle-3

%py2_install
mv %{buildroot}%{_bindir}/pycodestyle %{buildroot}%{_bindir}/pycodestyle-%{python2_version}
ln -s ./pycodestyle-%{python2_version} %{buildroot}%{_bindir}/pycodestyle
ln -s ./pycodestyle-%{python2_version} %{buildroot}%{_bindir}/pycodestyle-2

install -D docs/_build/man/%{module_name}.1 %{buildroot}%{_mandir}/man1/%{module_name}.1


%check
%{__python2} pycodestyle.py --testsuite testsuite
%{__python2} pycodestyle.py --doctest
%{__python3} pycodestyle.py --testsuite testsuite
%{__python3} pycodestyle.py --doctest


%files -n python2-%{module_name}
%defattr(-,root,root,-)
%doc CHANGES.txt README.rst
%{_bindir}/pycodestyle
%{_bindir}/pycodestyle-2
%{_bindir}/pycodestyle-2.7
%{python2_sitelib}/%{module_name}.py*
%{python2_sitelib}/%{module_name}-%{version}-*.egg-info

%if %{with python3}
%files -n python3-pycodestyle
%doc README.rst CHANGES.txt
%{_mandir}/man1/%{module_name}.1.gz
%{_bindir}/pycodestyle-3
%{_bindir}/pycodestyle-%{python3_version}
%{python3_sitelib}/%{module_name}.py*
%{python3_sitelib}/%{module_name}-%{version}-*.egg-info/
%{python3_sitelib}/__pycache__/%{module_name}*
%endif

%changelog
* Thu Aug  4 2016 Luke Macken <lmacken@redhat.com> - 2.0.0-2
- Use the new python setup/build/install macros
- Remove Obsoletes/Provides for pep8, since it is currently not a drop-in replacement.
  https://bugzilla.redhat.com/show_bug.cgi?id=1342839#c10

* Sun Jun 05 2016 Luke Macken <lmacken@redhat.com> - 2.0.0-1
- The pep8 project has been renamed to pycodestyle
- Create python2 subpackage
- Update the source url to use pypi.io
- Build a man page instead of html docs

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Nov 11 2015 Robert Kuska <rkuska@redhat.com> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Nov 11 2015 Matthias Runge <mrunge@redhat.com> - 1.6.2-1
- update to 1.6.2

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 1.5.7-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 20 2014 Matthias Runge <mrunge@redhat.com> - 1.5.7-1
- update to 1.5.7

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed May 14 2014 Matthias Runge <mrunge@redhat.com> - 1.5.6-1
- update to 1.5.6 (rhbz#1087351)

* Tue Apr 08 2014 Matthias Runge <mrunge@redhat.com> - 1.5.4-1
- require python3-setuptools (rhbz#1084756)
- update to 1.5.4 (rhbz#1081516)

* Wed Feb 26 2014 Matthias Runge <mrunge@redhat.com> -1.4.6-2
- rename py3 version of pep8 to python3-pep8 (rhbz#1060408)

* Tue Aug 13 2013 Ian Weller <iweller@redhat.com> - 1.4.6-1
- update to 1.4.6

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Matthias Runge <mrunge@redhat.com> - 1.4.5-1
- update to 1.4.5 (rhbz#918924)
- introduce py3 package (rhbz#971941)

* Tue Feb 26 2013 Ian Weller <iweller@redhat.com> - 1.4.4-1
- Update to 1.4.4

* Mon Feb 11 2013 Ian Weller <iweller@redhat.com> - 1.4.2-1
- Update to 1.4.2

* Tue Jan 29 2013 Ian Weller <iweller@redhat.com> - 1.4.1-1
- Update to 1.4.1
- Add Sphinx docs

* Fri Sep 07 2012 Ian Weller <iweller@redhat.com> - 1.3.3-3
- Run test suite using the pep8.py that has been installed

* Fri Sep 07 2012 Ian Weller <iweller@redhat.com> - 1.3.3-2
- Add test suite

* Thu Sep 06 2012 Ian Weller <iweller@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Ian Weller <iweller@redhat.com> - 1.3-1
- Update to 1.3

* Sat Apr 07 2012 Ian Weller <iweller@redhat.com> - 1.0.1-1
- Update to 1.0.1

* Fri Jan 27 2012 Ian Weller <iweller@redhat.com> - 0.6.1-1
- Update to 0.6.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Ian Weller <iweller@redhat.com> - 0.6.0-2
- RHBZ 633102: Requires: python-setuptools

* Tue Nov 16 2010 Ian Weller <iweller@redhat.com> - 0.6.0-1
- Changed upstream (same code, new maintainer, new URL)
- New release

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov  9 2009 Ian Weller <ian@ianweller.org> - 0.4.2-2
- Add BR: python-setuptools
- Change URL to the correct upstream

* Sun Nov  8 2009 Ian Weller <ian@ianweller.org> - 0.4.2-1
- Initial package build
