%define major 0
%define beta %{nil}
%define scmrev 20130619
%define libname %mklibname solv %{major}
%define extlibname %mklibname solvext %{major}
%define devname %mklibname solv -d

Name: libsolv
Version: 0.3.0
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 2
Source0: %{name}-%{version}.tar.bz2
%else
Release: 0.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release: 0.%{beta}.1
Source0: %{name}-%{version}%{beta}.tar.bz2
%else
Release: 0.%{beta}.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%endif
Patch0: libsolv-20130619-rpm5.patch
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
%if "%{scmrev}" == ""
%setup -q -n %{name}-%{version}%{beta}
%else
%setup -q -n %{name}
%endif
%apply_patches
%cmake \
	-DENABLE_RPM5:BOOL=ON \
	-DENABLE_BZIP2_COMPRESSION:BOOL=ON \
	-DENABLE_COMPS:BOOL=ON \
	-DENABLE_HELIXREPO:BOOL=ON \
	-DENABLE_LZMA_COMPRESSION:BOOL=ON \
	-DENABLE_MDKREPO:BOOL=ON \
	-DENABLE_RPM5:BOOL=ON \
	-DENABLE_RPMDB:BOOL=ON \
	-DENABLE_ENABLE_RPMDB_BYRPMHEADER:BOOL=ON \
	-DENABLE_RPMDB_PUBKEY:BOOL=ON \
	-DENABLE_RPMMD:BOOL=ON \
	-DENABLE_SUSEREPO:BOOL=ON

%build
cd build
%make

%install
cd build
%makeinstall_std

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libsolv.so.%{major}*

%files -n %{extlibname}
%{_libdir}/libsolvext.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/cmake/Modules/FindLibSolv.cmake
%{_mandir}/man3/*
