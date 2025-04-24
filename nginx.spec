# TODO
# - /etc/sysconfig/nginx file
# - missing perl build/install requires
# - add njs: https://nginx.org/en/docs/njs/
#
# Conditional build for nginx:
# Features
%bcond_with	debug		# enable debug logging: http://nginx.org/en/docs/debugging_log.html
%bcond_without	file_aio	# file AIO support
%bcond_without	threads		# thread pool support
# Modules
%bcond_without	addition	# http addition module
%bcond_without	auth_request	# auth_request module
%bcond_without	dav		# WebDAV
%bcond_without	flv		# http FLV module
%bcond_without	gd		# without http image filter module
%bcond_without	geoip		# without http geoip module and stream geoip module
%bcond_without	http2		# HTTP/2 module
%bcond_without	http3		# HTTP/3 module
%bcond_without	mail		# don't build imap/mail proxy
%bcond_without	perl		# don't build with perl module
%bcond_without	poll		# poll module
%bcond_without	realip		# real ip (behind proxy)
%bcond_without	select		# select module
%bcond_without	ssl		# ssl support and http ssl module
%bcond_without	stream		# TCP/UDP proxy module
%bcond_without	stub_status	# http stub status module
%bcond_without	sub		# ngx_http_sub_module
%bcond_without	xslt		# without http xslt module
%bcond_with	http_browser	# http browser module (header "User-agent" parser)
%bcond_without	modsecurity	# modsecurity module
%bcond_with	rtmp		# rtmp support
%bcond_without	vts		# virtual host traffic status module
%bcond_without	headers_more	# headers more module

%ifarch x32
%undefine	with_rtsig
%endif

%define		ssl_version	1.0.2
%define		rtmp_version	1.2.2
%define		vts_version	0.2.4
%define		headers_more_version	0.38
%define		modsecurity_version	1.0.3
%define		http_cache_purge_version	2.5.3

Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
# nginx mainline is recommended by nginx team: https://www.nginx.com/blog/nginx-1-6-1-7-released/
# http://nginx.org/en/download.html
Name:		nginx
Version:	1.28.0
Release:	1
License:	BSD-like
Group:		Networking/Daemons/HTTP
Source0:	https://nginx.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	1ad2b6606c3709ed1268ca32ae447c21
Source1:	https://nginx.org/favicon.ico
# Source1-md5:	72e228c3809db53da8a884b6676ed36a
Source2:	proxy.conf
Source3:	%{name}.logrotate
Source4:	%{name}.mime
Source6:	%{name}.monitrc
Source7:	%{name}.init
Source14:	%{name}.conf
Source17:	%{name}-mime.types.sh
Source18:	%{name}.service
Source33:	https://github.com/SpiderLabs/ModSecurity-nginx/releases/download/v%{modsecurity_version}/modsecurity-%{name}-v%{modsecurity_version}.tar.gz
# Source33-md5:	b85e1996f81b51a06a32e73b3be4709d
Source101:	https://github.com/arut/nginx-rtmp-module/archive/v%{rtmp_version}/%{name}-rtmp-module-%{rtmp_version}.tar.gz
# Source101-md5:	9bb7a06aede38d9e36ad13dc1354d8f9
Source102:	https://github.com/vozlt/nginx-module-vts/archive/v%{vts_version}.tar.gz
# Source102-md5:	ed27608606c25d49d5facb56bc8d5256
Source103:	https://github.com/openresty/headers-more-nginx-module/archive/v%{headers_more_version}.tar.gz
# Source103-md5:	520e4099ea40b62069ec92534d723627
# https://github.com/nginx-modules/ngx_cache_purge
Source104:	https://github.com/nginx-modules/ngx_cache_purge/archive/refs/tags/%{http_cache_purge_version}.tar.gz
# Source104-md5:	bf92baae08e4c850825a8543c7d4aaa8
Patch0:		%{name}-no-Werror.patch
Patch1:		modsecurity-gcc14.patch
URL:		https://nginx.org/
BuildRequires:	mailcap
BuildRequires:	pcre2-8-devel
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	zlib-devel
%if %{with geoip}
BuildRequires:	GeoIP-devel
%endif
%if %{with gd}
BuildRequires:	gd-devel
%endif
%if %{with modsecurity}
BuildRequires:	lua-devel
BuildRequires:  libmodsecurity-devel
%endif
%if %{with perl}
BuildRequires:	perl-CGI
BuildRequires:	perl-devel
BuildRequires:	python3
BuildRequires:	rpm-perlprov
%endif
%if %{with ssl}
BuildRequires:	openssl-devel >= %{ssl_version}
Requires:	openssl >= %{ssl_version}
%endif
%if %{with xslt}
BuildRequires:	libxslt-devel
%endif
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
Obsoletes:	nginx-common < 1.13.3
Obsoletes:	nginx-light < 1.13.3
Obsoletes:	nginx-standard < 1.13.3
Conflicts:	rpm < 4.4.2-0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_nginxdir	/home/services/%{name}

