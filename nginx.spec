# TODO
# - /etc/sysconfig/nginx file
# - missing perl build/install requires
# - prepare pld style like nginx.conf
# - maybe -with-cpu-opt=CPU (pentium, pentiumpro, pentium3, pentium4, athlon, opteron, amd64, sparc32, sparc64, ppc64)
#
# Conditional build for nginx:
%bcond_without	light		# don't build light version
%bcond_without	mail		# don't build imap/mail proxy
%bcond_without	perl		# don't build with perl module
%bcond_without	addition	# adds module
%bcond_without	dav		# WebDAV
%bcond_without	flv		# FLV stream
%bcond_without	sub		# ngx_http_sub_module
%bcond_without	poll		# poll
%bcond_without	realip		# real ip (behind proxy)
%bcond_without	rtsig		# rtsig
%bcond_without	select		# select
%bcond_without	status		# stats module
%bcond_without	ssl		# ssl support
%bcond_with	http_browser	# header "User-agent" parser
#
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
Name:		nginx
Version:	0.5.33
Release:	0.5
License:	BSD-like
Group:		Networking/Daemons
Source0:	http://sysoev.ru/nginx/%{name}-%{version}.tar.gz
# Source0-md5:	a78be74b4fd8e009545ef02488fcac86
Source1:	http://www.nginx.eu/favicon.ico
# Source1-md5:	2aaf2115c752cbdbfb8a2f0b3c3189ab
Source2:	http://www.nginx.eu/download/proxy.conf
# Source2-md5:	f5263ae01c2edb18f46d5d1df2d3a5cd
Source3:	%{name}.logrotate
Source4:	%{name}.mime
Source5:	%{name}-light.conf
Source6:	%{name}-light.monitrc
Source7:	%{name}-mail.conf
Source8:	%{name}-mail.monitrc
Source9:	%{name}-perl.conf
Source10:	%{name}-perl.monitrc
Source11:	%{name}-standard.conf
Source12:	%{name}-standard.monitrc
Patch0:		%{name}-config.patch
URL:		http://nginx.net/
BuildRequires:	mailcap
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
%{?with_perl:BuildRequires: perl-CGI}
%{?with_perl:BuildRequires: perl-devel}
%{?with_perl:BuildRequires: rpm-perlprov}
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	monit
Requires:	openssl
Requires:	pcre
Requires:	rc-scripts >= 0.2.0
Requires:	zlib
Provides:	group(http)
Provides:	group(nginx)
Provides:	user(nginx)
Provides:	webserver
Conflicts:	logrotate < 3.7-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_nginxdir	/home/services/%{name}

%description
Nginx ("engine x") is a high-performance HTTP server and reverse
proxy, as well as an IMAP/POP3 proxy server. Nginx was written by Igor
Sysoev for Rambler.ru, Russia's second-most visited website, where it
has been running in production for over two and a half years. Igor has
released the source code under a BSD-like license. Although still in
beta, Nginx is known for its stability, rich feature set, simple
configuration, and low resource consumption.

Common files for Nginx daemon.

%description -l pl.UTF-8
Nginx ("engine x") jest wysokowydajnym serwerem HTTP, odwrotnym proxy
a także IMAP/POP3 proxy. Nginx został napisany przez Igora Sysoev'a
na potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle
w fazie beta, już zas�yn�� dzieki stabilno�i, bogactwu dodatków,
prostej konfiguracji oraz ma�ej "zasobożerno�i".

Niezb�dne pliki dla Nginx.

%package light
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
License:	BSD-like
Group:		Networking/Daemons
URL:		http://nginx.net/
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	%{name} = %{version}-%{release}
Requires:	openssl
Requires:	pcre
Requires:	zlib
Provides:	group(http)
Provides:	group(nginx)
Provides:	user(nginx)
Provides:	webserver
#Conflicts:	%{name}
#Conflicts:	%{name}-mail
#Conflicts:	%{name}-perl

%description light
The smallest, but also the fastest Nginx edition. No additional
modules, no Perl, no DAV, no FLV, no IMAP, POP3, SMTP proxy.

