# TODO
# - bconds for modules as these are statically linked in
# - initscript
Summary:	High perfomance HTTP and reverse proxy server
Summary(pl):	Serwer HTTP i odwrotne proxy o wysokiej wydajno¶ci
Name:		nginx
Version:	0.5.10
Release:	1
License:	BSD-like
Group:		Applications
Source0:	http://sysoev.ru/nginx/nginx-0.5.10.tar.gz
# Source0-md5:	fb2a1656d63371b7f68ba36862110232
URL:		http://nginx.net/
%if %{with initscript}
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	rc-scripts
Requires(post,preun):	/sbin/chkconfig
%endif
BuildRequires:	pcre-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir /etc/%{name}

%description
High perfomance HTTP and reverse proxy server.

%description -l pl
Serwer HTTP i odwrotne proxy o wysokiej wydajno¶ci.

%prep
%setup -q

%build
# NB: not autoconf generated configure
./configure \
	--prefix=%{_prefix} \
	--sbin-path=%{_sbindir}/%{name} \
	--conf-path=%{_sysconfdir}/%{name}.conf \
	--error-log-path=%{_localstatedir}/log/%{name}/error.log \
	--pid-path=%{_localstatedir}/run/%{name}.pid \
	--user=nobody \
	--group=nobody \
	--with-rtsig_module \
	--with-select_module \
	--with-poll_module \
	--with-http_ssl_module \
	--http-log-path=%{_localstatedir}/log/%{name}/access.log \
	--http-client-body-temp-path=%{_localstatedir}/cache/%{name}/client_body_temp \
	--http-proxy-temp-path=%{_localstatedir}/cache/%{name}/proxy_temp \
	--http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}/fastcgi_temp \
	--with-imap \
	--with-cc="%{__cc}" \
	--with-cc-opt="%{rpmcflags}" \
	--with-ld-opt="%{rpmldflags}" \
	%{?debug:--with-debug}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}}

cp -a conf/* $RPM_BUILD_ROOT%{_sysconfdir}

cp objs/%{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.default
rm -rf $RPM_BUILD_ROOT%{_prefix}/html

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with initscript}
%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README html/index.html conf/nginx.conf
%doc %lang(ru) CHANGES.ru
%dir %{_sysconfdir}
%{_sysconfdir}/koi-win
%{_sysconfdir}/mime.types
%{_sysconfdir}/nginx.conf
%attr(755,root,root) %{_sbindir}/nginx
