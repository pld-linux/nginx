# TODO
# - /etc/sysconfig/nginx file
# - missing perl build/install requires
# - mod_spdy build http://mailman.nginx.org/pipermail/nginx-devel/2012-June/002343.html patch from http://nginx.org/patches/attic/spdy/
#   http://nginx.org/en/docs/http/ngx_http_spdy_module.html
#
# Conditional build for nginx:
%bcond_without	light		# don't build light version
%bcond_without	mail		# don't build imap/mail proxy
%bcond_without	perl		# don't build with perl module
%bcond_without	addition	# adds module
%bcond_without	dav		# WebDAV
%bcond_without	flv		# FLV stream
%bcond_without	ipv6		# build without ipv6 support
%bcond_without	sub		# ngx_http_sub_module
%bcond_without	poll		# poll
%bcond_without	realip		# real ip (behind proxy)
%bcond_without	rtsig		# rtsig
%bcond_without	select		# select
%bcond_without	status		# stats module
%bcond_without	ssl		# ssl support
%bcond_with	http_browser	# header "User-agent" parser
%bcond_without	rtmp		# rtmp support
%bcond_without	auth_request	# auth_request module

%define		rtmp_version	1.1.3
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
# nginx lines:
# - stable: production quality with stable API
# - mainline: production quality but API can change
Name:		nginx
Version:	1.7.3
Release:	1
License:	BSD-like
Group:		Networking/Daemons/HTTP
Source0:	http://nginx.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	2b7f37f86e0af9bbb109c4dc225c6247
Source1:	http://nginx.net/favicon.ico
# Source1-md5:	2aaf2115c752cbdbfb8a2f0b3c3189ab
Source2:	proxy.conf
Source3:	%{name}.logrotate
Source4:	%{name}.mime
Source5:	%{name}-light.conf
Source6:	%{name}-light.monitrc
Source7:	%{name}-light.init
Source8:	%{name}-mail.conf
Source9:	%{name}-mail.monitrc
Source10:	%{name}-mail.init
Source11:	%{name}-perl.conf
Source12:	%{name}-perl.monitrc
Source13:	%{name}-perl.init
Source14:	%{name}-standard.conf
Source15:	%{name}-standard.monitrc
Source16:	%{name}-standard.init
Source17:	%{name}-mime.types.sh
Source18:	%{name}-standard.service
Source19:	%{name}-light.service
Source20:	%{name}-perl.service
Source21:	%{name}-mail.service
Source101:	https://github.com/arut/nginx-rtmp-module/archive/v%{rtmp_version}.tar.gz
# Source101-md5:	66ee2b74799e03a25a9e3aaadd874436
Patch0:		nginx-no-Werror.patch
URL:		http://nginx.net/
BuildRequires:	mailcap
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
%{?with_perl:BuildRequires: perl-CGI}
%{?with_perl:BuildRequires: perl-devel}
%{?with_perl:BuildRequires: python}
%{?with_perl:BuildRequires: rpm-perlprov}
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_nginxdir	/home/services/%{name}

%description
nginx ("engine x") is a high-performance HTTP server and reverse
proxy, as well as an IMAP/POP3 proxy server. nginx was written by Igor
Sysoev for Rambler.ru, Russia's second-most visited website, where it
has been running in production for over two and a half years. Igor has
released the source code under a BSD-like license. Although still in
beta, nginx is known for its stability, rich feature set, simple
configuration, and low resource consumption.

%description -l pl.UTF-8
nginx ("engine x") jest wysokowydajnym serwerem HTTP, odwrotnym proxy
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva
na potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle
w fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
prostej konfiguracji oraz małej "zasobożerności".

%package common
Summary:	nginx - common files
Summary(pl.UTF-8):	nginx - pliki wspólne
Group:		Networking/Daemons/HTTP
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	openssl
Requires:	pcre
Requires:	rc-scripts >= 0.2.0
Requires:	systemd-units >= 38
Requires:	zlib
Provides:	group(http)
Provides:	group(nginx)
Provides:	user(nginx)
Provides:	webserver
Conflicts:	logrotate < 3.8.0
Obsoletes:	%{name} < 1.4.1-4.1

%description common
Common files for the nginx daemon.

%description common -l pl.UTF-8
Niezbędne pliki dla nginx.

%package light
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
Group:		Networking/Daemons/HTTP
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-common = %{version}-%{release}
Requires:	openssl
Requires:	pcre
Requires:	zlib
Provides:	nginx-daemon
Provides:	webserver