# minimizing restarts logics. we restart webserver:
#
# 1. at the end of transaction. (posttrans, feature from rpm 4.4.2)
# 2. first install of module (post: $1 = 1)
# 2. uninstall of module (postun: $1 == 0)
#
# the strict internal deps between modules and
# main package are very important for all this to work.

# restart webserver at the end of transaction

%define	restart_webserver \
	%systemd_post %{name}.service \
	%service %{name} force-reload \
	%{nil}

# macro called at module post scriptlet
%define	module_post \
if [ "$1" = "1" ]; then \
	%restart_webserver \
fi

# macro called at module postun scriptlet
%define	module_postun \
if [ "$1" = "0" ]; then \
	%restart_webserver \
fi

# it's sooo annoying to write them
%define	module_scripts() \
%post %1 \
%module_post \
\
%postun %1 \
%module_postun

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

%package mod_headers_more
Summary:	Nginx HTTP headers more module
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_headers_more
Set and clear input and output headers...more than "add".

%package mod_http_geoip
Summary:	Nginx HTTP geoip module
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	GeoIP

%description mod_http_geoip
Nginx HTTP geoip module.

%package mod_stream_geoip
Summary:	Nginx stream geoip module
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-mod_stream = %{version}-%{release}
Requires:	GeoIP

%description mod_stream_geoip
Nginx stream geoip module.

%package mod_http_image_filter
Summary:	Nginx HTTP image filter module
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_http_image_filter
Nginx HTTP image filter module.

%package mod_http_perl
Summary:	Nginx HTTP Perl module
Group:		Networking/Daemons/HTTP
Requires:	%{name} = %{version}-%{release}

%description mod_http_perl
Nginx HTTP Perl module.

%package mod_http_xslt_filter
Summary:	Nginx XSLT module
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_http_xslt_filter
Nginx XSLT module.

%package mod_mail
Summary:	Nginx mail module
Group:		Networking/Daemons/HTTP
Requires:	%{name} = %{version}-%{release}

%description mod_mail
Nginx mail module.

%package mod_vts
Summary:	Nginx virtual host traffic status module
Group:		Networking/Daemons/HTTP
Requires:	%{name} = %{version}-%{release}

%description mod_vts
Nginx virtual host traffic status module.

%package mod_stream
Summary:	Nginx stream modules
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_stream
Nginx stream modules.

%package mod_http_cache_purge
Summary:	Nginx cache purge module
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_http_cache_purge
`ngx_cache_purge` is `nginx` module which adds ability to purge
content from `FastCGI`, `proxy`, `SCGI` and `uWSGI` caches.

%package mod_http_modsecurity
Summary:	Nginx modsecurity module
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_http_modsecurity
The ModSecurity-nginx connector takes the form of an nginx module. The
module simply serves as a layer of communication between nginx and
ModSecurity.

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
%setup -q %{?with_rtmp:-a101} %{?with_modsecurity:-a33} %{?with_vts:-a102} %{?with_headers_more:-a103} -a104
%patch -P0 -p0
%{?with_modsecurity:%patch -P1 -p1 -d modsecurity-nginx-v%{modsecurity_version}}