%description light -l pl.UTF-8
Najmniejsza i najszybsza wersja Nginx. Bez wsparcia dla Perla,
DAV, FLV oraz IMAP, POP3, SMTP proxy.

%package perl
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
License:	BSD-like
Group:		Networking/Daemons
URL:		http://nginx.net/
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	%{name} = %{version}-%{release}
Requires:	openssl
Provides:	group(http)
Provides:	group(nginx)
Provides:	user(nginx)
Provides:	webserver
#Conflicts:	%{name}
#Conflicts:	%{name}-light
#Conflicts:	%{name}-mail

%description perl
Nginx with Perl support. Mail modules not included.

%description perl -l pl.UTF-8
Nignx z obsługą Perla. Bez wsparcia dla modułów poczty.

%package mail
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
License:	BSD-like
Group:		Networking/Daemons
URL:		http://nginx.net/
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	%{name} = %{version}-%{release}
Requires:	openssl
Requires:	pcre
Requires:	zlib
Provides:	group(http)
Provides:	group(nginx)
Provides:	user(nginx)
Provides:	webserver
#Conflicts:	%{name}
#Conflicts:	%{name}-light
#Conflicts:	%{name}-perl

%description mail
Nginx with mail support. Only mail modules included.

%description mail -l pl.UTF-8
Nginx ze wsparciem tylko dla modułów poczty.

%package standard
Summary:	Configuration files and documentation for Nginx
Summary(pl.UTF-8):	Pliki konfiguracyjne i dokumentacja dla Nginx
License:	BSD-like
Group:		Networking/Daemons
URL:		http://nginx.net/
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	%{name} = %{version}-%{release}
Conflicts:	logrotate < 3.7-4

%description standard
Nginx ("engine x") is a high-performance HTTP server and reverse
proxy, as well as an IMAP/POP3 proxy server. Nginx was written by Igor
Sysoev for Rambler.ru, Russia's second-most visited website, where it
has been running in production for over two and a half years. Igor has
released the source code under a BSD-like license. Although still in
beta, Nginx is known for its stability, rich feature set, simple
configuration, and low resource consumption.

This is standard nginx version, without perl support and imap, pop3,
smtp proxy. 

%description standard -l pl.UTF-8
Nginx ("engine x") jest wysokowydajnym serwerem HTTP, odwrotnym proxy
a także IMAP/POP3 proxy. Nginx został napisany przez Igora Sysoev'a
na potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle
w fazie beta, już zas�yn�� dzieki stabilno�i, bogactwu dodatków,
prostej konfiguracji oraz ma�ej "zasobożerno�i".

To jest standardowa wersja nginx, bez obs?ugi perla oraz proxy dla
imap, pop3, smtp.

%prep
%setup -q
%patch0 -p0

%build
# NB: not autoconf generated configure
cp -f configure auto/
#
%if %{with perl}
./configure \
	--prefix=%{_prefix} \
	--sbin-path=%{_sbindir}/%{name}-perl \
	--conf-path=%{_sysconfdir}/%{name}-perl.conf \
	--error-log-path=%{_localstatedir}/log/%{name}/%{name}-perl_error.log \
	--http-log-path=%{_localstatedir}/log/%{name}/%{name}-perl_access.log \
	--pid-path=%{_localstatedir}/run/%{name}-perl.pid \
	--lock-path=%{_localstatedir}/lock/subsys/%{name}-perl \
	--user=nginx \
	--group=nginx \
	--with-http_perl_module \
	--without-mail_pop3_module \
	--without-mail_imap_module \
	--without-mail_smtp_module \
	%{?with_addition:--with-http_addition_module} \
	%{?with_dav:--with-http_dav_module} \
	%{?with_flv:--with-http_flv_module} \
	%{?with_sub:--with-http_sub_module} \
	%{?with_poll:--with-poll_module} \
	%{?with_realip:--with-http_realip_module} \
	%{?with_rtsig:--with-rtsig_module} \
	%{?with_select:--with-select_module} \
	%{?with_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	%{!?with_http_browser:--without-http_browser_module} \
	--http-client-body-temp-path=%{_localstatedir}/cache/%{name}-perl/client_body_temp \
	--http-proxy-temp-path=%{_localstatedir}/cache/%{name}-perl/proxy_temp \
	--http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}-perl/fastcgi_temp \
	--with-cc="%{__cc}" \
	--with-cc-opt="%{rpmcflags}" \
	--with-ld-opt="%{rpmldflags}"