%description light
nginx ("engine x") is a high-performance HTTP server and reverse
proxy, as well as an IMAP/POP3 proxy server. nginx was written by Igor
Sysoev for Rambler.ru, Russia's second-most visited website, where it
has been running in production for over two and a half years. Igor has
released the source code under a BSD-like license. Although still in
beta, nginx is known for its stability, rich feature set, simple
configuration, and low resource consumption.

The smallest, but also the fastest nginx edition. No additional
modules, no Perl, no DAV, no FLV, no IMAP, POP3, SMTP proxy.

%description light -l pl.UTF-8
nginx ("engine x") jest wysokowydajnym serwerem HTTP, odwrotnym proxy
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva
na potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle
w fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
prostej konfiguracji oraz małej "zasobożerności".

Najmniejsza i najszybsza wersja nginx. Bez wsparcia dla Perla, DAV,
FLV oraz IMAP, POP3, SMTP proxy.

%package perl
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
Group:		Networking/Daemons/HTTP
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-common = %{version}-%{release}
Requires:	openssl
Provides:	nginx-daemon
Provides:	webserver

%description perl
nginx ("engine x") is a high-performance HTTP server and reverse
proxy, as well as an IMAP/POP3 proxy server. nginx was written by Igor
Sysoev for Rambler.ru, Russia's second-most visited website, where it
has been running in production for over two and a half years. Igor has
released the source code under a BSD-like license. Although still in
beta, nginx is known for its stability, rich feature set, simple
configuration, and low resource consumption.

nginx with Perl support. Mail modules not included.

%description perl -l pl.UTF-8
nginx ("engine x") jest wysokowydajnym serwerem HTTP, odwrotnym proxy
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva
na potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle
w fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
prostej konfiguracji oraz małej "zasobożerności".

nginx z obsługą Perla. Bez wsparcia dla modułów poczty.

%package mail
Summary:	High perfomance IMAP, POP3, SMTP proxy server
Summary(pl.UTF-8):	IMAP, POP3, SMTP proxy o wysokiej wydajności
Group:		Networking/Daemons/HTTP
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-common = %{version}-%{release}
Requires:	openssl
Requires:	pcre
Requires:	zlib
Provides:	nginx-daemon

%description mail
nginx ("engine x") is a high-performance HTTP server and reverse
proxy, as well as an IMAP/POP3 proxy server. nginx was written by Igor
Sysoev for Rambler.ru, Russia's second-most visited website, where it
has been running in production for over two and a half years. Igor has
released the source code under a BSD-like license. Although still in
beta, nginx is known for its stability, rich feature set, simple
configuration, and low resource consumption.

nginx with mail support. Only mail modules included.

%description mail -l pl.UTF-8
nginx ("engine x") jest wysokowydajnym serwerem HTTP, odwrotnym proxy
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva
na potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle
w fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
prostej konfiguracji oraz małej "zasobożerności".

nginx ze wsparciem tylko dla modułów poczty.

%package standard
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
Group:		Networking/Daemons/HTTP
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-common = %{version}-%{release}
Requires:	openssl
Provides:	nginx
Provides:	nginx-daemon
Conflicts:	logrotate < 3.7-4

%description standard
nginx ("engine x") is a high-performance HTTP server and reverse
proxy, as well as an IMAP/POP3 proxy server. nginx was written by Igor
Sysoev for Rambler.ru, Russia's second-most visited website, where it
has been running in production for over two and a half years. Igor has
released the source code under a BSD-like license. Although still in
beta, nginx is known for its stability, rich feature set, simple
configuration, and low resource consumption.

This is standard nginx version, without Perl support and IMAP, POP3,
SMTP proxy. 

%description standard -l pl.UTF-8
nginx ("engine x") jest wysokowydajnym serwerem HTTP, odwrotnym proxy
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva
na potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle
w fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
prostej konfiguracji oraz małej "zasobożerności".
ginx ("engine x") jest wysokowydajnym serwerem HTTP, odwrotnym proxy
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva
na potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle
w fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
prostej konfiguracji oraz małej "zasobożerności".

To jest standardowa wersja nginx, bez obsługi Perla oraz proxy dla
IMAP, POP3, SMTP.

%package -n monit-rc-nginx
Summary:	nginx support for monit
Summary(pl.UTF-8):	Wsparcie nginx dla monit
Group:		Applications/System
URL:		http://nginx.eu/
Requires:	%{name}-common = %{version}-%{release}
Requires:	monit

