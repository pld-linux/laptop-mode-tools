#
# TODO:
# - subpackage with files for pbbuttonsd and pmud
#
Summary:	Laptop Mode Tools
Summary(pl.UTF-8):	Narzędzia do trybu laptopowego
Name:		laptop-mode-tools
Version:	1.34
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://samwel.tk/laptop_mode/tools/downloads/%{name}_%{version}.tar.gz
# Source0-md5:	c6edc3b2abbc3770d6673f155a40473d
Source1:	%{name}.init
URL:		http://www.samwel.tk/laptop_mode/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-scripts = %{epoch}:%{version}-%{release}
BuildArch:	noarch
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
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	acpid
Provides:	%{name}-scripts = %{epoch}:%{version}-%{release}

%description acpi
ACPI scripts for laptop mode tools.

%description acpi -l pl.UTF-8
Skrypty ACPI dla narzędzi do trybu laptopowego.

%package apm
Summary:	APM scripts for laptop mode tools
Summary(pl.UTF-8):	Skrypty APM dla narzędzi do trybu laptopowego
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	apmd
Provides:	%{name}-scripts = %{epoch}:%{version}-%{release}

%description apm
APM scripts for laptop mode tools.

%description apm -l pl.UTF-8
Skrypty APM dla narzędzi do trybu laptopowego.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d,apm/event.d,acpi/{actions,events}} \
	$RPM_BUILD_ROOT{%{_mandir}/man8,%{_libdir}/%{name}/modules,%{_sbindir}} \
	$RPM_BUILD_ROOT/etc/laptop-mode/{{batt,lm-ac,nolm-ac}-{start,stop},conf.d}

install man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

install etc/laptop-mode/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/laptop-mode
install etc/laptop-mode/conf.d/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/laptop-mode/conf.d
install usr/lib/laptop-mode-tools/modules/wireless-ipw-power $RPM_BUILD_ROOT%{_libdir}/%{name}/modules
install usr/sbin/{laptop_mode,lm-syslog-setup,lm-profiler} $RPM_BUILD_ROOT%{_sbindir}

install etc/acpi/actions/* $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions
install etc/acpi/events/* $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events

install etc/apm/event.d/* $RPM_BUILD_ROOT%{_sysconfdir}/apm/event.d

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/laptop-mode

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
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%attr(755,root,root) %{_libdir}/%{name}/modules/wireless-ipw-power
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*.8*

%files acpi
%defattr(644,root,root,755)
%attr(750,root,root) %{_sysconfdir}/acpi/*/*

%files apm
%defattr(644,root,root,755)
%attr(750,root,root) %{_sysconfdir}/apm/event.d/*