%{__make}
mv -f objs/nginx contrib/nginx-perl
mv -f objs/src/http/modules/perl/blib/arch/auto/nginx/nginx.bs contrib/nginx.bs
mv -f objs/src/http/modules/perl/blib/arch/auto/nginx/nginx.so contrib/nginx.so
mv -f objs/src/http/modules/perl/nginx.pm contrib/nginx.pm
%endif

%if %{with mail}
%{__make} clean
./configure \
	--prefix=%{_prefix} \
	--sbin-path=%{_sbindir}/%{name}-mail \
	--conf-path=%{_sysconfdir}/%{name}-mail.conf \
	--error-log-path=%{_localstatedir}/log/%{name}/%{name}-mail_error.log \
	--http-log-path=%{_localstatedir}/log/%{name}/%{name}-mail_access.log \
	--pid-path=%{_localstatedir}/run/%{name}-mail.pid \
	--lock-path=%{_localstatedir}/lock/subsys/%{name}-mail \
	--user=nginx \
	--group=nginx \
	--with-imap \
	--with-mail \
	--with-mail_ssl_module \
	--without-http \
	%{?with_poll:--with-poll_module} \
	%{?with_rtsig:--with-rtsig_module} \
	%{?with_select:--with-select_module} \
	--http-client-body-temp-path=%{_localstatedir}/cache/%{name}-mail/client_body_temp \
	--http-proxy-temp-path=%{_localstatedir}/cache/%{name}-mail/proxy_temp \
	--http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}-mail/fastcgi_temp \
	--with-cc="%{__cc}" \
	--with-cc-opt="%{rpmcflags}" \
	--with-ld-opt="%{rpmldflags}" \
	%{?debug:--with-debug}
%{__make}
mv -f objs/nginx contrib/nginx-mail
%endif

%if %{with light}
%{__make} clean
./configure \
	--prefix=%{_prefix} \
	--sbin-path=%{_sbindir}/%{name}-light \
	--conf-path=%{_sysconfdir}/%{name}-light.conf \
	--error-log-path=%{_localstatedir}/log/%{name}/%{name}-light_error.log \
	--http-log-path=%{_localstatedir}/log/%{name}/%{name}-light_access.log \
	--pid-path=%{_localstatedir}/run/%{name}-light.pid \
	--lock-path=%{_localstatedir}/lock/subsys/%{name}-light \
	--user=nginx \
	--group=nginx \
	%{?with_poll:--with-poll_module} \
	%{?with_realip:--with-http_realip_module} \
	%{?with_rtsig:--with-rtsig_module} \
	%{?with_select:--with-select_module} \
	%{?with_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	--without-http_browser_module \
	--without-mail_pop3_module \
	--without-mail_imap_module \
	--without-mail_smtp_module \
	--http-client-body-temp-path=%{_localstatedir}/cache/%{name}-light/client_body_temp \
	--http-proxy-temp-path=%{_localstatedir}/cache/%{name}-light/proxy_temp \
	--http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}-light/fastcgi_temp \
	--with-cc="%{__cc}" \
	--with-cc-opt="%{rpmcflags}" \
	--with-ld-opt="%{rpmldflags}" \
	%{?debug:--with-debug}
%{__make}
mv -f objs/nginx contrib/nginx-light
%endif

