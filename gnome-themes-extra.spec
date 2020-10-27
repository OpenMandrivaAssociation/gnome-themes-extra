# fix build (debuginfo package is empty...):
%define debug_package %{nil}

%define url_ver %(echo %{version} | cut -d. -f1,2)

Name:		gnome-themes-extra
Version:	3.28
Release:	1
Summary:	Standard themes for GNOME applications
Group:		Graphical desktop/GNOME
License:	LGPLv2+
URL:		https://gitlab.gnome.org/GNOME/gnome-themes-extra
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Patch1337:	gnome-themes-standard-3.20.2-allow-modification-of-bg-colour.patch
BuildRequires:	intltool
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(librsvg-2.0)

# just for /usr/bin/gtk-update-icon-cache:
BuildRequires:	gtk-update-icon-cache
# patch
BuildRequires:	git-core

Requires:	abattis-cantarell-fonts
Requires:	adwaita-icon-theme
Requires:	adwaita-cursor-theme

Obsoletes:	gnome-themes-extras < 2.22.0-14
Obsoletes:	gnome-themes-standard < 3.28
Provides:	gnome-themes-standard = %{version}-%{release}
Provides:	gnome-background-standard = %{version}-%{release}
Provides:	gnome-themes = %{version}-%{release}

%description
The gnome-themes-extra package contains the standard theme for the GNOME
desktop, which provides default appearance for cursors, desktop background,
window borders and GTK+ applications.

%package -n adwaita-gtk2-theme
Summary:	Adwaita gtk2 theme
Group:		Graphical desktop/GNOME
Requires:	adwaita-icon-theme
Requires:	adwaita-cursor-theme
Requires:	abattis-cantarell-fonts
# for HighContrast theme
Requires:	gtk2-hc-engine

# ease upgrade mga6 -> mga7 (mga#24553)
Conflicts:	gnome-themes-standard < 3.28
# ease upgrade mga7 -> mga8 (mga#26598)
Conflicts:	gnome-themes-extra < 3.28-7

%description -n adwaita-gtk2-theme
The adwaita-gtk2-theme package contains a gtk2 theme for presenting widgets
with a GNOME look and feel.

%prep
%autosetup -Sgit

%build
%configure
%make_build

%install
%make_install

# for icon cache
touch %{buildroot}%{_iconsdir}/HighContrast/icon-theme.cache

# we don't want these
find %{buildroot} -name '*.la' -delete

# shipped with gtk3
rm -rf %{buildroot}%{_datadir}/themes/Adwaita{,-dark}/gtk-3.0/

# automatic gtk icon cache update on rpm installs/removals
%transfiletriggerin --  %{_datadir}/icons/HighContrast/
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --force --quiet /usr/share/icons/HighContrast
fi

%transfiletriggerpostun --  %{_datadir}/icons/HighContrast/
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --force --quiet /usr/share/icons/HighContrast
fi

%files
%doc NEWS
# A11y themes
%dir %{_iconsdir}/HighContrast/
%{_iconsdir}/HighContrast/*/
%ghost %{_iconsdir}/HighContrast/icon-theme.cache
%{_iconsdir}/HighContrast/index.theme
%dir %{_datadir}/icons/HighContrast
%{_datadir}/icons/HighContrast/16x16/
%{_datadir}/icons/HighContrast/22x22/
%{_datadir}/icons/HighContrast/24x24/
%{_datadir}/icons/HighContrast/32x32/
%{_datadir}/icons/HighContrast/48x48/
%{_datadir}/icons/HighContrast/256x256/
%{_datadir}/icons/HighContrast/scalable/
%{_datadir}/icons/HighContrast/index.theme
%ghost %{_datadir}/icons/HighContrast/icon-theme.cache
%{_datadir}/themes/HighContrast/gtk-3.0/

%files -n adwaita-gtk2-theme
%{_libdir}/gtk-2.0/2.10.0/engines/libadwaita.so

%dir %{_datadir}/themes/Adwaita/
%{_datadir}/themes/Adwaita/gtk-2.0/
%{_datadir}/themes/Adwaita/index.theme

%dir %{_datadir}/themes/Adwaita-dark/
%{_datadir}/themes/Adwaita-dark/gtk-2.0/
%{_datadir}/themes/Adwaita-dark/index.theme

%dir %{_datadir}/themes/HighContrast
%{_datadir}/themes/HighContrast/gtk-2.0/
%{_datadir}/themes/HighContrast/index.theme
