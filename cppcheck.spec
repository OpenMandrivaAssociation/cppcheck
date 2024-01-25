%define _disable_ld_no_undefined 1
%define _empty_manifest_terminate_build 0

Name:		cppcheck
Version:	2.13.2
Release:	1
License:	GPLv3+
Summary:	Static analysis tool for C/C++
Group:		Development/Other
Url:		http://cppcheck.sourceforge.net/
Source0:	https://github.com/danmar/cppcheck/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	pcre-devel
BuildRequires:	tinyxml2-devel

%description
This program tries to detect bugs that your C/C++ compiler don't see. Cppcheck
is versatile. You can check non-standard code that includes various compiler
extensions, inline assembly code, etc. Its goal is no false positives.

%prep
%setup -q

%build
CXXFLAGS="%{optflags}" LDFLAGS="%{ldflags}" CXX="%{__cxx} -std=c++11" %make HAVE_RULES=yes TINYXML="-ltinyxml2" FILESDIR=%{_datadir}/cppcheck

# this command line is documented inside cppcheck.1.xml
cd man
xsltproc --nonet --param man.charmap.use.subset "0" \
   --param make.year.ranges "1" --param make.single.year.ranges "1" \
   /usr/share/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl \
   cppcheck.1.xml

%check
CXXFLAGS="%{optflags}" LDFLAGS="%{ldflags}" CXX="%{__cxx} -std=c++11" make HAVE_RULES=yes TINYXML="-ltinyxml2" test

%install
%makeinstall_std DESTDIR=%{buildroot} HAVE_RULES=yes TINYXML="-ltinyxml2" FILESDIR=%{_datadir}/cppcheck
mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 man/cppcheck.1 %{buildroot}/%{_mandir}/man1

rm -f %{buildroot}%{_bindir}/*.py

%files
%doc AUTHORS readme.txt
%{_mandir}/man1/cppcheck.1*
%{_bindir}/cppcheck
%{_bindir}/cppcheck-htmlreport
%{_datadir}/cppcheck
