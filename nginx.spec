# TODO
# - /etc/sysconfig/nginx file
# - prepare pld style like nginx.conf
# - split into nginx-common, nginx, nginx-perl packages
#
# Conditional build for nginx:
%bcond_without	addition	# adds module
%bcond_without	dav		# WebDAV
%bcond_without	flv		# FLV stream
%bcond_without	imap		# imap proxy
%bcond_without	mail		# mail module
%bcond_without	perl		# perl module
%bcond_without	poll		# poll
%bcond_without	realip		# real ip (behind proxy)
%bcond_without	rtsig		# rtsig
%bcond_without	select		# select
%bcond_without	status		# stats module
%bcond_without	ssl		# ssl support
%bcond_with	http_browser		# header "User-agent" parser
#
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl.UTF-8):	Serwer HTTP i odwrotne proxy o wysokiej wydajności
Name:		nginx
Version:	0.5.31
Release:	4.1
License:	BSD-like
Group:		Networking/Daemons
Source0:	http://sysoev.ru/nginx/%{name}-%{version}.tar.gz
# Source0-md5:	d84ef8e624b8953faf9cee2b5da535c1
Source1:	%{name}.init
Source2:	%{name}-mime.types.sh
Source3:	http://www.nginx.eu/favicon.ico
# Source3-md5:	2aaf2115c752cbdbfb8a2f0b3c3189ab
Source4:	http://www.nginx.eu/download/proxy.conf
# Source4-md5:	f5263ae01c2edb18f46d5d1df2d3a5cd
Source5:	http://www.nginx.eu/download/%{name}.monitrc
# Source5-md5:	1d3f5eedfd34fe95213f9e0fc19daa88
Source6:	http://www.nginx.eu/download/%{name}.conf
# Source6-md5:	1c112d6f03d0f365e4acc98c1d96261a
Source7:	%{name}.logrotate
Patch0:		%{name}-config.patch
Patch1:		%{name}-autoindexDoS.patch
URL:		http://nginx.net/
BuildRequires:	mailcap
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
%{?with_perl:BuildRequires: perl-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
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

%description -l pl.UTF-8
Serwer HTTP i odwrotne proxy o wysokiej wydajności.

#%package common
#Summary:	Configuration files and documentation for Nginx
#Summary(pl.UTF-8):	Pliki konfiguracyjne i dokumentacja dla Nginx
#Group:		Networking/Daemons

%package -n monit-rc-nginx
Summary:	Nginx  support for monit
Summary(pl.UTF-8):	Wsparcie nginx dla monit
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	monit

%description -n monit-rc-nginx
monitrc file for monitoring nginx webserver server.

%description -n monit-rc-nginx -l pl.UTF-8
Plik monitrc do monitorowania serwera www nginx.


%prep
%setup -q
%patch0 -p0
%patch1 -p0

# build mime.types.conf
sh %{SOURCE2} /etc/mime.types

%build
# NB: not autoconf generated configure
./configure \
	--prefix=%{_prefix} \
	--sbin-path=%{_sbindir}/%{name} \
	--conf-path=%{_sysconfdir}/%{name}.conf \
	--error-log-path=%{_localstatedir}/log/%{name}/error.log \
	--pid-path=%{_localstatedir}/run/%{name}.pid \
	--lock-path=%{_localstatedir}/lock/subsys/%{name} \
	--user=nginx \
	--group=nginx \
	%{?with_addition:--with-http_addition_module} \
	%{?with_dav:--with-http_dav_module} \
	%{?with_flv:--with-http_flv_module} \
	%{?with_imap:--with-imap} \
	%{?with_mail:--with-mail} \
	%{?with_mail:--with-mail_ssl_module} \
	%{?with_perl:--with-http_perl_module} \
	%{?with_poll:--with-poll_module} \
	%{?with_realip:--with-http_realip_module} \
	%{?with_rtsig:--with-rtsig_module} \
	%{?with_select:--with-select_module} \
	%{?with_status:--with-http_stub_status_module} \
	%{?with_ssl:--with-http_ssl_module} \
	%{!?with_http_browser:--without-http_browser_module} \
	--http-log-path=%{_localstatedir}/log/%{name}/access.log \
	--http-client-body-temp-path=%{_localstatedir}/cache/%{name}/client_body_temp \
	--http-proxy-temp-path=%{_localstatedir}/cache/%{name}/proxy_temp \
	--http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}/fastcgi_temp \
	--with-cc="%{__cc}" \
	--with-cc-opt="%{rpmcflags}" \
	--with-ld-opt="%{rpmldflags}" \
	%{?debug:--with-debug}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT%{_nginxdir}/{cgi-bin,html,errors} \
	$RPM_BUILD_ROOT{%{_localstatedir}/log/{%{name},archive/%{name}},%{_localstatedir}/cache/%{name}} \
	$RPM_BUILD_ROOT%{_localstatedir}/lock/subsys/%{name} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{%{perl_vendorarch},%{perl_vendorarch}/auto/%{name}} \
	$RPM_BUILD_ROOT/etc/{logrotate.d,monit}

