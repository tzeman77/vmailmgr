Name: vmailmgr
Version: @VERSION@
Release: 1
Group: Utilities/System
URL: http://em.ca/~bruceg/vmailmgr/
Copyright: GPL
Source: http://em.ca/~bruceg/vmailmgr/archive/%{PACKAGE_VERSION}/vmailmgr-%{PACKAGE_VERSION}.tar.gz
Summary: Simple virtualizing POP3 password interface
Packager: Bruce Guenter <bruceg@em.ca>
Buildroot: /tmp/vmailmgr
Obsoletes: checkvpw

%description
Vmailmgr provides a virtualizing password-checking interface to
qmail-pop3d as well as both a delivery agent to automatically delivery
mail within a virtual domain and a set of tools to manage such a domain.

%package cgi
Summary: CGI applications for vmailmgr
Group: Utilities/System
Requires: vmailmgr-daemon = %{PACKAGE_VERSION}
%description cgi
This package contains CGI applications to allow web-based administration
of vmailmgr systems.

%package daemon
Summary: Vmailmgr daemon for CGIs
Requires: daemontools >= 0.61
Requires: supervise-scripts >= 2.2
Group: Utilities/System
%description daemon
This package contains the vmailmgrd daemon that provides virtual domain
manipulation services to support unprivileged clients like CGIs.

%package python
Summary: Python modules and CGIs for vmailmgr
Group: Utilities/System
Requires: python >= 1.5
Requires: vmailmgr-daemon = %{PACKAGE_VERSION}
%description python
This package contains vmailmgr code written in/for Python, including one
CGI.

%prep
%setup
CFLAGS="$RPM_OPT_FLAGS" \
CXXFLAGS="$RPM_OPT_FLAGS" \
LDFLAGS="-s" \
./configure --prefix=/usr

%build
make all

%install
rm -rf $RPM_BUILD_ROOT
for dir in var/service/vmailmgrd/log var/log/vmailmgrd \
	etc/rc.d/init.d etc/rc.d/rc{0,1,2,3,4,5,6}.d etc/vmailmgr
do
	mkdir -p $RPM_BUILD_ROOT/$dir
done
make prefix=$RPM_BUILD_ROOT/usr \
	cgidir=$RPM_BUILD_ROOT/home/httpd/cgi-bin \
	pythonlibdir=$RPM_BUILD_ROOT/usr/lib/python1.5 install-strip
install -m 755 daemon/init $RPM_BUILD_ROOT/etc/rc.d/init.d/vmailmgrd
install -m 755 daemon/run-svc $RPM_BUILD_ROOT/var/service/vmailmgrd/run
install -m 755 daemon/run-log $RPM_BUILD_ROOT/var/service/vmailmgrd/log/run
pushd $RPM_BUILD_ROOT/etc/rc.d
ln -s ../init.d/vmailmgrd rc0.d/K35vmailmgrd
ln -s ../init.d/vmailmgrd rc1.d/K35vmailmgrd
ln -s ../init.d/vmailmgrd rc2.d/S65vmailmgrd
ln -s ../init.d/vmailmgrd rc3.d/S65vmailmgrd
ln -s ../init.d/vmailmgrd rc4.d/S65vmailmgrd
ln -s ../init.d/vmailmgrd rc5.d/S65vmailmgrd
ln -s ../init.d/vmailmgrd rc6.d/K35vmailmgrd
popd
pushd $RPM_BUILD_ROOT/etc/vmailmgr
echo users >user-dir
echo passwd >password-file
echo ./Maildir/ >default-maildir
echo maildir >maildir-arg-str
echo /var/service/vmailmgrd/socket >socket-file

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $# -eq 2 -a -f /etc/vmailmgr.conf ]; then
  vconf2dir /etc/vmailmgr.conf /etc/vmailmgr
fi

%files
%defattr(-,root,root)
%doc doc/ChangeLog* AUTHORS COPYING NEWS doc/TODO doc/YEAR2000
%doc doc/*.txt doc/*.html
%dir /etc/vmailmgr
%config(missingok,noreplace) %verify(user,group,mode) /etc/vmailmgr/*
/usr/bin/*
/usr/man/man1/*
/usr/man/man5/*
/usr/man/man7/*
/usr/man/man8/*

%files cgi
%defattr(-,root,root)
/home/httpd/cgi-bin/*

%files daemon
%defattr(-,root,root)
%config /etc/rc.d/init.d/vmailmgrd
%config /etc/rc.d/rc?.d/*vmailmgrd
/usr/sbin/vmailmgrd
%dir /var/service/vmailmgrd
%dir /var/service/vmailmgrd/log
/var/service/vmailmgrd/log/run
/var/service/vmailmgrd/run
%attr(0700,root,root) /var/log/vmailmgrd

%files python
%defattr(-,root,root)
/usr/lib/python1.5/*