%description -n monit-rc-nginx
monitrc file for monitoring nginx webserver.

%description -n monit-rc-nginx -l pl.UTF-8
Plik monitrc do monitorowania serwera WWW nginx.

%prep
%setup -q %{?with_rtmp:-a101}
%patch0 -p0

%if %{with rtmp}
mv nginx-rtmp-module-%{rtmp_version} nginx-rtmp-module
%endif

# build mime.types.conf
#sh %{SOURCE17} /etc/mime.types

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
	%{?with_ipv6:--with-ipv6} \
	%{?with_sub:--with-http_sub_module} \
	%{?with_poll:--with-poll_module} \
	%{?with_realip:--with-http_realip_module} \
	%{?with_rtsig:--with-rtsig_module} \
	%{?with_select:--with-select_module} \
	%{?with_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	%{!?with_http_browser:--without-http_browser_module} \
	%{?with_rtmp:--add-module=./nginx-rtmp-module} \
	%{?with_auth_request:--with-http_auth_request_module} \
	--with-http_secure_link_module \
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
	%{?with_ipv6:--with-ipv6} \
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
	%{?with_ipv6:--with-ipv6} \
	%{?with_poll:--with-poll_module} \
	%{?with_realip:--with-http_realip_module} \
	%{?with_rtsig:--with-rtsig_module} \
	%{?with_select:--with-select_module} \
	%{?with_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	%{?with_rtmp:--add-module=./nginx-rtmp-module} \
	%{?with_auth_request:--with-http_auth_request_module} \
	--without-http_browser_module \
	--without-mail_pop3_module \
	--without-mail_imap_module \
	--without-mail_smtp_module \
	--with-http_secure_link_module \
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

./configure \
	--prefix=%{_prefix} \
	--sbin-path=%{_sbindir}/%{name}-standard \
	--conf-path=%{_sysconfdir}/%{name}-standard.conf \
	--error-log-path=%{_localstatedir}/log/%{name}/%{name}-standard_error.log \
	--http-log-path=%{_localstatedir}/log/%{name}/%{name}-standard_access.log \
	--pid-path=%{_localstatedir}/run/%{name}-standard.pid \
	--lock-path=%{_localstatedir}/lock/subsys/%{name}-standard \
	--user=nginx \
	--group=nginx \
	%{?with_addition:--with-http_addition_module} \
	%{?with_dav:--with-http_dav_module} \
	%{?with_flv:--with-http_flv_module} \
	%{?with_ipv6:--with-ipv6} \
	%{?with_sub:--with-http_sub_module} \
	%{?with_poll:--with-poll_module} \
	%{?with_realip:--with-http_realip_module} \
	%{?with_rtsig:--with-rtsig_module} \
	%{?with_select:--with-select_module} \
	%{?with_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	%{!?with_http_browser:--without-http_browser_module} \
	%{?with_rtmp:--add-module=./nginx-rtmp-module} \
	%{?with_auth_request:--with-http_auth_request_module} \
	--with-http_secure_link_module \
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
	$RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/{vhosts,webapps}.d} \
	$RPM_BUILD_ROOT/etc/{logrotate.d,monit} \
	$RPM_BUILD_ROOT{%{systemdunitdir},/etc/systemd/system}

install conf/fastcgi_params $RPM_BUILD_ROOT%{_sysconfdir}/fastcgi.params
install conf/scgi_params $RPM_BUILD_ROOT%{_sysconfdir}/scgi.params
install conf/uwsgi_params $RPM_BUILD_ROOT%{_sysconfdir}/uwsgi.params
install conf/koi-utf $RPM_BUILD_ROOT%{_sysconfdir}/koi-utf
install conf/koi-win $RPM_BUILD_ROOT%{_sysconfdir}/koi-win
install conf/win-utf $RPM_BUILD_ROOT%{_sysconfdir}/win-utf
install html/index.html $RPM_BUILD_ROOT%{_nginxdir}/html
install html/50x.html $RPM_BUILD_ROOT%{_nginxdir}/errors
install %{SOURCE1} $RPM_BUILD_ROOT%{_nginxdir}/html/favicon.ico
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/proxy.conf
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/mime.types
install %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-standard.conf
install %{SOURCE15} $RPM_BUILD_ROOT/etc/monit/%{name}-standard.monitrc
install %{SOURCE16} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-standard
install %{SOURCE18} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}-standard.service
install objs/%{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}-standard
ln -sf %{systemdunitdir}/%{name}-standard.service $RPM_BUILD_ROOT/etc/systemd/system/nginx.service

%if %{with light}
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-light.conf
install %{SOURCE6} $RPM_BUILD_ROOT/etc/monit/%{name}-light.monitrc
install %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-light
install %{SOURCE19} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}-light.service
install contrib/nginx-light $RPM_BUILD_ROOT%{_sbindir}/%{name}-light
%endif

