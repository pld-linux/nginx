# TODO
# - /etc/sysconfig/nginx file
# - missing perl build/install requires
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
%bcond_without	select		# select
%bcond_without	http2		# HTTP/2 module
%bcond_without	status		# status module
%bcond_without	ssl		# ssl support
%bcond_without	threads		# thread pool support
%bcond_with	http_browser	# header "User-agent" parser
%bcond_with	rtmp		# rtmp support
%bcond_with	debug		# enable debug logging: http://nginx.org/en/docs/debugging_log.html
%bcond_without	auth_request	# auth_request module
%bcond_with	modsecurity	# modsecurity module

%ifarch x32
%undefine	with_rtsig
%endif

%define		ssl_version	1.0.2
%define		rtmp_version	1.1.7
%define		modsecurity_version	2.9.1
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
# nginx lines:
# - stable: production quality with stable API
# - mainline: production quality but API can change
Name:		nginx
Version:	1.11.3
Release:	1
License:	BSD-like
Group:		Networking/Daemons/HTTP
Source0:	http://nginx.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	18275c1daa39c5fac12e56c34907d45b
Source1:	http://nginx.net/favicon.ico
# Source1-md5:	2aaf2115c752cbdbfb8a2f0b3c3189ab
Source2:	proxy.conf
Source3:	%{name}.logrotate
Source4:	%{name}.mime
Source6:	%{name}-light.monitrc
Source7:	%{name}.init
Source8:	%{name}-mail.conf
Source9:	%{name}-mail.monitrc
Source12:	%{name}-perl.monitrc
Source14:	%{name}.conf
Source15:	%{name}-standard.monitrc
Source17:	%{name}-mime.types.sh
Source18:	%{name}-standard.service
Source19:	%{name}-light.service
Source20:	%{name}-perl.service
Source21:	%{name}-mail.service
Source22:	http://www.modsecurity.org/tarball/%{modsecurity_version}/modsecurity-%{modsecurity_version}.tar.gz
# Source22-md5:	0fa92b852abc857a20b9e24f83f814cf
Source101:	https://github.com/arut/nginx-rtmp-module/archive/v%{rtmp_version}/nginx-rtmp-module-%{rtmp_version}.tar.gz
# Source101-md5:	8006de2560db3e55bb15d110220076ac
Patch0:		%{name}-no-Werror.patch
Patch1:		%{name}-modsecurity-xheaders.patch
URL:		http://nginx.net/
%{?with_modsecurity:BuildRequires: lua-devel}
BuildRequires:	mailcap
%{?with_ssl:BuildRequires: openssl-devel >= %{ssl_version}}
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
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva na
potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle w
fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
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
Requires:	rc-scripts >= 0.2.0
Requires:	systemd-units >= 38
Suggests:	vim-syntax-nginx
Provides:	group(http)
Provides:	group(nginx)
Provides:	user(nginx)
Provides:	webserver
Provides:	webserver(access)
Provides:	webserver(alias)
Provides:	webserver(auth)
Provides:	webserver(expires)
Provides:	webserver(headers)
Provides:	webserver(indexfile)
Provides:	webserver(log)
Provides:	webserver(mime)
Provides:	webserver(reqtimeout)
Provides:	webserver(rewrite)
Provides:	webserver(setenv)
Obsoletes:	nginx < 1.4.1-4.1
Conflicts:	logrotate < 3.8.0

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
%{?with_ssl:Requires: openssl >= %{ssl_version}}
Provides:	nginx-daemon
Provides:	webserver
Provides:	webserver(access)
Provides:	webserver(alias)
Provides:	webserver(auth)
Provides:	webserver(expires)
Provides:	webserver(headers)
Provides:	webserver(indexfile)
Provides:	webserver(log)
Provides:	webserver(mime)
Provides:	webserver(reqtimeout)
Provides:	webserver(rewrite)
Provides:	webserver(setenv)

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
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva na
potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle w
fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
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
%{?with_ssl:Requires: openssl >= %{ssl_version}}
Provides:	nginx-daemon
Provides:	webserver
Provides:	webserver(access)
Provides:	webserver(alias)
Provides:	webserver(auth)
Provides:	webserver(expires)
Provides:	webserver(headers)
Provides:	webserver(indexfile)
Provides:	webserver(log)
Provides:	webserver(mime)
Provides:	webserver(reqtimeout)
Provides:	webserver(rewrite)
Provides:	webserver(setenv)

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
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva na
potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle w
fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
prostej konfiguracji oraz małej "zasobożerności".

nginx z obsługą Perla. Bez wsparcia dla modułów poczty.

