#Module-Specific definitions
%define mod_name mod_random
%define mod_conf 17_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_Random is a DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	2.1
Release:	%mkrel 1
Group:		System/Servers
License:	BSD
URL:		http://www.tangent.org/
Source0: 	http://download.tangent.org/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mod Random provides three services. The first service is redirection: you feed
it URLs and it will redirect to random URLs that you have loaded. The second is
providing environment variables that can be used for implementing ad banner
systems. The third is displaying entire pages of random HTML, using its own
custom handlers in combination with with random ads and quotes that you feed
into the system. It can also supply text via an environment variable called
RANDOM_QUOTE, RANDOM_AD, or by environment variables that you specify. This can
be used to implement fortune cookies, message of the day, entire random pages,
or banner ads.

%prep

%setup -q -n %{mod_name}-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -c mod_random.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

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


