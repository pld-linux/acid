# TODO
# - proper webapps integration: make config NOT accessible from web
Summary:	Analysis Console for Incident Databases
Summary(pl.UTF-8):	Konsola do analizy baz danych o incydentach (ACID)
Name:		acid
Version:	0.9.6b23
Release:	10
License:	GPL/PHP
Group:		Applications/WWW
Source0:	http://acidlab.sourceforge.net/%{name}-%{version}.tar.gz
# Source0-md5:	d8c49614393fa05ac140de349f57e438
Source1:	%{name}.conf
Patch0:		%{name}-config.patch
URL:		http://acidlab.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.461
Requires:	%{name}(DB_Driver) = %{version}-%{release}
Requires:	adodb >= 4.67-1.17
Requires:	jpgraph >= 1.8
Requires:	php(gd)
Requires:	webapps
Requires:	webserver(php) < 5.0.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
ACID is a PHP-based analysis engine to search and process a database
of security incidents generated by the security-related software such
as the NIDS Snort.

%description -l pl.UTF-8
ACID jest bazującym na PHP silnikiem do przeszukiwania i analizy baz
danych zawierających informacje o incydentach bezpieczeństwa
wygenerowanych przez oprogramowanie takie jak NIDS Snort.

%package db-mysql
Summary:	ACID DB Driver for MySQL
Summary(pl.UTF-8):	Sterownik bazy danych MySQL dla ACID
Group:		Applications/WWW
Requires:	php(mysql)
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-mysql
This virtual package provides MySQL database backend for ACID.

%description db-mysql -l pl.UTF-8
Ten wirtualny pakiet dostarcza backend bazy danych MySQL dla ACID.

%package db-pgsql
Summary:	ACID DB Driver for PostgreSQL
Summary(pl.UTF-8):	Sterownik bazy danych PostgreSQL dla ACID
Group:		Applications/WWW
Requires:	php(pgsql)
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-pgsql
This virtual package provides PostgreSQL database backend for ACID.

%description db-pgsql -l pl.UTF-8
Ten wirtualny pakiet dostarcza backend bazy danych PostgreSQL dla
ACID.

%prep
%setup -q -n %{name}
%patch0 -p1

find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}

install acid* index.html $RPM_BUILD_ROOT%{_appdir}
# TODO: patch source instead
mv -f $RPM_BUILD_ROOT%{_appdir}/acid_conf.php $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/acid_conf.php $RPM_BUILD_ROOT%{_appdir}/acid_conf.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} < 0.9.6b23-5.2
%{__sed} -i -e 's,%{php_pear_dir}/adodb,%{php_data_dir}/adodb,' %{_sysconfdir}/acid_conf.php

%files
%defattr(644,root,root,755)
%doc create* CHANGELOG CREDITS README TODO
%dir %attr(750,root,http) %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/acid_conf.php
%{_appdir}

%files db-mysql
%defattr(644,root,root,755)

%files db-pgsql
%defattr(644,root,root,755)
