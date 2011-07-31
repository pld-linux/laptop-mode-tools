#
# Conditional build:
%bcond_with	apm		# build apm package
%bcond_without	acpi	# build acpi package

# TODO:
# - subpackage with files for pbbuttonsd and pmud
# - fix *.conf manuals (should be .5 and referenced as such)
# - /etc/apm not owned, should it be /etc/pm?

%ifnarch %{ix86} %{x8664} ia64
%undefine		with_acpi
%endif
%ifnarch %{ix86} arm mips ppc sh
%undefine		with_apm
%endif
Summary:	Laptop Mode Tools
Summary(pl.UTF-8):	Narzędzia do trybu laptopowego
Name:		laptop-mode-tools
Version:	1.58
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://samwel.tk/laptop_mode/tools/downloads/%{name}_%{version}.tar.gz
# Source0-md5:	c7a234ada284eaaece0e04bd260e87af
Source1:	%{name}.init
Patch0:		%{name}-kver.patch
URL:		http://www.samwel.tk/laptop_mode/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
%if %{with apm} && %{with acpi}
Requires:	%{name}-scripts = %{version}-%{release}
%else
%{?with_acpi:Requires:	acpid}
%{?with_apm:Requires:	apmd}
Obsoletes:	laptop-mode-tools-scripts
%endif
Suggests:	hdparm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Laptop mode (also known as laptopmode, laptop-mode and laptop_mode,
for search engine purposes :) ) is a kernel "mode" that allows you to
extend the battery life of your laptop. It does this by intelligently
grouping write activity on your disks, so that only reads of uncached
data result in a disk spinup. It causes a significant improvement in
battery life (for usage patterns that allow it).

%description -l pl.UTF-8
Tryb laptopowy (laptop mode) to "tryb" pracy jądra umożliwiający
wydłużenie czasu życia baterii laptopa. Czyni to inteligentnie
grupując zapisy na dyski w ten sposób, że tylko odczyt
niezbuforowanych danych powoduje rozpędzenie dysku. Powoduje znaczącą
poprawę czasu życia baterii.

%package acpi
Summary:	ACPI scripts for laptop mode tools
Summary(pl.UTF-8):	Skrypty ACPI dla narzędzi do trybu laptopowego
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	acpid
Provides:	%{name}-scripts = %{version}-%{release}

%description acpi
ACPI scripts for laptop mode tools.

%description acpi -l pl.UTF-8
Skrypty ACPI dla narzędzi do trybu laptopowego.

%package apm
Summary:	APM scripts for laptop mode tools
Summary(pl.UTF-8):	Skrypty APM dla narzędzi do trybu laptopowego
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	apmd
Provides:	%{name}-scripts = %{version}-%{release}

%description apm
APM scripts for laptop mode tools.

%description apm -l pl.UTF-8
Skrypty APM dla narzędzi do trybu laptopowego.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT{%{_mandir}/man8,%{_datadir}/%{name}/modules,%{_sbindir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/laptop-mode/{{batt,lm-ac,nolm-ac}-{start,stop},conf.d} \
	$RPM_BUILD_ROOT%{_varrun}/%{name}

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/laptop-mode
cp -a etc/laptop-mode/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/laptop-mode
cp -a etc/laptop-mode/conf.d/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/laptop-mode/conf.d
install usr/share/laptop-mode-tools/modules/* $RPM_BUILD_ROOT%{_datadir}/%{name}/modules
install -p usr/sbin/{laptop_mode,lm-syslog-setup,lm-profiler} $RPM_BUILD_ROOT%{_sbindir}
cp -a man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%if %{with acpi}
install -d $RPM_BUILD_ROOT/etc/acpi/{actions,events}
install -p etc/acpi/actions/* $RPM_BUILD_ROOT/etc/acpi/actions
install -p etc/acpi/events/* $RPM_BUILD_ROOT/etc/acpi/events
%endif

%if %{with apm}
install -d $RPM_BUILD_ROOT/etc/apm/event.d
install -p etc/apm/event.d/* $RPM_BUILD_ROOT/etc/apm/event.d
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add laptop-mode
%service laptop-mode restart

%preun
if [ "$1" = "0" ]; then
	%service laptop-mode stop
	/sbin/chkconfig --del laptop-mode
fi

%files
%defattr(644,root,root,755)
%doc README Documentation/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/laptop-mode/*.conf
%dir %{_sysconfdir}/laptop-mode
%dir %{_sysconfdir}/laptop-mode/batt-start
%dir %{_sysconfdir}/laptop-mode/batt-stop
%dir %{_sysconfdir}/laptop-mode/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/laptop-mode/conf.d/*.conf
%dir %{_sysconfdir}/laptop-mode/lm-ac-start
%dir %{_sysconfdir}/laptop-mode/lm-ac-stop
%dir %{_sysconfdir}/laptop-mode/nolm-ac-start
%dir %{_sysconfdir}/laptop-mode/nolm-ac-stop
%attr(754,root,root) /etc/rc.d/init.d/laptop-mode
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/modules
%dir %{_varrun}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/modules/*
%attr(755,root,root) %{_sbindir}/laptop_mode
%attr(755,root,root) %{_sbindir}/lm-profiler
%attr(755,root,root) %{_sbindir}/lm-syslog-setup
%{_mandir}/man8/laptop_mode.8*
%{_mandir}/man8/lm-profiler.8*
%{_mandir}/man8/lm-syslog-setup.8*
# should be man5
%{_mandir}/man8/laptop-mode.conf.8*
%{_mandir}/man8/lm-profiler.conf.8*

%if %{with acpi}
# skip subpackage if only one backend built
%{?with_apm:%files acpi}
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysconfdir}/acpi/actions/lm_*.sh
%{_sysconfdir}/acpi/events/lm_*
%endif

%if %{with apm}
# skip subpackage if only one backend built
%{?with_acpi:%files apm}
%defattr(644,root,root,755)
# XXX: dir not owned
%attr(755,root,root) %{_sysconfdir}/apm/event.d/laptop-mode
%endif
