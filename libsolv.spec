# (ngompa) disable rpmlint to avoid terrible cyclic dependency problem in rpm5->rpm4 + python2->python3 transition
# remove after rpm5->rpm4 transition is complete
%undefine _build_pkgcheck_set
%undefine _build_pkgcheck_srpm
%undefine _nonzero_exit_pkgcheck_terminate_build
###

%define major 0
%define libname %mklibname solv %{major}
%define extlibname %mklibname solvext %{major}
%define devname %mklibname solv -d

Summary:	Package dependency solver and repository storage system
Name:		libsolv
Version:	0.6.34
Release:	1
License:	MIT
Group:		System/Libraries
# See also: https://github.com/openSUSE/libsolv
URL:		http://en.opensuse.org/openSUSE:Libzypp_satsolver
Source0:	https://github.com/openSUSE/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

# Backports from upstream
Patch0001:	0001-source-binary-rpm-detection-heuristic-when-ENABLE_RP.patch
Patch0002:	0002-Tweak-source-heuristic-in-ENABLE_RPMPKG_LIBRPM-case.patch
Patch0003:	0003-Remove-wrong-solv_free-data-vincore-in-repodata_inte.patch
Patch0004:	0004-bindings-expose-repodata_str2dir-repodata_dir2str-an.patch
Patch0005:	0005-Tweak-documentation-of-add_dirstr-method.patch
Patch0006:	0006-Fix-fp-double-close-work-around-some-false-positives.patch

# OpenMandriva patch for transitioning from RPM5
Patch1001:	1001-ext-Ignore-DistEpoch-entirely.patch
# ARMv8 support https://github.com/openSUSE/libsolv/pull/260
Patch1002:	https://github.com/openSUSE/libsolv/pull/260/commits/3c2b27fbf1c2e7b2d91c2b43a54dbcdf1771dcb0.patch
# znver1 support
Patch1003:	libsolv-0.6.34-znver1.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libxml-2.0)
BuildConflicts:	pkgconfig(rpm) >= 5
Requires:	gzip
Requires:	bzip2
Requires:	xz
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
Requires:	%{name} = %{EVRD}

%description -n %{libname}
Package dependency solver and repository storage system.

%package -n %{extlibname}
Summary:	Package dependency solver and repository storage system
Group:		System/Libraries

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
	-DENABLE_COMPLEX_DEPS:BOOL=ON \
	-DENABLE_RPMDB_BYRPMHEADER:BOOL=ON \
	-DENABLE_RPMDB_LIBRPM:BOOL=ON \
	-DENABLE_RPMPKG_LIBRPM:BOOL=ON \
	-DENABLE_LZMA_COMPRESSION:BOOL=ON \
	-DENABLE_BZIP2_COMPRESSION:BOOL=ON \
	-DENABLE_COMPS:BOOL=ON \
	-DENABLE_APPDATA:BOOL=ON \
	-DENABLE_HELIXREPO:BOOL=ON \
	-DENABLE_RPMDB:BOOL=ON \
	-DENABLE_COMPLEX_DEPS:BOOL=ON \
	-DENABLE_SUSEREPO:BOOL=ON

%build
%ninja_build -C build

%install
%ninja_install -C build

%files
%{_bindir}/*
%exclude %{_bindir}/solv
%{_mandir}/man1/*

files demo
%{_bindir}/solv

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
%{_mandir}/man3/*