%if %{with mail}
install %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-mail.conf
install %{SOURCE9} $RPM_BUILD_ROOT/etc/monit/%{name}-mail.monitrc
install %{SOURCE10} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-mail
install %{SOURCE21} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}-mail.service
install contrib/nginx-mail $RPM_BUILD_ROOT%{_sbindir}/%{name}-mail
%endif

%if %{with perl}
install -d $RPM_BUILD_ROOT{%{perl_vendorarch},%{perl_vendorarch}/auto/%{name}}
install %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-perl.conf
install %{SOURCE12} $RPM_BUILD_ROOT/etc/monit/%{name}-perl.monitrc
install %{SOURCE13} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-perl
install %{SOURCE20} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}-perl.service
install contrib/nginx.pm $RPM_BUILD_ROOT%{perl_vendorarch}/%{name}.pm
install contrib/nginx.so $RPM_BUILD_ROOT%{perl_vendorarch}/auto/%{name}/%{name}.so
install contrib/nginx.bs $RPM_BUILD_ROOT%{perl_vendorarch}/auto/%{name}/%{name}.bs
install contrib/nginx-perl $RPM_BUILD_ROOT%{_sbindir}/%{name}-perl
%endif

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.default
rm -rf $RPM_BUILD_ROOT%{_prefix}/html

%clean
rm -rf $RPM_BUILD_ROOT

%pre common
%groupadd -r -g 213 %{name}
%groupadd -g 51 http
%useradd -r -u 213 -d /usr/share/empty -s /bin/false -c "Nginx HTTP User" -g %{name} %{name}
%addusertogroup %{name} http

%post standard
for a in access.log error.log; do
	if [ ! -f /var/log/%{name}/nginx-standard_$a ]; then
		umask 022
		touch /var/log/%{name}/nginx-standard_$a
		chown nginx:nginx /var/log/%{name}/nginx-standard_$a
		chmod 644 /var/log/%{name}/nginx-standard_$a
	fi
done
/sbin/chkconfig --add %{name}-standard
%systemd_post %{name}-standard.service
%service %{name}-standard restart
echo 'NOTE: this nginx daemon is using "/etc/nginx/nginx-standard.conf" as config.'
if ! [ -L /etc/systemd/system/nginx.service ] ; then
	ln -s %{systemdunitdir}/%{name}-standard.service /etc/systemd/system/nginx.service || :
fi

%post light
for a in access.log error.log; do
	if [ ! -f /var/log/%{name}/nginx-light_$a ]; then
		umask 022
		touch /var/log/%{name}/nginx-light_$a
		chown nginx:nginx /var/log/%{name}/nginx-light_$a
		chmod 644 /var/log/%{name}/nginx-light_$a
	fi
done
/sbin/chkconfig --add %{name}-light
%systemd_post %{name}-light.service
%service %{name}-light restart
echo 'NOTE: this nginx daemon is using "/etc/nginx/nginx-light.conf" as config'

%post perl
for a in access.log error.log; do
	if [ ! -f /var/log/%{name}/nginx-perl_$a ]; then
		umask 022
		touch /var/log/%{name}/nginx-perl_$a
		chown nginx:nginx /var/log/%{name}/nginx-perl_$a
		chmod 644 /var/log/%{name}/nginx-perl_$a
	fi
done
/sbin/chkconfig --add %{name}-perl
%systemd_post %{name}-perl.service
%service %{name}-perl restart
echo 'NOTE: this nginx daemon is using "/etc/nginx/nginx-perl.conf" as config'

%post mail
for a in access.log error.log; do
	if [ ! -f /var/log/%{name}/nginx-mail_$a ]; then
		umask 022
		touch /var/log/%{name}/nginx-mail_$a
		chown nginx:nginx /var/log/%{name}/nginx-mail_$a
		chmod 644 /var/log/%{name}/nginx-mail_$a
	fi
