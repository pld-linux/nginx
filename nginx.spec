# TODO
# - /etc/sysconfig/nginx file
# - missing perl build/install requires
#
# Conditional build for nginx:
%bcond_with	light		# don't build light version
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
Version:	1.11.5
Release:	0.1
License:	BSD-like
Group:		Networking/Daemons/HTTP
Source0:	http://nginx.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	db43f2b19746f6f47401c3afc3924dc6
Source1:	http://nginx.net/favicon.ico
# Source1-md5:	2aaf2115c752cbdbfb8a2f0b3c3189ab
Source2:	proxy.conf
Source3:	%{name}.logrotate
Source4:	%{name}.mime
Source6:	%{name}.monitrc
Source7:	%{name}.init
Source14:	%{name}.conf
Source17:	%{name}-mime.types.sh
Source18:	%{name}.service
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
%{?with_ssl:Requires:	openssl >= %{ssl_version}}
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
Conflicts:	logrotate < 3.8.0
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts >= 0.2.0
Requires:	systemd-units >= 38
Suggests:	vim-syntax-nginx
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

%package mod_http_perl
Summary:	Nginx HTTP Perl module
Group:		Networking/Daemons/HTTP
Requires:	%{name} = %{version}-%{release}

%description mod_http_perl
Nginx HTTP Perl module.

%package mod_mail
Summary:	Nginx mail module
Group:		Networking/Daemons/HTTP
Requires:	%{name} = %{version}-%{release}

%description mod_mail
Nginx mail module.

%package -n monit-rc-nginx
Summary:	nginx support for monit
Summary(pl.UTF-8):	Wsparcie nginx dla monit
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
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
	--modules-path=%{_libdir}/%{name}/modules \
	--sbin-path=%{_sbindir}/%{name} \
	--conf-path=%{_sysconfdir}/%{name}.conf \
	--error-log-path=%{_localstatedir}/log/%{name}/error.log \
	--http-log-path=%{_localstatedir}/log/%{name}/access.log \
	--pid-path=%{_localstatedir}/run/%{name}.pid \
	--lock-path=%{_localstatedir}/lock/subsys/%{name} \
	--http-client-body-temp-path=%{_localstatedir}/cache/%{name}/client_body_temp \
	--http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}/fastcgi_temp \
	--http-proxy-temp-path=%{_localstatedir}/cache/%{name}/proxy_temp \
	--user=nginx \
	--group=nginx \
	%{?with_ipv6:--with-ipv6} \
	%{?with_select:--with-select_module} \
	%{?with_poll:--with-poll_module} \
	%{?with_rtsig:--with-rtsig_module} \
%if %{with perl}
	--with-http_perl_module=dynamic \
%endif
%if %{with mail}
	--with-mail=dynamic \
	--with-mail_ssl_module \
%endif
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

%if %{with perl} && 0
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

%if %{with mail} && 0
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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT%{_nginxdir}/{cgi-bin,html,errors} \
	$RPM_BUILD_ROOT%{_localstatedir}/log/{%{name},archive/%{name}} \
	$RPM_BUILD_ROOT%{_localstatedir}/cache/%{name} \
	$RPM_BUILD_ROOT%{_localstatedir}/lock/subsys/%{name} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/{vhosts,webapps}.d} \
	$RPM_BUILD_ROOT/etc/{logrotate.d,monit} \
	$RPM_BUILD_ROOT{%{systemdunitdir},/etc/systemd/system}

%{__make} install \
	INSTALLDIRS=vendor \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/*.default

cp -p %{_sourcedir}/%{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{_sourcedir}/%{name}.service $RPM_BUILD_ROOT%{systemdunitdir}
cp -p %{_sourcedir}/%{name}.monitrc $RPM_BUILD_ROOT/etc/monit
install -p %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/proxy.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/mime.types
rm -r $RPM_BUILD_ROOT%{_prefix}/html
cp -p html/index.html $RPM_BUILD_ROOT%{_nginxdir}/html
cp -p html/50x.html $RPM_BUILD_ROOT%{_nginxdir}/errors
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_nginxdir}/html/favicon.ico

%if %{with perl}
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/nginx/.packlist
%endif

# only touch these for ghost packaging
touch $RPM_BUILD_ROOT%{_sysconfdir}/{fastcgi,scgi,uwsgi}.params

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -r -g 213 %{name}
%groupadd -g 51 http
%useradd -r -u 213 -d /usr/share/empty -s /bin/false -c "Nginx HTTP User" -g %{name} %{name}
%addusertogroup %{name} http

%post
for a in access.log error.log; do
	if [ ! -f /var/log/%{name}/$a ]; then
		umask 022
		touch /var/log/%{name}/$a
		chown nginx:nginx /var/log/%{name}/$a
		chmod 644 /var/log/%{name}/$a
	fi
done
/sbin/chkconfig --add %{name}
%systemd_post %{name}.service
%service %{name} force-reload

%preun
if [ "$1" = "0" ];then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi
%systemd_reload

%triggerpostun -- %{name} < 1.8.0-2
# skip *this* trigger on downgrade
[ $1 -le 1 ] && exit 0
ln -sf fastcgi_params %{_sysconfdir}/fastcgi.params
ln -sf scgi_params %{_sysconfdir}/scgi.params
ln -sf uwsgi_params %{_sysconfdir}/uwsgi.params
exit 0

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README html/index.html conf/nginx.conf
%doc %lang(ru) CHANGES.ru
%dir %attr(750,root,nginx) %{_sysconfdir}
%dir %{_nginxdir}
%dir %{_nginxdir}/cgi-bin
%dir %{_nginxdir}/html
%dir %{_nginxdir}/errors
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
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

%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}
%attr(770,root,%{name}) /var/cache/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%{systemdunitdir}/%{name}.service

%if %{with mail}
%files mod_mail
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_mail_module.so
%endif

%if %{with perl}
%files mod_http_perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_http_perl_module.so
%dir %{perl_vendorarch}/auto/%{name}
%attr(755,root,root) %{perl_vendorarch}/auto/%{name}/%{name}.so
%{perl_vendorarch}/%{name}.pm
%{_mandir}/man3/nginx.3pm*
%endif

%files -n monit-rc-nginx
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}.monitrc
