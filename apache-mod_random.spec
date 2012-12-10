#Module-Specific definitions
%define mod_name mod_random
%define mod_conf 17_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	2.1
Release:	11
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

cp %{SOURCE1} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_bindir}/apxs -c mod_random.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

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

%files
%doc ChangeLog README faq.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-11mdv2012.0
+ Revision: 772751
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-10
+ Revision: 678405
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-9mdv2011.0
+ Revision: 588051
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-8mdv2010.1
+ Revision: 516167
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-7mdv2010.0
+ Revision: 406638
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-6mdv2009.1
+ Revision: 326225
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-5mdv2009.0
+ Revision: 235073
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-4mdv2009.0
+ Revision: 215624
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-3mdv2008.1
+ Revision: 181846
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:2.1-2mdv2008.1
+ Revision: 170743
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Mon Dec 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-1mdv2008.1
+ Revision: 137432
- build fix
- 2.1
- drop redundant patches
- bunzip S1

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 1:2.0-6mdv2008.1
+ Revision: 119821
- rebuild b/c of missing package on ia32

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-5mdv2008.0
+ Revision: 82663
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0-4mdv2007.1
+ Revision: 140732
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-3mdv2007.0
+ Revision: 79489
- Import apache-mod_random

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-3mdv2007.0
- rebuild

* Fri Dec 16 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-2mdk
- rebuilt against apache-2.2.0 (P1)

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0-3mdk
- fix deps

* Thu Jun 09 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0-2mdk
- added the http://nux.se/apache-mod_random.html web page 
  as the RandomURL to guide confused users :-)

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-4mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_2.0-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_2.0-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_2.0-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_2.0-1mdk
- built for apache 2.0.49

