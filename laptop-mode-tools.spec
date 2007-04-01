Summary:	Laptop Mode Tools
Summary(pl):	Narz�dzia do trybu laptopowego
Name:		laptop-mode-tools
Version:	1.32
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.xs4all.nl/~bsamwel/laptop_mode/tools/downloads/%{name}_%{version}.tar.gz
# Source0-md5:	120723749b1a067fa6dec1c767ad2786
Source1:	%{name}.init
URL:		http://www.samwel.tk/laptop_mode/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-scripts = %{epoch}:%{version}-%{release}
BuildArch:	noarch
ExclusiveArch:	%{ix86} ppc noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Laptop mode (also known as laptopmode, laptop-mode and laptop_mode,
for search engine purposes :) ) is a kernel "mode" that allows you to
extend the battery life of your laptop. It does this by intelligently
grouping write activity on your disks, so that only reads of uncached
data result in a disk spinup. It causes a significant improvement in
battery life (for usage patterns that allow it).

%description -l pl
Tryb laptopowy (laptop mode) to "tryb" pracy j�dra umo�liwiaj�cy
wyd�u�enie czasu �ycia baterii laptopa. Czyni to inteligentnie
grupuj�c zapisy na dyski w ten spos�b, �e tylko odczyt
niezbuforowanych danych powoduje rozp�dzenie dysku. Powoduje znacz�c�
popraw� czasu �ycia baterii.

%package acpi
Summary:	ACPI scripts for laptop mode tools
Summary(pl):	Skrypty ACPI dla narz�dzi do trybu laptopowego
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	acpid
Provides:	%{name}-scripts = %{epoch}:%{version}-%{release}

%description acpi
ACPI scripts for laptop mode tools.

%description acpi -l pl
Skrypty ACPI dla narz�dzi do trybu laptopowego.

%package apm
Summary:	APM scripts for laptop mode tools
Summary(pl):	Skrypty APM dla narz�dzi do trybu laptopowego
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	apmd
Provides:	%{name}-scripts = %{epoch}:%{version}-%{release}

%description apm
APM scripts for laptop mode tools.

%description apm -l pl
Skrypty APM dla narz�dzi do trybu laptopowego.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d,laptop-mode,apm/event.d,acpi/{actions,events}} \
	$RPM_BUILD_ROOT{%{_mandir}/man8,%{_sbindir}}

install man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

install etc/laptop-mode/laptop-mode.conf $RPM_BUILD_ROOT%{_sysconfdir}/laptop-mode
install usr/sbin/laptop_mode usr/sbin/lm-syslog-setup $RPM_BUILD_ROOT%{_sbindir}

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/laptop-mode/*.*
%dir %{_sysconfdir}/laptop-mode
%attr(754,root,root) /etc/rc.d/init.d/laptop-mode
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*.8*

%files acpi
%defattr(644,root,root,755)
%attr(750,root,root) %{_sysconfdir}/acpi/*/*

%files apm
%defattr(644,root,root,755)
%attr(750,root,root) %{_sysconfdir}/apm/event.d/*