install conf/* $RPM_BUILD_ROOT%{_sysconfdir}
install mime.types $RPM_BUILD_ROOT%{_sysconfdir}/mime.types
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_nginxdir}/html/favicon.ico
install html/index.html $RPM_BUILD_ROOT%{_nginxdir}/html
install html/50x.html $RPM_BUILD_ROOT%{_nginxdir}/errors
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/proxy.conf
install %{SOURCE5} $RPM_BUILD_ROOT/etc/monit/%{name}.monitrc
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/nginx.conf
install %{SOURCE7} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install objs/src/http/modules/perl/nginx.pm $RPM_BUILD_ROOT%{perl_vendorarch}/%{name}.pm
install objs/src/http/modules/perl/blib/arch/auto/nginx/nginx.so $RPM_BUILD_ROOT%{perl_vendorarch}/auto/%{name}/%{name}.so
install objs/src/http/modules/perl/blib/arch/auto/nginx/nginx.bs $RPM_BUILD_ROOT%{perl_vendorarch}/auto/%{name}/%{name}.bs
install objs/%{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.default
rm -rf $RPM_BUILD_ROOT%{_prefix}/html

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
		touch /var/log/%{name}/$a
		chown nginx:nginx /var/log/%{name}/$a
		chmod 644 /var/log/%{name}/$a
	fi
done
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README html/index.html conf/nginx.conf objs/src/http/modules/perl/blib/man3/nginx.3pm
%doc %lang(ru) CHANGES.ru
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %attr(754,root,root) %{_sysconfdir}
%dir %{_nginxdir}
%dir %{_nginxdir}/cgi-bin
%dir %{_nginxdir}/html
%dir %{_nginxdir}/errors
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(640,root,root) %{_sysconfdir}/*[_-]*
%attr(640,root,root) %{_sysconfdir}/proxy.conf
%attr(640,root,root) %{_sysconfdir}/mime.types
%attr(755,root,root) %{_sbindir}/%{name}
%dir %{perl_vendorarch}/auto/%{name}
%attr(755,root,root) %{perl_vendorarch}/auto/%{name}/%{name}.so
%attr(700,root,root) %{perl_vendorarch}/auto/%{name}/%{name}.bs
%attr(700,root,root) %{perl_vendorarch}/%{name}.pm
%attr(770,root,%{name}) /var/cache/%{name}
%attr(750,root,root) %dir /var/log/archive/%{name}
%attr(750,%{name},logs) /var/log/%{name}
%config(noreplace,missingok) %verify(not md5 mtime size) %{_nginxdir}/html/*
%config(noreplace,missingok) %verify(not md5 mtime size) %{_nginxdir}/errors/*

%files -n monit-rc-nginx
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}.monitrc