%package mail
Summary:	High perfomance IMAP, POP3, SMTP proxy server
Summary(pl.UTF-8):	IMAP, POP3, SMTP proxy o wysokiej wydajności
Group:		Networking/Daemons/HTTP
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-common = %{version}-%{release}
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
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva na
potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle w
fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
prostej konfiguracji oraz małej "zasobożerności".

nginx ze wsparciem tylko dla modułów poczty.

%package standard
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
Group:		Networking/Daemons/HTTP
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-common = %{version}-%{release}
%{?with_ssl:Requires: openssl >= %{ssl_version}}
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
a także IMAP/POP3 proxy. nginx został napisany przez Igora Sysoeva na
potrzeby serwisu Rambler.ru. Jest to drugi pod względem ilości
odwiedzin serwis w Rosji i działa od ponad dwóch i pół roku. Igor
opublikował źródła na licencji BSD. Mimo, że projekt jest ciągle w
fazie beta, już zasłynął dzięki stabilności, bogactwu dodatków,
prostej konfiguracji oraz małej "zasobożerności". ginx ("engine x")
jest wysokowydajnym serwerem HTTP, odwrotnym proxy a także IMAP/POP3
proxy. nginx został napisany przez Igora Sysoeva na potrzeby serwisu
Rambler.ru. Jest to drugi pod względem ilości odwiedzin serwis w Rosji
i działa od ponad dwóch i pół roku. Igor opublikował źródła na
licencji BSD. Mimo, że projekt jest ciągle w fazie beta, już zasłynął
dzięki stabilności, bogactwu dodatków, prostej konfiguracji oraz małej
"zasobożerności".

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
%setup -q %{?with_rtmp:-a101} %{?with_modsecurity:-a22}
%patch0 -p0
%{?with_modsecurity:%patch1 -p0}

%if %{with rtmp}
mv nginx-rtmp-module-%{rtmp_version} nginx-rtmp-module
%endif

# build mime.types.conf
#sh %{SOURCE17} /etc/mime.types

%build
# NB: not autoconf generated configure
cp -f configure auto/

install -d bin

# build with default options
build() {
	local type=$1; shift
./configure \
	--prefix=%{_prefix} \
	--sbin-path=%{_sbindir}/%{name}-$type \
	--conf-path=%{_sysconfdir}/%{name}-$type.conf \
	--error-log-path=%{_localstatedir}/log/%{name}/%{name}-${type}_error.log \
	--http-log-path=%{_localstatedir}/log/%{name}/%{name}-${type}_access.log \
	--pid-path=%{_localstatedir}/run/%{name}-$type.pid \
	--lock-path=%{_localstatedir}/lock/subsys/%{name}-$type \
	--http-client-body-temp-path=%{_localstatedir}/cache/%{name}-$type/client_body_temp \
	--http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}-$type/fastcgi_temp \
	--http-proxy-temp-path=%{_localstatedir}/cache/%{name}-$type/proxy_temp \
	--user=nginx \
	--group=nginx \
	%{?with_ipv6:--with-ipv6} \
	%{?with_select:--with-select_module} \
	%{?with_poll:--with-poll_module} \
	%{?with_rtsig:--with-rtsig_module} \
	--with-cc="%{__cc}" \
	--with-cc-opt="%{rpmcflags}" \
	--with-ld-opt="%{rpmldflags}" \
	%{?with_debug:--with-debug} \
	"$@"
%{__make}
}

%if %{with modsecurity}
cd modsecurity-%{modsecurity_version}
./autogen.sh
%configure \
	--enable-standalone-module \
	--disable-mlogc \
	--enable-alp2 \
	--with-lua=/usr
%{__make}
cd ..
%endif