%{__make} clean
./configure \
	--prefix=%{_prefix} \
	--sbin-path=%{_sbindir}/%{name}-standard \
	--conf-path=%{_sysconfdir}/%{name}.conf \
	--error-log-path=%{_localstatedir}/log/%{name}/%{name}-standard_error.log \
	--http-log-path=%{_localstatedir}/log/%{name}/%{name}-standard_access.log \
	--pid-path=%{_localstatedir}/run/%{name}-standard.pid \
	--lock-path=%{_localstatedir}/lock/subsys/%{name}-standard \
	--user=nginx \
	--group=nginx \
	%{?with_addition:--with-http_addition_module} \
	%{?with_dav:--with-http_dav_module} \
	%{?with_flv:--with-http_flv_module} \
	%{?with_sub:--with-http_sub_module} \
	%{?with_poll:--with-poll_module} \
	%{?with_realip:--with-http_realip_module} \
	%{?with_rtsig:--with-rtsig_module} \
	%{?with_select:--with-select_module} \
	%{?with_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	%{!?with_http_browser:--without-http_browser_module} \
	--http-client-body-temp-path=%{_localstatedir}/cache/%{name}-standard/client_body_temp \
	--http-proxy-temp-path=%{_localstatedir}/cache/%{name}-standard/proxy_temp \
	--http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}-standard/fastcgi_temp \
	--with-cc="%{__cc}" \
	--with-cc-opt="%{rpmcflags}" \
	--with-ld-opt="%{rpmldflags}" \
	%{?debug:--with-debug}
%{__make}


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT%{_nginxdir}/{cgi-bin,html,errors} \
	$RPM_BUILD_ROOT%{_localstatedir}/log/{%{name},archive/%{name}} \
	$RPM_BUILD_ROOT%{_localstatedir}/cache/{%{name}-standard,%{name}-perl,%{name}-mail,%{name}-light} \
	$RPM_BUILD_ROOT%{_localstatedir}/lock/subsys/{%{name}-standard,%{name}-perl,%{name}-mail,%{name}-light} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT/etc/{logrotate.d,monit}

#install conf/* $RPM_BUILD_ROOT%{_sysconfdir}
install html/index.html $RPM_BUILD_ROOT%{_nginxdir}/html
install html/50x.html $RPM_BUILD_ROOT%{_nginxdir}/errors
install %{SOURCE1} $RPM_BUILD_ROOT%{_nginxdir}/html/favicon.ico
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/proxy.conf
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/mime.types
install %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-standard.conf
install %{SOURCE12} $RPM_BUILD_ROOT/etc/monit/%{name}-standard.monitrc
install objs/%{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}-standard
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-standard

%if %{with light}
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-light.conf
install %{SOURCE6} $RPM_BUILD_ROOT/etc/monit/%{name}-light.monitrc
install contrib/nginx-light $RPM_BUILD_ROOT%{_sbindir}/%{name}-light
%endif

%if %{with mail}
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-mail.conf
install %{SOURCE8} $RPM_BUILD_ROOT/etc/monit/%{name}-mail.monitrc
install contrib/nginx-mail $RPM_BUILD_ROOT%{_sbindir}/%{name}-mail
%endif

%if %{with perl}
install -d $RPM_BUILD_ROOT{%{perl_vendorarch},%{perl_vendorarch}/auto/%{name}}
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-perl.conf
install %{SOURCE8} $RPM_BUILD_ROOT/etc/monit/%{name}-perl.monitrc
install contrib/nginx.pm $RPM_BUILD_ROOT%{perl_vendorarch}/%{name}.pm
install contrib/nginx.so $RPM_BUILD_ROOT%{perl_vendorarch}/auto/%{name}/%{name}.so
install contrib/nginx.bs $RPM_BUILD_ROOT%{perl_vendorarch}/auto/%{name}/%{name}.bs
install contrib/nginx-perl $RPM_BUILD_ROOT%{_sbindir}/%{name}-perl
%endif

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.default
rm -rf $RPM_BUILD_ROOT%{_prefix}/html

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -r -g 213 %{name}
%groupadd -g 51 http
%useradd -r -u 213 -d /usr/share/empty -s /bin/false -c "Nginx HTTP User" -g %{name} %{name}
%addusertogroup %{name} http

