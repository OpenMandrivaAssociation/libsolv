%define major 0
%define libname %mklibname solv %{major}
%define extlibname %mklibname solvext %{major}
%define devname %mklibname solv -d

Name: libsolv
Version: 0.6.21
Release: 3
Source0: https://github.com/openSUSE/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

# Backports from upstream
# https://github.com/openSUSE/libsolv/commit/fe64933a5c9125401f0ae3e928c406d19075c202
Patch0: libsolv-yumobs-remove-bogus-queue_empty-call.patch
# https://github.com/openSUSE/libsolv/commit/f96788c66542de33a08ed10b0383ad5e44b375d4
Patch1: libsolv-generic-system-release.patch

# OpenMandriva specific patches
Patch1000: libsolv-20140110-repo2solv-omv.patch
# Attempt to ignore DistEpoch for solver calculations
Patch1001: libsolv-ext-Ignore-DistEpoch-entirely.patch

Summary: Package dependency solver and repository storage system
URL: http://en.opensuse.org/openSUSE:Libzypp_satsolver
# See also: https://github.com/openSUSE/libsolv
License: MIT
Group: System/Libraries
BuildRequires: cmake
BuildRequires: pkgconfig(rpm)
BuildRequires: bzip2-devel
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(expat)

%description
Solving dependencies is the core functionality for any software management
application on Linux.

Dependancies are used to divide and share functionalities across multiple
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

%package -n %{libname}
Summary: Package dependency solver and repository storage system
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
Package dependency solver and repository storage system

%package -n %{extlibname}
Summary: Package dependency solver and repository storage system
Group: System/Libraries

%description -n %{extlibname}
Package dependency solver and repository storage system

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}
Requires: %{extlibname} = %{EVRD}
Provides: solv-devel = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%setup -q
%apply_patches

%build

# The parameters below are intended to ensure
# that the DNF stack works correctly on OpenMandriva
# The FEDORA switch sets some definitions up that aren't
# otherwise available. The RPM5 definition switches on
# support for RPM5 (without requiring patching).
%cmake \
	-DRPM5:BOOL=ON -DFEDORA=1 \
	-DENABLE_LZMA_COMPRESSION:BOOL=ON \
	-DENABLE_BZIP2_COMPRESSION:BOOL=ON \
	-DENABLE_COMPS:BOOL=ON \
	-DENABLE_HELIXREPO:BOOL=ON \
	-DENABLE_RPMDB:BOOL=ON \
	-DENABLE_RPMMD:BOOL=ON \
	-DENABLE_MDKREPO:BOOL=ON \
	-DENABLE_SUSEREPO:BOOL=ON

%make

%install
cd build
%makeinstall_std

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libsolv.so.%{major}

%files -n %{extlibname}
%{_libdir}/libsolvext.so.%{major}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/pkgconfig/libsolv.pc
%{_libdir}/*.so
%{_datadir}/cmake/Modules/FindLibSolv.cmake
%{_mandir}/man3/*
%{_mandir}/man1/*
