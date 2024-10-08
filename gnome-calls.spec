# TODO:
# - use gtk4-update-icon-cache
# - separate ModemManager/ofono/sofia-sip plugins?
# - system call-ui library (when it's ready to use system-wide)
#
# Conditional build:
%bcond_without	apidocs	# gtk-doc based API documentation

Summary:	GNOME phone dialer and call handler
Summary(pl.UTF-8):	Aplikacja GNOME do dzwonienia i przyjmowania połączeń
Name:		gnome-calls
Version:	47.0
Release:	1
License:	GPL v3+
Group:		Applications/Communication
Source0:	https://download.gnome.org/sources/calls/47/calls-%{version}.tar.xz
# Source0-md5:	1913e1584192ad088bf6c01559fa1bbf
URL:		https://gitlab.gnome.org/GNOME/calls
BuildRequires:	ModemManager-devel >= 1.12.0
BuildRequires:	evolution-data-server-devel >= 1.2
BuildRequires:	folks-devel
BuildRequires:	gettext-tools
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.74
BuildRequires:	gom-devel
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gtk4-devel >= 4.12
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	libadwaita-devel >= 1.5
BuildRequires:	libcallaudio-devel >= 0.1
BuildRequires:	libfeedback-devel
BuildRequires:	libpeas2-devel >= 2.0
BuildRequires:	libsecret-devel
BuildRequires:	meson >= 1.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
# pkgconfig(sofia-sip-ua-glib)
BuildRequires:	sofia-sip-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	vala-evolution-data-server >= 1.2
BuildRequires:	vala-folks
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.74
Requires(post,postun):	gtk-update-icon-cache
Requires:	ModemManager >= 1.12.0
Requires:	evolution-data-server
Requires:	glib2 >= 1:2.74
Requires:	gtk4 >= 4.12
Requires:	hicolor-icon-theme
Requires:	libadwaita >= 1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME phone dialer and call handler.

%description -l pl.UTF-8
Aplikacja GNOME do dzwonienia i przyjmowania połączeń.

%package apidocs
Summary:	Documentation of GNOME Calls DBus API
Summary(pl.UTF-8):	Dokumentacja API DBus aplikacji GNOME Calls
Group:		Documentation
BuildArch:	noarch

%description apidocs
Documentation of GNOME Calls DBus API.

%description apidocs -l pl.UTF-8
Dokumentacja API DBus aplikacji GNOME Calls.

%prep
%setup -q -n calls-%{version}

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# calls and calls-ui domains
%find_lang calls --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_desktop_database
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_desktop_database
%update_icon_cache hicolor

%files -f calls.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/gnome-calls
%{_sysconfdir}/xdg/autostart/org.gnome.Calls-daemon.desktop
%dir %{_libdir}/calls
%dir %{_libdir}/calls/plugins
%dir %{_libdir}/calls/plugins/provider
%dir %{_libdir}/calls/plugins/provider/dummy
%attr(755,root,root) %{_libdir}/calls/plugins/provider/dummy/libdummy.so
%{_libdir}/calls/plugins/provider/dummy/dummy.plugin
%dir %{_libdir}/calls/plugins/provider/mm
# R: ModemManager
%attr(755,root,root) %{_libdir}/calls/plugins/provider/mm/libmm.so
%{_libdir}/calls/plugins/provider/mm/mm.plugin
%dir %{_libdir}/calls/plugins/provider/ofono
# R: ofono
%attr(755,root,root) %{_libdir}/calls/plugins/provider/ofono/libofono.so
%{_libdir}/calls/plugins/provider/ofono/ofono.plugin
# R: sofia-sip
%dir %{_libdir}/calls/plugins/provider/sip
%attr(755,root,root) %{_libdir}/calls/plugins/provider/sip/libsip.so
%{_libdir}/calls/plugins/provider/sip/sip.plugin
%{systemduserunitdir}/calls-daemon.service
%{_datadir}/dbus-1/services/org.gnome.Calls.service
%{_datadir}/glib-2.0/schemas/org.gnome.Calls.gschema.xml
%{_datadir}/metainfo/org.gnome.Calls.metainfo.xml
%{_desktopdir}/org.gnome.Calls.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Calls.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Calls-symbolic.svg
%{_mandir}/man1/gnome-calls.1*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/calls
%endif
