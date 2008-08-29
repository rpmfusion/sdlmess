%ifarch x86_64
%define arch_flags PTR64=1
%endif
%ifarch ppc
%define arch_flags BIGENDIAN=1
%endif
%ifarch ppc64
%define arch_flags BIGENDIAN=1 PTR64=1
%endif

Name:           sdlmess
Version:        0127
Release:        1%{?dist}
Summary:        SDL Multiple Emulator Super System

Group:          Applications/Emulators
License:        MAME License
URL:            http://rbelmont.mameworld.info/?page_id=163
Source0:        http://rbelmont.mameworld.info/sdlmess%{version}.zip
Source1:        %{name}-ctrlr.tgz
Patch0:         %{name}-warnings.patch
Patch1:         %{name}-expat.patch
Patch2:         %{name}-bne.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  SDL-devel expat-devel zlib-devel libGL-devel gtk2-devel
BuildRequires:  GConf2-devel

%description
MESS is an acronym that stands for Multiple Emulator Super System.  MESS will
more or less faithfully reproduce computer and console systems on a PC.

MESS emulates the hardware of the systems and sometimes utilizes ROM images to
load programs and games.  Therefore, these systems are NOT simulations, but
the actual emulations of the hardware.

%package tools
Summary:        Tools used for the sdlmess package
Group:          Applications/Emulators
Requires:       %{name} = %{version}-%{release}

%description tools
%{summary}.

%package data
Summary:        Data files used for the sdlmess package
Group:          Applications/Emulators
Requires:       %{name} = %{version}-%{release}

%description data
%{summary}.

%package debug
Summary:        Debug enabled version of sdlmess
Group:          Applications/Emulators
Requires(hint): %{name}-debuginfo = %{version}-%{release}

%description debug
%{summary}.


%prep
%setup -qn %{name}%{version}
%patch0 -p0 -b .warnings~
%patch1 -p0 -b .expat~
%patch2 -p0 -b .bne~

# Create mess.ini file
cat > mess.ini << EOF
# Define multi-user paths
artpath                 %{_datadir}/mess/artwork
rompath                 %{_datadir}/mess/roms
ctrlrpath               %{_datadir}/mess/ctrlr
fontpath                %{_datadir}/mess/fonts
hashpath                %{_datadir}/mess/hash
samplepath              %{_datadir}/mess/samples
cheatpath               %{_datadir}/mess/cheats

# Allow user to override ini settings
inipath                 \$HOME/.mess/ini;%{_sysconfdir}/mess

# Set paths for local storage
cfg_directory           \$HOME/.mess/cfg
comment_directory       \$HOME/.mess/comments
diff_directory          \$HOME/.mess/diff
input_directory         \$HOME/.mess/inp
memcard_directory       \$HOME/.mess/memcard
nvram_directory         \$HOME/.mess/nvram
state_directory         \$HOME/.mess/sta
snapshot_directory      \$HOME/.mess/snap

# Fedora custom defaults
video                   opengl
joystick                1
EOF

# Fix end-of-line encoding
rm -fr docs/win*
find docs -type f -exec sed -i 's/\r//' {} \;
mv docs/imgtool.txt .

#Fix newvideo.txt encoding
pushd docs
/usr/bin/iconv -f cp1250 -t utf-8 newvideo.txt > newvideo.txt.conv
/bin/mv -f newvideo.txt.conv newvideo.txt
popd

# remove extraneous file in installed artwork
rm -f artwork/dir.txt


%build
make %{?arch_flags} DEBUG=1 SYMBOLS=1 \
    OPT_FLAGS='%{optflags} -DINI_PATH="\"%{_sysconfdir}/mess;\""' -f makefile.sdl
make %{?arch_flags} \
    OPT_FLAGS='%{optflags} -DINI_PATH="\"%{_sysconfdir}/mess;\""' -f makefile.sdl


%install
rm -rf $RPM_BUILD_ROOT

# Create directories
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/mess/artwork
install -d $RPM_BUILD_ROOT%{_datadir}/mess/roms
install -d $RPM_BUILD_ROOT%{_datadir}/mess/ctrlr
install -d $RPM_BUILD_ROOT%{_datadir}/mess/fonts
install -d $RPM_BUILD_ROOT%{_datadir}/mess/hash
install -d $RPM_BUILD_ROOT%{_datadir}/mess/samples
install -d $RPM_BUILD_ROOT%{_datadir}/mess/software
install -d $RPM_BUILD_ROOT%{_datadir}/mess/cheats
install -d $RPM_BUILD_ROOT%{_sysconfdir}/mess
install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.mess/cfg
install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.mess/comments
install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.mess/diff
install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.mess/ini
install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.mess/inp
install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.mess/memcard
install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.mess/nvram
install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.mess/sta
install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.mess/snap