%if %{with rtmp}
mv nginx-rtmp-module-%{rtmp_version} nginx-rtmp-module
%endif

%if %{with vts}
mv nginx-module-vts-%{vts_version} nginx-vts-module
%endif

%if %{with headers_more}
mv headers-more-nginx-module-%{headers_more_version} nginx-headers-more-module
%endif

mv ngx_cache_purge-* ngx_cache_purge

# build mime.types.conf
#sh %{SOURCE17} /etc/mime.types

%build
# NB: not autoconf generated configure
cp -f configure auto/

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
	--http-uwsgi-temp-path=%{_localstatedir}/cache/%{name}/uwsgi_temp \
	--http-scgi-temp-path=%{_localstatedir}/cache/%{name}/scgi_temp \
	--user=nginx \
	--group=nginx \
 	--with-compat \
	%{?with_select:--with-select_module} \
	%{?with_poll:--with-poll_module} \
	%{?with_rtsig:--with-rtsig_module} \
	%{?with_perl:--with-http_perl_module=dynamic} \
	%{?with_gd:--with-http_image_filter_module=dynamic} \
	%{?with_xslt:--with-http_xslt_module=dynamic} \
	%{?with_geoip:--with-http_geoip_module=dynamic} \
	%{?with_geoip:--with-stream_geoip_module=dynamic} \
%if %{with mail}
	--with-mail=dynamic \
	--with-mail_ssl_module \
%endif
%if %{with stream}
	--with-stream=dynamic \
	--with-stream_ssl_module \
%endif
	--with-cc="%{__cc}" \
	--with-cc-opt="%{rpmcflags}" \
	--with-ld-opt="%{rpmldflags}" \
	%{?with_debug:--with-debug} \
	%{?with_addition:--with-http_addition_module} \
	%{?with_dav:--with-http_dav_module} \
	%{?with_flv:--with-http_flv_module} \
	%{?with_sub:--with-http_sub_module} \
	%{?with_realip:--with-http_realip_module} \
	%{?with_stub_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	%{!?with_http_browser:--without-http_browser_module} \
	--add-dynamic-module=./ngx_cache_purge \
	%{?with_headers_more:--add-dynamic-module=./nginx-headers-more-module} \
	%{?with_rtmp:--add-module=./nginx-rtmp-module} \
	%{?with_vts:--add-dynamic-module=./nginx-vts-module} \
	%{?with_auth_request:--with-http_auth_request_module} \
	%{?with_threads:--with-threads} \
	%{?with_http2:--with-http_v2_module} \
	%{?with_http3:--with-http_v3_module} \
	%{?with_modsecurity:--add-dynamic-module=modsecurity-nginx-v%{modsecurity_version}} \
	--with-http_secure_link_module \
	%{?with_file_aio:--with-file-aio} \
	%{nil}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT%{_nginxdir}/{cgi-bin,html,errors} \
	$RPM_BUILD_ROOT%{_localstatedir}/log/{%{name},archive/%{name}} \
	$RPM_BUILD_ROOT%{_localstatedir}/cache/%{name} \
	$RPM_BUILD_ROOT%{_localstatedir}/lock/subsys/%{name} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/{conf,modules,vhosts,webapps}.d} \
	$RPM_BUILD_ROOT%{_sysconfdir}/snippets \
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

load_module() {
	local module=ngx_${1}_module.so conffile=mod_$1.conf
	printf 'load_module "%{_libdir}/%{name}/modules/%s";' "$module" \
		> $RPM_BUILD_ROOT%{_sysconfdir}/modules.d/$conffile
}

%if %{with perl}
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/nginx/.packlist
load_module http_perl
%endif

