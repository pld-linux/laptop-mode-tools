# TODO:
# - unpackaged:
#   /etc/power/event.d/laptop-mode
#   /etc/power/scripts.d/laptop-mode
# - (PPC) subpackage with files for pbbuttonsd and pmud
# - fix *.conf manuals (should be .5 and referenced as such)
# - /etc/apm not owned, should it be /etc/pm?
#
# Conditional build:
%bcond_with	apm	# build apm package
%bcond_without	acpi	# build acpi package

%ifnarch %{ix86} %{x8664} ia64
%undefine		with_acpi
%endif
%ifnarch %{ix86} %{arm} mips ppc sh
%undefine		with_apm
%endif
Summary:	Laptop Mode Tools
Summary(pl.UTF-8):	Narzędzia do trybu laptopowego
Name:		laptop-mode-tools
Version:	1.74
Release:	1
License:	GPL v2+
Group:		Applications/System
#Source0Download: https://github.com/rickysarraf/laptop-mode-tools/releases
Source0:	https://github.com/rickysarraf/laptop-mode-tools/releases/download/%{version}/%{name}_%{version}.tar.gz
# Source0-md5:	c035e95e24f6f368952a20414c4ac224
Source1:	%{name}.init
Patch0:		no-exec-redirection.patch
Patch2:		intel_perf_bias.patch
URL:		https://github.com/rickysarraf/laptop-mode-tools
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires(post,preun):	/sbin/chkconfig
%if %{with apm} && %{with acpi}
Requires:	%{name}-scripts = %{version}-%{release}
%else
%{?with_acpi:Requires:	acpid}
%{?with_apm:Requires:	apmd}
Obsoletes:	laptop-mode-tools-acpi < %{version}-%{release}
Obsoletes:	laptop-mode-tools-apm < %{version}-%{release}
Obsoletes:	laptop-mode-tools-scripts < %{version}-%{release}
%endif
Suggests:	hdparm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# no binaries; not noarch because of libdir paths
%define		_enable_debug_packages	0

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

%package -n pm-utils-lmt
Summary:	Laptop mode tools script for pm-utils
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	pm-utils

%description -n pm-utils-lmt
Laptop mode tools script for pm-utils.

%package gui
Summary:	GUI for laptop mode tools
Summary(pl.UTF-8):	GUI dla narzędzi do trybu laptopowego
Group:		Applications/X11
Requires:	%{name} = %{version}-%{release}
Requires:	python3-PyQt5
Requires:	python3-modules
BuildArch:	noarch

%description gui
GUI for laptop mode tools.

%description gui -l pl.UTF-8
GUI dla narzędzi do trybu laptopowego.

%prep
%setup -q -n %{name}_%{version}
%patch -P0 -p1
%patch -P2 -p1

%{__sed} -i -e '1s|/usr/bin/env python3|%{__python3}|' gui/lmt.py

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir}}

%{__make} install \
	INSTALL=install \
	INIT_D=$RPM_BUILD_ROOT/etc/rc.d/init.d \
	ULIB_D=%{_libdir} \
	MAN_D=%{_mandir} \
	TMPFILES_D=%{systemdtmpfilesdir} \
	%{!?with_acpi:ACPI=disabled} \
	%{!?with_apm:APM=disabled} \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/laptop-mode

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
%doc README.md Documentation/*
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
%attr(755,root,root) /lib/udev/lmt-udev
/lib/udev/rules.d/99-laptop-mode.rules
%{systemdtmpfilesdir}/laptop-mode.conf
%{systemdunitdir}/laptop-mode.service
%{systemdunitdir}/laptop-mode.timer
%{systemdunitdir}/lmt-poll.service
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/modules
%attr(755,root,root) %{_datadir}/%{name}/modules/*
%dir %{_datadir}/%{name}/module-helpers
%attr(755,root,root) %{_datadir}/%{name}/module-helpers/*
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

%files -n pm-utils-lmt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pm-utils/sleep.d/01laptop-mode

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lmt-config-gui
%attr(755,root,root) %{_sbindir}/lmt-config-gui-pkexec
%{_datadir}/%{name}/lmt.py
%{_datadir}/polkit-1/actions/org.linux.lmt.gui.policy
%{_desktopdir}/laptop-mode-tools.desktop
%{_pixmapsdir}/laptop-mode-tools.svg
