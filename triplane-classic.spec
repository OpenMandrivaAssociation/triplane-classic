
%define name	triplane-classic
%define version	1.04
%define rel	1

Summary:	A side-scrolling dogfighting game
Name:		%{name}
Version:	%{version}
Release:	%mkrel %rel
License:	GPLv3+
URL:		http://triplane.sourceforge.net/
Source:		http://sourceforge.net/projects/triplane/files/%name-%version.tar.gz
# darcs get http://iki.fi/lindi/darcs/triplane-testsuite
# cd triplane-testsuite; darcs changes (check that tere are actual changes since last update)
# darcs dist; xzme triplane-testsuite.tar.gz; mv triplane-testsuite.tar.xz ../triplane-testsuite-20090609.tar.xz
Source1:	triplane-testsuite-20090609.tar.xz
# Fix parameter handling issues (overflows and non-literal fmt string)
Patch0:		triplane-parameter-handling.patch
Group:		Games/Arcade
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
# for conversions
BuildRequires:	man
BuildRequires:	imagemagick
# for testsuite:
BuildRequires:	x11-server-xvfb
%if %{mdkversion} <= 201000
# on 2010.0 and earlier there was no dependency in SDL_mixer on this
Requires:	%{_lib}mikmod3
%endif

%description
Triplane Classic is a side-scrolling dogfighting game featuring solo
missions and multiplayer mode with up to four players. It is a port of
the original Triplane Turmoil game for DOS and aims to match the
original game exactly so that high scores remain comparable to the
original.

%prep
%setup -q -a 1
%patch0 -p1

# Convert the man page to a html page, this is a game after all:
# tail removes the first Context-type line and sed removes links to http targets
man2html doc/%{name}.6 | tail -n +2 | sed -r 's,<a href="http[^>]+>(.*)</a>,\1,ig' > %{name}.html

%build
for i in depend all; do
	%make OPTIFLAG="%{optflags}" LDFLAGS="%{?ldflags}" PREFIX=%{_prefix} $i
done

%install
rm -rf %{buildroot}
%makeinstall_std PREFIX=%{_prefix}

install -D -m644 doc/%{name}.6 %{buildroot}%{_mandir}/man6/%{name}.6

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Triplane Classic
GenericName=Dogfighting game
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;ArcadeGame;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-manual.desktop <<EOF
[Desktop Entry]
Name=Triplane Classic manual
Comment=Open help file of Triplane Classic
Exec=xdg-open %{_docdir}/%{name}/%{name}.html
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;ArcadeGame;
EOF

for i in 16 32 48; do
	install -d -m755 %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	convert data/application_icon/%{name}.xpm -resize $i %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/%{name}.png
done

# Xvfb segfaults on BS on 2010.0
%if %mdkversion >= 201010
%check
xvfb-run %make test
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{name}.html doc/TODO doc/lvledit-keys.txt
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*x*/apps/%{name}.png
%doc %{_datadir}/applications/mandriva-%{name}-manual.desktop
%{_mandir}/man6/%{name}.6*