%if %{with perl}
build perl \
	--with-http_perl_module \
	%{?with_addition:--with-http_addition_module} \
	%{?with_dav:--with-http_dav_module} \
	%{?with_flv:--with-http_flv_module} \
	%{?with_sub:--with-http_sub_module} \
	%{?with_realip:--with-http_realip_module} \
	%{?with_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	%{!?with_http_browser:--without-http_browser_module} \
	%{?with_rtmp:--add-module=./nginx-rtmp-module} \
	%{?with_auth_request:--with-http_auth_request_module} \
	%{?with_threads:--with-threads} \
	%{?with_http2:--with-http_v2_module} \
	--with-http_secure_link_module \
	%{nil}

mv -f objs/nginx bin/nginx-perl
mv -f objs/src/http/modules/perl/blib/arch/auto/nginx/nginx.so bin/nginx.so
mv -f objs/src/http/modules/perl/nginx.pm bin/nginx.pm
%endif

%if %{with mail}
build mail \
	--without-http \
	--with-imap \
	--with-mail \
	--with-mail_ssl_module \
	%{nil}

mv -f objs/nginx bin/nginx-mail
%endif

%if %{with light}
build light \
	%{?with_realip:--with-http_realip_module} \
	%{?with_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	%{?with_rtmp:--add-module=./nginx-rtmp-module} \
	%{?with_auth_request:--with-http_auth_request_module} \
	%{?with_threads:--with-threads} \
	%{?with_http2:--with-http_v2_module} \
	%{?with_modsecurity:--add-module=modsecurity-%{modsecurity_version}/nginx/modsecurity} \
	--without-http_browser_module \
	--with-http_secure_link_module \
	%{nil}

mv -f objs/nginx bin/nginx-light
%endif

build standard \
	%{?with_addition:--with-http_addition_module} \
	%{?with_dav:--with-http_dav_module} \
	%{?with_flv:--with-http_flv_module} \
	%{?with_sub:--with-http_sub_module} \
	%{?with_realip:--with-http_realip_module} \
	%{?with_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	%{!?with_http_browser:--without-http_browser_module} \
	%{?with_rtmp:--add-module=./nginx-rtmp-module} \
	%{?with_auth_request:--with-http_auth_request_module} \
	%{?with_threads:--with-threads} \
	%{?with_http2:--with-http_v2_module} \
	%{?with_modsecurity:--add-module=modsecurity-%{modsecurity_version}/nginx/modsecurity} \
	--with-http_secure_link_module \
	%{nil}

mv -f objs/nginx bin/nginx-standard

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

cp -p conf/*_params $RPM_BUILD_ROOT%{_sysconfdir}
cp -p conf/koi-utf $RPM_BUILD_ROOT%{_sysconfdir}/koi-utf
cp -p conf/koi-win $RPM_BUILD_ROOT%{_sysconfdir}/koi-win
cp -p conf/win-utf $RPM_BUILD_ROOT%{_sysconfdir}/win-utf
cp -p html/index.html $RPM_BUILD_ROOT%{_nginxdir}/html
cp -p html/50x.html $RPM_BUILD_ROOT%{_nginxdir}/errors
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_nginxdir}/html/favicon.ico
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/proxy.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/mime.types

install_build() {
	local type=$1
	%{__sed} -e "s/@type@/${type}/g" %{_sourcedir}/%{name}.conf \
		> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-$type.conf

	install -p %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-$type
	%{__sed} -i -e "s/@type@/${type}/g" $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-$type

	cp -p %{_sourcedir}/%{name}-$type.service $RPM_BUILD_ROOT%{systemdunitdir}
	cp -p %{_sourcedir}/%{name}-$type.monitrc $RPM_BUILD_ROOT/etc/monit
	install -p bin/%{name}-$type $RPM_BUILD_ROOT%{_sbindir}
}

install_build standard
ln -sf %{systemdunitdir}/%{name}-standard.service $RPM_BUILD_ROOT/etc/systemd/system/nginx.service

%if %{with light}
install_build light
%endif

%if %{with perl}
install -d $RPM_BUILD_ROOT{%{perl_vendorarch},%{perl_vendorarch}/auto/%{name}}
install_build perl
cp -p bin/nginx.pm $RPM_BUILD_ROOT%{perl_vendorarch}/%{name}.pm
install -p bin/nginx.so $RPM_BUILD_ROOT%{perl_vendorarch}/auto/%{name}/%{name}.so
install -p bin/nginx-perl $RPM_BUILD_ROOT%{_sbindir}
%endif

%if %{with mail}
install_build mail
%endif

# only touch these for ghost packaging
touch $RPM_BUILD_ROOT%{_sysconfdir}/{fastcgi,scgi,uwsgi}.params

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
%service %{name}-standard force-reload
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
%service %{name}-light force-reload
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
%service %{name}-perl force-reload
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
%service %{name}-mail force-reload
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

%triggerpostun common -- %{name}-common < 1.8.0-2
# skip *this* trigger on downgrade
[ $1 -le 1 ] && exit 0
ln -sf fastcgi_params %{_sysconfdir}/fastcgi.params
ln -sf scgi_params %{_sysconfdir}/scgi.params
ln -sf uwsgi_params %{_sysconfdir}/uwsgi.params
exit 0

%files common
%defattr(644,root,root,755)
%doc CHANGES LICENSE README html/index.html conf/nginx.conf
%doc %lang(ru) CHANGES.ru
%dir %attr(750,root,nginx) %{_sysconfdir}
%dir %{_nginxdir}
%dir %{_nginxdir}/cgi-bin
%dir %{_nginxdir}/html
%dir %{_nginxdir}/errors
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
# XXX: duplicates, don't use such glob here
#%attr(640,root,root) %{_sysconfdir}/*[_-]*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/proxy.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fastcgi_params
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scgi_params
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/uwsgi_params
%ghost %{_sysconfdir}/fastcgi.params
%ghost %{_sysconfdir}/scgi.params
%ghost %{_sysconfdir}/uwsgi.params
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
