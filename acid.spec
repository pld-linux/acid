Summary:	Analysis Console for Incident Databases
Summary(pl):	Konsola do analizy baz danych o incydentach (ACID)
Name:		acid
Version:	0.9.6b13
Release:	2
Group:		Libraries
License:	GPL/PHP
Source0:	http://acidlab.sourceforge.net/%{name}-%{version}.tar.gz
Patch0:		%{name}-config.patch
URL:		http://acidlab.sourceforge.net/
Requires:	adodb >= 0.93
Requires:	phplot >= 4.4.6
Requires:	php-common >= 4.0.4
Requires:	php-gd
Requires:	apache
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ACID is a PHP-based analysis engine to search and process a database
of security incidents generated by the security-related software such
as the NIDS Snort.

%description -l pl
ACID jest bazującym na PHP silnikiem do przeszukiwania i analizy baz
danych zawierających informacje o incydentach bezpieczeństwa
wygenerowanych przez oprogramowanie takie jak NIDS Snort.

%prep
%setup  -q -n %{name}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/home/httpd/html/%{name}

install acid* index.html $RPM_BUILD_ROOT/home/httpd/html/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc create* CHANGELOG CREDITS README TODO
%attr(750,root,root) %dir /home/httpd/html/%{name}
%attr(640,root,http) /home/httpd/html/%{name}/*
