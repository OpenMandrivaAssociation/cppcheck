Name:		cppcheck
Version:	1.47
Release:	%mkrel 1
License:	GPLv3+
Group:		Development/Other
Url:		http://cppcheck.sourceforge.net/
Source:		http://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt-proc
Summary:	Static analysis tool for C/C++

%description
This program tries to detect bugs that your C/C++ compiler don't see. Cppcheck
is versatile. You can check non-standard code that includes various compiler
extensions, inline assembly code, etc. Its goal is no false positives.

%prep
%setup -q

%build
CXXFLAGS="%{optflags}" LDFLAGS="%{ldflags}" %make

# this command line is documented inside cppcheck.1.xml
cd man
xsltproc --nonet --param man.charmap.use.subset "0" \
   --param make.year.ranges "1" --param make.single.year.ranges "1" \
   /usr/share/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl \
   cppcheck.1.xml

%check
CXXFLAGS="%{optflags}" LDFLAGS="%{ldflags}"  %make test

%install
rm -rf %{buildroot}
%makeinstall DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 man/cppcheck.1 %{buildroot}/%{_mandir}/man1

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS readme.txt
%{_mandir}/man1/cppcheck.1*
%{_bindir}/cppcheck