%post standard
for a in access.log error.log; do
	if [ ! -f /var/log/%{name}/nginx-standard_$a ]; then
		touch /var/log/%{name}/nginx-standard_$a
		chown nginx:nginx /var/log/%{name}/nginx-standard_$a
		chmod 644 /var/log/%{name}/nginx-standard_$a
	fi
done

%post light
for a in access.log error.log; do
	if [ ! -f /var/log/%{name}/nginx-light_$a ]; then
		touch /var/log/%{name}/nginx-light_$a
		chown nginx:nginx /var/log/%{name}/nginx-light_$a
		chmod 644 /var/log/%{name}/nginx-light_$a
	fi
done

%post perl
for a in access.log error.log; do
	if [ ! -f /var/log/%{name}/nginx-perl_$a ]; then
		touch /var/log/%{name}/nginx-perl_$a
		chown nginx:nginx /var/log/%{name}/nginx-perl_$a
		chmod 644 /var/log/%{name}/nginx-perl_$a
	fi
done

%post mail
for a in access.log error.log; do
	if [ ! -f /var/log/%{name}/nginx-mail_$a ]; then
		touch /var/log/%{name}/nginx-mail_$a
		chown nginx:nginx /var/log/%{name}/nginx-mail_$a
		chmod 644 /var/log/%{name}/nginx-mail_$a
	fi
done

%pre standard
/sbin/chkconfig --add %{name}-standard
%service %{name}-standard restart

%pre light
/sbin/chkconfig --add %{name}-light
%service %{name}-light restart

%pre perl
/sbin/chkconfig --add %{name}-perl
%service %{name}-perl restart

%pre mail
/sbin/chkconfig --add %{name}-mail
%service %{name}-mail restart

%preun standard
if [ "$1" = "0" ]; then
	%service -q %{name}-standard stop
	/sbin/chkconfig --del %{name}-standard
fi

%preun light
if [ "$1" = "0" ]; then
	%service -q %{name}-light stop
	/sbin/chkconfig --del %{name}-light
fi

%preun perl
if [ "$1" = "0" ]; then
	%service -q %{name}-perl stop
	/sbin/chkconfig --del %{name}-perl
fi

%preun mail
if [ "$1" = "0" ]; then
	%service -q %{name}-mail stop
	/sbin/chkconfig --del %{name}-mail
fi

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README html/index.html conf/nginx.conf
%doc %lang(ru) CHANGES.ru
%dir %attr(754,root,root) %{_sysconfdir}
%dir %{_nginxdir}
%dir %{_nginxdir}/cgi-bin
%dir %{_nginxdir}/html
%dir %{_nginxdir}/errors
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(640,root,root) %{_sysconfdir}/*[_-]*
%attr(640,root,root) %{_sysconfdir}/proxy.conf
%attr(640,root,root) %{_sysconfdir}/mime.types
%attr(750,root,root) %dir /var/log/archive/%{name}
%attr(750,%{name},logs) /var/log/%{name}
%config(noreplace,missingok) %verify(not md5 mtime size) %{_nginxdir}/html/*
%config(noreplace,missingok) %verify(not md5 mtime size) %{_nginxdir}/errors/*

%files standard
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}-standard
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}-standard.conf
%attr(770,root,%{name}) /var/cache/%{name}-standard
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}-standard.monitrc

%if %{with mail}
%files mail
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}-mail
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}-mail.conf
%attr(770,root,%{name}) /var/cache/%{name}-mail
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}-mail.monitrc
%endif

%if %{with light}
%files light
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}-light
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}-light.conf
%attr(770,root,%{name}) /var/cache/%{name}-light
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}-light.monitrc
%endif

%if %{with perl}
%files perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}-perl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}-perl.conf
%dir %{perl_vendorarch}/auto/%{name}
%attr(755,root,root) %{perl_vendorarch}/auto/%{name}/%{name}.so
%attr(700,root,root) %{perl_vendorarch}/auto/%{name}/%{name}.bs
%attr(700,root,root) %{perl_vendorarch}/%{name}.pm
%attr(770,root,%{name}) /var/cache/%{name}-perl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}-perl.monitrc
%endif