# Install binaries and config files
install -pm 755 mess $RPM_BUILD_ROOT%{_bindir}/mess
install -pm 755 messd $RPM_BUILD_ROOT%{_bindir}/messd
install -pm 755 imgtool messtest $RPM_BUILD_ROOT%{_bindir}
install -pm 644 sysinfo.dat $RPM_BUILD_ROOT%{_datadir}/mess
install -pm 644 artwork/* $RPM_BUILD_ROOT%{_datadir}/mess/artwork
install -pm 644 hash/* $RPM_BUILD_ROOT%{_datadir}/mess/hash
install -pm 644 mess.ini $RPM_BUILD_ROOT%{_sysconfdir}/mess
install -pm 644 %{SOURCE1} .

# Install controller files
tar --extract --directory $RPM_BUILD_ROOT%{_datadir}/mess/ctrlr \
    --file %{SOURCE1}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc *.txt docs/*
%config(noreplace) %{_sysconfdir}/mess/mess.ini
%dir %{_sysconfdir}/mess
%{_bindir}/mess
%dir %{_datadir}/mess
%dir %{_datadir}/mess/artwork
%dir %{_datadir}/mess/roms
%dir %{_datadir}/mess/ctrlr
%dir %{_datadir}/mess/fonts
%dir %{_datadir}/mess/hash
%dir %{_datadir}/mess/samples
%dir %{_datadir}/mess/software
%dir %{_datadir}/mess/cheats
%{_sysconfdir}/skel/.mess

%files tools
%defattr(-,root,root,-)
%doc imgtool.txt
%{_bindir}/imgtool
%{_bindir}/messtest

%files data
%defattr(-,root,root,-)
%{_datadir}/mess/sysinfo.dat
%{_datadir}/mess/artwork/*
%{_datadir}/mess/ctrlr/*
%{_datadir}/mess/hash/*

%files debug
%defattr(-,root,root,-)
%doc docs/license.txt
%{_bindir}/messd


%changelog
* Fri Aug 29 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0127-1
- Updated to 0.127
- Dropped cheat_file and added cheatpath to the default ini

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0126-3
- rebuild for buildsys cflags issue

* Mon Jul 14 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-2
- Added ppc64 arch_flags
- Patched bne-- inline assembly to allow ppc64 build
- Updated the expat patch to make new rpm happy

* Mon Jul 11 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-1
- Updated to 0.126
- Dropped DEBUGGER=1, it is default now

* Fri May 16 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0125-1
- Updated to 0.125
- Dropped %%{?dist} from %%changelog
- Added hyphen before version number in %%changelog

* Thu Mar 27 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0124-1
- Updated to 0.124
- Fixed newvideo.txt encoding
- Fixed wrong rompath
- Dropped rpath patch
- Updated and reenabled warnings patch
- Changed the inipath to \$HOME/.mess/ini;%%{_sysconfdir}/mess
- Dropped %%{?_smp_mflags} again

* Thu Feb 14 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0123-1
- Updated to 0.123
- Added DEBUGGER=1 to -debug subpackage build command
- Disabled the warnings patch
- Patched src/osd/sdl/sdl.mak to remove invalid rpath

* Mon Jan  7 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0122-2
- Fixed ppc build

* Wed Jan  2 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0122-1
- Updated to 0.122
- Added %%{?_smp_mflags}

* Mon Nov 26 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0121-1
- Updated to 0.121
- Fixed PPC build
- Enabled joystick by default, as per MAME

* Sun Oct 21 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0120-1
- Updated to 0.120
- Dropped verbosebuild patch

* Mon Sep 17 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0119-1
- Updated to 0.119
- Updated the sdlmess-ctrlr.tgz archive for the input changes
- Cleaned up the spec
- Changed biospath to rompath
- Dropped beta part, as MESS never releases intermediate updates
- Added patch to remove -Werror from makefile, as per sdlmame
- ExcludeArch: ppc until the png2bdc problem is solved
- Patched the makefile to make the build verbose

* Sun May 06 2007 XulChris <tkmame@retrogames.com> - 0115-1
- Upstream sync
- Just package *.txt in %%doc

* Sun Apr 22 2007 XulChris <tkmame@retrogames.com> - 0114-1
- Upstream sync
- Remove no longer needed patch
- No longer install whatsnew.txt sperately, it is in source tarball now
- Install controller data from seperate tarball

* Sun Mar 11 2007 XulChris <tkmame@retrogames.com> - 0113-2
- Add SDL patch for FC5 builds

* Sat Mar 10 2007 XulChris <tkmame@retrogames.com> - 0113-1
- Upstream sync
- Add whatsnew.txt to sources since RB forgot to package it
- Use PREFIX=sdl to avoid linker conflict

* Thu Feb 15 2007 XulChris <tkmame@retrogames.com> - 0112-3
- Remove extraneous file from installed artwork

* Tue Feb 13 2007 XulChris <tkmame@retrogames.com> - 0112-2
- Add artwork to data subpackage
- Clean up spec file to more closely match sdlmame spec

* Sat Feb 10 2007 XulChris <tkmame@retrogames.com> - 0112-1
- Upstream sync
- Add dist tags to changelog
- Remove no longer need extra sources and patches
- Move creation of ini file to %%prep
- Fix group tag for tools subpackage
- Add messtest to tools
- Move imgtool docs to tools package
- Create a data subpackage
- Remove softwarepath from ini file

* Thu Dec 28 2006 XulChris <tkmame@retrogames.com> - 0111-1
- Initial release for Fedora