done
/sbin/chkconfig --add %{name}-mail
%systemd_post %{name}-mail.service
%service %{name}-mail restart
echo 'NOTE: this nginx daemon is using "/etc/nginx/nginx-mail.conf" as config'

%preun standard
if [ "$1" = "0" ];then
	%service %{name}-standard stop
	/sbin/chkconfig --del %{name}-standard
fi
%systemd_preun %{name}-standard.service

%preun light
if [ "$1" = "0" ]; then
	%service %{name}-light stop
	/sbin/chkconfig --del %{name}-light
fi
%systemd_preun %{name}-light.service

%preun perl
if [ "$1" = "0" ]; then
	%service %{name}-perl stop
	/sbin/chkconfig --del %{name}-perl
fi
%systemd_preun %{name}-perl.service

%preun mail
if [ "$1" = "0" ]; then
	%service %{name}-mail stop
	/sbin/chkconfig --del %{name}-mail
fi
%systemd_preun %{name}-mail.service

%postun common
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%postun standard
%systemd_reload

%postun light
%systemd_reload

%postun perl
%systemd_reload

%postun mail
%systemd_reload

%triggerpostun -- %{name}-standard < 1.4.1-4
%systemd_trigger %{name}-standard.service

%triggerpostun -- %{name}-light < 1.4.1-4
%systemd_trigger %{name}-light.service

%triggerpostun -- %{name}-perl < 1.4.1-4
%systemd_trigger %{name}-perl.service

%triggerpostun -- %{name}-mail < 1.4.1-4
%systemd_trigger %{name}-mail.service

%files common
%defattr(644,root,root,755)
%doc CHANGES LICENSE README html/index.html conf/nginx.conf
%doc %lang(ru) CHANGES.ru
%dir %attr(754,root,root) %{_sysconfdir}
%dir %{_nginxdir}
%dir %{_nginxdir}/cgi-bin
%dir %{_nginxdir}/html
%dir %{_nginxdir}/errors
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
# XXX: duplicates, don't use such glob here
#%attr(640,root,root) %{_sysconfdir}/*[_-]*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/proxy.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fastcgi.params
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scgi.params
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/uwsgi.params
%attr(640,root,root) %{_sysconfdir}/mime.types
%attr(640,root,root) %{_sysconfdir}/koi-utf
%attr(640,root,root) %{_sysconfdir}/koi-win
%attr(640,root,root) %{_sysconfdir}/win-utf
%dir %{_sysconfdir}/webapps.d
%dir %{_sysconfdir}/vhosts.d
%attr(750,nginx,logs) %dir /var/log/archive/%{name}
%attr(750,nginx,logs) /var/log/%{name}
%config(noreplace,missingok) %verify(not md5 mtime size) %{_nginxdir}/html/*
%config(noreplace,missingok) %verify(not md5 mtime size) %{_nginxdir}/errors/*
%ghost /etc/systemd/system/nginx.service

%files standard
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}-standard
%attr(770,root,%{name}) /var/cache/%{name}-standard
%attr(754,root,root) /etc/rc.d/init.d/%{name}-standard
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}-standard.conf
%{systemdunitdir}/%{name}-standard.service

%if %{with mail}
%files mail
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}-mail
%attr(770,root,%{name}) /var/cache/%{name}-mail
%attr(754,root,root) /etc/rc.d/init.d/%{name}-mail
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}-mail.conf
%{systemdunitdir}/%{name}-mail.service
%endif

%if %{with light}
%files light
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}-light
%attr(770,root,%{name}) /var/cache/%{name}-light
%attr(754,root,root) /etc/rc.d/init.d/%{name}-light
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}-light.conf
%{systemdunitdir}/%{name}-light.service
%endif

%if %{with perl}
%files perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}-perl
%attr(754,root,root) /etc/rc.d/init.d/%{name}-perl
%attr(770,root,%{name}) /var/cache/%{name}-perl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}-perl.conf
%dir %{perl_vendorarch}/auto/%{name}
%attr(755,root,root) %{perl_vendorarch}/auto/%{name}/%{name}.so
%{perl_vendorarch}/auto/%{name}/%{name}.bs
%{perl_vendorarch}/%{name}.pm
%{systemdunitdir}/%{name}-perl.service
%endif

%files -n monit-rc-nginx
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}-standard.monitrc
%if %{with perl}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}-perl.monitrc
%endif
%if %{with light}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}-light.monitrc
%endif
%if %{with mail}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}-mail.monitrc
%endif