%if %{with geoip}
load_module http_geoip
load_module stream_geoip
%endif
%if %{with gd}
load_module http_image_filter
%endif
%if %{with xslt}
load_module http_xslt_filter
%endif
%if %{with mail}
load_module mail
%endif
%{?with_vts:load_module http_vhost_traffic_status}
%{?with_headers_more:load_module http_headers_more_filter}
%if %{with stream}
load_module stream
%endif
%if %{with modsecurity}
load_module http_modsecurity
%endif
load_module http_cache_purge

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

%posttrans
%restart_webserver

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

%module_scripts mod_http_geoip
%module_scripts mod_http_image_filter
%module_scripts mod_http_perl
%module_scripts mod_http_xslt_filter
%module_scripts mod_mail
%module_scripts mod_vts
%module_scripts mod_headers_more
%module_scripts mod_stream
%module_scripts mod_stream_geoip
%module_scripts mod_http_cache_purge

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README.md html/index.html conf/nginx.conf
%doc %lang(ru) CHANGES.ru
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %attr(750,root,nginx) %{_sysconfdir}
%dir %{_sysconfdir}/conf.d
%dir %{_sysconfdir}/modules.d
%dir %{_sysconfdir}/snippets
%dir %{_sysconfdir}/vhosts.d
%dir %{_sysconfdir}/webapps.d
%attr(640,root,root) %{_sysconfdir}/mime.types
%attr(640,root,root) %{_sysconfdir}/koi-utf
%attr(640,root,root) %{_sysconfdir}/koi-win
%attr(640,root,root) %{_sysconfdir}/win-utf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fastcgi.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nginx.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/proxy.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fastcgi_params
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scgi_params
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/uwsgi_params
%attr(755,root,root) %{_sbindir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{systemdunitdir}/%{name}.service

%attr(750,nginx,logs) %dir /var/log/archive/%{name}
%attr(750,nginx,logs) /var/log/%{name}
%attr(770,root,nginx) /var/cache/%{name}

%dir %{_nginxdir}
%dir %{_nginxdir}/cgi-bin
%dir %{_nginxdir}/html
%dir %{_nginxdir}/errors
%config(noreplace,missingok) %verify(not md5 mtime size) %{_nginxdir}/html/*
%config(noreplace,missingok) %verify(not md5 mtime size) %{_nginxdir}/errors/*

%if %{with geoip}
%files mod_http_geoip
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_http_geoip.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_http_geoip_module.so

%files mod_stream_geoip
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_stream_geoip.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_stream_geoip_module.so
%endif

%if %{with gd}
%files mod_http_image_filter
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_http_image_filter.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_http_image_filter_module.so
%endif

%if %{with perl}
%files mod_http_perl
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_http_perl.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_http_perl_module.so
%dir %{perl_vendorarch}/auto/%{name}
%attr(755,root,root) %{perl_vendorarch}/auto/%{name}/%{name}.so
%{perl_vendorarch}/%{name}.pm
%{_mandir}/man3/nginx.3pm*
%endif

%if %{with xslt}
%files mod_http_xslt_filter
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_http_xslt_filter.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_http_xslt_filter_module.so
%endif

%if %{with mail}
%files mod_mail
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_mail.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_mail_module.so
%endif

%if %{with headers_more}
%files mod_headers_more
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_http_headers_more_filter.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_http_headers_more_filter_module.so
%endif

%if %{with vts}
%files mod_vts
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_http_vhost_traffic_status.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_http_vhost_traffic_status_module.so
%endif

%if %{with stream}
%files mod_stream
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_stream.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_stream_module.so
%endif

%files mod_http_cache_purge
%defattr(644,root,root,755)
%doc ngx_cache_purge/{CHANGES,README.md}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_http_cache_purge.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_http_cache_purge_module.so

%files mod_http_modsecurity
%defattr(644,root,root,755)
%doc ngx_cache_purge/{CHANGES,README.md}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_http_modsecurity.conf
%attr(755,root,root) %{_libdir}/%{name}/modules/ngx_http_modsecurity_module.so

%files -n monit-rc-nginx
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}.monitrc
