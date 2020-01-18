%define	mce_inject_last_git_commit 4cbe4632
%define aer_inject_last_git_commit 9bd5e2c7
%define mce_test_last_git_commit a4c080bd

Summary:	RAS Utilities
Name:		ras-utils
Version:	7.0
Release:	6%{?dist}
Group:		Development/Tools
License:	GPLv2
Source0:	mce-inject-%{mce_inject_last_git_commit}.tar.bz2
Source1:	aer-inject-%{aer_inject_last_git_commit}.tar.bz2
Source2:	mce-test-%{mce_test_last_git_commit}.tar.bz2
# URL for mce-inject
URL:		https://github.com/andikleen/mce-inject.git
# URL for aer-inject
#		git://git.kernel.org/pub/scm/linux/kernel/git/gong.chen/aer-inject.git
# URL for mce-test
#		git://git.kernel.org/pub/scm/utils/cpu/mce/mce-test.git
Buildroot:	%{_tmppath}/%{name}-%{version}-root
ExclusiveArch:	x86_64 aarch64 ppc64le
BuildRequires:	bison, flex

%description
This package contains both the PCIE AER Injection (aer-inject) and MCE
Injection (mce-inject) tools.  They can be used to insert software simulated
AER and MCE errors.

%prep
%setup -q -c -D -T
%setup -q -c -D -a 1
%setup -q -D -a 2

%build
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mkdir -p $RPM_BUILD_ROOT/%{_docdir}

%ifarch x86_64
(cd mce-inject-%{mce_inject_last_git_commit}; make)
%endif

(cd aer-inject-%{aer_inject_last_git_commit}; make)

%install
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/aer-inject-0.1

install -p -m700 aer-inject-%{aer_inject_last_git_commit}/aer-inject $RPM_BUILD_ROOT/%{_sbindir}/aer-inject
install -p -m644 aer-inject-%{aer_inject_last_git_commit}/README $RPM_BUILD_ROOT/%{_docdir}/aer-inject-0.1/README

%ifarch x86_64
mkdir -p $RPM_BUILD_ROOT/opt/mce-test
cp -R mce-test-%{mce_test_last_git_commit} $RPM_BUILD_ROOT/opt/mce-test

install -p -m700 mce-inject-%{mce_inject_last_git_commit}/mce-inject $RPM_BUILD_ROOT/%{_sbindir}/mce-inject

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m644 mce-inject-%{mce_inject_last_git_commit}/mce-inject.8 $RPM_BUILD_ROOT/%{_mandir}/man8/mce-inject.8
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_sbindir}/*
%{_docdir}/aer-inject-0.1/README
%ifarch x86_64
%{_mandir}/man8/*
/opt/mce-test
%endif

%changelog
* Mon Sep 15 2014 Prarit Bhargava <prarit@redhat.com> 7.0-6
- exclude mce from ppc64le [1125665]

* Mon Sep 15 2014 Prarit Bhargava <prarit@redhat.com> 7.0-5
- exclude mce from aarch64 [1070975]

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 7.0-2
- Mass rebuild 2013-12-27

* Mon Aug 12 2013 Prarit Bhargava <prarit@redhat.com>
- Initial import from git://git.kernel.org/pub/scm/utils/cpu/mce/mce-test.git
- updated mce-inject to commit 4cbe4632
* Wed May 15 2013 Prarit Bhargava <prarit@redhat.com>
- Initial import from https://github.com/andikleen/mce-inject.git
- Initial import from git://git.kernel.org/pub/scm/linux/kernel/git/gong.chen/aer-inject.git
