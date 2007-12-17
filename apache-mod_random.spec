#Module-Specific definitions
%define mod_name mod_random
%define mod_conf 17_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_Random is a DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	2.0
Release:	%mkrel 6
Group:		System/Servers
License:	BSD
URL:		http://www.tangent.org/
Source0: 	%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_random-register.patch
Patch1:		mod_random-2.0-apache220.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1

%description
Mod_Random provides three services. The first service is as a
redirector. You feed it URLs and it will redirect to random URLs
that you have loaded. The second is that it provides environmental
variables that can be used for doing ad banner systems. The third
is that it can be used to display entire pages of random html. It
uses its own custom handlers in combination witl" S with random
ads and quotes that you feed into the system. 

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0
%patch1 -p0

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

# make doesn't work, but this does (real qute!)
%{_sbindir}/apxs -c mod_random.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README faq.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


