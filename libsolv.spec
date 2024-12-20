# (tpg) reduce bloat by excluding cmake requires on devel packages
%global __requires_exclude ^cmake.*$

%define major 1
%define oldlibname %mklibname solv 1
%define libname %mklibname solv
%define oldextlibname %mklibname solvext 1
%define extlibname %mklibname solvext
%define devname %mklibname solv -d

Summary:	Package dependency solver and repository storage system
Name:		libsolv
Version:	0.7.31
Release:	1
License:	MIT
Group:		System/Libraries
# See also: https://github.com/openSUSE/libsolv
URL:		https://en.opensuse.org/openSUSE:Libzypp_satsolver
Source0:	https://github.com/openSUSE/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
# OpenMandriva specific patches
## znver1 support
Patch1001:	libsolv-0.6.34-znver1.patch
Patch1002:	libsolv-fix-versionscript-check.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(zck)
Requires:	pigz
Requires:	pbzip2
Requires:	xz
Requires:	zchunk
Requires:	zstd
Requires:	coreutils
Requires:	findutils

%description
Solving dependencies is the core functionality for any software management
application on Linux.

Dependencies are used to divide and share functionalities across multiple
software elements.

Linux (and Unix) follows two basic concepts to implement Divide & Conquer -
breaking a large problem into smaller, more manageable ones.

* Make each program do one thing well. See Basics of the Unix Philosophy
  for details.
* Use shared libraries to share implementations and save disk and memory
  space

Every software package expresses the functionalities it provides to others
and those it requires from others through dependencies.

The task of the dependency resolver is to check and fulfill all these
relations when managing software.

Basic laws of resolving

The dependency solver tries to solve dependencies without user intervention
based on two basic rules

* Fulfill the install/remove requests given at start
* Keep the (dependencies of the) installed system consistent

Since the solver treats every package alike, these rules have some major and
sometimes unexpected implications. A broken dependency might result in
removal of lots of packages - the resulting system is still consistent
but highly unusable.

%package demo
Summary:	Package dependency solver and repository storage system
Group:		System/Libraries
Requires:	%{name} = %{EVRD}
Requires:	curl
Requires:	gnupg

%description demo
Applications demoing the %{name} library.

%package -n %{libname}
Summary:	Package dependency solver and repository storage system
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
Package dependency solver and repository storage system.

%package -n %{extlibname}
Summary:	Package dependency solver and repository storage system
Group:		System/Libraries
%rename %{oldextlibname}

%description -n %{extlibname}
Package dependency solver and repository storage system.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{extlibname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	solv-devel = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%autosetup -p1

# The parameters below are intended to ensure
# that the DNF stack works correctly on OpenMandriva
# The FEDORA switch sets some definitions up that aren't
# otherwise available.
%cmake -GNinja \
	-DFEDORA=1 \
	-DWITH_LIBXML2:BOOL=ON \
	-DWITH_SYSTEM_ZCHUNK:BOOL=ON \
	-DENABLE_COMPLEX_DEPS:BOOL=ON \
	-DENABLE_RPMMD=ON \
	-DENABLE_RPMDB=ON \
	-DENABLE_RPMDB_BYRPMHEADER:BOOL=ON \
	-DENABLE_RPMDB_LIBRPM:BOOL=ON \
	-DENABLE_RPMPKG_LIBRPM:BOOL=ON \
	-DENABLE_LZMA_COMPRESSION:BOOL=ON \
	-DENABLE_ZSTD_COMPRESSION:BOOL=ON \
	-DENABLE_ZCHUNK_COMPRESSION:BOOL=ON \
	-DENABLE_BZIP2_COMPRESSION:BOOL=ON \
	-DENABLE_COMPS:BOOL=ON \
	-DENABLE_APPDATA:BOOL=ON \
	-DENABLE_HELIXREPO:BOOL=ON \
	-DENABLE_SUSEREPO:BOOL=ON \
	-DPKG_CONFIG_EXECUTABLE:FILEPATH=%{_bindir}/pkg-config

%build
%ninja_build -C build

%install
%ninja_install -C build

%check
make ARGS=--output-on-failure test

%files
%{_bindir}/*
%exclude %{_bindir}/solv
%doc %{_mandir}/man1/*
%exclude %{_mandir}/man1/solv.1*

%files demo
%{_bindir}/solv
%doc %{_mandir}/man1/solv.1*

%files -n %{libname}
%{_libdir}/libsolv.so.%{major}

%files -n %{extlibname}
%{_libdir}/libsolvext.so.%{major}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/pkgconfig/libsolv.pc
%{_libdir}/pkgconfig/libsolvext.pc
%{_libdir}/*.so
%{_datadir}/cmake/Modules/FindLibSolv.cmake
%doc %{_mandir}/man3/*
