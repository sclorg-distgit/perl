%{?scl:%scl_package perl}

%global perl_version    5.24.0
%global perl_epoch      4
%global perl_arch_stem -thread-multi
%global perl_archname %{_arch}-%{_os}%{perl_arch_stem}

%global multilib_64_archs aarch64 %{power64} s390x sparc64 x86_64
%global parallel_tests 1
%global tapsetdir   %{_datadir}/systemtap/tapset

%global dual_life 0
%global rebuild_from_scratch 1

%if ! ( 0%{?rhel} && 0%{?rhel} < 7 )
# This overrides filters from build root (/usr/lib/rpm/macros.d/macros.perl)
# intentionally (unversioned perl(DB) is removed and versioned one is kept).
# Filter provides from *.pl files, bug #924938
%global __provides_exclude_from .*%{_docdir}|.*%{perl_archlib}/.*\\.pl$|.*%{perl_privlib}/.*\\.pl$
%global __requires_exclude_from %{_docdir}
%global __provides_exclude perl\\((VMS|Win32|BSD::|DB\\)$)
%global __requires_exclude perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here)
# same as we provide in /usr/lib/rpm/macros.d/macros.perl

%endif

%global perl5_testdir   %{_libexecdir}/perl5-tests

# We can bootstrap without gdbm
%bcond_without gdbm
# We can skip %%check phase
%bcond_without test

Name:           %{?scl_prefix}perl
Version:        %{perl_version}
# release number must be even higher, because dual-lived modules will be broken otherwise
Release:        375%{?dist}
Epoch:          %{perl_epoch}
Summary:        Practical Extraction and Report Language
Group:          Development/Languages
# These are all found licenses. They are distributed among various
# subpackages.
# dist/Tie-File/lib/Tie/File.pm:        GPLv2+ or Artistic
# cpan/Getopt-Long/lib/Getopt/Long.pm:  GPLv2+ or Artistic
# lib/unicore:                          UCD
# ext/SDBM_File/sdbm.{c,h}:             Public domain
# regexec.c, regcomp.c:                 HSLR
# time64.c:                             MIT
# pod/perlunicook.pod:                  (GPL+ or Artistic) and Public Domain
# pod/perlgpl.pod:                      GPL text
# pod/perlartistic.pod:                 Artistic text
# ext/File-Glob/bsd_glob.{c,h}:         BSD
# Other files:                          GPL+ or Artistic
## Unbundled
# cpan/Compress-Raw-Bzip2/bzip2-src:    BSD
# cpan/Compress-Raw-Zlib/zlib-src:      zlib
## perl sub-package notice
# perluniprops.pod is generated from lib/unicore sources:   UCD
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and BSD and Public Domain and UCD
Url:            http://www.perl.org/
Source0:        http://www.cpan.org/src/5.0/perl-%{perl_version}.tar.bz2
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
Source3:        macros.perl-rh6
%else
Source3:        macros.perl
%endif
#Systemtap tapset and example that make use of systemtap-sdt-devel
# build requirement. Written by lberk; Not yet upstream.
Source4:        perl.stp
Source5:        perl-example.stp
# Tom Christiansen confirms Pod::Html uses the same license as perl
Source6:        Pod-Html-license-clarification

# Pregenerated dependencies for bootstrap.
# If your RPM tool fails on including the source file, then you forgot to
# define _sourcedir macro to point to the directory with the sources.
Source7:        gendep.macros
%if %{defined perl_bootstrap}
%global gendep_perl \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.0.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.10.1 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.3.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.7.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.7.3 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.9.1 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.9.4 \
Requires: %{?scl_prefix}perl(B) \
Requires: %{?scl_prefix}perl(B::Concise) \
Requires: %{?scl_prefix}perl(B::Op_private) \
Requires: %{?scl_prefix}perl(B::Terse) \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Class::Struct) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(ExtUtils::Constant::Base) \
Requires: %{?scl_prefix}perl(ExtUtils::Constant::Utils) \
Requires: %{?scl_prefix}perl(ExtUtils::Constant::XS) \
Requires: %{?scl_prefix}perl(Fcntl) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Path) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(File::Spec::Functions) \
Requires: %{?scl_prefix}perl(I18N::LangTags) \
Requires: %{?scl_prefix}perl(IO::File) \
Requires: %{?scl_prefix}perl(IPC::Open3) \
Requires: %{?scl_prefix}perl(Opcode) >= 1.01 \
Requires: %{?scl_prefix}perl(POSIX) \
Requires: %{?scl_prefix}perl(Scalar::Util) >= 1.10 \
Requires: %{?scl_prefix}perl(Symbol) \
Requires: %{?scl_prefix}perl(Text::Tabs) \
Requires: %{?scl_prefix}perl(Text::Wrap) \
Requires: %{?scl_prefix}perl(Tie::Handle) \
Requires: %{?scl_prefix}perl(Tie::Hash) \
Requires: %{?scl_prefix}perl(Tie::StdHandle) \
Requires: %{?scl_prefix}perl(Time::tm) \
Requires: %{?scl_prefix}perl(Unicode::Normalize) \
Requires: %{?scl_prefix}perl(XSLoader) \
Requires: %{?scl_prefix}perl(_charnames) \
Requires: %{?scl_prefix}perl(bytes) \
Requires: %{?scl_prefix}perl(charnames) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(feature) \
Requires: %{?scl_prefix}perl(if) \
Requires: %{?scl_prefix}perl(integer) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(parent) \
Requires: %{?scl_prefix}perl(re) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(subs) \
Requires: %{?scl_prefix}perl(threads) \
Requires: %{?scl_prefix}perl(threads::shared) \
Requires: %{?scl_prefix}perl(unicore::Name) \
Requires: %{?scl_prefix}perl(utf8) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Requires: %{?scl_prefix}perl(warnings::register) \
Provides: %{?scl_prefix}perl(AnyDBM_File) = 1.01 \
Provides: %{?scl_prefix}perl(AutoLoader) = 5.74 \
Provides: %{?scl_prefix}perl(AutoSplit) = 1.06 \
Provides: %{?scl_prefix}perl(B) = 1.62 \
Provides: %{?scl_prefix}perl(B::Concise) = 0.996 \
Provides: %{?scl_prefix}perl(B::Deparse) = 1.37 \
Provides: %{?scl_prefix}perl(B::OBJECT) \
Provides: %{?scl_prefix}perl(B::Op_private) = 5.024000 \
Provides: %{?scl_prefix}perl(B::Showlex) = 1.05 \
Provides: %{?scl_prefix}perl(B::Terse) = 1.06 \
Provides: %{?scl_prefix}perl(B::Xref) = 1.05 \
Provides: %{?scl_prefix}perl(Benchmark) = 1.22 \
Provides: %{?scl_prefix}perl(Class::Struct) = 0.65 \
Provides: %{?scl_prefix}perl(Class::Struct::Tie_ISA) \
Provides: %{?scl_prefix}perl(Config) = 5.024000 \
Provides: %{?scl_prefix}perl(Config::Extensions) = 0.01 \
Provides: %{?scl_prefix}perl(DB) = 1.08 \
Provides: %{?scl_prefix}perl(DBM_Filter) = 0.06 \
Provides: %{?scl_prefix}perl(DBM_Filter::compress) = 0.03 \
Provides: %{?scl_prefix}perl(DBM_Filter::encode) = 0.03 \
Provides: %{?scl_prefix}perl(DBM_Filter::int32) = 0.03 \
Provides: %{?scl_prefix}perl(DBM_Filter::null) = 0.03 \
Provides: %{?scl_prefix}perl(DBM_Filter::utf8) = 0.03 \
Provides: %{?scl_prefix}perl(DirHandle) = 1.04 \
Provides: %{?scl_prefix}perl(Dumpvalue) = 1.18 \
Provides: %{?scl_prefix}perl(DynaLoader) = 1.38 \
Provides: %{?scl_prefix}perl(EVERY) \
Provides: %{?scl_prefix}perl(EVERY::LAST) \
Provides: %{?scl_prefix}perl(English) = 1.10 \
Provides: %{?scl_prefix}perl(ExtUtils::Constant) = 0.23 \
Provides: %{?scl_prefix}perl(ExtUtils::Constant::Base) = 0.05 \
Provides: %{?scl_prefix}perl(ExtUtils::Constant::ProxySubs) = 0.08 \
Provides: %{?scl_prefix}perl(ExtUtils::Constant::Utils) = 0.03 \
Provides: %{?scl_prefix}perl(ExtUtils::Constant::XS) = 0.03 \
Provides: %{?scl_prefix}perl(Fcntl) = 1.13 \
Provides: %{?scl_prefix}perl(File::Basename) = 2.85 \
Provides: %{?scl_prefix}perl(File::Compare) = 1.1006 \
Provides: %{?scl_prefix}perl(File::Copy) = 2.31 \
Provides: %{?scl_prefix}perl(File::DosGlob) = 1.12 \
Provides: %{?scl_prefix}perl(File::Find) = 1.34 \
Provides: %{?scl_prefix}perl(File::Glob) = 1.26 \
Provides: %{?scl_prefix}perl(File::stat) = 1.07 \
Provides: %{?scl_prefix}perl(FileCache) = 1.09 \
Provides: %{?scl_prefix}perl(FileHandle) = 2.02 \
Provides: %{?scl_prefix}perl(FindBin) = 1.51 \
Provides: %{?scl_prefix}perl(GDBM_File) = 1.15 \
Provides: %{?scl_prefix}perl(Getopt::Std) = 1.11 \
Provides: %{?scl_prefix}perl(Hash::Util) = 0.19 \
Provides: %{?scl_prefix}perl(Hash::Util::FieldHash) = 1.19 \
Provides: %{?scl_prefix}perl(I18N::Collate) = 1.02 \
Provides: %{?scl_prefix}perl(I18N::LangTags) = 0.40 \
Provides: %{?scl_prefix}perl(I18N::LangTags::Detect) = 1.05 \
Provides: %{?scl_prefix}perl(I18N::LangTags::List) = 0.39 \
Provides: %{?scl_prefix}perl(I18N::Langinfo) = 0.13 \
Provides: %{?scl_prefix}perl(IPC::Open2) = 1.04 \
Provides: %{?scl_prefix}perl(IPC::Open3) = 1.20 \
Provides: %{?scl_prefix}perl(NDBM_File) = 1.14 \
Provides: %{?scl_prefix}perl(NEXT) = 0.65 \
Provides: %{?scl_prefix}perl(NEXT::ACTUAL) \
Provides: %{?scl_prefix}perl(NEXT::ACTUAL::DISTINCT) \
Provides: %{?scl_prefix}perl(NEXT::ACTUAL::UNSEEN) \
Provides: %{?scl_prefix}perl(NEXT::DISTINCT) \
Provides: %{?scl_prefix}perl(NEXT::DISTINCT::ACTUAL) \
Provides: %{?scl_prefix}perl(NEXT::UNSEEN) \
Provides: %{?scl_prefix}perl(NEXT::UNSEEN::ACTUAL) \
Provides: %{?scl_prefix}perl(Net::hostent) = 1.01 \
Provides: %{?scl_prefix}perl(Net::netent) = 1.00 \
Provides: %{?scl_prefix}perl(Net::protoent) = 1.00 \
Provides: %{?scl_prefix}perl(Net::servent) = 1.01 \
Provides: %{?scl_prefix}perl(O) = 1.01 \
Provides: %{?scl_prefix}perl(ODBM_File) = 1.14 \
Provides: %{?scl_prefix}perl(Opcode) = 1.34 \
Provides: %{?scl_prefix}perl(POSIX) = 1.65 \
Provides: %{?scl_prefix}perl(POSIX::SigAction) \
Provides: %{?scl_prefix}perl(POSIX::SigRt) \
Provides: %{?scl_prefix}perl(POSIX::SigSet) \
Provides: %{?scl_prefix}perl(PerlIO) = 1.09 \
Provides: %{?scl_prefix}perl(PerlIO::encoding) = 0.24 \
Provides: %{?scl_prefix}perl(PerlIO::mmap) = 0.016 \
Provides: %{?scl_prefix}perl(PerlIO::scalar) = 0.24 \
Provides: %{?scl_prefix}perl(PerlIO::via) = 0.16 \
Provides: %{?scl_prefix}perl(Pod::Functions) = 1.10 \
Provides: %{?scl_prefix}perl(SDBM_File) = 1.14 \
Provides: %{?scl_prefix}perl(Safe) = 2.39 \
Provides: %{?scl_prefix}perl(Search::Dict) = 1.07 \
Provides: %{?scl_prefix}perl(SelectSaver) = 1.02 \
Provides: %{?scl_prefix}perl(Symbol) = 1.07 \
Provides: %{?scl_prefix}perl(Sys::Hostname) = 1.20 \
Provides: %{?scl_prefix}perl(Term::Complete) = 1.403 \
Provides: %{?scl_prefix}perl(Term::ReadLine) = 1.15 \
Provides: %{?scl_prefix}perl(Term::ReadLine::Stub) \
Provides: %{?scl_prefix}perl(Term::ReadLine::TermCap) \
Provides: %{?scl_prefix}perl(Term::ReadLine::Tk) \
Provides: %{?scl_prefix}perl(Text::Abbrev) = 1.02 \
Provides: %{?scl_prefix}perl(Thread) = 3.04 \
Provides: %{?scl_prefix}perl(Thread::Semaphore) = 2.12 \
Provides: %{?scl_prefix}perl(Tie::Array) = 1.06 \
Provides: %{?scl_prefix}perl(Tie::ExtraHash) \
Provides: %{?scl_prefix}perl(Tie::File) = 1.02 \
Provides: %{?scl_prefix}perl(Tie::File::Cache) \
Provides: %{?scl_prefix}perl(Tie::File::Heap) \
Provides: %{?scl_prefix}perl(Tie::Handle) = 4.2 \
Provides: %{?scl_prefix}perl(Tie::Hash) \
Provides: %{?scl_prefix}perl(Tie::Hash) = 1.05 \
Provides: %{?scl_prefix}perl(Tie::Hash::NamedCapture) = 0.09 \
Provides: %{?scl_prefix}perl(Tie::Memoize) = 1.1 \
Provides: %{?scl_prefix}perl(Tie::RefHash) = 1.39 \
Provides: %{?scl_prefix}perl(Tie::RefHash::Nestable) \
Provides: %{?scl_prefix}perl(Tie::Scalar) = 1.04 \
Provides: %{?scl_prefix}perl(Tie::StdArray) \
Provides: %{?scl_prefix}perl(Tie::StdHandle) = 4.4 \
Provides: %{?scl_prefix}perl(Tie::StdHash) \
Provides: %{?scl_prefix}perl(Tie::StdScalar) \
Provides: %{?scl_prefix}perl(Tie::SubstrHash) = 1.00 \
Provides: %{?scl_prefix}perl(Time::gmtime) = 1.03 \
Provides: %{?scl_prefix}perl(Time::localtime) = 1.02 \
Provides: %{?scl_prefix}perl(Time::tm) = 1.00 \
Provides: %{?scl_prefix}perl(UNIVERSAL) = 1.13 \
Provides: %{?scl_prefix}perl(Unicode::UCD) = 0.64 \
Provides: %{?scl_prefix}perl(User::grent) = 1.01 \
Provides: %{?scl_prefix}perl(User::pwent) = 1.00 \
Provides: %{?scl_prefix}perl(_charnames) = 1.43 \
Provides: %{?scl_prefix}perl(arybase) = 0.11 \
Provides: %{?scl_prefix}perl(attributes) = 0.27 \
Provides: %{?scl_prefix}perl(autouse) = 1.11 \
Provides: %{?scl_prefix}perl(base) = 2.23 \
Provides: %{?scl_prefix}perl(blib) = 1.06 \
Provides: %{?scl_prefix}perl(bytes) = 1.05 \
Provides: %{?scl_prefix}perl(bytes_heavy.pl) \
Provides: %{?scl_prefix}perl(charnames) = 1.43 \
Provides: %{?scl_prefix}perl(deprecate) = 0.03 \
Provides: %{?scl_prefix}perl(diagnostics) = 1.34 \
Provides: %{?scl_prefix}perl(dumpvar.pl) \
Provides: %{?scl_prefix}perl(encoding::warnings) = 0.12 \
Provides: %{?scl_prefix}perl(feature) = 1.42 \
Provides: %{?scl_prefix}perl(fields) = 2.23 \
Provides: %{?scl_prefix}perl(filetest) = 1.03 \
Provides: %{?scl_prefix}perl(if) = 0.0606 \
Provides: %{?scl_prefix}perl(less) = 0.03 \
Provides: %{?scl_prefix}perl(lib) = 0.63 \
Provides: %{?scl_prefix}perl(locale) = 1.09 \
Provides: %{?scl_prefix}perl(mro) = 1.18 \
Provides: %{?scl_prefix}perl(ops) = 1.02 \
Provides: %{?scl_prefix}perl(overload) = 1.26 \
Provides: %{?scl_prefix}perl(overload::numbers) \
Provides: %{?scl_prefix}perl(overloading) = 0.02 \
Provides: %{?scl_prefix}perl(perl5db.pl) \
Provides: %{?scl_prefix}perl(sigtrap) = 1.08 \
Provides: %{?scl_prefix}perl(sort) = 2.02 \
Provides: %{?scl_prefix}perl(subs) = 1.02 \
Provides: %{?scl_prefix}perl(vars) = 1.03 \
Provides: %{?scl_prefix}perl(vmsish) = 1.04 \
Provides: %{?scl_prefix}perl(warnings::register) = 1.04 \
Provides: %{?scl_prefix}perl(x86-64) = 4:5.24.0-364.fc25 \
%{nil}
%global gendep_perl_Archive_Tar \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(Archive::Tar) \
Requires: %{?scl_prefix}perl(Archive::Tar::Constant) \
Requires: %{?scl_prefix}perl(Archive::Tar::File) \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(Data::Dumper) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Find) \
Requires: %{?scl_prefix}perl(File::Path) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(File::Spec::Unix) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(Getopt::Std) \
Requires: %{?scl_prefix}perl(IO::File) \
Requires: %{?scl_prefix}perl(IO::Handle) \
Requires: %{?scl_prefix}perl(IO::Zlib) \
Requires: %{?scl_prefix}perl(Pod::Usage) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Archive::Tar) = 2.04 \
Provides: %{?scl_prefix}perl(Archive::Tar::Constant) = 2.04 \
Provides: %{?scl_prefix}perl(Archive::Tar::File) = 2.04 \
%{nil}
%global gendep_perl_Attribute_Handlers \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Attribute::Handlers) = 0.99 \
%{nil}
%global gendep_perl_B_Debug \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(B) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(strict) \
Provides: %{?scl_prefix}perl(B::Debug) = 1.23 \
%{nil}
%global gendep_perl_CPAN \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(App::Cpan) \
Requires: %{?scl_prefix}perl(CPAN) >= 1.80 \
Requires: %{?scl_prefix}perl(CPAN::Author) \
Requires: %{?scl_prefix}perl(CPAN::Bundle) \
Requires: %{?scl_prefix}perl(CPAN::CacheMgr) \
Requires: %{?scl_prefix}perl(CPAN::Complete) \
Requires: %{?scl_prefix}perl(CPAN::Debug) \
Requires: %{?scl_prefix}perl(CPAN::DeferredCode) \
Requires: %{?scl_prefix}perl(CPAN::Distribution) \
Requires: %{?scl_prefix}perl(CPAN::Distroprefs) \
Requires: %{?scl_prefix}perl(CPAN::Distrostatus) \
Requires: %{?scl_prefix}perl(CPAN::Exception::RecursiveDependency) \
Requires: %{?scl_prefix}perl(CPAN::Exception::yaml_not_installed) \
Requires: %{?scl_prefix}perl(CPAN::Exception::yaml_process_error) \
Requires: %{?scl_prefix}perl(CPAN::FTP) \
Requires: %{?scl_prefix}perl(CPAN::FTP::netrc) \
Requires: %{?scl_prefix}perl(CPAN::HTTP::Credentials) \
Requires: %{?scl_prefix}perl(CPAN::HandleConfig) \
Requires: %{?scl_prefix}perl(CPAN::Index) >= 1.93 \
Requires: %{?scl_prefix}perl(CPAN::InfoObj) \
Requires: %{?scl_prefix}perl(CPAN::LWP::UserAgent) \
Requires: %{?scl_prefix}perl(CPAN::Mirrors) \
Requires: %{?scl_prefix}perl(CPAN::Module) \
Requires: %{?scl_prefix}perl(CPAN::Prompt) \
Requires: %{?scl_prefix}perl(CPAN::Queue) \
Requires: %{?scl_prefix}perl(CPAN::Shell) \
Requires: %{?scl_prefix}perl(CPAN::Tarzip) \
Requires: %{?scl_prefix}perl(CPAN::URL) \
Requires: %{?scl_prefix}perl(CPAN::Version) \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(DirHandle) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(ExtUtils::MakeMaker) \
Requires: %{?scl_prefix}perl(Fcntl) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Copy) \
Requires: %{?scl_prefix}perl(File::Find) \
Requires: %{?scl_prefix}perl(File::Path) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(File::Spec::Functions) \
Requires: %{?scl_prefix}perl(FileHandle) \
Requires: %{?scl_prefix}perl(Getopt::Std) \
Requires: %{?scl_prefix}perl(HTTP::Tiny) >= 0.005 \
Requires: %{?scl_prefix}perl(Net::Ping) \
Requires: %{?scl_prefix}perl(Safe) \
Requires: %{?scl_prefix}perl(Sys::Hostname) \
Requires: %{?scl_prefix}perl(Text::ParseWords) \
Requires: %{?scl_prefix}perl(Text::Wrap) \
Requires: %{?scl_prefix}perl(autouse) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(if) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(App::Cpan) = 1.63 \
Provides: %{?scl_prefix}perl(CPAN) = 2.11 \
Provides: %{?scl_prefix}perl(CPAN::Author) = 5.5002 \
Provides: %{?scl_prefix}perl(CPAN::Bundle) = 5.5001 \
Provides: %{?scl_prefix}perl(CPAN::CacheMgr) = 5.5002 \
Provides: %{?scl_prefix}perl(CPAN::Complete) = 5.5001 \
Provides: %{?scl_prefix}perl(CPAN::Debug) = 5.5001 \
Provides: %{?scl_prefix}perl(CPAN::DeferredCode) = 5.50 \
Provides: %{?scl_prefix}perl(CPAN::Distribution) = 2.04 \
Provides: %{?scl_prefix}perl(CPAN::Distroprefs) = 6.0001 \
Provides: %{?scl_prefix}perl(CPAN::Distroprefs::Iterator) \
Provides: %{?scl_prefix}perl(CPAN::Distroprefs::Pref) \
Provides: %{?scl_prefix}perl(CPAN::Distroprefs::Result) \
Provides: %{?scl_prefix}perl(CPAN::Distroprefs::Result::Error) \
Provides: %{?scl_prefix}perl(CPAN::Distroprefs::Result::Fatal) \
Provides: %{?scl_prefix}perl(CPAN::Distroprefs::Result::Success) \
Provides: %{?scl_prefix}perl(CPAN::Distroprefs::Result::Warning) \
Provides: %{?scl_prefix}perl(CPAN::Distrostatus) = 5.5 \
Provides: %{?scl_prefix}perl(CPAN::Eval) \
Provides: %{?scl_prefix}perl(CPAN::Exception::RecursiveDependency) = 5.5 \
Provides: %{?scl_prefix}perl(CPAN::Exception::blocked_urllist) = 1.001 \
Provides: %{?scl_prefix}perl(CPAN::Exception::yaml_not_installed) = 5.5 \
Provides: %{?scl_prefix}perl(CPAN::Exception::yaml_process_error) = 5.5 \
Provides: %{?scl_prefix}perl(CPAN::FTP) = 5.5006 \
Provides: %{?scl_prefix}perl(CPAN::FTP::netrc) = 1.01 \
Provides: %{?scl_prefix}perl(CPAN::FirstTime) = 5.5307 \
Provides: %{?scl_prefix}perl(CPAN::HTTP::Client) = 1.9601 \
Provides: %{?scl_prefix}perl(CPAN::HTTP::Credentials) = 1.9601 \
Provides: %{?scl_prefix}perl(CPAN::HandleConfig) = 5.5006 \
Provides: %{?scl_prefix}perl(CPAN::Index) = 1.9601 \
Provides: %{?scl_prefix}perl(CPAN::InfoObj) = 5.5 \
Provides: %{?scl_prefix}perl(CPAN::Kwalify) = 5.50 \
Provides: %{?scl_prefix}perl(CPAN::LWP::UserAgent) = 1.9601 \
Provides: %{?scl_prefix}perl(CPAN::Mirrored::By) \
Provides: %{?scl_prefix}perl(CPAN::Mirrors) = 1.9601 \
Provides: %{?scl_prefix}perl(CPAN::Module) = 5.5002 \
Provides: %{?scl_prefix}perl(CPAN::Nox) = 5.5001 \
Provides: %{?scl_prefix}perl(CPAN::Plugin) = 0.95 \
Provides: %{?scl_prefix}perl(CPAN::Plugin::Specfile) = 0.01 \
Provides: %{?scl_prefix}perl(CPAN::Prompt) = 5.5 \
Provides: %{?scl_prefix}perl(CPAN::Queue) = 5.5002 \
Provides: %{?scl_prefix}perl(CPAN::Queue::Item) \
Provides: %{?scl_prefix}perl(CPAN::Shell) = 5.5005 \
Provides: %{?scl_prefix}perl(CPAN::Tarzip) = 5.5012 \
Provides: %{?scl_prefix}perl(CPAN::URL) = 5.5 \
Provides: %{?scl_prefix}perl(CPAN::Version) = 5.5003 \
%{nil}
%global gendep_perl_CPAN_Meta \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(CPAN::Meta::Converter) >= 2.141170 \
Requires: %{?scl_prefix}perl(CPAN::Meta::Feature) \
Requires: %{?scl_prefix}perl(CPAN::Meta::Prereqs) \
Requires: %{?scl_prefix}perl(CPAN::Meta::Requirements) >= 2.121 \
Requires: %{?scl_prefix}perl(CPAN::Meta::Validator) \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Parse::CPAN::Meta) >= 1.4400 \
Requires: %{?scl_prefix}perl(Parse::CPAN::Meta) >= 1.4414 \
Requires: %{?scl_prefix}perl(Scalar::Util) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(CPAN::Meta) = 2.150005 \
Provides: %{?scl_prefix}perl(CPAN::Meta::Converter) = 2.150005 \
Provides: %{?scl_prefix}perl(CPAN::Meta::Feature) = 2.150005 \
Provides: %{?scl_prefix}perl(CPAN::Meta::History) = 2.150005 \
Provides: %{?scl_prefix}perl(CPAN::Meta::Merge) = 2.150005 \
Provides: %{?scl_prefix}perl(CPAN::Meta::Prereqs) = 2.150005 \
Provides: %{?scl_prefix}perl(CPAN::Meta::Spec) = 2.150005 \
Provides: %{?scl_prefix}perl(CPAN::Meta::Validator) = 2.150005 \
%{nil}
%global gendep_perl_CPAN_Meta_Requirements \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(CPAN::Meta::Requirements) = 2.132000 \
%{nil}
%global gendep_perl_CPAN_Meta_YAML \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.1 \
Requires: %{?scl_prefix}perl(B) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Scalar::Util) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(CPAN::Meta::YAML) = 0.018 \
%{nil}
%global gendep_perl_Carp \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Carp) = 1.40 \
Provides: %{?scl_prefix}perl(Carp::Heavy) = 1.40 \
Provides: %{?scl_prefix}perl(Carp::Heavy) = 1.40 \
%{nil}
%global gendep_perl_Compress_Raw_Bzip2 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(bytes) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Compress::Raw::Bzip2) = 2.069 \
%{nil}
%global gendep_perl_Compress_Raw_Zlib \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(bytes) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Compress::Raw::Zlib) = 2.069 \
%{nil}
%global gendep_perl_Config_Perl_V \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Config::Perl::V) = 0.25 \
%{nil}
%global gendep_perl_DB_File \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.3 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(Tie::Hash) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(DB_File) = 1.835 \
Provides: %{?scl_prefix}perl(DB_File::BTREEINFO) \
Provides: %{?scl_prefix}perl(DB_File::HASHINFO) \
Provides: %{?scl_prefix}perl(DB_File::RECNOINFO) \
%{nil}
%global gendep_perl_Data_Dumper \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(overload) \
Provides: %{?scl_prefix}perl(Data::Dumper) = 2.160 \
%{nil}
%global gendep_perl_Devel_PPPort \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Devel::PPPort) = 3.32 \
%{nil}
%global gendep_perl_Devel_Peek \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(XSLoader) \
Provides: %{?scl_prefix}perl(Devel::Peek) = 1.23 \
%{nil}
%global gendep_perl_Devel_SelfStubber \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(SelfLoader) \
Provides: %{?scl_prefix}perl(Devel::SelfStubber) = 1.05 \
%{nil}
%global gendep_perl_Digest \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Digest) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Digest) = 1.17 \
Provides: %{?scl_prefix}perl(Digest::base) = 1.16 \
Provides: %{?scl_prefix}perl(Digest::file) = 1.16 \
%{nil}
%global gendep_perl_Digest_MD5 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Digest::MD5) = 2.54 \
%{nil}
%global gendep_perl_Digest_SHA \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.3.0 \
Requires: %{?scl_prefix}perl(DynaLoader) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Fcntl) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(integer) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Digest::SHA) = 5.95 \
%{nil}
%global gendep_perl_Encode \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.1 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Encode) \
Requires: %{?scl_prefix}perl(Encode::Alias) \
Requires: %{?scl_prefix}perl(Encode::CJKConstants) \
Requires: %{?scl_prefix}perl(Encode::CN::HZ) \
Requires: %{?scl_prefix}perl(Encode::Config) \
Requires: %{?scl_prefix}perl(Encode::Encoding) \
Requires: %{?scl_prefix}perl(Encode::Guess) \
Requires: %{?scl_prefix}perl(Encode::JP::JIS7) \
Requires: %{?scl_prefix}perl(Encode::KR::2022_KR) \
Requires: %{?scl_prefix}perl(Encode::MIME::Header) \
Requires: %{?scl_prefix}perl(Encode::Unicode) \
Requires: %{?scl_prefix}perl(Exporter) >= 5.57 \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(Getopt::Std) \
Requires: %{?scl_prefix}perl(MIME::Base64) \
Requires: %{?scl_prefix}perl(XSLoader) \
Requires: %{?scl_prefix}perl(bytes) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(parent) \
Requires: %{?scl_prefix}perl(re) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(utf8) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Encode) = 2.80 \
Provides: %{?scl_prefix}perl(Encode::Alias) = 2.20 \
Provides: %{?scl_prefix}perl(Encode::Byte) = 2.4 \
Provides: %{?scl_prefix}perl(Encode::CJKConstants) = 2.2 \
Provides: %{?scl_prefix}perl(Encode::CN) = 2.3 \
Provides: %{?scl_prefix}perl(Encode::CN::HZ) = 2.7 \
Provides: %{?scl_prefix}perl(Encode::Config) = 2.5 \
Provides: %{?scl_prefix}perl(Encode::EBCDIC) = 2.2 \
Provides: %{?scl_prefix}perl(Encode::Encoder) = 2.3 \
Provides: %{?scl_prefix}perl(Encode::Encoding) = 2.7 \
Provides: %{?scl_prefix}perl(Encode::GSM0338) = 2.5 \
Provides: %{?scl_prefix}perl(Encode::Guess) = 2.6 \
Provides: %{?scl_prefix}perl(Encode::Internal) \
Provides: %{?scl_prefix}perl(Encode::JP) = 2.4 \
Provides: %{?scl_prefix}perl(Encode::JP::H2Z) = 2.2 \
Provides: %{?scl_prefix}perl(Encode::JP::JIS7) = 2.5 \
Provides: %{?scl_prefix}perl(Encode::KR) = 2.3 \
Provides: %{?scl_prefix}perl(Encode::KR::2022_KR) = 2.3 \
Provides: %{?scl_prefix}perl(Encode::MIME::Header) = 2.19 \
Provides: %{?scl_prefix}perl(Encode::MIME::Header::ISO_2022_JP) = 1.4 \
Provides: %{?scl_prefix}perl(Encode::MIME::Name) = 1.1 \
Provides: %{?scl_prefix}perl(Encode::Symbol) = 2.2 \
Provides: %{?scl_prefix}perl(Encode::TW) = 2.3 \
Provides: %{?scl_prefix}perl(Encode::UTF_EBCDIC) \
Provides: %{?scl_prefix}perl(Encode::Unicode) = 2.15 \
Provides: %{?scl_prefix}perl(Encode::Unicode::UTF7) = 2.8 \
Provides: %{?scl_prefix}perl(Encode::XS) \
Provides: %{?scl_prefix}perl(Encode::utf8) \
%{nil}
%global gendep_perl_Encode_devel \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(File::Find) \
Requires: %{?scl_prefix}perl(Getopt::Std) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
%{nil}
%global gendep_perl_Env \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Tie::Array) \
Provides: %{?scl_prefix}perl(Env) = 1.04 \
Provides: %{?scl_prefix}perl(Env::Array) \
Provides: %{?scl_prefix}perl(Env::Array::VMS) \
%{nil}
%global gendep_perl_Errno \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Provides: %{?scl_prefix}perl(Errno) = 1.25 \
%{nil}
%global gendep_perl_Exporter \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Provides: %{?scl_prefix}perl(Exporter) = 5.72 \
Provides: %{?scl_prefix}perl(Exporter::Heavy) \
%{nil}
%global gendep_perl_ExtUtils_CBuilder \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(ExtUtils::CBuilder::Base) \
Requires: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::Unix) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Path) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(File::Spec::Functions) \
Requires: %{?scl_prefix}perl(File::Temp) \
Requires: %{?scl_prefix}perl(IO::File) \
Requires: %{?scl_prefix}perl(IPC::Cmd) \
Requires: %{?scl_prefix}perl(Perl::OSType) \
Requires: %{?scl_prefix}perl(Text::ParseWords) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Base) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::Unix) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::VMS) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::Windows) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::Windows::BCC) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::Windows::GCC) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::Windows::MSVC) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::aix) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::android) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::cygwin) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::darwin) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::dec_osf) = 0.280225 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::linux) = 0.280206 \
Provides: %{?scl_prefix}perl(ExtUtils::CBuilder::Platform::os2) = 0.280225 \
%{nil}
%global gendep_perl_ExtUtils_Command \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.30 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(ExtUtils::Command) = 7.10 \
%{nil}
%global gendep_perl_ExtUtils_Embed \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(ExtUtils::Embed) = 1.33 \
%{nil}
%global gendep_perl_ExtUtils_Install \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.30 \
Requires: %{?scl_prefix}perl(AutoSplit) \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(ExtUtils::MakeMaker) \
Requires: %{?scl_prefix}perl(ExtUtils::Packlist) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Compare) \
Requires: %{?scl_prefix}perl(File::Copy) \
Requires: %{?scl_prefix}perl(File::Find) \
Requires: %{?scl_prefix}perl(File::Path) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(ExtUtils::Install) = 2.04 \
Provides: %{?scl_prefix}perl(ExtUtils::Install::Warn) \
Provides: %{?scl_prefix}perl(ExtUtils::Installed) = 2.04 \
Provides: %{?scl_prefix}perl(ExtUtils::Packlist) = 2.04 \
%{nil}
%global gendep_perl_ExtUtils_MM_Utils \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(ExtUtils::MM::Utils) = 7.11 \
%{nil}
%global gendep_perl_ExtUtils_MakeMaker \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.2 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(DirHandle) \
Requires: %{?scl_prefix}perl(Encode) \
Requires: %{?scl_prefix}perl(Encode::Alias) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(ExtUtils::Installed) \
Requires: %{?scl_prefix}perl(ExtUtils::Liblist) \
Requires: %{?scl_prefix}perl(ExtUtils::Liblist::Kid) \
Requires: %{?scl_prefix}perl(ExtUtils::MM) \
Requires: %{?scl_prefix}perl(ExtUtils::MM_Any) \
Requires: %{?scl_prefix}perl(ExtUtils::MM_Unix) \
Requires: %{?scl_prefix}perl(ExtUtils::MM_Win32) \
Requires: %{?scl_prefix}perl(ExtUtils::MY) \
Requires: %{?scl_prefix}perl(ExtUtils::MakeMaker) \
Requires: %{?scl_prefix}perl(ExtUtils::MakeMaker::Config) \
Requires: %{?scl_prefix}perl(ExtUtils::MakeMaker::version) \
Requires: %{?scl_prefix}perl(ExtUtils::Packlist) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Path) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(IO::File) \
Requires: %{?scl_prefix}perl(base) \
Requires: %{?scl_prefix}perl(lib) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(ExtUtils::Command::MM) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::Liblist) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::Liblist::Kid) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_AIX) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_Any) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_BeOS) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_Cygwin) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_DOS) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_Darwin) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_MacOS) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_NW5) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_OS2) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_QNX) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_UWIN) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_Unix) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_VMS) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_VOS) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_Win32) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MM_Win95) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MY) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MakeMaker) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MakeMaker::Config) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MakeMaker::Locale) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::MakeMaker::version) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::Mkbootstrap) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::Mksymlists) = 7.10 \
Provides: %{?scl_prefix}perl(ExtUtils::testlib) = 7.10 \
Provides: %{?scl_prefix}perl(MM) \
Provides: %{?scl_prefix}perl(MY) \
%{nil}
%global gendep_perl_ExtUtils_Manifest \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Copy) \
Requires: %{?scl_prefix}perl(File::Find) \
Requires: %{?scl_prefix}perl(File::Spec) >= 0.8 \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(ExtUtils::Manifest) = 1.70 \
%{nil}
%global gendep_perl_ExtUtils_Miniperl \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(ExtUtils::Embed) >= 1.31 \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(ExtUtils::Miniperl) = 1.05 \
%{nil}
%global gendep_perl_ExtUtils_ParseXS \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.1 \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(ExtUtils::ParseXS) \
Requires: %{?scl_prefix}perl(ExtUtils::ParseXS::Constants) \
Requires: %{?scl_prefix}perl(ExtUtils::ParseXS::CountLines) \
Requires: %{?scl_prefix}perl(ExtUtils::ParseXS::Eval) \
Requires: %{?scl_prefix}perl(ExtUtils::ParseXS::Utilities) \
Requires: %{?scl_prefix}perl(ExtUtils::Typemaps) \
Requires: %{?scl_prefix}perl(ExtUtils::Typemaps::InputMap) \
Requires: %{?scl_prefix}perl(ExtUtils::Typemaps::OutputMap) \
Requires: %{?scl_prefix}perl(ExtUtils::Typemaps::Type) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(Symbol) \
Requires: %{?scl_prefix}perl(re) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(ExtUtils::ParseXS) = 3.31 \
Provides: %{?scl_prefix}perl(ExtUtils::ParseXS::Constants) = 3.31 \
Provides: %{?scl_prefix}perl(ExtUtils::ParseXS::CountLines) = 3.31 \
Provides: %{?scl_prefix}perl(ExtUtils::ParseXS::Eval) = 3.31 \
Provides: %{?scl_prefix}perl(ExtUtils::ParseXS::Utilities) = 3.31 \
Provides: %{?scl_prefix}perl(ExtUtils::Typemaps) = 3.31 \
Provides: %{?scl_prefix}perl(ExtUtils::Typemaps::Cmd) = 3.31 \
Provides: %{?scl_prefix}perl(ExtUtils::Typemaps::InputMap) = 3.31 \
Provides: %{?scl_prefix}perl(ExtUtils::Typemaps::OutputMap) = 3.31 \
Provides: %{?scl_prefix}perl(ExtUtils::Typemaps::Type) = 3.31 \
%{nil}
%global gendep_perl_File_Fetch \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Copy) \
Requires: %{?scl_prefix}perl(File::Path) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(File::Spec::Unix) \
Requires: %{?scl_prefix}perl(File::Temp) \
Requires: %{?scl_prefix}perl(FileHandle) \
Requires: %{?scl_prefix}perl(IPC::Cmd) \
Requires: %{?scl_prefix}perl(Locale::Maketext::Simple) \
Requires: %{?scl_prefix}perl(Module::Load::Conditional) \
Requires: %{?scl_prefix}perl(Params::Check) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(File::Fetch) = 0.48 \
%{nil}
%global gendep_perl_File_Path \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(File::Path) = 2.12 \
%{nil}
%global gendep_perl_File_Temp \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(Errno) \
Requires: %{?scl_prefix}perl(Exporter) >= 5.57 \
Requires: %{?scl_prefix}perl(Fcntl) >= 1.03 \
Requires: %{?scl_prefix}perl(File::Path) >= 2.06 \
Requires: %{?scl_prefix}perl(File::Spec) >= 0.8 \
Requires: %{?scl_prefix}perl(IO::Handle) \
Requires: %{?scl_prefix}perl(IO::Seekable) \
Requires: %{?scl_prefix}perl(Scalar::Util) \
Requires: %{?scl_prefix}perl(Symbol) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(parent) >= 0.221 \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(File::Temp) = 0.2304 \
Provides: %{?scl_prefix}perl(File::Temp::Dir) \
%{nil}
%global gendep_perl_Filter \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(DynaLoader) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Filter::Util::Call) = 1.55 \
%{nil}
%global gendep_perl_Filter_Simple \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Filter::Util::Call) \
Requires: %{?scl_prefix}perl(Text::Balanced) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Filter::Simple) = 0.92 \
%{nil}
%global gendep_perl_Getopt_Long \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.4.0 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Getopt::Long) = 2.48 \
Provides: %{?scl_prefix}perl(Getopt::Long::CallBack) \
Provides: %{?scl_prefix}perl(Getopt::Long::Parser) \
%{nil}
%global gendep_perl_HTTP_Tiny \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Errno) \
Requires: %{?scl_prefix}perl(IO::Socket) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(HTTP::Tiny) = 0.056 \
%{nil}
%global gendep_perl_IO \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Errno) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Fcntl) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(File::stat) \
Requires: %{?scl_prefix}perl(IO) \
Requires: %{?scl_prefix}perl(IO::File) \
Requires: %{?scl_prefix}perl(IO::Handle) \
Requires: %{?scl_prefix}perl(IO::Seekable) \
Requires: %{?scl_prefix}perl(IO::Socket) \
Requires: %{?scl_prefix}perl(IO::Socket::INET) \
Requires: %{?scl_prefix}perl(IO::Socket::UNIX) \
Requires: %{?scl_prefix}perl(SelectSaver) \
Requires: %{?scl_prefix}perl(Socket) >= 1.3 \
Requires: %{?scl_prefix}perl(Symbol) \
Requires: %{?scl_prefix}perl(Tie::Hash) \
Requires: %{?scl_prefix}perl(XSLoader) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Requires: %{?scl_prefix}perl(warnings::register) \
Provides: %{?scl_prefix}perl(IO) = 1.36 \
Provides: %{?scl_prefix}perl(IO::Dir) = 1.10 \
Provides: %{?scl_prefix}perl(IO::File) = 1.16 \
Provides: %{?scl_prefix}perl(IO::Handle) = 1.36 \
Provides: %{?scl_prefix}perl(IO::Pipe) = 1.15 \
Provides: %{?scl_prefix}perl(IO::Pipe::End) \
Provides: %{?scl_prefix}perl(IO::Poll) = 0.10 \
Provides: %{?scl_prefix}perl(IO::Seekable) = 1.10 \
Provides: %{?scl_prefix}perl(IO::Select) = 1.22 \
Provides: %{?scl_prefix}perl(IO::Socket) = 1.38 \
Provides: %{?scl_prefix}perl(IO::Socket::INET) = 1.35 \
Provides: %{?scl_prefix}perl(IO::Socket::UNIX) = 1.26 \
%{nil}
%global gendep_perl_IO_Compress \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Compress::Raw::Bzip2) >= 2.069 \
Requires: %{?scl_prefix}perl(Compress::Raw::Zlib) >= 2.069 \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Encode) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Fcntl) \
Requires: %{?scl_prefix}perl(File::GlobMapper) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(IO::Compress::Adapter::Bzip2) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Compress::Adapter::Deflate) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Compress::Adapter::Identity) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Compress::Base) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Compress::Base::Common) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Compress::Gzip) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Compress::Gzip::Constants) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Compress::RawDeflate) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Compress::Zip::Constants) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Compress::Zlib::Constants) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Compress::Zlib::Extra) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::File) \
Requires: %{?scl_prefix}perl(IO::Handle) \
Requires: %{?scl_prefix}perl(IO::Uncompress::Adapter::Bunzip2) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Uncompress::Adapter::Identity) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Uncompress::Adapter::Inflate) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Uncompress::Base) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Uncompress::Gunzip) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Uncompress::Inflate) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Uncompress::RawInflate) >= 2.069 \
Requires: %{?scl_prefix}perl(IO::Uncompress::Unzip) >= 2.069 \
Requires: %{?scl_prefix}perl(List::Util) \
Requires: %{?scl_prefix}perl(POSIX) \
Requires: %{?scl_prefix}perl(Scalar::Util) \
Requires: %{?scl_prefix}perl(Symbol) \
Requires: %{?scl_prefix}perl(bytes) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(utf8) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Compress::Zlib) = 2.069 \
Provides: %{?scl_prefix}perl(File::GlobMapper) = 1.000 \
Provides: %{?scl_prefix}perl(IO::Compress::Adapter::Bzip2) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Adapter::Deflate) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Adapter::Identity) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Base) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Base::Common) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Bzip2) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Deflate) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Gzip) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Gzip::Constants) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::RawDeflate) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Zip) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Zip::Constants) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Zlib::Constants) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Compress::Zlib::Extra) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::Adapter::Bunzip2) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::Adapter::Identity) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::Adapter::Inflate) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::AnyInflate) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::AnyUncompress) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::Base) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::Bunzip2) \
Provides: %{?scl_prefix}perl(IO::Uncompress::Bunzip2) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::Gunzip) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::Inflate) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::RawInflate) = 2.069 \
Provides: %{?scl_prefix}perl(IO::Uncompress::Unzip) = 2.069 \
Provides: %{?scl_prefix}perl(U64) \
Provides: %{?scl_prefix}perl(Zlib::OldDeflate) \
Provides: %{?scl_prefix}perl(Zlib::OldInflate) \
%{nil}
%global gendep_perl_IO_Socket_IP \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Errno) \
Requires: %{?scl_prefix}perl(IO::Socket) \
Requires: %{?scl_prefix}perl(IO::Socket::IP) \
Requires: %{?scl_prefix}perl(POSIX) \
Requires: %{?scl_prefix}perl(Socket) >= 1.97 \
Requires: %{?scl_prefix}perl(base) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(IO::Socket::IP) = 0.37 \
%{nil}
%global gendep_perl_IO_Zlib \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Fcntl) \
Requires: %{?scl_prefix}perl(Symbol) \
Requires: %{?scl_prefix}perl(Tie::Handle) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(IO::Zlib) = 1.10 \
%{nil}
%global gendep_perl_IPC_Cmd \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(Locale::Maketext::Simple) \
Requires: %{?scl_prefix}perl(Module::Load::Conditional) \
Requires: %{?scl_prefix}perl(Params::Check) \
Requires: %{?scl_prefix}perl(Symbol) \
Requires: %{?scl_prefix}perl(Text::ParseWords) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(IPC::Cmd) = 0.92 \
%{nil}
%global gendep_perl_IPC_SysV \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Class::Struct) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(IPC::SysV) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(IPC::Msg) = 2.06 \
Provides: %{?scl_prefix}perl(IPC::Msg::stat) \
Provides: %{?scl_prefix}perl(IPC::Semaphore) = 2.06 \
Provides: %{?scl_prefix}perl(IPC::Semaphore::stat) \
Provides: %{?scl_prefix}perl(IPC::SharedMem) = 2.06 \
Provides: %{?scl_prefix}perl(IPC::SharedMem::stat) \
Provides: %{?scl_prefix}perl(IPC::SysV) = 2.06 \
%{nil}
%global gendep_perl_JSON_PP \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(B) \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(JSON::PP) \
Requires: %{?scl_prefix}perl(base) \
Requires: %{?scl_prefix}perl(bytes) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Provides: %{?scl_prefix}perl(JSON::PP) = 2.27300 \
Provides: %{?scl_prefix}perl(JSON::PP::Boolean) \
Provides: %{?scl_prefix}perl(JSON::PP::IncrParser) = 1.01 \
%{nil}
%global gendep_perl_Locale_Codes \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.2.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Locale::Codes) \
Requires: %{?scl_prefix}perl(Locale::Codes::Constants) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(utf8) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Locale::Codes) = 3.25 \
Provides: %{?scl_prefix}perl(Locale::Codes) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Codes::Constants) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Codes::Country) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Codes::Currency) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Codes::LangExt) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Codes::LangFam) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Codes::LangVar) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Codes::Language) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Codes::Script) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Country) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Currency) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Language) = 3.37 \
Provides: %{?scl_prefix}perl(Locale::Script) = 3.37 \
%{nil}
%global gendep_perl_Locale_Maketext \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(I18N::LangTags) \
Requires: %{?scl_prefix}perl(I18N::LangTags::Detect) \
Requires: %{?scl_prefix}perl(Locale::Maketext) \
Requires: %{?scl_prefix}perl(integer) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Locale::Maketext) = 1.26 \
Provides: %{?scl_prefix}perl(Locale::Maketext::Guts) = 1.20 \
Provides: %{?scl_prefix}perl(Locale::Maketext::GutsLoader) = 1.20 \
%{nil}
%global gendep_perl_Locale_Maketext_Simple \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(Locale::Maketext) \
Requires: %{?scl_prefix}perl(base) \
Requires: %{?scl_prefix}perl(strict) \
Provides: %{?scl_prefix}perl(Locale::Maketext::Simple) = 0.21 \
%{nil}
%global gendep_perl_MIME_Base64 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(MIME::Base64) \
Requires: %{?scl_prefix}perl(XSLoader) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(MIME::Base64) = 3.15 \
Provides: %{?scl_prefix}perl(MIME::QuotedPrint) = 3.13 \
%{nil}
%global gendep_perl_Math_BigInt \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.1 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(integer) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Math::BigFloat) = 1.999715 \
Provides: %{?scl_prefix}perl(Math::BigInt) = 1.999715 \
Provides: %{?scl_prefix}perl(Math::BigInt::Calc) = 1.999715 \
Provides: %{?scl_prefix}perl(Math::BigInt::CalcEmu) = 1.999715 \
%{nil}
%global gendep_perl_Math_BigInt_FastCalc \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Math::BigInt::Calc) >= 1.999706 \
Requires: %{?scl_prefix}perl(XSLoader) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Math::BigInt::FastCalc) = 0.40 \
%{nil}
%global gendep_perl_Math_BigRat \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Math::BigFloat) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Math::BigRat) = 0.260802 \
%{nil}
%global gendep_perl_Math_Complex \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Math::Complex) >= 1.59 \
Requires: %{?scl_prefix}perl(Scalar::Util) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Math::Complex) = 1.59 \
Provides: %{?scl_prefix}perl(Math::Trig) = 1.23 \
%{nil}
%global gendep_perl_Memoize \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(NDBM_File) \
Requires: %{?scl_prefix}perl(SDBM_File) \
Requires: %{?scl_prefix}perl(Storable) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Memoize) = 1.03 \
Provides: %{?scl_prefix}perl(Memoize::AnyDBM_File) = 1.03 \
Provides: %{?scl_prefix}perl(Memoize::Expire) = 1.03 \
Provides: %{?scl_prefix}perl(Memoize::ExpireFile) = 1.03 \
Provides: %{?scl_prefix}perl(Memoize::ExpireTest) = 1.03 \
Provides: %{?scl_prefix}perl(Memoize::NDBM_File) = 1.03 \
Provides: %{?scl_prefix}perl(Memoize::SDBM_File) = 1.03 \
Provides: %{?scl_prefix}perl(Memoize::Storable) = 1.03 \
%{nil}
%global gendep_perl_Module_CoreList \
Requires: %{?scl_prefix}perl(Module::CoreList) \
Requires: %{?scl_prefix}perl(Module::CoreList::TieHashDelta) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(version) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Module::CoreList) = 5.20160506 \
Provides: %{?scl_prefix}perl(Module::CoreList::TieHashDelta) = 5.20160506 \
Provides: %{?scl_prefix}perl(Module::CoreList::Utils) = 5.20160506 \
%{nil}
%global gendep_perl_Module_CoreList_tools \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(List::Util) \
Requires: %{?scl_prefix}perl(Module::CoreList) \
Requires: %{?scl_prefix}perl(Pod::Usage) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
%{nil}
%global gendep_perl_Module_Load \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Module::Load) = 0.32 \
%{nil}
%global gendep_perl_Module_Load_Conditional \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(FileHandle) \
Requires: %{?scl_prefix}perl(Locale::Maketext::Simple) \
Requires: %{?scl_prefix}perl(Module::Load) \
Requires: %{?scl_prefix}perl(Module::Metadata) \
Requires: %{?scl_prefix}perl(Params::Check) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(version) \
Provides: %{?scl_prefix}perl(Module::Load::Conditional) = 0.64 \
%{nil}
%global gendep_perl_Module_Loaded \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Module::Loaded) = 0.08 \
%{nil}
%global gendep_perl_Module_Metadata \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(File::Find) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(version) >= 0.87 \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Module::Metadata) = 1.000031 \
%{nil}
%global gendep_perl_Net_Ping \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.2.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Fcntl) \
Requires: %{?scl_prefix}perl(FileHandle) \
Requires: %{?scl_prefix}perl(POSIX) \
Requires: %{?scl_prefix}perl(Socket) \
Requires: %{?scl_prefix}perl(Time::HiRes) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Net::Ping) = 2.43 \
%{nil}
%global gendep_perl_Params_Check \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Locale::Maketext::Simple) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Params::Check) = 0.38 \
%{nil}
%global gendep_perl_Parse_CPAN_Meta \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.1 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Provides: %{?scl_prefix}perl(Parse::CPAN::Meta) = 1.4417 \
%{nil}
%global gendep_perl_PathTools \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(File::Spec::Unix) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Cwd) = 3.63 \
Provides: %{?scl_prefix}perl(File::Spec) = 3.63 \
Provides: %{?scl_prefix}perl(File::Spec::AmigaOS) = 3.64 \
Provides: %{?scl_prefix}perl(File::Spec::Cygwin) = 3.63 \
Provides: %{?scl_prefix}perl(File::Spec::Epoc) = 3.63 \
Provides: %{?scl_prefix}perl(File::Spec::Functions) = 3.63 \
Provides: %{?scl_prefix}perl(File::Spec::Mac) = 3.63 \
Provides: %{?scl_prefix}perl(File::Spec::OS2) = 3.63 \
Provides: %{?scl_prefix}perl(File::Spec::Unix) = 3.63 \
Provides: %{?scl_prefix}perl(File::Spec::Win32) = 3.63 \
%{nil}
%global gendep_perl_Perl_OSType \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Perl::OSType) = 1.009 \
%{nil}
%global gendep_perl_PerlIO_via_QuotedPrint \
Requires: %{?scl_prefix}perl(MIME::QuotedPrint) \
Requires: %{?scl_prefix}perl(strict) \
Provides: %{?scl_prefix}perl(PerlIO::via::QuotedPrint) = 0.08 \
%{nil}
%global gendep_perl_Pod_Checker \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(Pod::Checker) \
Requires: %{?scl_prefix}perl(Pod::ParseUtils) \
Requires: %{?scl_prefix}perl(Pod::Parser) \
Requires: %{?scl_prefix}perl(Pod::Usage) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Pod::Checker) = 1.60 \
%{nil}
%global gendep_perl_Pod_Escapes \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Pod::Escapes) = 1.07 \
%{nil}
%global gendep_perl_Pod_Html \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(File::Spec::Unix) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(Pod::Html) \
Requires: %{?scl_prefix}perl(Pod::Simple::Search) \
Requires: %{?scl_prefix}perl(Pod::Simple::XHTML) \
Requires: %{?scl_prefix}perl(locale) \
Requires: %{?scl_prefix}perl(parent) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Pod::Html) = 1.22 \
Provides: %{?scl_prefix}perl(Pod::Simple::XHTML::LocalPodLinks) \
%{nil}
%global gendep_perl_Pod_Parser \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Find) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(Pod::InputObjects) \
Requires: %{?scl_prefix}perl(Pod::Parser) >= 1.04 \
Requires: %{?scl_prefix}perl(Pod::Select) \
Requires: %{?scl_prefix}perl(Pod::Usage) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Pod::Cache) \
Provides: %{?scl_prefix}perl(Pod::Cache::Item) \
Provides: %{?scl_prefix}perl(Pod::Find) = 1.63 \
Provides: %{?scl_prefix}perl(Pod::Hyperlink) \
Provides: %{?scl_prefix}perl(Pod::InputObjects) = 1.63 \
Provides: %{?scl_prefix}perl(Pod::InputSource) \
Provides: %{?scl_prefix}perl(Pod::InteriorSequence) \
Provides: %{?scl_prefix}perl(Pod::List) \
Provides: %{?scl_prefix}perl(Pod::Paragraph) \
Provides: %{?scl_prefix}perl(Pod::ParseTree) \
Provides: %{?scl_prefix}perl(Pod::ParseUtils) = 1.63 \
Provides: %{?scl_prefix}perl(Pod::Parser) = 1.63 \
Provides: %{?scl_prefix}perl(Pod::PlainText) = 2.07 \
Provides: %{?scl_prefix}perl(Pod::Select) = 1.63 \
%{nil}
%global gendep_perl_Pod_Perldoc \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.0.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Encode) \
Requires: %{?scl_prefix}perl(Fcntl) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Spec::Functions) \
Requires: %{?scl_prefix}perl(IO::Select) \
Requires: %{?scl_prefix}perl(Pod::Man) >= 2.18 \
Requires: %{?scl_prefix}perl(Pod::Perldoc) \
Requires: %{?scl_prefix}perl(Pod::Perldoc::BaseTo) \
Requires: %{?scl_prefix}perl(Pod::Perldoc::GetOptsOO) \
Requires: %{?scl_prefix}perl(Pod::Simple::RTF) \
Requires: %{?scl_prefix}perl(Pod::Simple::XMLOutStream) \
Requires: %{?scl_prefix}perl(Pod::Text) \
Requires: %{?scl_prefix}perl(Pod::Text::Color) \
Requires: %{?scl_prefix}perl(Pod::Text::Termcap) \
Requires: %{?scl_prefix}perl(parent) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Pod::Perldoc) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::BaseTo) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::GetOptsOO) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::ToANSI) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::ToChecker) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::ToMan) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::ToNroff) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::ToPod) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::ToRtf) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::ToTerm) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::ToText) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::ToTk) = 3.25 \
Provides: %{?scl_prefix}perl(Pod::Perldoc::ToXml) = 3.25 \
%{nil}
%global gendep_perl_Pod_Simple \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.0.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Cwd) \
Requires: %{?scl_prefix}perl(Encode) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(Pod::Escapes) >= 1.04 \
Requires: %{?scl_prefix}perl(Pod::Simple) \
Requires: %{?scl_prefix}perl(Pod::Simple::BlackBox) \
Requires: %{?scl_prefix}perl(Pod::Simple::HTML) \
Requires: %{?scl_prefix}perl(Pod::Simple::LinkSection) \
Requires: %{?scl_prefix}perl(Pod::Simple::Methody) \
Requires: %{?scl_prefix}perl(Pod::Simple::PullParser) \
Requires: %{?scl_prefix}perl(Pod::Simple::PullParserEndToken) \
Requires: %{?scl_prefix}perl(Pod::Simple::PullParserStartToken) \
Requires: %{?scl_prefix}perl(Pod::Simple::PullParserTextToken) \
Requires: %{?scl_prefix}perl(Pod::Simple::PullParserToken) \
Requires: %{?scl_prefix}perl(Pod::Simple::Search) \
Requires: %{?scl_prefix}perl(Symbol) \
Requires: %{?scl_prefix}perl(Text::Wrap) >= 98.112902 \
Requires: %{?scl_prefix}perl(integer) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Pod::Simple) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::BlackBox) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::Checker) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::Debug) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::DumpAsText) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::DumpAsXML) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::HTML) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::HTMLBatch) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::HTMLLegacy) = 5.01 \
Provides: %{?scl_prefix}perl(Pod::Simple::LinkSection) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::Methody) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::Progress) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::PullParser) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::PullParserEndToken) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::PullParserStartToken) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::PullParserTextToken) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::PullParserToken) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::RTF) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::Search) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::SimpleTree) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::Text) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::TextContent) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::TiedOutFH) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::Transcode) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::TranscodeDumb) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::TranscodeSmart) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::XHTML) = 3.32 \
Provides: %{?scl_prefix}perl(Pod::Simple::XMLOutStream) = 3.32 \
%{nil}
%global gendep_perl_Pod_Usage \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(Pod::Usage) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Pod::Usage) = 1.68 \
%{nil}
%global gendep_perl_Scalar_List_Utils \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(List::Util) \
Requires: %{?scl_prefix}perl(XSLoader) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(List::Util) = 1.42 \
Provides: %{?scl_prefix}perl(List::Util::XS) = 1.42 \
Provides: %{?scl_prefix}perl(Scalar::Util) = 1.42 \
Provides: %{?scl_prefix}perl(Sub::Util) = 1.42 \
%{nil}
%global gendep_perl_SelfLoader \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.0 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(IO::Handle) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(SelfLoader) = 1.23 \
%{nil}
%global gendep_perl_Socket \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(XSLoader) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings::register) \
Provides: %{?scl_prefix}perl(Socket) = 2.020 \
%{nil}
%global gendep_perl_Storable \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(XSLoader) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Storable) = 2.56 \
%{nil}
%global gendep_perl_Sys_Syslog \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(POSIX) \
Requires: %{?scl_prefix}perl(Socket) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Requires: %{?scl_prefix}perl(warnings::register) \
Provides: %{?scl_prefix}perl(Sys::Syslog) = 0.33 \
%{nil}
%global gendep_perl_Term_ANSIColor \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Term::ANSIColor) = 4.04 \
%{nil}
%global gendep_perl_Term_Cap \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Term::Cap) = 1.17 \
%{nil}
%global gendep_perl_Test \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.4.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Test) = 1.28 \
%{nil}
%global gendep_perl_Test_Harness \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(App::Prove) \
Requires: %{?scl_prefix}perl(App::Prove::State) \
Requires: %{?scl_prefix}perl(App::Prove::State::Result) \
Requires: %{?scl_prefix}perl(App::Prove::State::Result::Test) \
Requires: %{?scl_prefix}perl(Benchmark) \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Find) \
Requires: %{?scl_prefix}perl(File::Path) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(IO::Handle) \
Requires: %{?scl_prefix}perl(IO::Select) \
Requires: %{?scl_prefix}perl(POSIX) \
Requires: %{?scl_prefix}perl(TAP::Base) \
Requires: %{?scl_prefix}perl(TAP::Formatter::Base) \
Requires: %{?scl_prefix}perl(TAP::Formatter::Console::Session) \
Requires: %{?scl_prefix}perl(TAP::Formatter::File::Session) \
Requires: %{?scl_prefix}perl(TAP::Formatter::Session) \
Requires: %{?scl_prefix}perl(TAP::Harness) \
Requires: %{?scl_prefix}perl(TAP::Harness::Env) \
Requires: %{?scl_prefix}perl(TAP::Object) \
Requires: %{?scl_prefix}perl(TAP::Parser::Aggregator) \
Requires: %{?scl_prefix}perl(TAP::Parser::Grammar) \
Requires: %{?scl_prefix}perl(TAP::Parser::Iterator) \
Requires: %{?scl_prefix}perl(TAP::Parser::Iterator::Array) \
Requires: %{?scl_prefix}perl(TAP::Parser::Iterator::Process) \
Requires: %{?scl_prefix}perl(TAP::Parser::Iterator::Stream) \
Requires: %{?scl_prefix}perl(TAP::Parser::IteratorFactory) \
Requires: %{?scl_prefix}perl(TAP::Parser::Result) \
Requires: %{?scl_prefix}perl(TAP::Parser::Result::Bailout) \
Requires: %{?scl_prefix}perl(TAP::Parser::Result::Comment) \
Requires: %{?scl_prefix}perl(TAP::Parser::Result::Plan) \
Requires: %{?scl_prefix}perl(TAP::Parser::Result::Pragma) \
Requires: %{?scl_prefix}perl(TAP::Parser::Result::Test) \
Requires: %{?scl_prefix}perl(TAP::Parser::Result::Unknown) \
Requires: %{?scl_prefix}perl(TAP::Parser::Result::Version) \
Requires: %{?scl_prefix}perl(TAP::Parser::Result::YAML) \
Requires: %{?scl_prefix}perl(TAP::Parser::ResultFactory) \
Requires: %{?scl_prefix}perl(TAP::Parser::Scheduler::Job) \
Requires: %{?scl_prefix}perl(TAP::Parser::Scheduler::Spinner) \
Requires: %{?scl_prefix}perl(TAP::Parser::Source) \
Requires: %{?scl_prefix}perl(TAP::Parser::SourceHandler) \
Requires: %{?scl_prefix}perl(TAP::Parser::SourceHandler::Executable) \
Requires: %{?scl_prefix}perl(TAP::Parser::SourceHandler::File) \
Requires: %{?scl_prefix}perl(TAP::Parser::SourceHandler::Handle) \
Requires: %{?scl_prefix}perl(TAP::Parser::SourceHandler::Perl) \
Requires: %{?scl_prefix}perl(TAP::Parser::SourceHandler::RawTAP) \
Requires: %{?scl_prefix}perl(TAP::Parser::YAMLish::Reader) \
Requires: %{?scl_prefix}perl(TAP::Parser::YAMLish::Writer) \
Requires: %{?scl_prefix}perl(Text::ParseWords) \
Requires: %{?scl_prefix}perl(base) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(App::Prove) = 3.36 \
Provides: %{?scl_prefix}perl(App::Prove::State) = 3.36 \
Provides: %{?scl_prefix}perl(App::Prove::State::Result) = 3.36 \
Provides: %{?scl_prefix}perl(App::Prove::State::Result::Test) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Base) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Formatter::Base) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Formatter::Color) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Formatter::Console) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Formatter::Console::ParallelSession) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Formatter::Console::Session) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Formatter::File) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Formatter::File::Session) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Formatter::Session) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Harness) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Harness::Env) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Object) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Aggregator) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Grammar) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Iterator) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Iterator::Array) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Iterator::Process) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Iterator::Stream) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::IteratorFactory) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Multiplexer) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Result) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Result::Bailout) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Result::Comment) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Result::Plan) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Result::Pragma) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Result::Test) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Result::Unknown) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Result::Version) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Result::YAML) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::ResultFactory) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Scheduler) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Scheduler::Job) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Scheduler::Spinner) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::Source) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::SourceHandler) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::SourceHandler::Executable) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::SourceHandler::File) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::SourceHandler::Handle) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::SourceHandler::Perl) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::SourceHandler::RawTAP) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::YAMLish::Reader) = 3.36 \
Provides: %{?scl_prefix}perl(TAP::Parser::YAMLish::Writer) = 3.36 \
Provides: %{?scl_prefix}perl(Test::Harness) = 3.36 \
%{nil}
%global gendep_perl_Test_Simple \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(IO::Handle) \
Requires: %{?scl_prefix}perl(Symbol) \
Requires: %{?scl_prefix}perl(Test::Builder) >= 0.99 \
Requires: %{?scl_prefix}perl(Test::Builder) >= 1.00 \
Requires: %{?scl_prefix}perl(Test::Builder::Module) >= 0.99 \
Requires: %{?scl_prefix}perl(Test::Builder::Tester) \
Requires: %{?scl_prefix}perl(Test::More) \
Requires: %{?scl_prefix}perl(Test::Tester::Capture) \
Requires: %{?scl_prefix}perl(Test::Tester::CaptureRunner) \
Requires: %{?scl_prefix}perl(Test::Tester::Delegate) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Test::Builder) = 1.001014 \
Provides: %{?scl_prefix}perl(Test::Builder::IO::Scalar) = 2.113 \
Provides: %{?scl_prefix}perl(Test::Builder::Module) = 1.001014 \
Provides: %{?scl_prefix}perl(Test::Builder::Tester) = 1.28 \
Provides: %{?scl_prefix}perl(Test::Builder::Tester::Color) = 1.290001 \
Provides: %{?scl_prefix}perl(Test::Builder::Tester::Tie) \
Provides: %{?scl_prefix}perl(Test::More) = 1.001014 \
Provides: %{?scl_prefix}perl(Test::Simple) = 1.001014 \
Provides: %{?scl_prefix}perl(Test::Tester) = 0.114 \
Provides: %{?scl_prefix}perl(Test::Tester::Capture) \
Provides: %{?scl_prefix}perl(Test::Tester::CaptureRunner) \
Provides: %{?scl_prefix}perl(Test::Tester::Delegate) \
Provides: %{?scl_prefix}perl(Test::use::ok) = 0.16 \
Provides: %{?scl_prefix}perl(ok) = 0.16 \
%{nil}
%global gendep_perl_Text_Balanced \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.5.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(SelfLoader) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Text::Balanced) = 2.03 \
Provides: %{?scl_prefix}perl(Text::Balanced::ErrorMsg) \
Provides: %{?scl_prefix}perl(Text::Balanced::Extractor) \
%{nil}
%global gendep_perl_Text_ParseWords \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Provides: %{?scl_prefix}perl(Text::ParseWords) = 3.30 \
%{nil}
%global gendep_perl_Text_Tabs_Wrap \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.10.0 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Text::Tabs) \
Requires: %{?scl_prefix}perl(re) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings::register) \
Provides: %{?scl_prefix}perl(Text::Tabs) = 2013.0523 \
Provides: %{?scl_prefix}perl(Text::Wrap) = 2013.0523 \
%{nil}
%global gendep_perl_Thread_Queue \
Requires: %{?scl_prefix}perl(Scalar::Util) >= 1.10 \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(threads::shared) >= 1.21 \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Thread::Queue) = 3.09 \
%{nil}
%global gendep_perl_Time_HiRes \
Requires: %{?scl_prefix}perl(DynaLoader) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Provides: %{?scl_prefix}perl(Time::HiRes) = 1.9733 \
%{nil}
%global gendep_perl_Time_Local \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(Time::Local) = 1.2300 \
%{nil}
%global gendep_perl_Time_Piece \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(DynaLoader) \
Requires: %{?scl_prefix}perl(Exporter) >= 5.57 \
Requires: %{?scl_prefix}perl(Time::Local) \
Requires: %{?scl_prefix}perl(Time::Seconds) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(integer) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Provides: %{?scl_prefix}perl(Time::Piece) = 1.31 \
Provides: %{?scl_prefix}perl(Time::Seconds) = 1.31 \
%{nil}
%global gendep_perl_Unicode_Collate \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(DynaLoader) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(Unicode::Collate) \
Requires: %{?scl_prefix}perl(base) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Unicode::Collate) = 1.14 \
Provides: %{?scl_prefix}perl(Unicode::Collate::CJK::Big5) = 1.14 \
Provides: %{?scl_prefix}perl(Unicode::Collate::CJK::GB2312) = 1.14 \
Provides: %{?scl_prefix}perl(Unicode::Collate::CJK::JISX0208) = 1.14 \
Provides: %{?scl_prefix}perl(Unicode::Collate::CJK::Korean) = 1.14 \
Provides: %{?scl_prefix}perl(Unicode::Collate::CJK::Pinyin) = 1.14 \
Provides: %{?scl_prefix}perl(Unicode::Collate::CJK::Stroke) = 1.14 \
Provides: %{?scl_prefix}perl(Unicode::Collate::CJK::Zhuyin) = 1.14 \
Provides: %{?scl_prefix}perl(Unicode::Collate::Locale) = 1.14 \
%{nil}
%global gendep_perl_Unicode_Normalize \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(DynaLoader) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Unicode::Normalize) = 1.25 \
%{nil}
%global gendep_perl_autodie \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(Exporter) >= 5.57 \
Requires: %{?scl_prefix}perl(Fatal) \
Requires: %{?scl_prefix}perl(Scalar::Util) \
Requires: %{?scl_prefix}perl(Tie::RefHash) \
Requires: %{?scl_prefix}perl(autodie::Scope::Guard) \
Requires: %{?scl_prefix}perl(autodie::Scope::GuardStack) \
Requires: %{?scl_prefix}perl(autodie::Util) \
Requires: %{?scl_prefix}perl(autodie::exception) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(lib) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(parent) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Fatal) = 2.29 \
Provides: %{?scl_prefix}perl(autodie) = 2.29 \
Provides: %{?scl_prefix}perl(autodie::Scope::Guard) = 2.29 \
Provides: %{?scl_prefix}perl(autodie::Scope::GuardStack) = 2.29 \
Provides: %{?scl_prefix}perl(autodie::Util) = 2.29 \
Provides: %{?scl_prefix}perl(autodie::exception) = 2.29 \
Provides: %{?scl_prefix}perl(autodie::exception::system) = 2.29 \
Provides: %{?scl_prefix}perl(autodie::hints) = 2.29 \
Provides: %{?scl_prefix}perl(autodie::skip) = 2.29 \
%{nil}
%global gendep_perl_bignum \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Math::BigFloat) \
Requires: %{?scl_prefix}perl(Math::BigInt) \
Requires: %{?scl_prefix}perl(bigint) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Math::BigFloat::Trace) = 0.42 \
Provides: %{?scl_prefix}perl(Math::BigInt::Trace) = 0.42 \
Provides: %{?scl_prefix}perl(bigint) = 0.42 \
Provides: %{?scl_prefix}perl(bignum) = 0.42 \
Provides: %{?scl_prefix}perl(bigrat) = 0.42 \
%{nil}
%global gendep_perl_constant \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.0 \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings::register) \
Provides: %{?scl_prefix}perl(constant) = 1.33 \
%{nil}
%global gendep_perl_core \
%{nil}
%global gendep_perl_debuginfo \
%{nil}
%global gendep_perl_devel \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(ExtUtils::Constant) \
Requires: %{?scl_prefix}perl(ExtUtils::Installed) \
Requires: %{?scl_prefix}perl(File::Compare) \
Requires: %{?scl_prefix}perl(File::Path) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(Text::Wrap) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
%{nil}
%global gendep_perl_encoding \
Requires: %{?scl_prefix}perl(Encode) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(encoding) = 2.17 \
%{nil}
%global gendep_perl_experimental \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(feature) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(version) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(experimental) = 0.016 \
%{nil}
%global gendep_perl_libnet \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.1 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Errno) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Fcntl) \
Requires: %{?scl_prefix}perl(FileHandle) \
Requires: %{?scl_prefix}perl(IO::Select) \
Requires: %{?scl_prefix}perl(IO::Socket) \
Requires: %{?scl_prefix}perl(Net::Cmd) \
Requires: %{?scl_prefix}perl(Net::Config) \
Requires: %{?scl_prefix}perl(Net::FTP::I) \
Requires: %{?scl_prefix}perl(Net::FTP::dataconn) \
Requires: %{?scl_prefix}perl(Socket) \
Requires: %{?scl_prefix}perl(Symbol) \
Requires: %{?scl_prefix}perl(Time::Local) \
Requires: %{?scl_prefix}perl(constant) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Net::Cmd) = 3.08 \
Provides: %{?scl_prefix}perl(Net::Config) = 3.08 \
Provides: %{?scl_prefix}perl(Net::Domain) = 3.08 \
Provides: %{?scl_prefix}perl(Net::FTP) = 3.08 \
Provides: %{?scl_prefix}perl(Net::FTP::A) = 3.08 \
Provides: %{?scl_prefix}perl(Net::FTP::E) = 3.08 \
Provides: %{?scl_prefix}perl(Net::FTP::I) = 3.08 \
Provides: %{?scl_prefix}perl(Net::FTP::L) = 3.08 \
Provides: %{?scl_prefix}perl(Net::FTP::_SSL_SingleSessionCache) \
Provides: %{?scl_prefix}perl(Net::FTP::dataconn) = 3.08 \
Provides: %{?scl_prefix}perl(Net::NNTP) = 3.08 \
Provides: %{?scl_prefix}perl(Net::NNTP::_SSL) \
Provides: %{?scl_prefix}perl(Net::Netrc) = 3.08 \
Provides: %{?scl_prefix}perl(Net::POP3) = 3.08 \
Provides: %{?scl_prefix}perl(Net::POP3::_SSL) \
Provides: %{?scl_prefix}perl(Net::SMTP) = 3.08 \
Provides: %{?scl_prefix}perl(Net::SMTP::_SSL) \
Provides: %{?scl_prefix}perl(Net::Time) = 3.08 \
%{nil}
%global gendep_perl_libnetcfg \
Requires: %{?scl_prefix}perl(ExtUtils::MakeMaker) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(Getopt::Std) \
Requires: %{?scl_prefix}perl(IO::File) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
%{nil}
%global gendep_perl_libs \
Requires: %{?scl_prefix}perl(integer) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(:MODULE_COMPAT_5.24.0) \
Provides: %{?scl_prefix}perl(:VERSION) = 5.24.0 \
Provides: %{?scl_prefix}perl(:WITH_ITHREADS) \
Provides: %{?scl_prefix}perl(:WITH_LARGEFILES) \
Provides: %{?scl_prefix}perl(:WITH_PERLIO) \
Provides: %{?scl_prefix}perl(:WITH_THREADS) \
Provides: %{?scl_prefix}perl(XSLoader) = 0.22 \
Provides: %{?scl_prefix}perl(integer) = 1.01 \
Provides: %{?scl_prefix}perl(re) = 0.32 \
Provides: %{?scl_prefix}perl(strict) = 1.11 \
Provides: %{?scl_prefix}perl(unicore::Name) \
Provides: %{?scl_prefix}perl(utf8) = 1.19 \
Provides: %{?scl_prefix}perl(utf8_heavy.pl) \
Provides: %{?scl_prefix}perl(warnings) = 1.36 \
%{nil}
%global gendep_perl_macros \
%{nil}
%global gendep_perl_open \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.1 \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(open) = 1.10 \
%{nil}
%global gendep_perl_parent \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Provides: %{?scl_prefix}perl(parent) = 0.234 \
%{nil}
%global gendep_perl_perlfaq \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(perlfaq) = 5.021010 \
%{nil}
%global gendep_perl_podlators \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.0 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Encode) \
Requires: %{?scl_prefix}perl(Exporter) \
Requires: %{?scl_prefix}perl(Getopt::Long) \
Requires: %{?scl_prefix}perl(POSIX) \
Requires: %{?scl_prefix}perl(Pod::Man) \
Requires: %{?scl_prefix}perl(Pod::Simple) \
Requires: %{?scl_prefix}perl(Pod::Text) \
Requires: %{?scl_prefix}perl(Pod::Usage) \
Requires: %{?scl_prefix}perl(Term::ANSIColor) \
Requires: %{?scl_prefix}perl(Term::Cap) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(subs) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(Pod::Man) = 4.07 \
Provides: %{?scl_prefix}perl(Pod::ParseLink) = 4.07 \
Provides: %{?scl_prefix}perl(Pod::Text) = 4.07 \
Provides: %{?scl_prefix}perl(Pod::Text::Color) = 4.07 \
Provides: %{?scl_prefix}perl(Pod::Text::Overstrike) = 4.07 \
Provides: %{?scl_prefix}perl(Pod::Text::Termcap) = 4.07 \
%{nil}
%global gendep_perl_tests \
%{nil}
%global gendep_perl_threads \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.0 \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(XSLoader) \
Requires: %{?scl_prefix}perl(overload) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(threads) = 2.07 \
%{nil}
%global gendep_perl_threads_shared \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.8.0 \
Requires: %{?scl_prefix}perl(Scalar::Util) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(warnings) \
Provides: %{?scl_prefix}perl(threads::shared) = 1.51 \
%{nil}
%global gendep_perl_utils \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.9.1 \
Requires: %{?scl_prefix}perl(Carp) \
Requires: %{?scl_prefix}perl(Config) \
Requires: %{?scl_prefix}perl(File::Basename) \
Requires: %{?scl_prefix}perl(File::Path) \
Requires: %{?scl_prefix}perl(File::Spec) \
Requires: %{?scl_prefix}perl(File::Temp) \
Requires: %{?scl_prefix}perl(Getopt::Std) \
Requires: %{?scl_prefix}perl(Text::Tabs) \
Requires: %{?scl_prefix}perl(re) \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(warnings) \
%{nil}
%global gendep_perl_version \
Requires: %{?scl_prefix}perl(:VERSION) >= 5.6.2 \
Requires: %{?scl_prefix}perl(strict) \
Requires: %{?scl_prefix}perl(vars) \
Requires: %{?scl_prefix}perl(version::regex) \
Requires: %{?scl_prefix}perl(warnings::register) \
Provides: %{?scl_prefix}perl(version) = 0.9916 \
Provides: %{?scl_prefix}perl(version::regex) = 0.9916 \
%{nil}
%endif

# Removes date check, Fedora/RHEL specific
Patch1:         perl-perlbug-tag.patch

# Fedora/RHEL only (64bit only)
Patch3:         perl-5.8.0-libdir64.patch

# Fedora/RHEL specific (use libresolv instead of libbind)
Patch4:         perl-5.10.0-libresolv.patch

# FIXME: May need the "Fedora" references removed before upstreaming
# patches ExtUtils-MakeMaker
Patch5:         perl-USE_MM_LD_RUN_PATH.patch

# Provide maybe_command independently, bug #1129443
Patch6:         perl-5.22.1-Provide-ExtUtils-MM-methods-as-standalone-ExtUtils-M.patch

# The Fedora builders started randomly failing this futime test
# only on x86_64, so we just don't run it. Works fine on normal
# systems.
Patch7:         perl-5.10.0-x86_64-io-test-failure.patch

# switch off test, which is failing only on koji (fork)
Patch8:         perl-5.14.1-offtest.patch

# Define SONAME for libperl.so
Patch15:        perl-5.16.3-create_libperl_soname.patch

# Install libperl.so to -Dshrpdir value
Patch16:        perl-5.22.0-Install-libperl.so-to-shrpdir-on-Linux.patch

# Document Math::BigInt::CalcEmu requires Math::BigInt, rhbz#959096,
# CPAN RT#85015
Patch22:        perl-5.18.1-Document-Math-BigInt-CalcEmu-requires-Math-BigInt.patch

# Make *DBM_File desctructors thread-safe, bug #1107543, RT#61912
Patch26:        perl-5.18.2-Destroy-GDBM-NDBM-ODBM-SDBM-_File-objects-only-from-.patch

# Workaround for Coro, bug #1231165, CPAN RT#101063. To remove in the future.
Patch28:        perl-5.22.0-Revert-const-the-core-magic-vtables.patch

# Replace ExtUtils::MakeMaker dependency with ExtUtils::MM::Utils.
# This allows not to require perl-devel. Bug #1129443
Patch30:        perl-5.22.1-Replace-EU-MM-dependnecy-with-EU-MM-Utils-in-IPC-Cmd.patch

# Fix a memory leak when compiling a regular expression with a POSIX class,
# RT#128313, in upstream after 5.25.1
Patch31:        perl-5.24.0-Fix-a-memory-leak-in-strict-regex-posix-classes.patch

# Do not mangle errno from failed socket calls, RT#128316,
# in upstream after 5.25.1
Patch32:        perl-5.25.1-perl-128316-preserve-errno-from-failed-system-calls.patch

# Fix compiling regular expressions like /\X*(?0)/, RT#128109, in upstream
# after 5.25.1
Patch33:        perl-5.24.0-fix-128109-do-not-move-RExC_open_parens-0-in-reginse.patch

# Do not use unitialized memory in $h{\const} warnings, RT#128189,
# in upstream after 5.25.2
Patch34:        perl-5.25.2-uninit-warning-from-h-const-coredumped.patch

# Fix precedence in hv_ename_delete, RT#128086, in upstream after 5.25.0
Patch35:        perl-5.25.0-Fix-precedence-in-hv_ename_delete.patch

# Do not treat %: as a stash, RT#128238, in upstream after 5.25.2
Patch36:        perl-5.25.2-only-treat-stash-entries-with-.-as-sub-stashes.patch

# Do not crash when inserting a non-stash into a stash, RT#128238,
# in upstream after 5.25.2
Patch37:        perl-5.25.2-perl-128238-Crash-with-non-stash-in-stash.patch

# Fix line numbers with perl -x, RT#128508, in upstream after 5.25.2
Patch38:        perl-5.25.2-perl-128508-Fix-line-numbers-with-perl-x.patch

# Do not let XSLoader load relative paths, CVE-2016-6185, RT#115808,
# in upstream after 5.25.2
Patch39:        perl-5.25.2-Don-t-let-XSLoader-load-relative-paths.patch

# Fix a crash when vivifying a stub in a deleted package, RT#128532,
# in upstream after 5.25.2
Patch40:        perl-5.25.2-perl-128532-Crash-vivifying-stub-in-deleted-pkg.patch

# Fix a crash in "Subroutine redefined" warning, RT#128257,
# in upstream after 5.25.2
Patch41:        perl-5.25.2-SEGV-in-Subroutine-redefined-warning.patch

# Fix a crash in lexical scope warnings, RT#128597, in upstream after 5.25.2
Patch42:        perl-5.25.2-perl-128597-Crash-from-gp_free-ckWARN_d.patch

# Link XS modules to libperl.so with EU::CBuilder on Linux, bug #960048
Patch200:       perl-5.16.3-Link-XS-modules-to-libperl.so-with-EU-CBuilder-on-Li.patch

# Link XS modules to libperl.so with EU::MM on Linux, bug #960048
Patch201:       perl-5.16.3-Link-XS-modules-to-libperl.so-with-EU-MM-on-Linux.patch

# SCL specific patches
# Fix perlvar pod rhbz#957079
Patch300:        perl-5.16.3-perlvar-pod.patch

# gdbm does not provide symlink /usr/lib/include/dbm.h on RHEL 6.x.
# Patch Configure and ODBM_File.xs to use gdbm/dbm.h
Patch301:        perl-scl-use-gdbm-dbm_h.patch

# Patch makefile to create preload for each build
Patch302:       perl-scl-use-preload-each-time.patch

# Update some of the bundled modules
# see http://fedoraproject.org/wiki/Perl/perl.spec for instructions

BuildRequires:  bash
BuildRequires:  bzip2-devel
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
%if %{with gdbm}
BuildRequires:  gdbm-devel
%endif
# glibc-common for iconv
BuildRequires:  glibc-common
# Build-require groff tools for populating %%Config correctly, bug #135101

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
BuildRequires:  db4-devel
BuildRequires:  groff
%else
BuildRequires:  groff-base
BuildRequires:  libdb-devel
%endif
BuildRequires:  make
%if !%{defined perl_bootstrap}
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-generators
%endif
BuildRequires:  sed
BuildRequires:  systemtap-sdt-devel
BuildRequires:  tar
BuildRequires:  tcsh
BuildRequires:  zlib-devel
%{?scl:BuildRequires: %{scl}-runtime}
%{?scl:BuildRequires: %{scl}-build}

# For tests
%if %{with test}
BuildRequires:  procps
BuildRequires:  rsyslog
%endif

# The long line of Perl provides.


# compat macro needed for rebuild
%global perl_compat %{?scl_prefix}perl(:MODULE_COMPAT_5.24.0)

# File provides
Provides: %{?scl_prefix}perl(bytes_heavy.pl)
Provides: %{?scl_prefix}perl(dumpvar.pl)
Provides: %{?scl_prefix}perl(perl5db.pl)

# suidperl isn't created by upstream since 5.12.0
Obsoletes: %{?scl_prefix}perl-suidperl <= 4:5.12.2

Requires: %{?scl_prefix}perl-libs = %{perl_epoch}:%{perl_version}-%{release}
# Require this till perl sub-package requires any modules
Requires: %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl
%endif

# We need this to break the dependency loop, and ensure that perl-libs
# gets installed before perl.
Requires(post): %{?scl_prefix}perl-libs
# Same as perl-libs. We need macros in basic buildroot, where Perl is only
# because of git.
Requires(post): %{?scl_prefix}perl-macros

%{?scl:Requires: %{scl_name}-runtime}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
# filter pkgconfig Provides and Requires
%{?scl:
%filter_provides_in .*/auto/.*\.so$\|.*%{_docdir}\|.*%{perl_archlib}/.*\.pl$\|.*%{perl_privlib}/.*\.pl$

%filter_from_provides /perl(\(VMS::Stdio\|VMS::Filespec\|unicore::Name\))\s*$/d
%filter_from_provides /perl(\(BSD::.*\|CGI\|DB\|Win32.*\|Fh\|MultipartBuffer\))\s*$/d

%filter_from_requires /perl(\(VMS\|BSD::\|Win32\|Tk\|Mac::\|FCGI\)/d
%filter_from_requires /perl(\(.::test.pl\|test.pl\))/d
%filter_from_requires /perl(\(Your::Module::Here\|unicore::Name\)/d
%filter_from_requires /\(DBD::SQLite\|DBIx::Simple\)/d
%filter_requires_in %{_docdir}

%filter_setup
}
%else

# To filter invalid perl provides
# For unknown reason the requires like "perl516-perl >= 1:5.8.0" is
# included into sub-package's provides
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\s>=

%endif

%description
Perl is a high-level programming language with roots in C, sed, awk and shell
scripting.  Perl is good at handling processes and files, and is especially
good at handling text.  Perl's hallmarks are practicality and efficiency.
While it is used to do a lot of different things, Perl's most common
applications are system administration utilities and web programming.

Install this package if you want to program in Perl or enable your system to
handle Perl scripts with %{_bindir}/perl interpreter.

If your script requires some Perl modules, you can install them with
"perl(MODULE)" where "MODULE" is a name of required module. E.g. install
"perl(Test::More)" to make Test::More Perl module available.

If you need all the Perl modules that come with upstream Perl sources, so
called core modules, install perl-core package.

If you only need perl run-time as a shared library, i.e. Perl interpreter
embedded into another application, the only essential package is perl-libs.

Perl header files can be found in perl-devel package.

Perl utils like "splain" or "perlbug" can be found in perl-utils package.


%package libs
Summary:        The libraries for the perl run-time
Group:          Development/Languages
License:        (GPL+ or Artistic) and HSLR and MIT and UCD
# Compat provides
Provides:       %perl_compat
# Interpreter version to fulfil required genersted from "require 5.006;"
Provides:       %{?scl_prefix}perl(:VERSION) = %{perl_version}
# Threading provides
Provides:       %{?scl_prefix}perl(:WITH_ITHREADS)
Provides:       %{?scl_prefix}perl(:WITH_THREADS)
# Largefile provides
Provides:       %{?scl_prefix}perl(:WITH_LARGEFILES)
# PerlIO provides
Provides:       %{?scl_prefix}perl(:WITH_PERLIO)
# Loaded by charnames, unicore/Name.pm does not declare unicore::Name module
Provides:       %{?scl_prefix}perl(unicore::Name)
# Keep utf8 modules in perl-libs because a sole regular expression like /\pN/
# causes loading utf8 and unicore/Heave.pl and unicore/lib files.
Provides:       %{?scl_prefix}perl(utf8_heavy.pl)
# utf8 and utf8_heavy.pl require Carp, re, strict, warnings, XSLoader
Requires:       %{?scl_prefix}perl(Carp)
Requires:       %{?scl_prefix}perl(Exporter)
# Term::Cap is optional
Requires:       %{?scl_prefix}perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_libs
%endif

# Remove private redefinitions
# XSLoader redefines DynaLoader name space for compatibility, but does not
# load the DynaLoader.pm (though the DynaLoader.xs is compiled into libperl).
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\((charnames|DynaLoader)\\)$

%description libs
The is a perl run-time (interpreter as a shared library and include
directories).


%package devel
Summary:        Header #files for use in perl development
Group:          Development/Languages
# l1_char_class_tab.h is generated from lib/unicore sources:    UCD
License:        (GPL+ or Artistic) and UCD
# Require $Config{libs} providers, bug #905482
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
BuildRequires:  db4-devel
%else
Requires:       libdb-devel
%endif
%if %{with gdbm}
Requires:       gdbm-devel
%endif
Requires:       glibc-devel
Requires:       systemtap-sdt-devel
Requires:       %{?scl_prefix}perl(ExtUtils::ParseXS)
Requires:       %perl_compat
# Match library and header files when downgrading releases
Requires:       %{?scl_prefix}perl-libs = %{perl_epoch}:%{perl_version}-%{release}
%if %{defined perl_bootstrap}
%gendep_perl_devel
%endif

%description devel
This package contains header files and development modules.
Most perl packages will need to install perl-devel to build.


%package macros
Summary:        Macros for rpmbuild
Group:          Development/Languages
License:        GPL+ or Artistic
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_macros
%endif

%description macros
Macros for rpmbuild are needed during build of srpm in koji. This
sub-package must be installed into buildroot, so it will be needed
by perl. Perl is needed because of git.


%package tests
Summary:        The Perl test suite
Group:          Development/Languages
License:        GPL+ or Artistic
# right?
AutoReqProv:    0
Requires:       %perl_compat
# FIXME - note this will need to change when doing the core/minimal swizzle
Requires:       %{?scl_prefix}perl-core
%if %{defined perl_bootstrap}
%gendep_perl_tests
%endif

%description tests
This package contains the test suite included with Perl %{perl_version}.

Install this if you want to test your Perl installation (binary and core
modules).


%package utils
Summary:        Utilities packaged with the Perl distribution
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        %{perl_version}
BuildArch:      noarch
# Match library exactly for splain messages
Requires:       %{?scl_prefix}perl-libs = %{perl_epoch}:%{perl_version}-%{release}
# Keep /usr/sbin/sendmail and Module::CoreList optional for the perlbug tool
%if %{defined perl_bootstrap}
%gendep_perl_utils
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-351

%description utils
Several utilities which come with Perl distribution like c2ph, h2ph, perlbug,
perlthanks, pl2pm, pstruct, and splain. Some utilities are provided by more
specific packages like perldoc by perl-Pod-Perldoc.


%package core
Summary:        Base perl metapackage
Group:          Development/Languages
# This rpm doesn't contain any copyrightable material.
# Nevertheless, it needs a License tag, so we'll use the generic
# "perl" license.
License:        GPL+ or Artistic
Epoch:          0
Version:        %{perl_version}
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl-libs = %{perl_epoch}:%{perl_version}-%{release}
Requires:       %{?scl_prefix}perl-devel = %{perl_epoch}:%{perl_version}-%{release}
Requires:       %{?scl_prefix}perl-macros
Requires:       %{?scl_prefix}perl-utils
%if %{defined perl_bootstrap}
%gendep_perl_core
%endif

Requires:       %{?scl_prefix}perl-Archive-Tar, %{?scl_prefix}perl-Attribute-Handlers, %{?scl_prefix}perl-autodie,
Requires:       %{?scl_prefix}perl-B-Debug, %{?scl_prefix}perl-bignum
Requires:       %{?scl_prefix}perl-Compress-Raw-Bzip2,
Requires:       %{?scl_prefix}perl-Carp, %{?scl_prefix}perl-Compress-Raw-Zlib, %{?scl_prefix}perl-Config-Perl-V,
Requires:       %{?scl_prefix}perl-constant,
Requires:       %{?scl_prefix}perl-CPAN, %{?scl_prefix}perl-CPAN-Meta, %{?scl_prefix}perl-CPAN-Meta-Requirements,
Requires:       %{?scl_prefix}perl-CPAN-Meta-YAML, %{?scl_prefix}perl-Encode, %{?scl_prefix}perl-encoding
Requires:       %{?scl_prefix}perl-Data-Dumper, %{?scl_prefix}perl-DB_File,
Requires:       %{?scl_prefix}perl-Devel-Peek, %{?scl_prefix}perl-Devel-PPPort, %{?scl_prefix}perl-Devel-SelfStubber,
Requires:       %{?scl_prefix}perl-Digest, %{?scl_prefix}perl-Digest-MD5,
Requires:       %{?scl_prefix}perl-Digest-SHA,
Requires:       %{?scl_prefix}perl-Env, %{?scl_prefix}perl-Errno, %{?scl_prefix}perl-Exporter, %{?scl_prefix}perl-experimental
Requires:       %{?scl_prefix}perl-ExtUtils-CBuilder, %{?scl_prefix}perl-ExtUtils-Command,
Requires:       %{?scl_prefix}perl-ExtUtils-Embed,
Requires:       %{?scl_prefix}perl-ExtUtils-Install, %{?scl_prefix}perl-ExtUtils-MakeMaker
Requires:       %{?scl_prefix}perl-ExtUtils-Manifest, %{?scl_prefix}perl-ExtUtils-Miniperl
Requires:       %{?scl_prefix}perl-ExtUtils-ParseXS, %{?scl_prefix}perl-File-Fetch
Requires:       %{?scl_prefix}perl-File-Path, %{?scl_prefix}perl-File-Temp, %{?scl_prefix}perl-Filter,
Requires:       %{?scl_prefix}perl-Filter-Simple, %{?scl_prefix}perl-Getopt-Long
Requires:       %{?scl_prefix}perl-HTTP-Tiny,
Requires:       %{?scl_prefix}perl-IO, %{?scl_prefix}perl-IO-Compress, %{?scl_prefix}perl-IO-Socket-IP
Requires:       %{?scl_prefix}perl-IO-Zlib, %{?scl_prefix}perl-IPC-Cmd, %{?scl_prefix}perl-IPC-SysV, %{?scl_prefix}perl-JSON-PP
Requires:       %{?scl_prefix}perl-libnet, %{?scl_prefix}perl-libnetcfg,
Requires:       %{?scl_prefix}perl-Locale-Codes, %{?scl_prefix}perl-Locale-Maketext,
Requires:       %{?scl_prefix}perl-Locale-Maketext-Simple
Requires:       %{?scl_prefix}perl-Math-BigInt, %{?scl_prefix}perl-Math-BigInt-FastCalc, %{?scl_prefix}perl-Math-BigRat,
Requires:       %{?scl_prefix}perl-Math-Complex, %{?scl_prefix}perl-Memoize,
Requires:       %{?scl_prefix}perl-MIME-Base64,
Requires:       %{?scl_prefix}perl-Module-CoreList,
Requires:       %{?scl_prefix}perl-Module-CoreList-tools, %{?scl_prefix}perl-Module-Load
Requires:       %{?scl_prefix}perl-Module-Load-Conditional, %{?scl_prefix}perl-Module-Loaded,
Requires:       %{?scl_prefix}perl-Module-Metadata, %{?scl_prefix}perl-Net-Ping,
Requires:       %{?scl_prefix}perl-open, %{?scl_prefix}perl-PathTools
Requires:       %{?scl_prefix}perl-Params-Check, %{?scl_prefix}perl-Parse-CPAN-Meta,
Requires:       %{?scl_prefix}perl-perlfaq,
Requires:       %{?scl_prefix}perl-PerlIO-via-QuotedPrint, %{?scl_prefix}perl-Perl-OSType
Requires:       %{?scl_prefix}perl-Pod-Checker, %{?scl_prefix}perl-Pod-Escapes, %{?scl_prefix}perl-Pod-Html,
Requires:       %{?scl_prefix}perl-Pod-Parser, %{?scl_prefix}perl-Pod-Perldoc, %{?scl_prefix}perl-Pod-Usage
Requires:       %{?scl_prefix}perl-podlators, %{?scl_prefix}perl-Pod-Simple, %{?scl_prefix}perl-Scalar-List-Utils
Requires:       %{?scl_prefix}perl-SelfLoader, %{?scl_prefix}perl-Socket, %{?scl_prefix}perl-Storable, %{?scl_prefix}perl-Sys-Syslog,
Requires:       %{?scl_prefix}perl-Term-ANSIColor, %{?scl_prefix}perl-Term-Cap,
Requires:       %{?scl_prefix}perl-Test, %{?scl_prefix}perl-Test-Harness, %{?scl_prefix}perl-Test-Simple
Requires:       %{?scl_prefix}perl-Text-Balanced, %{?scl_prefix}perl-Text-ParseWords, %{?scl_prefix}perl-Text-Tabs+Wrap,
Requires:       %{?scl_prefix}perl-Thread-Queue
Requires:       %{?scl_prefix}perl-Time-HiRes
Requires:       %{?scl_prefix}perl-Time-Local, %{?scl_prefix}perl-Time-Piece
Requires:       %{?scl_prefix}perl-Unicode-Collate, %{?scl_prefix}perl-Unicode-Normalize,
Requires:       %{?scl_prefix}perl-version, %{?scl_prefix}perl-threads, %{?scl_prefix}perl-threads-shared, %{?scl_prefix}perl-parent

%description core
A metapackage which requires all of the perl bits and modules in the upstream
tarball from perl.org.


%if %{dual_life} || %{rebuild_from_scratch}
%package Archive-Tar
Summary:        A module for Perl manipulation of .tar files
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.04
BuildArch:      noarch
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(IO::Zlib) >= 1.01
# Optional run-time:
Requires:       %{?scl_prefix}perl(IO::Compress::Bzip2) >= 2.015
# IO::String not used if perl supports useperlio which is true
# Use Compress::Zlib's version for IO::Uncompress::Bunzip2
Requires:       %{?scl_prefix}perl(IO::Uncompress::Bunzip2) >= 2.015
%if !%{defined perl_bootstrap}
Requires:       %{?scl_prefix}perl(Text::Diff)
%endif
%if %{defined perl_bootstrap}
%gendep_perl_Archive_Tar
%endif

%description Archive-Tar
Archive::Tar provides an object oriented mechanism for handling tar files.  It
provides class methods for quick and easy files handling while also allowing
for the creation of tar file objects for custom manipulation.  If you have the
IO::Zlib module installed, Archive::Tar will also support compressed or
gzipped tar files.
%endif

%package Attribute-Handlers
Summary:        Simpler definition of attribute handlers
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.99
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Attribute_Handlers
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-351

%description Attribute-Handlers
This Perl module, when inherited by a package, allows that package's class to
define attribute handler subroutines for specific attributes. Variables and
subroutines subsequently defined in that package, or in packages derived from
that package may be given attributes with the same names as the attribute
handler subroutines, which will then be called in one of the compilation
phases (i.e. in a "BEGIN", "CHECK", "INIT", or "END" block).

%if %{dual_life} || %{rebuild_from_scratch}
%package autodie
Summary:        Replace functions with ones that succeed or die
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.29
Requires:       %perl_compat
BuildArch:      noarch
Requires:       %{?scl_prefix}perl(B)
Requires:       %{?scl_prefix}perl(Fcntl)
Requires:       %{?scl_prefix}perl(overload)
Requires:       %{?scl_prefix}perl(POSIX)
%if %{defined perl_bootstrap}
%gendep_perl_autodie
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.16.2-259

%description autodie
The "autodie" and "Fatal" pragma provides a convenient way to replace
functions that normally return false on failure with equivalents that throw an
exception on failure.

However "Fatal" has been obsoleted by the new autodie pragma. Please use
autodie in preference to "Fatal".
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package B-Debug
Summary:        Walk Perl syntax tree, print debug information about op-codes
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.23
Requires:       %perl_compat
BuildArch:      noarch
%if %{defined perl_bootstrap}
%gendep_perl_B_Debug
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.20.1-310

%description B-Debug
Walk Perl syntax tree and print debug information about op-codes. See
B::Concise and B::Terse for other details.
%endif

%package bignum
Summary:        Use BigInts and BigFloats transparently
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.42
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
# Math::BigInt::Lite is optional
Requires:       %{?scl_prefix}perl(Math::BigRat)
Requires:       %{?scl_prefix}perl(warnings)
BuildArch:      noarch
%if %{defined perl_bootstrap}
%gendep_perl_bignum
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-348

%description bignum
This package attempts to make it easier to write scripts that use BigInts and
BigFloats in a transparent way.

%if %{dual_life} || %{rebuild_from_scratch}
%package Carp
Summary:        Alternative warn and die for modules
Epoch:          0
# Real version 1.40
Version:        1.40
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
Provides:       %{?scl_prefix}perl(Carp::Heavy) = %{version}
%if %{defined perl_bootstrap}
%gendep_perl_Carp
%endif
BuildArch:      noarch

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\(Carp\\)\\s*$

%description Carp
The Carp routines are useful in your own modules because they act like
die() or warn(), but with a message which is more likely to be useful to a
user of your module. In the case of cluck, confess, and longmess that
context is a summary of every call in the call-stack. For a shorter message
you can use carp or croak which report the error as being from where your
module was called. There is no guarantee that that is where the error was,
but it is a good educated guess.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Compress-Raw-Bzip2
Summary:        Low-Level Interface to bzip2 compression library
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.069
Requires:       %{?scl_prefix}perl(Exporter), %{?scl_prefix}perl(File::Temp)
%if %{defined perl_bootstrap}
%gendep_perl_Compress_Raw_Bzip2
%endif

%description Compress-Raw-Bzip2
This module provides a Perl interface to the bzip2 compression library.
It is used by IO::Compress::Bzip2.

%package Compress-Raw-Zlib
Summary:        Low-Level Interface to the zlib compression library
Group:          Development/Libraries
License:        (GPL+ or Artistic) and zlib
Epoch:          0
Version:        2.069
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Compress_Raw_Zlib
%endif

%description Compress-Raw-Zlib
This module provides a Perl interface to the zlib compression library.
It is used by IO::Compress::Zlib.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Config-Perl-V
Summary:        Structured data retrieval of perl -V output
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.25
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Config_Perl_V
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

%description Config-Perl-V
The command "perl -V" will return you an excerpt from the %%Config::Config
hash combined with the output of "perl -V" that is not stored inside the hash,
but only available to the perl binary itself. This package provides Perl
module that will return you the output of "perl -V" in a structure.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package constant
Summary:        Perl pragma to declare constants
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.33
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_constant
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.16.3-264

%description constant
This pragma allows you to declare constants at compile-time:

use constant PI => 4 * atan2(1, 1);

When you declare a constant such as "PI" using the method shown above,
each machine your script runs upon can have as many digits of accuracy
as it can use. Also, your program will be easier to read, more likely
to be maintained (and maintained correctly), and far less likely to
send a space probe to the wrong planet because nobody noticed the one
equation in which you wrote 3.14195.

When a constant is used in an expression, Perl replaces it with its
value at compile time, and may then optimize the expression further.
In particular, any code in an "if (CONSTANT)" block will be optimized
away if the constant is false.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN
Summary:        Query, download and build perl modules from CPAN sites
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        2.11
Requires:       make
# Prefer Archive::Tar and Compress::Zlib over tar and gzip
Requires:       %{?scl_prefix}perl(Archive::Tar) >= 1.50
Requires:       %{?scl_prefix}perl(base)
Requires:       %{?scl_prefix}perl(Data::Dumper)
%if !%{defined perl_bootstrap}
Requires:       %{?scl_prefix}perl(Devel::Size)
%endif
Requires:       %{?scl_prefix}perl(ExtUtils::Manifest)
%if !%{defined perl_bootstrap}
Requires:       %{?scl_prefix}perl(File::HomeDir) >= 0.65
%endif
Requires:       %{?scl_prefix}perl(File::Temp) >= 0.16
Requires:       %{?scl_prefix}perl(lib)
Requires:       %{?scl_prefix}perl(Net::Config)
Requires:       %{?scl_prefix}perl(Net::FTP)
Requires:       %{?scl_prefix}perl(POSIX)
Requires:       %{?scl_prefix}perl(Term::ReadLine)
%if !%{defined perl_bootstrap}
Requires:       %{?scl_prefix}perl(URI)
Requires:       %{?scl_prefix}perl(URI::Escape)
%endif
Requires:       %{?scl_prefix}perl(User::pwent)
# Optional but higly recommended:
%if !%{defined perl_bootstrap}
Requires:       %{?scl_prefix}perl(Archive::Zip)
Requires:       %{?scl_prefix}perl(Compress::Bzip2)
Requires:       %{?scl_prefix}perl(CPAN::Meta) >= 2.110350
%endif
Requires:       %{?scl_prefix}perl(Compress::Zlib)
Requires:       %{?scl_prefix}perl(Digest::MD5)
# CPAN encourages Digest::SHA strongly because of integrity checks
Requires:       %{?scl_prefix}perl(Digest::SHA)
Requires:       %{?scl_prefix}perl(Dumpvalue)
Requires:       %{?scl_prefix}perl(ExtUtils::CBuilder)
%if ! %{defined perl_bootstrap}
# Avoid circular deps local::lib -> Module::Install -> CPAN when bootstraping
# local::lib recommended by CPAN::FirstTime default choice, bug #1122498
Requires:       %{?scl_prefix}perl(local::lib)
%endif
Requires:       %{?scl_prefix}perl(Module::Build)
%if ! %{defined perl_bootstrap}
Requires:       %{?scl_prefix}perl(Text::Glob)
%endif
Requires:       %perl_compat
Provides:       %{?scl_prefix}cpan = %{version}
%if %{defined perl_bootstrap}
%gendep_perl_CPAN
%endif
BuildArch:      noarch

%description CPAN
The CPAN module automates or at least simplifies the make and install of
perl modules and extensions. It includes some primitive searching
capabilities and knows how to use LWP, HTTP::Tiny, Net::FTP and certain
external download clients to fetch distributions from the net.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta
Summary:        Distribution metadata for a CPAN dist
Epoch:          0
Version:        2.150005
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_CPAN_Meta
%endif
BuildArch:      noarch

%description CPAN-Meta
Software distributions released to the CPAN include a META.json or, for
older distributions, META.yml, which describes the distribution, its
contents, and the requirements for building and installing the
distribution. The data structure stored in the META.json file is described
in CPAN::Meta::Spec.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta-Requirements
Summary:        Set of version requirements for a CPAN dist
Epoch:          0
# Real version 2.132000
Version:        2.132
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
BuildArch:      noarch
# CPAN-Meta-Requirements used to have six decimal places
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\(CPAN::Meta::Requirements\\)
%if ( 0%{?rhel} && ( 0%{?rhel} < 7 ))
%filter_from_provides /perl(CPAN::Meta::Requirements)/d
%filter_setup
%endif
Provides:       %{?scl_prefix}perl(CPAN::Meta::Requirements) = %{version}000
%if %{defined perl_bootstrap}
%gendep_perl_CPAN_Meta_Requirements
%endif

%description CPAN-Meta-Requirements
A CPAN::Meta::Requirements object models a set of version constraints like
those specified in the META.yml or META.json files in CPAN distributions.
It can be built up by adding more and more constraints, and it will reduce
them to the simplest representation.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta-YAML
Version:        0.018
Epoch:          0
Summary:        Read and write a subset of YAML for CPAN Meta files
License:        GPL+ or Artistic
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_CPAN_Meta_YAML
%endif

%description CPAN-Meta-YAML
This module implements a subset of the YAML specification for use in reading
and writing CPAN metadata files like META.yml and MYMETA.yml. It should not be
used for any other general YAML parsing or generation task.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Data-Dumper
Summary:        Stringify perl data structures, suitable for printing and eval
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.160
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Scalar::Util)
Requires:       %{?scl_prefix}perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_Data_Dumper
%endif

%description Data-Dumper
Given a list of scalars or reference variables, writes out their contents
in perl syntax. The references can also be objects. The content of each
variable is output in a single Perl statement. Handles self-referential
structures correctly.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package DB_File
Summary:        Perl5 access to Berkeley DB version 1.x
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.835
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Fcntl)
Requires:       %{?scl_prefix}perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_DB_File
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.16.3-264

%description DB_File
DB_File is a module which allows Perl programs to make use of the facilities
provided by Berkeley DB version 1.x (if you have a newer version of DB, you
will be limited to functionality provided by interface of version 1.x). The
interface defined here mirrors the Berkeley DB interface closely.
%endif

%package Devel-Peek
Summary:        A data debugging tool for the XS programmer
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.23
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Devel_Peek
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-351

%description Devel-Peek
Devel::Peek contains functions which allows raw Perl datatypes to be
manipulated from a Perl script. This is used by those who do XS programming to
check that the data they are sending from C to Perl looks as they think it
should look.

%if %{dual_life} || %{rebuild_from_scratch}
%package Devel-PPPort
Summary:        Perl Pollution Portability header generator
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.32
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Devel_PPPort
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.20.1-310

%description Devel-PPPort
Perl's API has changed over time, gaining new features, new functions,
increasing its flexibility, and reducing the impact on the C name space
environment (reduced pollution). The header file written by this module,
typically ppport.h, attempts to bring some of the newer Perl API features
to older versions of Perl, so that you can worry less about keeping track
of old releases, but users can still reap the benefit.
%endif

%package Devel-SelfStubber
Summary:        Generate stubs for a SelfLoading module
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.05
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Devel_SelfStubber
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-351

%description Devel-SelfStubber
Devel::SelfStubber prints the stubs you need to put in the module before the
__DATA__ token (or you can get it to print the entire module with stubs
correctly placed). The stubs ensure that if a method is called, it will get
loaded. They are needed specifically for inherited autoloaded methods.

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest
Summary:        Modules that calculate message digests
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          0
Version:        1.17
BuildArch:      noarch
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(MIME::Base64)
%if %{defined perl_bootstrap}
%gendep_perl_Digest
%endif

%description Digest
The Digest:: modules calculate digests, also called "fingerprints" or
"hashes", of some data, called a message. The digest is (usually)
some small/fixed size string. The actual size of the digest depend of
the algorithm used. The message is simply a sequence of arbitrary
bytes or bits.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest-MD5
Summary:        Perl interface to the MD5 Algorithm
Group:          Development/Libraries
License:        (GPL+ or Artistic) and BSD
# Epoch bump for clean upgrade over old standalone package
Epoch:          0
Version:        2.54
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(XSLoader)
# Recommended
Requires:       %{?scl_prefix}perl(Digest::base) >= 1.00
%if %{defined perl_bootstrap}
%gendep_perl_Digest_MD5
%endif

%description Digest-MD5
The Digest::MD5 module allows you to use the RSA Data Security Inc. MD5
Message Digest algorithm from within Perl programs. The algorithm takes as
input a message of arbitrary length and produces as output a 128-bit
"fingerprint" or "message digest" of the input.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest-SHA
Summary:        Perl extension for SHA-1/224/256/384/512
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        5.95
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
# Recommended
Requires:       %{?scl_prefix}perl(Digest::base)
%if %{defined perl_bootstrap}
%gendep_perl_Digest_SHA
%endif

%description Digest-SHA
Digest::SHA is a complete implementation of the NIST Secure Hash
Standard.  It gives Perl programmers a convenient way to calculate
SHA-1, SHA-224, SHA-256, SHA-384, and SHA-512 message digests.  The
module can handle all types of input, including partial-byte data.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Encode
Summary:        Character encodings in Perl
Group:          Development/Libraries
License:        (GPL+ or Artistic) and UCD
Epoch:          4
Version:        2.80
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Encode
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.16.2-256

%description Encode
The Encode module provides the interface between Perl strings and the rest
of the system. Perl strings are sequences of characters.

%package encoding
Summary:        Write your Perl script in non-ASCII or non-UTF-8
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          4
Version:        2.17
# Keeping this sub-package arch-specific because it installs files into
# arch-specific directories.
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
# Config not needed on perl ≥ 5.008
# Consider Filter::Util::Call as mandatory, bug #1165183, CPAN RT#100427
Requires:       %{?scl_prefix}perl(Filter::Util::Call)
# I18N::Langinfo is optional
# PerlIO::encoding is optional
Requires:       %{?scl_prefix}perl(utf8)
%if %{defined perl_bootstrap}
%gendep_perl_encoding
%endif
Conflicts:      %{?scl_prefix}perl-Encode < 2:2.60-314

%description encoding
With the encoding pragma, you can write your Perl script in any encoding you
like (so long as the Encode module supports it) and still enjoy Unicode
support.

However, this encoding module is deprecated under perl 5.18. It uses
a mechanism provided by perl that is deprecated under 5.18 and higher, and may
be removed in a future version.

The easiest and the best alternative is to write your script in UTF-8.

%package Encode-devel
Summary:        Character encodings in Perl
Group:          Development/Libraries
License:        (GPL+ or Artistic) and UCD
Epoch:          4
Version:        2.80
Requires:       %perl_compat
Requires:       %{name}-Encode = %{epoch}:%{version}-%{release}
#Recommends:     perl-devel
%if %{defined perl_bootstrap}
%gendep_perl_Encode_devel
%endif
BuildArch:      noarch

%description Encode-devel
enc2xs builds a Perl extension for use by Encode from either Unicode Character
Mapping files (.ucm) or Tcl Encoding Files (.enc). You can use enc2xs to add
your own encoding to perl. No knowledge of XS is necessary.
%endif
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_provides_in .*\.e2x$
%filter_requires_in .*\.e2x$
%filter_setup
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Env
Summary:        Perl module that imports environment variables as scalars or arrays
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.04
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Env
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.16.2-265

%description Env
Perl maintains environment variables in a special hash named %%ENV. For when
this access method is inconvenient, the Perl module Env allows environment
variables to be treated as scalar or array variables.
%endif

%package Errno
Summary:        System errno constants
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.25
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Errno
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-351

%description Errno
"Errno" defines and conditionally exports all the error constants defined in
your system "errno.h" include file. It has a single export tag, ":POSIX",
which will export all POSIX defined error numbers.

%if %{dual_life} || %{rebuild_from_scratch}
%package experimental
Summary:        Experimental features made easy
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.016
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_experimental
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.20.0-303

%description experimental
This pragma provides an easy and convenient way to enable or disable
experimental features.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Exporter
Summary:        Implements default import method for modules
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        5.72
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp) >= 1.05
%if %{defined perl_bootstrap}
%gendep_perl_Exporter
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.16.2-265

%description Exporter
The Exporter module implements an import method which allows a module to
export functions and variables to its users' name spaces. Many modules use
Exporter rather than implementing their own import method because Exporter
provides a highly flexible interface, with an implementation optimized for
the common case.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-CBuilder
Summary:        Compile and link C code for Perl modules
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.280225
BuildArch:      noarch
Requires:       %{?scl_prefix}perl-devel
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(DynaLoader)
Requires:       %{?scl_prefix}perl(ExtUtils::Mksymlists)
Requires:       %{?scl_prefix}perl(File::Spec) >= 3.13
Requires:       %{?scl_prefix}perl(Perl::OSType) >= 1
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_CBuilder
%endif

%description ExtUtils-CBuilder
This module can build the C portions of Perl modules by invoking the
appropriate compilers and linkers in a cross-platform manner. It was motivated
by the Module::Build project, but may be useful for other purposes as well.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-Command
Summary:        Perl routines to replace common UNIX commands in Makefiles
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        7.10
BuildArch:      noarch
Requires:       %perl_compat
Conflicts:      %{?scl_prefix}perl < 4:5.20.1-312
Requires:       %{?scl_prefix}perl(File::Find)
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Command
%endif

%description ExtUtils-Command
This Perl module is used to replace common UNIX commands. In all cases the
functions work with @ARGV rather than taking arguments. This makes them
easier to deal with in Makefiles.
%endif

%package ExtUtils-Embed
Summary:        Utilities for embedding Perl in C/C++ applications
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.33
Requires:       %{?scl_prefix}perl-devel
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Embed
%endif
BuildArch:      noarch

%description ExtUtils-Embed
Utilities for embedding Perl in C/C++ applications.


%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-Install
Summary:        Install files from here to there
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.04
BuildArch:      noarch
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Data::Dumper)
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Install
%endif

%description ExtUtils-Install
Handles the installing and uninstalling of perl modules, scripts, man
pages, etc.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-MakeMaker
Summary:        Create a module Makefile
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        7.10
# If an XS module is built, code generated from XS will be compiled and it
# includes Perl header files.
# TODO: This dependency will be weaken in order to relieve building noarch
# packages from perl-devel and gcc.
Requires:       %{?scl_prefix}perl-devel
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Data::Dumper)
Requires:       %{?scl_prefix}perl(DynaLoader)
Requires:       %{?scl_prefix}perl(ExtUtils::Command)
Requires:       %{?scl_prefix}perl(ExtUtils::Install)
Requires:       %{?scl_prefix}perl(ExtUtils::Manifest)
Requires:       %{?scl_prefix}perl(File::Find)
Requires:       %{?scl_prefix}perl(Getopt::Long)
# Optional Pod::Man is needed for generating manual pages from POD
Requires:       %{?scl_prefix}perl(Pod::Man)
Requires:       %{?scl_prefix}perl(POSIX)
Requires:       %{?scl_prefix}perl(Test::Harness)
Requires:       %{?scl_prefix}perl(version)
# If an XS module is compiled, xsubpp(1) is needed
Requires:       %{?scl_prefix}perl-ExtUtils-ParseXS
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_MakeMaker
%endif
BuildArch:      noarch

# Filter false DynaLoader provides. Versioned perl(DynaLoader) keeps
# unfiltered on perl package, no need to reinject it.
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\(DynaLoader\\)\\s*$
%global __provides_exclude %__provides_exclude|^%{?scl_prefix}perl\\(ExtUtils::MakeMaker::_version\\)
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_from_provides /perl(DynaLoader)\s*$/d
%filter_from_provides /perl(ExtUtils::MakeMaker::_version)\s*$/d
%filter_setup
%endif

%description ExtUtils-MakeMaker
Create a module Makefile.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-Manifest
Summary:        Utilities to write and check a MANIFEST file
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.70
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(File::Path)
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Manifest
%endif
BuildArch:      noarch

%description ExtUtils-Manifest
%{summary}.
%endif

%package ExtUtils-Miniperl
Summary:        Write the C code for perlmain.c
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.05
Requires:       %{?scl_prefix}perl-devel
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Miniperl
%endif
BuildArch:      noarch

%description ExtUtils-Miniperl
writemain() takes an argument list of directories containing archive libraries
that relate to perl modules and should be linked into a new perl binary. It
writes a corresponding perlmain.c file that is a plain C file containing all
the bootstrap code to make the If the first argument to writemain() is a
reference to a scalar it is used as the filename to open for ouput. Any other
reference is used as the filehandle to write to. Otherwise output defaults to
STDOUT.

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-MM-Utils
Summary:        ExtUtils::MM methods without dependency on ExtUtils::MakeMaker
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        7.11
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_MM_Utils
%endif

%description ExtUtils-MM-Utils
This is a collection of ExtUtils::MM subroutines that are used by many
other modules but that do not need full-featured ExtUtils::MakeMaker. The
issue with ExtUtils::MakeMaker is it pulls in Perl header files and that
is an overkill for small subroutines.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-ParseXS
Summary:        Module and a script for converting Perl XS code into C code
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.31
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_ParseXS
%endif
BuildArch:      noarch
Obsoletes:      %{?scl_prefix}perl-ExtUtils-Typemaps

%description ExtUtils-ParseXS
ExtUtils::ParseXS will compile XS code into C code by embedding the constructs
necessary to let C functions manipulate Perl values and creates the glue
necessary to let Perl access those functions.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package File-Fetch
Summary:        Generic file fetching mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.48
Requires:       %{?scl_prefix}perl(IPC::Cmd) >= 0.36
Requires:       %{?scl_prefix}perl(Module::Load::Conditional) >= 0.04
Requires:       %{?scl_prefix}perl(Params::Check) >= 0.07
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_File_Fetch
%endif
BuildArch:      noarch

%description File-Fetch
File::Fetch is a generic file fetching mechanism.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Path
Summary:        Create or remove directory trees
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.12
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_File_Path
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.16.2-265

%description File-Path
This module provides a convenient way to create directories of arbitrary
depth and to delete an entire directory subtree from the file system.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Temp
Summary:        Return name and handle of a temporary file safely
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
# Real version 0.2304
Version:        0.23.04
Requires:       %perl_compat
BuildArch:      noarch
Requires:       %{?scl_prefix}perl(File::Path) >= 2.06
Requires:       %{?scl_prefix}perl(POSIX)
%if %{defined perl_bootstrap}
%gendep_perl_File_Temp
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.16.2-265

%description File-Temp
File::Temp can be used to create and open temporary files in a safe way.
There is both a function interface and an object-oriented interface. The
File::Temp constructor or the tempfile() function can be used to return the
name and the open file handle of a temporary file. The tempdir() function
can be used to create a temporary directory.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
# FIXME Filter-Simple? version?
%package Filter
Summary:        Perl source filters
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          2
Version:        1.55
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Filter
%endif

%description Filter
Source filters alter the program text of a module before Perl sees it, much as
a C preprocessor alters the source text of a C program before the compiler
sees it.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Filter-Simple
Summary:        Simplified Perl source filtering
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.92
BuildArch:      noarch
Requires:       %perl_compat
Conflicts:      %{?scl_prefix}perl < 4:5.20.1-312
Requires:       %{?scl_prefix}perl(Text::Balanced) >= 1.97
Requires:       %{?scl_prefix}perl(warnings)
%if %{defined perl_bootstrap}
%gendep_perl_Filter_Simple
%endif

%description Filter-Simple
The Filter::Simple Perl module provides a simplified interface to
Filter::Util::Call; one that is sufficient for most common cases.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Getopt-Long
Summary:        Extended processing of command line options
Group:          Development/Libraries
License:        GPLv2+ or Artistic
Epoch:          0
Version:        2.48
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(overload)
Requires:       %{?scl_prefix}perl(Text::ParseWords)
# Recommended:
Requires:       %{?scl_prefix}perl(Pod::Usage) >= 1.14
%if %{defined perl_bootstrap}
%gendep_perl_Getopt_Long
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.16.3-268

%description Getopt-Long
The Getopt::Long module implements an extended getopt function called
GetOptions(). It parses the command line from @ARGV, recognizing and removing
specified options and their possible values.  It adheres to the POSIX syntax
for command line options, with GNU extensions. In general, this means that
options have long names instead of single letters, and are introduced with
a double dash "--". Support for bundling of command line options, as was the
case with the more traditional single-letter approach, is provided but not
enabled by default.
%endif

%package IO
Summary:        Perl input/output modules
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.36
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_IO
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-351

%description IO
This is a collection of Perl input/output modules.

%if %{dual_life} || %{rebuild_from_scratch}
%package IO-Compress
Summary:        IO::Compress wrapper for modules
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.069
Requires:       %perl_compat
Obsoletes:      %{?scl_prefix}perl-Compress-Zlib <= 2.020
Provides:       %{?scl_prefix}perl(IO::Uncompress::Bunzip2)
%if %{defined perl_bootstrap}
%gendep_perl_IO_Compress
%endif
BuildArch:      noarch

%description IO-Compress
This module is the base class for all IO::Compress and IO::Uncompress modules.
This module is not intended for direct use in application code. Its sole
purpose is to to be sub-classed by IO::Compress modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package IO-Socket-IP
Summary:        Drop-in replacement for IO::Socket::INET supporting both IPv4 and IPv6
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.37
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_IO_Socket_IP
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.20.0-303

%description IO-Socket-IP
This module provides a protocol-independent way to use IPv4 and IPv6
sockets, as a drop-in replacement for IO::Socket::INET. Most constructor
arguments and methods are provided in a backward-compatible way.
%endif

%package IO-Zlib
Summary:        Perl IO:: style interface to Compress::Zlib
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.10
Requires:       %{?scl_prefix}perl(Compress::Zlib)
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_IO_Zlib
%endif
BuildArch:      noarch

%description IO-Zlib
This modules provides an IO:: style interface to the Compress::Zlib package.
The main advantage is that you can use an IO::Zlib object in much the same way
as an IO::File object so you can have common code that doesn't know which sort
of file it is using.


%if %{dual_life} || %{rebuild_from_scratch}
%package IPC-Cmd
Summary:        Finding and running system commands made easy
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.92
Requires:       %{?scl_prefix}perl(ExtUtils::MM::Utils)
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_IPC_Cmd
%endif
BuildArch:      noarch

%description IPC-Cmd
IPC::Cmd allows you to run commands, interactively if desired, in a platform
independent way, but have them still work.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package IPC-SysV
Summary:        Object interface to System V IPC
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.06
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(DynaLoader)
%if %{defined perl_bootstrap}
%gendep_perl_IPC_SysV
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-351

%description IPC-SysV
This is an object interface for System V messages, semaphores, and
inter-process calls.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package HTTP-Tiny
Summary:        A small, simple, correct HTTP/1.1 client
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.056
Requires:       %{?scl_prefix}perl(bytes)
Requires:       %{?scl_prefix}perl(Carp)
Requires:       %{?scl_prefix}perl(IO::Socket)
Requires:       %{?scl_prefix}perl(Time::Local)
%if %{defined perl_bootstrap}
%gendep_perl_HTTP_Tiny
%endif
BuildArch:      noarch

%description HTTP-Tiny
This is a very simple HTTP/1.1 client, designed primarily for doing simple GET
requests without the overhead of a large framework like LWP::UserAgent.
It is more correct and more complete than HTTP::Lite. It supports proxies
(currently only non-authenticating ones) and redirection. It also correctly
resumes after EINTR.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package JSON-PP
Summary:        JSON::XS compatible pure-Perl module
Epoch:          0
Version:        2.27300
License:        GPL+ or Artistic
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Data::Dumper)
Requires:       %{?scl_prefix}perl(Encode)
Requires:       %{?scl_prefix}perl(Math::BigFloat)
Requires:       %{?scl_prefix}perl(Math::BigInt)
Requires:       %{?scl_prefix}perl(Scalar::Util)
Requires:       %{?scl_prefix}perl(subs)
%if %{defined perl_bootstrap}
%gendep_perl_JSON_PP
%endif
Conflicts:      %{?scl_prefix}perl-JSON < 2.50

%description JSON-PP
JSON::XS is the fastest and most proper JSON module on CPAN. It is written by
Marc Lehmann in C, so must be compiled and installed in the used environment.
JSON::PP is a pure-Perl module and is compatible with JSON::XS.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package libnet
Summary:        Perl clients for various network protocols
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.08
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(File::Basename)
Requires:       %{?scl_prefix}perl(IO::Socket) >= 1.05
# Prefer IO::Socket::IP over IO::Socket::INET6 and IO::Socket::INET
Requires:       %{?scl_prefix}perl(IO::Socket::IP) >= 0.20
Requires:       %{?scl_prefix}perl(POSIX)
Requires:       %{?scl_prefix}perl(Socket) >= 2.016
Requires:       %{?scl_prefix}perl(utf8)
%if %{defined perl_bootstrap}
%gendep_perl_libnet
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

%description libnet
This is a collection of Perl modules which provides a simple and
consistent programming interface (API) to the client side of various
protocols used in the internet community.
%endif

%package libnetcfg
Summary:        Configure libnet
Group:          Development/Tools
License:        GPL+ or Artistic
Epoch:          %perl_epoch
Version:        %perl_version
# Net::Config is optional
BuildArch:      noarch
%if %{defined perl_bootstrap}
%gendep_perl_libnetcfg
%endif
Conflicts:      %{?scl_prefix}perl-devel < 4:5.22.0-347

%description libnetcfg
The libnetcfg utility can be used to configure the libnet.

%if %{dual_life} || %{rebuild_from_scratch}
%package Locale-Codes
Summary:        Distribution of modules to handle locale codes
Epoch:          0
Version:        3.25
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(constant)
Provides:       %{?scl_prefix}perl(Locale::Codes) = %{version}
%if %{defined perl_bootstrap}
%gendep_perl_Locale_Codes
%endif
BuildArch:      noarch

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\(Locale::Codes\\)\\s*$

# Filter dependencies on private modules. Generator:
# for F in $(find lib -type f); do perl -e '$/ = undef; $_ = <>; if (/^package #\R([\w:]*);/m) { print qq{|^%{?scl_prefix}perl\\\\($1\\\\)} }' "$F"; done
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^%{?scl_prefix}perl\\(Locale::Codes::Country_Retired\\)|^%{?scl_prefix}perl\\(Locale::Codes::LangFam_Retired\\)|^%{?scl_prefix}perl\\(Locale::Codes::Script_Retired\\)|^%{?scl_prefix}perl\\(Locale::Codes::LangExt_Codes\\)|^%{?scl_prefix}perl\\(Locale::Codes::LangFam_Codes\\)|^%{?scl_prefix}perl\\(Locale::Codes::Script_Codes\\)|^%{?scl_prefix}perl\\(Locale::Codes::Language_Codes\\)|^%{?scl_prefix}perl\\(Locale::Codes::LangExt_Retired\\)|^%{?scl_prefix}perl\\(Locale::Codes::Currency_Codes\\)|^%{?scl_prefix}perl\\(Locale::Codes::LangVar_Retired\\)|^%{?scl_prefix}perl\\(Locale::Codes::Language_Retired\\)|^%{?scl_prefix}perl\\(Locale::Codes::Country_Codes\\)|^%{?scl_prefix}perl\\(Locale::Codes::LangVar_Codes\\)|^%{?scl_prefix}perl\\(Locale::Codes::Currency_Retired\\)

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_from_provides /perl(Locale::Codes)\s*$/d
%filter_from_requires /^%{?scl_prefix}perl(Locale::Codes::Country_Retired)\|^%{?scl_prefix}perl(Locale::Codes::LangFam_Retired)\|^%{?scl_prefix}perl(Locale::Codes::Script_Retired)\|^%{?scl_prefix}perl(Locale::Codes::LangExt_Codes)\|^%{?scl_prefix}perl(Locale::Codes::LangFam_Codes)\|^%{?scl_prefix}perl(Locale::Codes::Script_Codes)\|^%{?scl_prefix}perl(Locale::Codes::Language_Codes)\|^%{?scl_prefix}perl(Locale::Codes::LangExt_Retired)\|^%{?scl_prefix}perl(Locale::Codes::Currency_Codes)\|^%{?scl_prefix}perl(Locale::Codes::LangVar_Retired)\|^%{?scl_prefix}perl(Locale::Codes::Language_Retired)\|^%{?scl_prefix}perl(Locale::Codes::Country_Codes)\|^%{?scl_prefix}perl(Locale::Codes::LangVar_Codes)\|^%{?scl_prefix}perl(Locale::Codes::Currency_Retired)/d
%filter_setup
%endif

%description Locale-Codes
Locale-Codes is a distribution containing a set of modules. The modules
each deal with different types of codes which identify parts of the locale
including languages, countries, currency, etc.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Locale-Maketext
Summary:        Framework for localization
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.26
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Locale_Maketext
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.16.3-268

%description Locale-Maketext
It is a common feature of applications (whether run directly, or via the Web)
for them to be "localized" -- i.e., for them to present an English interface
to an English-speaker, a German interface to a German-speaker, and so on for
all languages it's programmed with. Locale::Maketext is a framework for
software localization; it provides you with the tools for organizing and
accessing the bits of text and text-processing code that you need for
producing localized applications.
%endif

%package Locale-Maketext-Simple
Summary:        Simple interface to Locale::Maketext::Lexicon
Group:          Development/Libraries
License:        MIT
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.21
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Locale_Maketext_Simple
%endif
BuildArch:      noarch

%description Locale-Maketext-Simple
This module is a simple wrapper around Locale::Maketext::Lexicon, designed
to alleviate the need of creating Language Classes for module authors.

%if %{dual_life} || %{rebuild_from_scratch}
%package Math-BigInt
Summary:        Arbitrary-size integer and float mathematics
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
# Real version 1.999715
Version:        1.9997.15
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
# File::Spec not used on recent perl
%if %{defined perl_bootstrap}
%gendep_perl_Math_BigInt
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\(Math::BigInt\\)\\s*$

%description Math-BigInt
This provides Perl modules for arbitrary-size integer and float mathematics.
%endif

%package Math-BigInt-FastCalc
Summary:        Math::BigInt::Calc XS implementation
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.40
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Math_BigInt_FastCalc
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-348

%description Math-BigInt-FastCalc
This package provides support for faster big integer calculations.

%package Math-BigRat
Summary:        Arbitrary big rational numbers
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
# Real version 0.2608.02
Version:        0.2608.02
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Math::BigInt)
%if %{defined perl_bootstrap}
%gendep_perl_Math_BigRat
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-348

%description Math-BigRat
Math::BigRat complements Math::BigInt and Math::BigFloat by providing support
for arbitrary big rational numbers.

%package Math-Complex
Summary:        Complex numbers and trigonometric functions
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.59
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Math_Complex
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-348

%description Math-Complex
This package lets you create and manipulate complex numbers. By default, Perl
limits itself to real numbers, but an extra "use" statement brings full
complex support, along with a full set of mathematical functions typically
associated with and/or extended to complex numbers.

%package Memoize
Summary:        Transparently speed up functions by caching return values
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.03
Requires:       %perl_compat
# Keep Time::HiRes optional
%if %{defined perl_bootstrap}
%gendep_perl_Memoize
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-350

%description Memoize
Memoizing a function makes it faster by trading space for time. It does
this by caching the return values of the function in a table. If you call
the function again with the same arguments, memoize jumps in and gives
you the value out of the table, instead of letting the function compute
the value all over again.

%if %{dual_life} || %{rebuild_from_scratch}
%package MIME-Base64
Summary:        Encoding and decoding of Base64 and quoted-printable strings
Group:          Development/Libraries
# cpan/MIME-Base64/Base64.xs:   (GPL+ or Artistic) and MIT (Bellcore's part)
# Other files:                  GPL+ or Artistic
License:        (GPL+ or Artistic) and MIT
Epoch:          0
Version:        3.15
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_MIME_Base64
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

%description MIME-Base64
This package contains a Base64 encoder/decoder and a quoted-printable
encoder/decoder. These encoding methods are specified in RFC 2045 - MIME
(Multipurpose Internet Mail Extensions).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Module-CoreList
Summary:        What modules are shipped with versions of perl
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          1
Version:        5.20160506
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(List::Util)
Requires:       %{?scl_prefix}perl(version) >= 0.88
%if %{defined perl_bootstrap}
%gendep_perl_Module_CoreList
%endif
BuildArch:      noarch

%description Module-CoreList
Module::CoreList provides information on which core and dual-life modules
are shipped with each version of perl.


%package Module-CoreList-tools
Summary:        Tool for listing modules shipped with perl
Group:          Development/Tools
License:        GPL+ or Artistic
Epoch:          1
Version:        5.20160506
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(feature)
Requires:       %{?scl_prefix}perl(version) >= 0.88
Requires:       %{?scl_prefix}perl-Module-CoreList = %{epoch}:%{version}-%{release}
%if %{defined perl_bootstrap}
%gendep_perl_Module_CoreList_tools
%endif
# The files were distributed with perl.spec's subpackage
# perl-Module-CoreList <= 1:5.020001-309
Conflicts:      %{?scl_prefix}perl-Module-CoreList < 1:5.020001-310
BuildArch:      noarch

%description Module-CoreList-tools
This package provides a corelist(1) tool which can be used to query what
modules were shipped with given perl version.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Load
Summary:        Runtime require of both modules and files
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.32
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Module_Load
%endif
BuildArch:      noarch

%description Module-Load
Module::Load eliminates the need to know whether you are trying to require
either a file or a module.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Load-Conditional
Summary:        Looking up module information / loading at runtime
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.64
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Module_Load_Conditional
%endif
BuildArch:      noarch

%description Module-Load-Conditional
Module::Load::Conditional provides simple ways to query and possibly load any
of the modules you have installed on your system during runtime.
%endif


%package Module-Loaded
Summary:        Mark modules as loaded or unloaded
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.08
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Module_Loaded
%endif
BuildArch:      noarch

%description Module-Loaded
When testing applications, often you find yourself needing to provide
functionality in your test environment that would usually be provided by
external modules. Rather than munging the %%INC by hand to mark these external
modules as loaded, so they are not attempted to be loaded by perl, this module
offers you a very simple way to mark modules as loaded and/or unloaded.


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Metadata
Summary:        Gather package and POD information from perl module files
Epoch:          0
Version:        1.000031
License:        GPL+ or Artistic
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Module_Metadata
%endif

%description Module-Metadata
Gather package and POD information from perl module files
%endif

%package Net-Ping
Summary:        Check a remote host for reachability
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.43
Requires:       %perl_compat
# Keep Net::Ping::External optional
%if %{defined perl_bootstrap}
%gendep_perl_Net_Ping
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-350

%description Net-Ping
Net::Ping module contains methods to test the reachability of remote hosts on
a network.

%package open
Summary:        Perl pragma to set default PerlIO layers for input and output
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.10
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
Requires:       %{?scl_prefix}perl(Encode)
Requires:       %{?scl_prefix}perl(encoding)
%if %{defined perl_bootstrap}
%gendep_perl_open
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.20.2-326
BuildArch:      noarch

%description open
The "open" pragma serves as one of the interfaces to declare default "layers"
(also known as "disciplines") for all I/O.

%if %{dual_life} || %{rebuild_from_scratch}
%package parent
Summary:        Establish an ISA relationship with base classes at compile time
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.234
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_parent
%endif
BuildArch:      noarch

%description parent
parent allows you to both load one or more modules, while setting up
inheritance from those modules at the same time. Mostly similar in effect to:

    package Baz;

    BEGIN {
        require Foo;
        require Bar;

        push @ISA, qw(Foo Bar);
    }
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Params-Check
Summary:        Generic input parsing/checking mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.38
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Params_Check
%endif
BuildArch:      noarch

%description Params-Check
Params::Check is a generic input parsing/checking mechanism.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Parse-CPAN-Meta
Summary:        Parse META.yml and other similar CPAN metadata files
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.4417
Requires:       %perl_compat
BuildArch:      noarch
Requires:       %{?scl_prefix}perl(CPAN::Meta::YAML) >= 0.002
Requires:       %{?scl_prefix}perl(JSON::PP) >= 2.27103
%if %{defined perl_bootstrap}
%gendep_perl_Parse_CPAN_Meta
%endif
# FIXME it could be removed now?
Obsoletes:      %{?scl_prefix}perl-Parse-CPAN-Meta < 1.40

%description Parse-CPAN-Meta
Parse::CPAN::Meta is a parser for META.yml files, based on the parser half of
YAML::Tiny.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package PathTools
Summary:        PathTools Perl module (Cwd, File::Spec)
Group:          Development/Libraries
License:        (GPL+ or Artistic) and BSD
Epoch:          0
Version:        3.63
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_PathTools
%endif

%description PathTools
PathTools Perl module (Cwd, File::Spec).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package perlfaq
Summary:        Frequently asked questions about Perl
Group:          Development/Libraries
# Code examples are Public Domain
License:        (GPL+ or Artistic) and Public Domain
Epoch:          0
Version:        5.021010
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_perlfaq
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

%description perlfaq
The perlfaq comprises several documents that answer the most commonly asked
questions about Perl and Perl programming.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package PerlIO-via-QuotedPrint
Summary:        PerlIO layer for quoted-printable strings
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.08
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_PerlIO_via_QuotedPrint
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

%description PerlIO-via-QuotedPrint
This module implements a PerlIO layer that works on files encoded in the
quoted-printable format. It will decode from quoted-printable while
reading from a handle, and it will encode as quoted-printable while
writing to a handle.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Perl-OSType
Summary:        Map Perl operating system names to generic types
Version:        1.009
Epoch:          0
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Perl_OSType
%endif
BuildArch:      noarch

%description Perl-OSType
Modules that provide OS-specific behaviors often need to know if the current
operating system matches a more generic type of operating systems. For example,
'linux' is a type of 'Unix' operating system and so is 'freebsd'.
This module provides a mapping between an operating system name as given by $^O
and a more generic type. The initial version is based on the OS type mappings
provided in Module::Build and ExtUtils::CBuilder (thus, Microsoft operating
systems are given the type 'Windows' rather than 'Win32').
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Checker
Summary:        Check POD documents for syntax errors
Epoch:          4
Version:        1.60
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Checker
%endif
BuildArch:      noarch

%description Pod-Checker
Module and tools to verify POD documentation contents for compliance with the
Plain Old Documentation format specifications.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Escapes
Summary:        Resolve POD escape sequences
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.07
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Escapes
%endif
BuildArch:      noarch

%description Pod-Escapes
This module provides things that are useful in decoding Pod E<...> sequences.
%endif

%package Pod-Html
Summary:        Convert POD files to HTML
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.22
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Html
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-350

%description Pod-Html
This package converts files from POD format (see perlpod) to HTML format. It
can automatically generate indexes and cross-references, and it keeps a cache
of things it knows how to cross-reference.

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Parser
Summary:        Basic perl modules for handling Plain Old Documentation (POD)
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.63
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Parser
%endif
BuildArch:      noarch

%description Pod-Parser
This software distribution contains the packages for using Perl5 POD (Plain
Old Documentation). See the "perlpod" and "perlsyn" manual pages from your
Perl5 distribution for more information about POD.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Perldoc
Summary:        Look up Perl documentation in Pod format
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.25
# Pod::Perldoc::ToMan executes roff
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
Requires:       groff
%else
Requires:       groff-base
%endif
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(File::Temp) >= 0.22
Requires:       %{?scl_prefix}perl(HTTP::Tiny)
Requires:       %{?scl_prefix}perl(IO::Handle)
Requires:       %{?scl_prefix}perl(IPC::Open3)
# POD2::Base is optional
# Pod::Checker is not needed if Pod::Simple::Checker is available
Requires:       %{?scl_prefix}perl(Pod::Simple::Checker)
Requires:       %{?scl_prefix}perl(Pod::Simple::RTF) >= 3.16
Requires:       %{?scl_prefix}perl(Pod::Simple::XMLOutStream) >= 3.16
Requires:       %{?scl_prefix}perl(Text::ParseWords)
# Tk is optional
Requires:       %{?scl_prefix}perl(Symbol)
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Perldoc
%endif
BuildArch:      noarch

%description Pod-Perldoc
perldoc looks up a piece of documentation in .pod format that is embedded
in the perl installation tree or in a perl script, and displays it via
"groff -man | $PAGER". This is primarily used for the documentation for
the perl library modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Simple
Summary:        Framework for parsing POD documentation
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.32
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Simple
%endif
BuildArch:      noarch

%description Pod-Simple
Pod::Simple is a Perl library for parsing text in the Pod ("plain old
documentation") markup language that is typically used for writing
documentation for Perl and for Perl modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Usage
Summary:        Print a usage message from embedded pod documentation
License:        GPL+ or Artistic
Group:          Development/Libraries
Epoch:          4
Version:        1.68
Requires:       %perl_compat
# Pod::Usage executes perldoc from perl-Pod-Perldoc by default
Requires:       %{?scl_prefix}perl-Pod-Perldoc
Requires:       %{?scl_prefix}perl(Pod::Text)
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Usage
%endif
BuildArch:      noarch

%description Pod-Usage
pod2usage will print a usage message for the invoking script (using its
embedded POD documentation) and then exit the script with the desired exit
status. The usage message printed may have any one of three levels of
"verboseness": If the verbose level is 0, then only a synopsis is printed.
If the verbose level is 1, then the synopsis is printed along with a
description (if present) of the command line options and arguments. If the
verbose level is 2, then the entire manual page is printed.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package podlators
Summary:        Format POD source into various output formats
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        4.07
BuildArch:      noarch
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(File::Spec) >= 0.8
Requires:       %{?scl_prefix}perl(Pod::Simple) >= 3.06
%if %{defined perl_bootstrap}
%gendep_perl_podlators
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.16.1-234

%description podlators
This package contains Pod::Man and Pod::Text modules which convert POD input
to *roff source output, suitable for man pages, or plain text.  It also
includes several sub-classes of Pod::Text for formatted output to terminals
with various capabilities.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Scalar-List-Utils
Summary:        A selection of general-utility scalar and list subroutines
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          3
# Real version 1.42_02
Version:        1.42
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Scalar_List_Utils
%endif

%description Scalar-List-Utils
Scalar::Util and List::Util contain a selection of subroutines that people have
expressed would be nice to have in the perl core, but the usage would not
really be high enough to warrant the use of a keyword, and the size so small
such that being individual extensions would be wasteful.
%endif

%package SelfLoader
Summary:        Load functions only on demand
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.23
BuildArch:      noarch
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_SelfLoader
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-351

%description SelfLoader
This Perl module tells its users that functions in a package are to be
autoloaded from after the "__DATA__" token. See also "Autoloading" in
perlsub.

%if %{dual_life} || %{rebuild_from_scratch}
%package Socket
Summary:        C socket.h defines and structure manipulators
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          4
Version:        2.020
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Socket
%endif

%description Socket
This module is just a translation of the C socket.h file.  Unlike the old
mechanism of requiring a translated socket.ph file, this uses the h2xs program
(see the Perl source distribution) and your native C compiler.  This means
that it has a far more likely chance of getting the numbers right.  This
includes all of the commonly used pound-defines like AF_INET, SOCK_STREAM, etc.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Storable
Summary:        Persistence for Perl data structures
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          1
Version:        2.56
Requires:       %perl_compat
# Carp substitutes missing Log::Agent
Requires:       %{?scl_prefix}perl(Carp)
Requires:       %{?scl_prefix}perl(Config)
# Fcntl is optional, but locking is good
Requires:       %{?scl_prefix}perl(Fcntl)
Requires:       %{?scl_prefix}perl(IO::File)
%if %{defined perl_bootstrap}
%gendep_perl_Storable
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.16.3-274

%description Storable
The Storable package brings persistence to your Perl data structures
containing scalar, array, hash or reference objects, i.e. anything that
can be conveniently stored to disk and retrieved at a later time.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Sys-Syslog
Summary:        Perl interface to the UNIX syslog(3) calls
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.33
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_Sys_Syslog
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.16.3-269

%description Sys-Syslog
Sys::Syslog is an interface to the UNIX syslog(3) function. Call syslog() with
a string priority and a list of printf() arguments just like at syslog(3).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Term-ANSIColor
Summary:        Color screen output using ANSI escape sequences
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        4.04
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Term_ANSIColor
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.18.2-302

%description Term-ANSIColor
This module has two interfaces, one through color() and colored() and the
other through constants. It also offers the utility functions uncolor(),
colorstrip(), colorvalid(), and coloralias(), which have to be explicitly
imported to be used.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Term-Cap
Summary:        Perl termcap interface
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.17
Requires:       %perl_compat
# ncurses for infocmp tool
Requires:       ncurses
Requires:       %{?scl_prefix}perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Term_Cap
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

%description Term-Cap
These are low-level functions to extract and use capabilities from a terminal
capability (termcap) database.
%endif

%package Test
Summary:        Simple framework for writing test scripts
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.28
Requires:       %perl_compat
# Algorithm::Diff 1.15 is optional
Requires:       %{?scl_prefix}perl(File::Temp)
%if %{defined perl_bootstrap}
%gendep_perl_Test
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-351

%description Test
The Test Perl module simplifies the task of writing test files for Perl modules,
such that their output is in the format that Test::Harness expects to see.

%if %{dual_life} || %{rebuild_from_scratch}
%package Test-Harness
Summary:        Run Perl standard test scripts with statistics
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        3.36
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Test_Harness
%endif
BuildArch:      noarch

%description Test-Harness
Run Perl standard test scripts with statistics.
Use TAP::Parser, Test::Harness package was whole rewritten.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Test-Simple
Summary:        Basic utilities for writing tests
Group:          Development/Languages
License:        (GPL+ or Artistic) and CC0 and Public Domain
Epoch:          0
Version:        1.001014
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Data::Dumper)
%if %{defined perl_bootstrap}
%gendep_perl_Test_Simple
%endif
BuildArch:      noarch

%description Test-Simple
Basic utilities for writing tests.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-Balanced
Summary:        Extract delimited text sequences from strings
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.03
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Text_Balanced
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

%description Text-Balanced
These Perl subroutines may be used to extract a delimited substring, possibly
after skipping a specified prefix string.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-ParseWords
Summary:        Parse text into an array of tokens or array of arrays
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.30
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Text_ParseWords
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.16.2-256

%description Text-ParseWords
Parse text into an array of tokens or array of arrays.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-Tabs+Wrap
Summary:        Expand tabs and do simple line wrapping
Group:          Development/Libraries
License:        TTWL
Epoch:          0
Version:        2013.0523
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Text_Tabs_Wrap
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.20.2-325

%description Text-Tabs+Wrap
Text::Tabs performs the same job that the UNIX expand(1) and unexpand(1)
commands do: adding or removing tabs from a document.

Text::Wrap::wrap() will reformat lines into paragraphs. All it does is break
up long lines, it will not join short lines together.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Thread-Queue
Summary:        Thread-safe queues
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.09
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Thread_Queue
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.16.2-257

%description Thread-Queue
This module provides thread-safe FIFO queues that can be accessed safely by
any number of threads.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Time-HiRes
Summary:        High resolution alarm, sleep, gettimeofday, interval timers
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.9733
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Time_HiRes
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.16.3-271

%description Time-HiRes
The Time::HiRes module implements a Perl interface to the usleep, nanosleep,
ualarm, gettimeofday, and setitimer/getitimer system calls, in other words,
high resolution time and timers.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Time-Local
Summary:        Efficiently compute time from local and GMT time
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.2300
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Time_Local
%endif
BuildArch:      noarch
Conflicts:      %{?scl_prefix}perl < 4:5.16.3-262

%description Time-Local
This module provides functions that are the inverse of built-in perl functions
localtime() and gmtime(). They accept a date as a six-element array, and
return the corresponding time(2) value in seconds since the system epoch
(Midnight, January 1, 1970 GMT on Unix, for example). This value can be
positive or negative, though POSIX only requires support for positive values,
so dates before the system's epoch may not work on all operating systems.
%endif

%package Time-Piece
Summary:        Time objects from localtime and gmtime
Group:          Development/Libraries
License:        (GPL+ or Artistic) and BSD
Epoch:          0
Version:        1.31
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Time_Piece
%endif

%description Time-Piece
The Time::Piece module replaces the standard localtime and gmtime functions
with implementations that return objects.  It does so in a backwards compatible
manner, so that using localtime or gmtime as documented in perlfunc still
behave as expected.

%if %{dual_life} || %{rebuild_from_scratch}
%package threads
Summary:        Perl interpreter-based threads
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          1
Version:        2.07
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_threads
%endif

%description threads
Since Perl 5.8, thread programming has been available using a model called
interpreter threads  which provides a new Perl interpreter for each thread,
and, by default, results in no data or state information being shared between
threads.

(Prior to Perl 5.8, 5005threads was available through the Thread.pm API. This
threading model has been deprecated, and was removed as of Perl 5.10.0.)

As just mentioned, all variables are, by default, thread local. To use shared
variables, you need to also load threads::shared.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package threads-shared
Summary:        Perl extension for sharing data structures between threads
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.51
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_threads_shared
%endif

%description threads-shared
By default, variables are private to each thread, and each newly created thread
gets a private copy of each existing variable. This module allows you to share
variables across different threads (and pseudo-forks on Win32). It is used
together with the threads module.  This module supports the sharing of the
following data types only: scalars and scalar refs, arrays and array refs, and
hashes and hash refs.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Unicode-Collate
Summary:        Unicode Collation Algorithm
Group:          Development/Libraries
License:        (GPL+ or Artistic) and UCD
Epoch:          0
Version:        1.14
Requires:       %perl_compat
Requires:       %{?scl_prefix}perl(Unicode::Normalize)
%if %{defined perl_bootstrap}
%gendep_perl_Unicode_Collate
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

%description Unicode-Collate
This package is Perl implementation of Unicode Technical Standard #10 (Unicode
Collation Algorithm).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Unicode-Normalize
Summary:        Unicode Normalization Forms
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.25
Requires:       %perl_compat
# unicore/CombiningClass.pl and unicore/Decomposition.pl from perl, perl is
# auto-detected.
%if %{defined perl_bootstrap}
%gendep_perl_Unicode_Normalize
%endif
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

%description Unicode-Normalize
This package provides Perl functions that can convert strings into various
Unicode normalization forms as defined in Unicode Standard Annex #15.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package version
Summary:        Perl extension for Version Objects
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          5
# real version 0.9916
Version:        0.99.16
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_version
%endif
BuildArch:      noarch

%description version
Perl extension for Version Objects
%endif

%prep
%setup -q -n perl-%{perl_version}
%patch1 -p1
%ifarch %{multilib_64_archs}
%patch3 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch15 -p1
%patch16 -p1
%patch22 -p1
%patch26 -p1
%patch28 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch200 -p1
%patch201 -p1
%patch300 -p1
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%patch301 -p1
%endif
%patch302 -p1

# Update libperl soname
%{?scl:sed -i 's|@scl@|%{?scl_prefix}|g' Makefile.SH}
%{!?scl:sed -i 's|@scl@||g' Makefile.SH}

%if !%{defined perl_bootstrap}
# Local patch tracking
perl -x patchlevel.h \
    'Fedora Patch1: Removes date check, Fedora/RHEL specific' \
%ifarch %{multilib_64_archs} \
    'Fedora Patch3: support for libdir64' \
%endif \
    'Fedora Patch4: use libresolv instead of libbind' \
    'Fedora Patch5: USE_MM_LD_RUN_PATH' \
    'Fedora Patch6: Provide MM::maybe_command independently (bug #1129443)' \
    'Fedora Patch7: Dont run one io test due to random builder failures' \
    'Fedora Patch15: Define SONAME for libperl.so' \
    'Fedora Patch16: Install libperl.so to -Dshrpdir value' \
    'Fedora Patch22: Document Math::BigInt::CalcEmu requires Math::BigInt (CPAN RT#85015)' \
    'Fedora Patch26: Make *DBM_File desctructors thread-safe (RT#61912)' \
    'Fedora Patch27: Make PadlistNAMES() lvalue again (CPAN RT#101063)' \
    'Fedora Patch28: Make magic vtable writable as a work-around for Coro (CPAN RT#101063)' \
    'Fedora Patch30: Replace EU::MakeMaker dependency with EU::MM::Utils in IPC::Cmd (bug #1129443)' \
    'Fedora Patch31: Fix a memory leak in compiling a POSIX class (RT#128313)' \
    'Fedora Patch32: Do not mangle errno from failed socket calls (RT#128316)' \
    'Fedora Patch33: Fix compiling regular expressions like /\X*(?0)/ (RT#128109)' \
    'Fedora Patch34: Do not use unitialized memory in $h{\const} warnings (RT#128189)' \
    'Fedora Patch35: Fix precedence in hv_ename_delete (RT#128086)' \
    'Fedora Patch36: Do not treat %: as a stash (RT#128238)' \
    'Fedora Patch37: Do not crash when inserting a non-stash into a stash (RT#128238)' \
    'Fedora Patch38: Fix line numbers with perl -x (RT#128508)' \
    'Fedora Patch39: Do not let XSLoader load relative paths (CVE-2016-6185)' \
    'Fedora Patch40: Fix a crash when vivifying a stub in a deleted package (RT#128532)' \
    'Fedora Patch41: Fix a crash in "Subroutine redefined" warning (RT#128257)' \
    'Fedora Patch42: Fix a crash in lexical scope warnings (RT#128597)' \
    'Fedora Patch200: Link XS modules to libperl.so with EU::CBuilder on Linux' \
    'Fedora Patch201: Link XS modules to libperl.so with EU::MM on Linux' \
    %{nil}
%endif

#copy the example script
cp -a %{SOURCE5} .

#copy Pod-Html license clarification
cp %{SOURCE6} .

#
# Candidates for doc recoding (need case by case review):
# find . -name "*.pod" -o -name "README*" -o -name "*.pm" | xargs file -i | grep charset= | grep -v '\(us-ascii\|utf-8\)'
recode()
{
        iconv -f "${2:-iso-8859-1}" -t utf-8 < "$1" > "${1}_"
        touch -r "$1" "${1}_"
        mv -f "${1}_" "$1"
}
# TODO iconv fail on this one
##recode README.tw big5
#recode pod/perlebcdic.pod
#recode pod/perlhack.pod
#recode pod/perlhist.pod
#recode pod/perlthrtut.pod
#recode AUTHORS

find . -name \*.orig -exec rm -fv {} \;

# Configure Compress::Zlib to use system zlib
sed -i 's|BUILD_ZLIB      = True|BUILD_ZLIB      = False|
    s|INCLUDE         = ./zlib-src|INCLUDE         = %{_root_includedir}|
    s|LIB             = ./zlib-src|LIB             = %{_root_libdir}|' \
    cpan/Compress-Raw-Zlib/config.in

# Ensure that we never accidentally bundle zlib or bzip2
rm -rf cpan/Compress-Raw-Zlib/zlib-src
rm -rf cpan/Compress-Raw-Bzip2/bzip2-src
sed -i '/\(bzip2\|zlib\)-src/d' MANIFEST

%if !%{with gdbm}
# Do not install anything requiring NDBM_File if NDBM is not available.
rm -rf 'cpan/Memoize/Memoize/NDBM_File.pm'
sed -i '\|cpan/Memoize/Memoize/NDBM_File.pm|d' MANIFEST
%endif


%build
echo "RPM Build arch: %{_arch}"

# use "lib", not %%{_lib}, for privlib, sitelib, and vendorlib
# To build production version, we would need -DDEBUGGING=-g

# Perl INC path (perl -V) in search order:
# - /usr/local/share/perl5            -- for CPAN     (site lib)
# - /usr/local/lib[64]/perl5          -- for CPAN     (site arch)
# - /usr/share/perl5/vendor_perl      -- 3rd party    (vendor lib)
# - /usr/lib[64]/perl5/vendor_perl    -- 3rd party    (vendor arch)
# - /usr/share/perl5                  -- Fedora       (priv lib)
# - /usr/lib[64]/perl5                -- Fedora       (arch lib)

%global privlib     %{_prefix}/share/perl5
%global archlib     %{_libdir}/perl5

%global perl_vendorlib  %{privlib}/vendor_perl
%global perl_vendorarch %{archlib}/vendor_perl

# Disable hardening due to some run-time failures, bug #1238804
%undefine _hardened_build
# ldflags is not used when linking XS modules.
# Only ldflags is used when linking miniperl.
# Only ccflags and ldflags are used for Configure's compiler checks.
# Set optimize=none to prevent from injecting upstream's value.
/bin/sh Configure -des \
        -Doptimize="none" \
        -Dccflags="$RPM_OPT_FLAGS" \
        -Dldflags="$RPM_LD_FLAGS" \
        -Dccdlflags="-Wl,--enable-new-dtags $RPM_LD_FLAGS" \
        -Dlddlflags="-shared $RPM_LD_FLAGS %{?scl:-L%{_libdir}}" \
        -Dshrpdir="%{_libdir}" \
        -DDEBUGGING=-g \
        -Dversion=%{perl_version} \
        -Dmyhostname=localhost \
        -Dperladmin=root@localhost \
        -Dcc='%{__cc}' \
        -Dcf_by='Red Hat, Inc.' \
        -Dprefix=%{_prefix} \
        -Dvendorprefix=%{_prefix} \
        -Dsiteprefix=%{_prefix}/local \
        -Dsitelib="%{_prefix}/local/share/perl5" \
        -Dsitearch="%{_prefix}/local/%{_lib}/perl5" \
        -Dprivlib="%{privlib}" \
        -Dvendorlib="%{perl_vendorlib}" \
        -Darchlib="%{archlib}" \
        -Dvendorarch="%{perl_vendorarch}" \
        -Darchname=%{perl_archname} \
%ifarch %{multilib_64_archs}
        -Dlibpth="/usr/local/lib64 /lib64 %{_root_prefix}/lib64" \
%endif
%ifarch sparc sparcv9
        -Ud_longdbl \
%endif
        -Duseshrplib \
        -Dusethreads \
        -Duseithreads \
        -Dusedtrace='/usr/bin/dtrace' \
        -Duselargefiles \
        -Dd_semctl_semun \
        -Di_db \
%if %{with gdbm}
        -Ui_ndbm \
        -Di_gdbm \
%endif
        -Di_shadow \
        -Di_syslog \
        -Dman3ext=3pm \
        -Dman1dir=%{_mandir}/man1 \
        -Dman3dir=%{_mandir}/man3 \
        -Duseperlio \
        -Dinstallusrbinperl=n \
        -Ubincompat5005 \
        -Uversiononly \
        -Dpager='/usr/bin/less -isr' \
        -Dd_gethostent_r_proto -Ud_endhostent_r_proto -Ud_sethostent_r_proto \
        -Ud_endprotoent_r_proto -Ud_setprotoent_r_proto \
        -Ud_endservent_r_proto -Ud_setservent_r_proto \
        -Dscriptdir='%{_bindir}' \
        -Dusesitecustomize \
        -Duse64bitint1

# -Duseshrplib creates libperl.so, -Ubincompat5005 help create DSO -> libperl.so

BUILD_BZIP2=0
BZIP2_LIB=%{_libdir}
export BUILD_BZIP2 BZIP2_LIB

%ifarch sparc64 %{arm}
make
%else
make %{?_smp_mflags}
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT

%global build_archlib $RPM_BUILD_ROOT%{archlib}
%global build_privlib $RPM_BUILD_ROOT%{privlib}
%global build_bindir  $RPM_BUILD_ROOT%{_bindir}
%global new_perl LD_PRELOAD="%{build_archlib}/CORE/libperl.so" \\\
    LD_LIBRARY_PATH="%{build_archlib}/CORE" \\\
    PERL5LIB="%{build_archlib}:%{build_privlib}" \\\
    %{build_bindir}/perl

# create directories in opt
mkdir -p $RPM_BUILD_ROOT%{privlib}
mkdir -p $RPM_BUILD_ROOT%{archlib}

mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}
mkdir -p $RPM_BUILD_ROOT%{perl_vendorarch}

# perl doesn't create the auto subdirectory, but modules put things in it,
# so we need to own it.
mkdir -p -m 755 %{build_archlib}/auto

# Make proper DSO names, move libperl to standard path.
%global soname libperl.so.%{?scl_prefix}%(echo '%{perl_version}' | sed 's/^\\([^.]*\\.[^.]*\\).*/\\1/')
mv "%{build_archlib}/CORE/libperl.so" \
    "$RPM_BUILD_ROOT%{_libdir}/libperl.so.%{?scl_prefix}%{perl_version}"
ln -s "libperl.so.%{?scl_prefix}%{perl_version}" "$RPM_BUILD_ROOT%{_libdir}/%{soname}"
ln -s "libperl.so.%{?scl_prefix}%{perl_version}" "$RPM_BUILD_ROOT%{_libdir}/libperl.so"
# XXX: Keep symlink from original location because various code glues
# $archlib/CORE/$libperl to get the DSO.
ln -s "../../libperl.so.%{?scl_prefix}%{perl_version}" "%{build_archlib}/CORE/libperl.so"

install -p -m 755 utils/pl2pm %{build_bindir}/pl2pm

for i in asm/termios.h syscall.h syslimits.h syslog.h \
    sys/ioctl.h sys/socket.h sys/time.h wait.h
do
    %{new_perl} %{build_bindir}/h2ph -a -d %{build_archlib} $i || true
done

# vendor directories (in this case for third party rpms)
# perl doesn't create the auto subdirectory, but modules put things in it,
# so we need to own it.

mkdir -p $RPM_BUILD_ROOT%{perl_vendorarch}/auto
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}

#
# perl RPM macros
#
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
mkdir -p ${RPM_BUILD_ROOT}%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/rpm
install -p -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/rpm/macros.%{?scl}%{!?scl:perl}
%{?scl:sed -i 's|@scl@|%{scl_macro_prefix}|g' ${RPM_BUILD_ROOT}%{_root_sysconfdir}/rpm/macros.%{scl}}
%{!?scl:sed -i 's|@scl@||g' ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm/macros.perl}
%else
mkdir -p ${RPM_BUILD_ROOT}%{_rpmconfigdir}/macros.d
install -p -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_rpmconfigdir}/macros.d/macros.%{?scl}%{!?scl:perl}
%{?scl:sed -i 's|@scl@|%{scl_macro_prefix}|g' ${RPM_BUILD_ROOT}%{_rpmconfigdir}/macros.d/macros.%{scl}}
%{!?scl:sed -i 's|@scl@||g' ${RPM_BUILD_ROOT}%{_rpmconfigdir}/macros.d/macros.perl}
%endif

#
# Core modules removal
#
# Dual-living binaries clashes on debuginfo files between perl and standalone
# packages. Excluding is not enough, we need to remove them. This is
# a work-around for rpmbuild bug #878863.
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -delete
chmod -R u+w $RPM_BUILD_ROOT/*

# miniperl? As an interpreter? How odd. Anyway, a symlink does it:
rm %{build_privlib}/ExtUtils/xsubpp
ln -s ../../../bin/xsubpp %{build_privlib}/ExtUtils/

# Don't need the .packlist
rm %{build_archlib}/.packlist

# Do not distribute File::Spec::VMS as it works on VMS only (bug #973713)
# We cannot remove it in %%prep because dist/Cwd/t/Spec.t test needs it.
rm %{build_archlib}/File/Spec/VMS.pm
rm $RPM_BUILD_ROOT%{_mandir}/man3/File::Spec::VMS.3*

# Fix some manpages to be UTF-8
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
pushd $RPM_BUILD_ROOT%{_mandir}/man1/
  for i in perl588delta.1 perldelta.1 ; do
    iconv -f MS-ANSI -t UTF-8 $i --output new-$i
    rm $i
    mv new-$i $i
  done
popd

# for now, remove Bzip2:
# Why? Now is missing Bzip2 files and provides
##find $RPM_BUILD_ROOT -name Bzip2 | xargs rm -r
##find $RPM_BUILD_ROOT -name '*B*zip2*'| xargs rm

# tests -- FIXME need to validate that this all works as expected
mkdir -p %{buildroot}%{perl5_testdir}/perl-tests

# "core"
tar -cf - t/ | ( cd %{buildroot}%{perl5_testdir}/perl-tests && tar -xf - )

# "dual-lifed"
for dir in `find ext/ -type d -name t -maxdepth 2` ; do

    tar -cf - $dir | ( cd %{buildroot}%{perl5_testdir}/perl-tests/t && tar -xf - )
done

# Systemtap tapset install
mkdir -p %{buildroot}%{tapsetdir}
%ifarch %{multilib_64_archs}
%global libperl_stp libperl%{?scl_prefix}%{perl_version}-64.stp
%else
%global libperl_stp libperl%{?scl_prefix}%{perl_version}-32.stp
%endif

sed \
  -e "s|LIBRARY_PATH|%{_libdir}/%{soname}|" \
  %{SOURCE4} \
  > %{buildroot}%{tapsetdir}/%{libperl_stp}

# TODO: Canonicalize test files (rewrite intrerpreter path, fix permissions)
# XXX: We cannot rewrite ./perl before %%check phase. Otherwise the test
# would run against system perl at build-time.
# See __spec_check_pre global macro in macros.perl.
#T_FILES=`find %%{buildroot}%%{perl5_testdir} -type f -name '*.t'`
#%%fix_shbang_line $T_FILES
#%%{__chmod} +x $T_FILES
#%%{_fixperms} %%{buildroot}%%{perl5_testdir}
#
# lib/perl5db.t will fail if Term::ReadLine::Gnu is available
%check
%if %{with test}
%{new_perl} -I/lib regen/lib_cleanup.pl
pushd t
%{new_perl} -I../lib porting/customized.t --regen
popd
%if %{parallel_tests}
    JOBS=$(printf '%%s' "%{?_smp_mflags}" | sed 's/.*-j\([0-9][0-9]*\).*/\1/')
    LC_ALL=C TEST_JOBS=$JOBS make test_harness
%else
    LC_ALL=C make test
%endif
%endif

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_bindir}/*
%{archlib}/*
%{privlib}/*


# libs
%exclude %dir %{archlib}
%exclude %dir %{archlib}/auto
%exclude %{archlib}/auto/re
%exclude %dir %{archlib}/CORE
%exclude %{archlib}/CORE/libperl.so
%exclude %{archlib}/re.pm
%exclude %{_libdir}/libperl.so.*
%exclude %dir %{perl_vendorarch}
%exclude %dir %{perl_vendorarch}/auto
%exclude %dir %{privlib}
%exclude %{privlib}/integer.pm
%exclude %{privlib}/strict.pm
%exclude %{privlib}/unicore
%exclude %{privlib}/utf8.pm
%exclude %{privlib}/utf8_heavy.pl
%exclude %{privlib}/warnings.pm
%exclude %{privlib}/XSLoader.pm
%exclude %dir %{perl_vendorlib}
%exclude %{_mandir}/man3/integer.*
%exclude %{_mandir}/man3/re.*
%exclude %{_mandir}/man3/strict.*
%exclude %{_mandir}/man3/utf8.*
%exclude %{_mandir}/man3/warnings.*
%exclude %{_mandir}/man3/XSLoader.*

# devel
%exclude %{_bindir}/h2xs
%exclude %{_mandir}/man1/h2xs*
%exclude %{_bindir}/perlivp
%exclude %{_mandir}/man1/perlivp*
%exclude %{archlib}/CORE/*.h
%exclude %{_libdir}/libperl.so
%exclude %{_mandir}/man1/perlxs*

# utils
%exclude %{_bindir}/c2ph
%exclude %{_bindir}/h2ph
%exclude %{_bindir}/perlbug
%exclude %{_bindir}/perlthanks
%exclude %{_bindir}/pl2pm
%exclude %{_bindir}/pstruct
%exclude %{_bindir}/splain
%exclude %{privlib}/pod/perlutil.pod
%exclude %{_mandir}/man1/c2ph.*
%exclude %{_mandir}/man1/h2ph.*
%exclude %{_mandir}/man1/perlbug.*
%exclude %{_mandir}/man1/perlthanks.*
%exclude %{_mandir}/man1/perlutil.*
%exclude %{_mandir}/man1/pl2pm.*
%exclude %{_mandir}/man1/pstruct.*
%exclude %{_mandir}/man1/splain.*

# Archive-Tar
%exclude %{_bindir}/ptar
%exclude %{_bindir}/ptardiff
%exclude %{_bindir}/ptargrep
%exclude %dir %{privlib}/Archive
%exclude %{privlib}/Archive/Tar
%exclude %{privlib}/Archive/Tar.pm
%exclude %{_mandir}/man1/ptar.1*
%exclude %{_mandir}/man1/ptardiff.1*
%exclude %{_mandir}/man1/ptargrep.1*
%exclude %{_mandir}/man3/Archive::Tar*

# Attribute-Handlers
%exclude %{privlib}/Attribute
%exclude %{_mandir}/man3/Attribute::Handlers.*

# autodie
%exclude %{privlib}/autodie/
%exclude %{privlib}/autodie.pm
%exclude %{privlib}/Fatal.pm
%exclude %{_mandir}/man3/autodie.3*
%exclude %{_mandir}/man3/autodie::*
%exclude %{_mandir}/man3/Fatal.3*

# B-Debug
%exclude %{privlib}/B/Debug.pm
%exclude %{_mandir}/man3/B::Debug.3*

# bignum
%exclude %{privlib}/bigint.pm
%exclude %{privlib}/bignum.pm
%exclude %{privlib}/bigrat.pm
%exclude %{privlib}/Math/BigFloat
%exclude %{privlib}/Math/BigInt/Trace.pm
%exclude %{_mandir}/man3/bigint.*
%exclude %{_mandir}/man3/bignum.*
%exclude %{_mandir}/man3/bigrat.*

# Carp
%exclude %{privlib}/Carp
%exclude %{privlib}/Carp.*
%exclude %{_mandir}/man3/Carp.*

# Config-Perl-V
%exclude %{privlib}/Config/Perl
%exclude %{_mandir}/man3/Config::Perl::V.*

# constant
%exclude %{privlib}/constant.pm
%exclude %{_mandir}/man3/constant.3*

# CPAN
%exclude %{_bindir}/cpan
%exclude %dir %{privlib}/App
%exclude %{privlib}/App/Cpan.pm
%exclude %{privlib}/CPAN
%exclude %{privlib}/CPAN.pm
%exclude %{_mandir}/man1/cpan.1*
%exclude %{_mandir}/man3/App::Cpan.*
%exclude %{_mandir}/man3/CPAN.*
%exclude %{_mandir}/man3/CPAN:*

# CPAN-Meta
%exclude %dir %{privlib}/CPAN
%exclude %{privlib}/CPAN/Meta.pm
%exclude %dir %{privlib}/CPAN/Meta
%exclude %{privlib}/CPAN/Meta/Converter.pm
%exclude %{privlib}/CPAN/Meta/Feature.pm
%exclude %dir %{privlib}/CPAN/Meta/History
%exclude %{privlib}/CPAN/Meta/History.pm
%exclude %{privlib}/CPAN/Meta/Merge.pm
%exclude %{privlib}/CPAN/Meta/Prereqs.pm
%exclude %{privlib}/CPAN/Meta/Spec.pm
%exclude %{privlib}/CPAN/Meta/Validator.pm
%exclude %{_mandir}/man3/CPAN::Meta*

# CPAN-Meta-Requirements
%exclude %dir %{privlib}/CPAN
%exclude %dir %{privlib}/CPAN/Meta
%exclude %{privlib}/CPAN/Meta/Requirements.pm
%exclude %{_mandir}/man3/CPAN::Meta::Requirements.3*

# CPAN-Meta-YAML
%exclude %dir %{privlib}/CPAN
%exclude %dir %{privlib}/CPAN/Meta
%exclude %{privlib}/CPAN/Meta/YAML.pm
%exclude %{_mandir}/man3/CPAN::Meta::YAML*

# Parse-CPAN-Meta
%exclude %dir %{privlib}/Parse
%exclude %dir %{privlib}/Parse/CPAN
%exclude %{privlib}/Parse/CPAN/Meta.pm
%exclude %{_mandir}/man3/Parse::CPAN::Meta.3*

# Compress-Raw-Bzip2
%exclude %dir %{archlib}/Compress
%exclude %dir %{archlib}/Compress/Raw
%exclude %{archlib}/Compress/Raw/Bzip2.pm
%exclude %dir %{archlib}/auto/Compress
%exclude %dir %{archlib}/auto/Compress/Raw
%exclude %{archlib}/auto/Compress/Raw/Bzip2
%exclude %{_mandir}/man3/Compress::Raw::Bzip2*

# Compress-Raw-Zlib
%exclude %dir %{archlib}/Compress
%exclude %dir %{archlib}/Compress/Raw
%exclude %{archlib}/Compress/Raw/Zlib.pm
%exclude %dir %{archlib}/auto/Compress
%exclude %dir %{archlib}/auto/Compress/Raw
%exclude %{archlib}/auto/Compress/Raw/Zlib
%exclude %{_mandir}/man3/Compress::Raw::Zlib*

# Data-Dumper
%exclude %dir %{archlib}/auto/Data
%exclude %dir %{archlib}/auto/Data/Dumper
%exclude %{archlib}/auto/Data/Dumper/Dumper.so
%exclude %dir %{archlib}/Data
%exclude %{archlib}/Data/Dumper.pm
%exclude %{_mandir}/man3/Data::Dumper.3*

# DB_File
%exclude %{archlib}/DB_File.pm
%exclude %dir %{archlib}/auto/DB_File
%exclude %{archlib}/auto/DB_File/DB_File.so
%exclude %{_mandir}/man3/DB_File*

# Devel-Peek
%dir %exclude %{archlib}/Devel
%exclude %{archlib}/Devel/Peek.pm
%dir %exclude %{archlib}/auto/Devel
%exclude %{archlib}/auto/Devel/Peek
%exclude %{_mandir}/man3/Devel::Peek.*

# Devel-PPPort
%exclude %{archlib}/Devel/PPPort.pm
%exclude %{_mandir}/man3/Devel::PPPort.3*

# Devel-SelfStubber
%exclude %dir %{privlib}/Devel
%exclude %{privlib}/Devel/SelfStubber.pm
%exclude %{_mandir}/man3/Devel::SelfStubber.*

# Digest
%exclude %{privlib}/Digest.pm
%exclude %dir %{privlib}/Digest
%exclude %{privlib}/Digest/base.pm
%exclude %{privlib}/Digest/file.pm
%exclude %{_mandir}/man3/Digest.3*
%exclude %{_mandir}/man3/Digest::base.3*
%exclude %{_mandir}/man3/Digest::file.3*

# Digest-MD5
%exclude %dir %{archlib}/Digest
%exclude %{archlib}/Digest/MD5.pm
%exclude %dir %{archlib}/auto/Digest
%exclude %{archlib}/auto/Digest/MD5
%exclude %{_mandir}/man3/Digest::MD5.3*

# Digest-SHA
%exclude %{_bindir}/shasum
%exclude %dir %{archlib}/Digest
%exclude %{archlib}/Digest/SHA.pm
%exclude %dir %{archlib}/auto/Digest
%exclude %{archlib}/auto/Digest/SHA
%exclude %{_mandir}/man1/shasum.1*
%exclude %{_mandir}/man3/Digest::SHA.3*

# Encode
%exclude %{_bindir}/encguess
%exclude %{_bindir}/piconv
%exclude %{archlib}/Encode*
%exclude %{archlib}/auto/Encode*
%exclude %{privlib}/Encode
%exclude %{_mandir}/man1/encguess.1*
%exclude %{_mandir}/man1/piconv.1*
%exclude %{_mandir}/man3/Encode*.3*

# encoding
%exclude %{archlib}/encoding.pm
%exclude %{_mandir}/man3/encoding.3*

# Encode-devel
%exclude %{_bindir}/enc2xs
%exclude %dir %{privlib}/Encode
%exclude %{privlib}/Encode/*.e2x
%exclude %{privlib}/Encode/encode.h
%exclude %{_mandir}/man1/enc2xs.1*

# Env
%exclude %{privlib}/Env.pm
%exclude %{_mandir}/man3/Env.3*

# Errno
%exclude %{archlib}/Errno.pm
%exclude %{_mandir}/man3/Errno.*

# Exporter
%exclude %{privlib}/Exporter*
%exclude %{_mandir}/man3/Exporter*

# experimental
%exclude %{privlib}/experimental*
%exclude %{_mandir}/man3/experimental*

# ExtUtils-CBuilder
%exclude %{privlib}/ExtUtils/CBuilder
%exclude %{privlib}/ExtUtils/CBuilder.pm
%exclude %{_mandir}/man3/ExtUtils::CBuilder*

# ExtUtils-Command
%exclude %{privlib}/ExtUtils/Command.pm
%exclude %{_mandir}/man3/ExtUtils::Command.*

# ExtUtils-Embed
%exclude %{privlib}/ExtUtils/Embed.pm
%exclude %{_mandir}/man3/ExtUtils::Embed*

# ExtUtils-Install
%exclude %{privlib}/ExtUtils/Install.pm
%exclude %{privlib}/ExtUtils/Installed.pm
%exclude %{privlib}/ExtUtils/Packlist.pm
%exclude %{_mandir}/man3/ExtUtils::Install.3*
%exclude %{_mandir}/man3/ExtUtils::Installed.3*
%exclude %{_mandir}/man3/ExtUtils::Packlist.3*

# ExtUtils-Manifest
%exclude %{privlib}/ExtUtils/Manifest.pm
%exclude %{privlib}/ExtUtils/MANIFEST.SKIP
%exclude %{_mandir}/man3/ExtUtils::Manifest.3*

# ExtUtils-MakeMaker
%exclude %{_bindir}/instmodsh
%exclude %{privlib}/ExtUtils/Command
%exclude %{privlib}/ExtUtils/Liblist
%exclude %{privlib}/ExtUtils/Liblist.pm
%exclude %{privlib}/ExtUtils/MakeMaker
%exclude %{privlib}/ExtUtils/MakeMaker.pm
%exclude %{privlib}/ExtUtils/MM.pm
%exclude %{privlib}/ExtUtils/MM_*.pm
%exclude %{privlib}/ExtUtils/MY.pm
%exclude %{privlib}/ExtUtils/Mkbootstrap.pm
%exclude %{privlib}/ExtUtils/Mksymlists.pm
%exclude %{privlib}/ExtUtils/testlib.pm
%exclude %{_mandir}/man1/instmodsh.1*
%exclude %{_mandir}/man3/ExtUtils::Command::MM*
%exclude %{_mandir}/man3/ExtUtils::Liblist.3*
%exclude %{_mandir}/man3/ExtUtils::MM.3*
%exclude %{_mandir}/man3/ExtUtils::MM_*
%exclude %{_mandir}/man3/ExtUtils::MY.3*
%exclude %{_mandir}/man3/ExtUtils::MakeMaker*
%exclude %{_mandir}/man3/ExtUtils::Mkbootstrap.3*
%exclude %{_mandir}/man3/ExtUtils::Mksymlists.3*
%exclude %{_mandir}/man3/ExtUtils::testlib.3*

# ExtUtils-Miniperl
%exclude %{privlib}/ExtUtils/Miniperl.pm
%exclude %{_mandir}/man3/ExtUtils::Miniperl.3*

# ExtUtils-MM-Utils
%exclude %dir %{privlib}/ExtUtils/MM
%exclude %{privlib}/ExtUtils/MM/Utils.pm
%exclude %{_mandir}/man3/ExtUtils::MM::Utils.*

# ExtUtils-ParseXS
%exclude %dir %{privlib}/ExtUtils/ParseXS
%exclude %{privlib}/ExtUtils/ParseXS.pm
%exclude %{privlib}/ExtUtils/ParseXS.pod
%exclude %{privlib}/ExtUtils/ParseXS/Constants.pm
%exclude %{privlib}/ExtUtils/ParseXS/CountLines.pm
%exclude %{privlib}/ExtUtils/ParseXS/Eval.pm
%exclude %{privlib}/ExtUtils/ParseXS/Utilities.pm
%exclude %dir %{privlib}/ExtUtils/Typemaps
%exclude %{privlib}/ExtUtils/Typemaps.pm
%exclude %{privlib}/ExtUtils/Typemaps/Cmd.pm
%exclude %{privlib}/ExtUtils/Typemaps/InputMap.pm
%exclude %{privlib}/ExtUtils/Typemaps/OutputMap.pm
%exclude %{privlib}/ExtUtils/Typemaps/Type.pm
%exclude %{privlib}/ExtUtils/xsubpp
%exclude %{_bindir}/xsubpp
%exclude %{_mandir}/man1/xsubpp*
%exclude %{_mandir}/man3/ExtUtils::ParseXS.3*
%exclude %{_mandir}/man3/ExtUtils::ParseXS::Constants.3*
%exclude %{_mandir}/man3/ExtUtils::ParseXS::Eval.3*
%exclude %{_mandir}/man3/ExtUtils::ParseXS::Utilities.3*
%exclude %{_mandir}/man3/ExtUtils::Typemaps.3*
%exclude %{_mandir}/man3/ExtUtils::Typemaps::Cmd.3*
%exclude %{_mandir}/man3/ExtUtils::Typemaps::InputMap.3*
%exclude %{_mandir}/man3/ExtUtils::Typemaps::OutputMap.3*
%exclude %{_mandir}/man3/ExtUtils::Typemaps::Type.3*

# File-Fetch
%exclude %{privlib}/File/Fetch.pm
%exclude %{_mandir}/man3/File::Fetch.3*

# File-Path
%exclude %{privlib}/File/Path.pm
%exclude %{_mandir}/man3/File::Path.3*

# File-Temp
%exclude %{privlib}/File/Temp.pm
%exclude %{_mandir}/man3/File::Temp.3*

# Filter
%exclude %dir %{archlib}/auto/Filter
%exclude %{archlib}/auto/Filter/Util
%exclude %dir %{archlib}/Filter
%exclude %{archlib}/Filter/Util
%exclude %{privlib}/pod/perlfilter.pod
%exclude %{_mandir}/man1/perlfilter.*
%exclude %{_mandir}/man3/Filter::Util::*

# Filter-Simple
%exclude %dir %{privlib}/Filter
%exclude %{privlib}/Filter/Simple.pm
%exclude %{_mandir}/man3/Filter::Simple.3*

# Getopt-Long
%exclude %{privlib}/Getopt/Long.pm
%exclude %{_mandir}/man3/Getopt::Long.3*

# IO
%exclude %dir %{archlib}/IO
%exclude %{archlib}/IO.pm
%exclude %{archlib}/IO/Dir.pm
%exclude %{archlib}/IO/File.pm
%exclude %{archlib}/IO/Handle.pm
%exclude %{archlib}/IO/Pipe.pm
%exclude %{archlib}/IO/Poll.pm
%exclude %{archlib}/IO/Seekable.pm
%exclude %{archlib}/IO/Select.pm
%exclude %dir %{archlib}/IO/Socket
%exclude %{archlib}/IO/Socket/INET.pm
%exclude %{archlib}/IO/Socket/UNIX.pm
%exclude %{archlib}/IO/Socket.pm
%exclude %dir %{archlib}/auto/IO
%exclude %{archlib}/auto/IO/IO.so
%exclude %{_mandir}/man3/IO.*
%exclude %{_mandir}/man3/IO::Dir.*
%exclude %{_mandir}/man3/IO::File.*
%exclude %{_mandir}/man3/IO::Handle.*
%exclude %{_mandir}/man3/IO::Pipe.*
%exclude %{_mandir}/man3/IO::Poll.*
%exclude %{_mandir}/man3/IO::Seekable.*
%exclude %{_mandir}/man3/IO::Select.*
%exclude %{_mandir}/man3/IO::Socket::INET.*
%exclude %{_mandir}/man3/IO::Socket::UNIX.*
%exclude %{_mandir}/man3/IO::Socket.*

# IO-Compress
%exclude %{_bindir}/zipdetails
%exclude %dir %{privlib}/IO
%exclude %dir %{privlib}/IO/Compress
%exclude %{privlib}/IO/Compress/FAQ.pod
%exclude %{_mandir}/man1/zipdetails.*
%exclude %{_mandir}/man3/IO::Compress::FAQ.*
# Compress-Zlib
%exclude %dir %{privlib}/Compress
%exclude %{privlib}/Compress/Zlib.pm
%exclude %{_mandir}/man3/Compress::Zlib*
# IO-Compress-Base
%exclude %{privlib}/File/GlobMapper.pm
%exclude %dir %{privlib}/IO
%exclude %dir %{privlib}/IO/Compress
%exclude %{privlib}/IO/Compress/Base
%exclude %{privlib}/IO/Compress/Base.pm
%exclude %dir %{privlib}/IO/Uncompress
%exclude %{privlib}/IO/Uncompress/AnyUncompress.pm
%exclude %{privlib}/IO/Uncompress/Base.pm
%exclude %{_mandir}/man3/File::GlobMapper.*
%exclude %{_mandir}/man3/IO::Compress::Base.*
%exclude %{_mandir}/man3/IO::Uncompress::AnyUncompress.*
%exclude %{_mandir}/man3/IO::Uncompress::Base.*
# IO-Compress-Zlib
%exclude %dir %{privlib}/IO
%exclude %dir %{privlib}/IO/Compress
%exclude %{privlib}/IO/Compress/Adapter
%exclude %{privlib}/IO/Compress/Deflate.pm
%exclude %{privlib}/IO/Compress/Gzip
%exclude %{privlib}/IO/Compress/Gzip.pm
%exclude %{privlib}/IO/Compress/RawDeflate.pm
%exclude %{privlib}/IO/Compress/Bzip2.pm
%exclude %{privlib}/IO/Compress/Zip
%exclude %{privlib}/IO/Compress/Zip.pm
%exclude %{privlib}/IO/Compress/Zlib
%exclude %dir %{privlib}/IO/Uncompress
%exclude %{privlib}/IO/Uncompress/Adapter
%exclude %{privlib}/IO/Uncompress/AnyInflate.pm
%exclude %{privlib}/IO/Uncompress/Bunzip2.pm
%exclude %{privlib}/IO/Uncompress/Gunzip.pm
%exclude %{privlib}/IO/Uncompress/Inflate.pm
%exclude %{privlib}/IO/Uncompress/RawInflate.pm
%exclude %{privlib}/IO/Uncompress/Unzip.pm
%exclude %{_mandir}/man3/IO::Compress::Deflate*
%exclude %{_mandir}/man3/IO::Compress::Bzip2*
%exclude %{_mandir}/man3/IO::Compress::Gzip*
%exclude %{_mandir}/man3/IO::Compress::RawDeflate*
%exclude %{_mandir}/man3/IO::Compress::Zip*
%exclude %{_mandir}/man3/IO::Uncompress::AnyInflate*
%exclude %{_mandir}/man3/IO::Uncompress::Bunzip2*
%exclude %{_mandir}/man3/IO::Uncompress::Gunzip*
%exclude %{_mandir}/man3/IO::Uncompress::Inflate*
%exclude %{_mandir}/man3/IO::Uncompress::RawInflate*
%exclude %{_mandir}/man3/IO::Uncompress::Unzip*

# IO-Socket-IP
%exclude %dir %{privlib}/IO
%exclude %dir %{privlib}/IO/Socket
%exclude %{privlib}/IO/Socket/IP.pm
%exclude %{_mandir}/man3/IO::Socket::IP.*

# IO-Zlib
%exclude %dir %{privlib}/IO
%exclude %{privlib}/IO/Zlib.pm
%exclude %{_mandir}/man3/IO::Zlib.*

# HTTP-Tiny
%exclude %dir %{privlib}/HTTP
%exclude %{privlib}/HTTP/Tiny.pm
%exclude %{_mandir}/man3/HTTP::Tiny*

# IPC-Cmd
%exclude %{privlib}/IPC/Cmd.pm
%exclude %{_mandir}/man3/IPC::Cmd.3*

# IPC-SysV
%exclude %{archlib}/auto/IPC
%exclude %{archlib}/IPC/Msg.pm
%exclude %{archlib}/IPC/Semaphore.pm
%exclude %{archlib}/IPC/SharedMem.pm
%exclude %{archlib}/IPC/SysV.pm
%exclude %{_mandir}/man3/IPC::Msg.*
%exclude %{_mandir}/man3/IPC::Semaphore.*
%exclude %{_mandir}/man3/IPC::SharedMem.*
%exclude %{_mandir}/man3/IPC::SysV.*

# JSON-PP
%exclude %{_bindir}/json_pp
%exclude %dir %{privlib}/JSON
%exclude %{privlib}/JSON/PP
%exclude %{privlib}/JSON/PP.pm
%exclude %{_mandir}/man1/json_pp.1*
%exclude %{_mandir}/man3/JSON::PP.3*
%exclude %{_mandir}/man3/JSON::PP::Boolean.3pm*

# libnet
%exclude %{privlib}/Net/Cmd.pm
%exclude %{privlib}/Net/Config.pm
%exclude %{privlib}/Net/Domain.pm
%exclude %{privlib}/Net/FTP
%exclude %{privlib}/Net/FTP.pm
%exclude %{privlib}/Net/libnetFAQ.pod
%exclude %{privlib}/Net/NNTP.pm
%exclude %{privlib}/Net/Netrc.pm
%exclude %{privlib}/Net/POP3.pm
%exclude %{privlib}/Net/SMTP.pm
%exclude %{privlib}/Net/Time.pm
%exclude %{_mandir}/man3/Net::Cmd.*
%exclude %{_mandir}/man3/Net::Config.*
%exclude %{_mandir}/man3/Net::Domain.*
%exclude %{_mandir}/man3/Net::FTP.*
%exclude %{_mandir}/man3/Net::libnetFAQ.*
%exclude %{_mandir}/man3/Net::NNTP.*
%exclude %{_mandir}/man3/Net::Netrc.*
%exclude %{_mandir}/man3/Net::POP3.*
%exclude %{_mandir}/man3/Net::SMTP.*
%exclude %{_mandir}/man3/Net::Time.*

# libnetcfg
%exclude %{_bindir}/libnetcfg
%exclude %{_mandir}/man1/libnetcfg*

# Locale-Codes
%exclude %dir %{privlib}/Locale
%exclude %{privlib}/Locale/Codes
%exclude %{privlib}/Locale/Codes.*
%exclude %{privlib}/Locale/Country.*
%exclude %{privlib}/Locale/Currency.*
%exclude %{privlib}/Locale/Language.*
%exclude %{privlib}/Locale/Script.*
%exclude %{_mandir}/man3/Locale::Codes::*
%exclude %{_mandir}/man3/Locale::Codes.*
%exclude %{_mandir}/man3/Locale::Country.*
%exclude %{_mandir}/man3/Locale::Currency.*
%exclude %{_mandir}/man3/Locale::Language.*
%exclude %{_mandir}/man3/Locale::Script.*

# Locale-Maketext
%exclude %dir %{privlib}/Locale
%exclude %dir %{privlib}/Locale/Maketext
%exclude %{privlib}/Locale/Maketext.*
%exclude %{privlib}/Locale/Maketext/Cookbook.*
%exclude %{privlib}/Locale/Maketext/Guts.*
%exclude %{privlib}/Locale/Maketext/GutsLoader.*
%exclude %{privlib}/Locale/Maketext/TPJ13.*
%exclude %{_mandir}/man3/Locale::Maketext.*
%exclude %{_mandir}/man3/Locale::Maketext::Cookbook.*
%exclude %{_mandir}/man3/Locale::Maketext::Guts.*
%exclude %{_mandir}/man3/Locale::Maketext::GutsLoader.*
%exclude %{_mandir}/man3/Locale::Maketext::TPJ13.*

# Locale-Maketext-Simple
%exclude %dir %{privlib}/Locale
%exclude %dir %{privlib}/Locale/Maketext
%exclude %{privlib}/Locale/Maketext/Simple.pm
%exclude %{_mandir}/man3/Locale::Maketext::Simple.*

# Math-BigInt
%exclude %{privlib}/Math/BigFloat.pm
%exclude %{privlib}/Math/BigInt.pm
%exclude %dir %exclude %{privlib}/Math/BigInt
%exclude %{privlib}/Math/BigInt/Calc.pm
%exclude %{privlib}/Math/BigInt/CalcEmu.pm
%exclude %{_mandir}/man3/Math::BigFloat.*
%exclude %{_mandir}/man3/Math::BigInt.*
%exclude %{_mandir}/man3/Math::BigInt::Calc.*
%exclude %{_mandir}/man3/Math::BigInt::CalcEmu.*

# Math-BigInt-FastCalc
%exclude %{archlib}/Math
%exclude %{archlib}/auto/Math
%exclude %{_mandir}/man3/Math::BigInt::FastCalc.*

# Math-BigRat
%exclude %{privlib}/Math/BigRat.pm
%exclude %{_mandir}/man3/Math::BigRat.*

# Math-Complex
%dir %exclude %{privlib}/Math
%exclude %{privlib}/Math/Complex.pm
%exclude %{privlib}/Math/Trig.pm
%exclude %{_mandir}/man3/Math::Complex.*
%exclude %{_mandir}/man3/Math::Trig.*

# Memoize
%exclude %{privlib}/Memoize
%exclude %{privlib}/Memoize.pm
%exclude %{_mandir}/man3/Memoize::*
%exclude %{_mandir}/man3/Memoize.*

# MIME-Base64
%exclude %{archlib}/auto/MIME
%exclude %{archlib}/MIME
%exclude %{_mandir}/man3/MIME::*

# Module-CoreList
%exclude %dir %{privlib}/Module
%exclude %{privlib}/Module/CoreList
%exclude %{privlib}/Module/CoreList.pm
%exclude %{privlib}/Module/CoreList.pod
%exclude %{_mandir}/man3/Module::CoreList*

# Module-CoreList-tools
%exclude %{_bindir}/corelist
%exclude %{_mandir}/man1/corelist*

# Module-Load
%exclude %dir %{privlib}/Module
%exclude %{privlib}/Module/Load.pm
%exclude %{_mandir}/man3/Module::Load.*

# Module-Load-Conditional
%exclude %dir %{privlib}/Module
%exclude %{privlib}/Module/Load
%exclude %{_mandir}/man3/Module::Load::Conditional*

# Module-Loaded
%exclude %dir %{privlib}/Module
%exclude %{privlib}/Module/Loaded.pm
%exclude %{_mandir}/man3/Module::Loaded*

# Module-Metadata
%exclude %dir %{privlib}/Module
%exclude %{privlib}/Module/Metadata.pm
%exclude %{_mandir}/man3/Module::Metadata.3pm*

# Net-Ping
%exclude %{privlib}/Net/Ping.pm
%exclude %{_mandir}/man3/Net::Ping.*

# PathTools
%exclude %{archlib}/Cwd.pm
%exclude %{archlib}/File/Spec*
%exclude %{archlib}/auto/Cwd/
%exclude %{_mandir}/man3/Cwd*
%exclude %{_mandir}/man3/File::Spec*

# Params-Check
%exclude %{privlib}/Params/
%exclude %{_mandir}/man3/Params::Check*

# perlfaq
%exclude %{privlib}/perlfaq.pm
%exclude %{privlib}/pod/perlfaq*
%exclude %{privlib}/pod/perlglossary.pod
%exclude %{_mandir}/man1/perlfaq*
%exclude %{_mandir}/man1/perlglossary.*

# PerlIO-via-QuotedPrint
%exclude %{privlib}/PerlIO
%exclude %{_mandir}/man3/PerlIO::via::QuotedPrint.*

# Perl-OSType
%exclude %dir %{privlib}/Perl
%exclude %{privlib}/Perl/OSType.pm
%exclude %{_mandir}/man3/Perl::OSType.3pm*

# open
%exclude %{privlib}/open.pm
%exclude %{_mandir}/man3/open.3*

# parent
%exclude %{privlib}/parent.pm
%exclude %{_mandir}/man3/parent.3*

# Pod-Checker
%exclude %{_bindir}/podchecker
%exclude %{privlib}/Pod/Checker.pm
%exclude %{_mandir}/man1/podchecker.*
%exclude %{_mandir}/man3/Pod::Checker.*

# Pod-Escapes
%exclude %{privlib}/Pod/Escapes.pm
%exclude %{_mandir}/man3/Pod::Escapes.*

# Pod-Html
%exclude %{_bindir}/pod2html
%exclude %{privlib}/Pod/Html.pm
%exclude %{_mandir}/man1/pod2html.1*
%exclude %{_mandir}/man3/Pod::Html.*

# Pod-Parser
%exclude %{_bindir}/podselect
%exclude %{privlib}/Pod/Find.pm
%exclude %{privlib}/Pod/InputObjects.pm
%exclude %{privlib}/Pod/ParseUtils.pm
%exclude %{privlib}/Pod/Parser.pm
%exclude %{privlib}/Pod/PlainText.pm
%exclude %{privlib}/Pod/Select.pm
%exclude %{_mandir}/man1/podselect.1*
%exclude %{_mandir}/man3/Pod::Find.*
%exclude %{_mandir}/man3/Pod::InputObjects.*
%exclude %{_mandir}/man3/Pod::ParseUtils.*
%exclude %{_mandir}/man3/Pod::Parser.*
%exclude %{_mandir}/man3/Pod::PlainText.*
%exclude %{_mandir}/man3/Pod::Select.*

# Pod-Perldoc
%exclude %{_bindir}/perldoc
%exclude %{privlib}/pod/perldoc.pod
%exclude %{privlib}/Pod/Perldoc.pm
%exclude %{privlib}/Pod/Perldoc/
%exclude %{_mandir}/man1/perldoc.1*
%exclude %{_mandir}/man3/Pod::Perldoc*

# Pod-Usage
%exclude %{_bindir}/pod2usage
%exclude %{privlib}/Pod/Usage.pm
%exclude %{_mandir}/man1/pod2usage.*
%exclude %{_mandir}/man3/Pod::Usage.*

# podlators
%exclude %{_bindir}/pod2man
%exclude %{_bindir}/pod2text
%exclude %{privlib}/pod/perlpodstyle.pod
%exclude %{privlib}/Pod/Man.pm
%exclude %{privlib}/Pod/ParseLink.pm
%exclude %{privlib}/Pod/Text
%exclude %{privlib}/Pod/Text.pm
%exclude %{_mandir}/man1/pod2man.1*
%exclude %{_mandir}/man1/pod2text.1*
%exclude %{_mandir}/man1/perlpodstyle.1*
%exclude %{_mandir}/man3/Pod::Man*
%exclude %{_mandir}/man3/Pod::ParseLink*
%exclude %{_mandir}/man3/Pod::Text*

# Pod-Simple
%exclude %{privlib}/Pod/Simple/
%exclude %{privlib}/Pod/Simple.pm
%exclude %{privlib}/Pod/Simple.pod
%exclude %{_mandir}/man3/Pod::Simple*

# Scalar-List-Utils
%exclude %{archlib}/List/
%exclude %{archlib}/Scalar/
%exclude %{archlib}/Sub/
%exclude %{archlib}/auto/List/
%exclude %{_mandir}/man3/List::Util*
%exclude %{_mandir}/man3/Scalar::Util*
%exclude %{_mandir}/man3/Sub::Util*

# SelfLoader
%exclude %{privlib}/SelfLoader.pm
%exclude %{_mandir}/man3/SelfLoader*

# Storable
%exclude %{archlib}/Storable.pm
%exclude %{archlib}/auto/Storable/
%exclude %{_mandir}/man3/Storable.*

# Sys-Syslog
%exclude %{archlib}/Sys/Syslog.pm
%exclude %{archlib}/auto/Sys/Syslog/
%exclude %{_mandir}/man3/Sys::Syslog.*

# Term-ANSIColor
%exclude %{privlib}/Term/ANSIColor.pm
%exclude %{_mandir}/man3/Term::ANSIColor*

# Term-Cap
%exclude %{privlib}/Term/Cap.pm
%exclude %{_mandir}/man3/Term::Cap.*

# Test
%exclude %{privlib}/Test.pm
%exclude %{_mandir}/man3/Test.*

# Test-Harness
%exclude %{_bindir}/prove
%exclude %dir %{privlib}/App
%exclude %{privlib}/App/Prove*
%exclude %{privlib}/TAP*
%exclude %dir %{privlib}/Test
%exclude %{privlib}/Test/Harness*
%exclude %{_mandir}/man1/prove.1*
%exclude %{_mandir}/man3/App::Prove*
%exclude %{_mandir}/man3/TAP*
%exclude %{_mandir}/man3/Test::Harness*

# Test-Simple
%exclude %{privlib}/ok*
%exclude %dir %{privlib}/Test
%exclude %{privlib}/Test/More*
%exclude %{privlib}/Test/Builder*
%exclude %{privlib}/Test/Tester*
%exclude %{privlib}/Test/Simple*
%exclude %{privlib}/Test/Tutorial*
%exclude %{privlib}/Test/use
%exclude %{_mandir}/man3/ok*
%exclude %{_mandir}/man3/Test::More*
%exclude %{_mandir}/man3/Test::Builder*
%exclude %{_mandir}/man3/Test::Tester*
%exclude %{_mandir}/man3/Test::Simple*
%exclude %{_mandir}/man3/Test::Tutorial*
%exclude %{_mandir}/man3/Test::use::*

# Text-Balanced
%exclude %{privlib}/Text/Balanced.pm
%exclude %{_mandir}/man3/Text::Balanced.*

# Text-ParseWords
%exclude %{privlib}/Text/ParseWords.pm
%exclude %{_mandir}/man3/Text::ParseWords.*

# Text-Tabs+Wrap
%exclude %{privlib}/Text/Tabs.pm
%exclude %{privlib}/Text/Wrap.pm
%exclude %{_mandir}/man3/Text::Tabs.*
%exclude %{_mandir}/man3/Text::Wrap.*

# Thread-Queue
%exclude %{privlib}/Thread/Queue.pm
%exclude %{_mandir}/man3/Thread::Queue.*

# Time-HiRes
%exclude %dir %{archlib}/Time
%exclude %{archlib}/Time/HiRes.pm
%exclude %dir %{archlib}/auto/Time
%exclude %{archlib}/auto/Time/HiRes
%exclude %{_mandir}/man3/Time::HiRes.*

# Time-Local
%exclude %{privlib}/Time/Local.pm
%exclude %{_mandir}/man3/Time::Local.*

# Time-Piece
%exclude %dir %{archlib}/Time
%exclude %{archlib}/Time/Piece.pm
%exclude %{archlib}/Time/Seconds.pm
%exclude %dir %{archlib}/auto/Time
%exclude %{archlib}/auto/Time/Piece
%exclude %{_mandir}/man3/Time::Piece.3*
%exclude %{_mandir}/man3/Time::Seconds.3*

# Socket
%exclude %dir %{archlib}/auto/Socket
%exclude %{archlib}/auto/Socket/Socket.*
%exclude %{archlib}/Socket.pm
%exclude %{_mandir}/man3/Socket.3*

# threads
%dir %exclude %{archlib}/auto/threads
%exclude %{archlib}/auto/threads/threads*
%exclude %{archlib}/threads.pm
%exclude %{_mandir}/man3/threads.3*

# threads-shared
%exclude %{archlib}/auto/threads/shared*
%exclude %dir %{archlib}/threads
%exclude %{archlib}/threads/shared*
%exclude %{_mandir}/man3/threads::shared*

# Unicode-Collate
%dir %exclude %{archlib}/auto/Unicode
%exclude %{archlib}/auto/Unicode/Collate
%dir %exclude %{archlib}/Unicode
%exclude %{archlib}/Unicode/Collate
%exclude %{archlib}/Unicode/Collate.pm
%exclude %{privlib}/Unicode/Collate
%exclude %{_mandir}/man3/Unicode::Collate.*
%exclude %{_mandir}/man3/Unicode::Collate::*

# Unicode-Normalize
%exclude %{archlib}/auto/Unicode/Normalize
%exclude %{archlib}/Unicode/Normalize.pm
%exclude %{_mandir}/man3/Unicode::Normalize.*

# version
%exclude %{privlib}/version.pm
%exclude %{privlib}/version.pod
%exclude %{privlib}/version/
%exclude %{_mandir}/man3/version.3*
%exclude %{_mandir}/man3/version::Internals.3*

%files libs
%doc Artistic Copying
%doc AUTHORS README Changes
%dir %{archlib}
%dir %{archlib}/auto
%{archlib}/auto/re
%dir %{archlib}/CORE
%{archlib}/CORE/libperl.so
%{archlib}/re.pm
%{_libdir}/libperl.so.*
%dir %{perl_vendorarch}
%dir %{perl_vendorarch}/auto
%dir %{privlib}
%{privlib}/integer.pm
%{privlib}/strict.pm
%{privlib}/unicore
%{privlib}/utf8.pm
%{privlib}/utf8_heavy.pl
%{privlib}/warnings.pm
%{privlib}/XSLoader.pm
%dir %{perl_vendorlib}
%{_mandir}/man3/integer.*
%{_mandir}/man3/re.*
%{_mandir}/man3/strict.*
%{_mandir}/man3/utf8.*
%{_mandir}/man3/warnings.*
%{_mandir}/man3/XSLoader.*

%files devel
%{_bindir}/h2xs
%{_mandir}/man1/h2xs*
%{_bindir}/perlivp
%{_mandir}/man1/perlivp*
%{archlib}/CORE/*.h
%{_libdir}/libperl.so
%{_mandir}/man1/perlxs*
%{tapsetdir}/%{libperl_stp}
%doc perl-example.stp

%files macros
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%attr(0644,root,root) %{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/rpm/macros.%{?scl}%{!?scl:perl}
%else
%{_rpmconfigdir}/macros.d/macros.%{?scl}%{!?scl:perl}
%endif

%files tests
%{perl5_testdir}/

%files utils
%{_bindir}/c2ph
%{_bindir}/h2ph
%{_bindir}/perlbug
%{_bindir}/perlthanks
%{_bindir}/pl2pm
%{_bindir}/pstruct
%{_bindir}/splain
%dir %{privlib}/pod
%{privlib}/pod/perlutil.pod
%{_mandir}/man1/c2ph.*
%{_mandir}/man1/h2ph.*
%{_mandir}/man1/perlbug.*
%{_mandir}/man1/perlthanks.*
%{_mandir}/man1/perlutil.*
%{_mandir}/man1/pl2pm.*
%{_mandir}/man1/pstruct.*
%{_mandir}/man1/splain.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Archive-Tar
%{_bindir}/ptar
%{_bindir}/ptardiff
%{_bindir}/ptargrep
%dir %{privlib}/Archive
%{privlib}/Archive/Tar
%{privlib}/Archive/Tar.pm
%{_mandir}/man1/ptar.1*
%{_mandir}/man1/ptardiff.1*
%{_mandir}/man1/ptargrep.1*
%{_mandir}/man3/Archive::Tar*
%endif

%files Attribute-Handlers
%{privlib}/Attribute
%{_mandir}/man3/Attribute::Handlers.*

%if %{dual_life} || %{rebuild_from_scratch}
%files autodie
%{privlib}/autodie/
%{privlib}/autodie.pm
%{privlib}/Fatal.pm
%{_mandir}/man3/autodie.3*
%{_mandir}/man3/autodie::*
%{_mandir}/man3/Fatal.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files B-Debug
%dir %{privlib}/B
%{privlib}/B/Debug.pm
%{_mandir}/man3/B::Debug.3*
%endif

%files bignum
%{privlib}/bigint.pm
%{privlib}/bignum.pm
%{privlib}/bigrat.pm
%dir %{privlib}/Math
%{privlib}/Math/BigFloat
%dir %{privlib}/Math/BigInt
%{privlib}/Math/BigInt/Trace.pm
%{_mandir}/man3/bigint.*
%{_mandir}/man3/bignum.*
%{_mandir}/man3/bigrat.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Carp
%{privlib}/Carp
%{privlib}/Carp.*
%{_mandir}/man3/Carp.*

%files Compress-Raw-Bzip2
%dir %{archlib}/Compress
%dir %{archlib}/Compress/Raw
%{archlib}/Compress/Raw/Bzip2.pm
%dir %{archlib}/auto/Compress
%dir %{archlib}/auto/Compress/Raw
%{archlib}/auto/Compress/Raw/Bzip2
%{_mandir}/man3/Compress::Raw::Bzip2*

%files Compress-Raw-Zlib
%dir %{archlib}/Compress
%dir %{archlib}/Compress/Raw
%{archlib}/Compress/Raw/Zlib.pm
%dir %{archlib}/auto/Compress
%dir %{archlib}/auto/Compress/Raw
%{archlib}/auto/Compress/Raw/Zlib
%{_mandir}/man3/Compress::Raw::Zlib*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Config-Perl-V
%dir %{privlib}/Config
%{privlib}/Config/Perl
%{_mandir}/man3/Config::Perl::V.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files constant
%{privlib}/constant.pm
%{_mandir}/man3/constant.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN
%{_bindir}/cpan
%dir %{privlib}/App
%{privlib}/App/Cpan.pm
%{privlib}/CPAN
%{privlib}/CPAN.pm
%{_mandir}/man1/cpan.1*
%{_mandir}/man3/App::Cpan.*
%{_mandir}/man3/CPAN.*
%{_mandir}/man3/CPAN:*
%exclude %{privlib}/CPAN/Meta/
%exclude %{privlib}/CPAN/Meta.pm
%exclude %{_mandir}/man3/CPAN::Meta*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta.pm
%{privlib}/CPAN/Meta/Converter.pm
%{privlib}/CPAN/Meta/Feature.pm
%dir %{privlib}/CPAN/Meta/History
%{privlib}/CPAN/Meta/History.pm
%{privlib}/CPAN/Meta/Merge.pm
%{privlib}/CPAN/Meta/Prereqs.pm
%{privlib}/CPAN/Meta/Spec.pm
%{privlib}/CPAN/Meta/Validator.pm
%{_mandir}/man3/CPAN::Meta*
%exclude %{_mandir}/man3/CPAN::Meta::YAML*
%exclude %{_mandir}/man3/CPAN::Meta::Requirements*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta-Requirements
%dir %{privlib}/CPAN
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta/Requirements.pm
%{_mandir}/man3/CPAN::Meta::Requirements.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta-YAML
%dir %{privlib}/CPAN
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta/YAML.pm
%{_mandir}/man3/CPAN::Meta::YAML*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Data-Dumper
%dir %{archlib}/auto/Data
%dir %{archlib}/auto/Data/Dumper
%{archlib}/auto/Data/Dumper/Dumper.so
%dir %{archlib}/Data
%{archlib}/Data/Dumper.pm
%{_mandir}/man3/Data::Dumper.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files DB_File
%{archlib}/DB_File.pm
%dir %{archlib}/auto/DB_File
%{archlib}/auto/DB_File/DB_File.so
%{_mandir}/man3/DB_File*
%endif

%files Devel-Peek
%dir %{archlib}/Devel
%{archlib}/Devel/Peek.pm
%dir %{archlib}/auto/Devel
%{archlib}/auto/Devel/Peek
%{_mandir}/man3/Devel::Peek.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Devel-PPPort
%dir %{archlib}/Devel
%{archlib}/Devel/PPPort.pm
%{_mandir}/man3/Devel::PPPort.3*
%endif

%files Devel-SelfStubber
%dir %{privlib}/Devel
%{privlib}/Devel/SelfStubber.pm
%{_mandir}/man3/Devel::SelfStubber.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest
%{privlib}/Digest.pm
%dir %{privlib}/Digest
%{privlib}/Digest/base.pm
%{privlib}/Digest/file.pm
%{_mandir}/man3/Digest.3*
%{_mandir}/man3/Digest::base.3*
%{_mandir}/man3/Digest::file.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest-MD5
%dir %{archlib}/Digest
%{archlib}/Digest/MD5.pm
%dir %{archlib}/auto/Digest
%{archlib}/auto/Digest/MD5
%{_mandir}/man3/Digest::MD5.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest-SHA
%{_bindir}/shasum
%dir %{archlib}/Digest
%{archlib}/Digest/SHA.pm
%dir %{archlib}/auto/Digest
%{archlib}/auto/Digest/SHA
%{_mandir}/man1/shasum.1*
%{_mandir}/man3/Digest::SHA.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Encode
%{_bindir}/encguess
%{_bindir}/piconv
%{archlib}/Encode*
%{archlib}/auto/Encode*
%{privlib}/Encode
%exclude %{privlib}/Encode/*.e2x
%exclude %{privlib}/Encode/encode.h
%{_mandir}/man1/encguess.1*
%{_mandir}/man1/piconv.1*
%{_mandir}/man3/Encode*.3*

%files encoding
%{archlib}/encoding.pm
%{_mandir}/man3/encoding.3*

%files Encode-devel
%{_bindir}/enc2xs
%dir %{privlib}/Encode
%{privlib}/Encode/*.e2x
%{privlib}/Encode/encode.h
%{_mandir}/man1/enc2xs.1*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Env
%{privlib}/Env.pm
%{_mandir}/man3/Env.3*
%endif

%files Errno
%{archlib}/Errno.pm
%{_mandir}/man3/Errno.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Exporter
%{privlib}/Exporter*
%{_mandir}/man3/Exporter*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files experimental
%{privlib}/experimental*
%{_mandir}/man3/experimental*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-CBuilder
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/CBuilder
%{privlib}/ExtUtils/CBuilder.pm
%{_mandir}/man3/ExtUtils::CBuilder*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-Command
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Command.pm
%{_mandir}/man3/ExtUtils::Command.*
%endif

%files ExtUtils-Embed
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Embed.pm
%{_mandir}/man3/ExtUtils::Embed*

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-Install
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Install.pm
%{privlib}/ExtUtils/Installed.pm
%{privlib}/ExtUtils/Packlist.pm
%{_mandir}/man3/ExtUtils::Install.3*
%{_mandir}/man3/ExtUtils::Installed.3*
%{_mandir}/man3/ExtUtils::Packlist.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-Manifest
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Manifest.pm
%{privlib}/ExtUtils/MANIFEST.SKIP
%{_mandir}/man3/ExtUtils::Manifest.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-MakeMaker
%{_bindir}/instmodsh
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Command/
%{privlib}/ExtUtils/Liblist
%{privlib}/ExtUtils/Liblist.pm
%{privlib}/ExtUtils/MakeMaker
%{privlib}/ExtUtils/MakeMaker.pm
%{privlib}/ExtUtils/MM.pm
%{privlib}/ExtUtils/MM_*.pm
%{privlib}/ExtUtils/MY.pm
%{privlib}/ExtUtils/Mkbootstrap.pm
%{privlib}/ExtUtils/Mksymlists.pm
%{privlib}/ExtUtils/testlib.pm
%{_mandir}/man1/instmodsh.1*
%{_mandir}/man3/ExtUtils::Command::MM*
%{_mandir}/man3/ExtUtils::Liblist.3*
%{_mandir}/man3/ExtUtils::MM.3*
%{_mandir}/man3/ExtUtils::MM_*
%{_mandir}/man3/ExtUtils::MY.3*
%{_mandir}/man3/ExtUtils::MakeMaker*
%{_mandir}/man3/ExtUtils::Mkbootstrap.3*
%{_mandir}/man3/ExtUtils::Mksymlists.3*
%{_mandir}/man3/ExtUtils::testlib.3*
%endif

%files ExtUtils-Miniperl
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Miniperl.pm
%{_mandir}/man3/ExtUtils::Miniperl.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-MM-Utils
%dir %{privlib}/ExtUtils
%dir %{privlib}/ExtUtils/MM
%{privlib}/ExtUtils/MM/Utils.pm
%{_mandir}/man3/ExtUtils::MM::Utils.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-ParseXS
%dir %{privlib}/ExtUtils
%dir %{privlib}/ExtUtils/ParseXS
%{privlib}/ExtUtils/ParseXS.pm
%{privlib}/ExtUtils/ParseXS.pod
%{privlib}/ExtUtils/ParseXS/Constants.pm
%{privlib}/ExtUtils/ParseXS/CountLines.pm
%{privlib}/ExtUtils/ParseXS/Eval.pm
%{privlib}/ExtUtils/ParseXS/Utilities.pm
%dir %{privlib}/ExtUtils/Typemaps
%{privlib}/ExtUtils/Typemaps.pm
%{privlib}/ExtUtils/Typemaps/Cmd.pm
%{privlib}/ExtUtils/Typemaps/InputMap.pm
%{privlib}/ExtUtils/Typemaps/OutputMap.pm
%{privlib}/ExtUtils/Typemaps/Type.pm
%{privlib}/ExtUtils/xsubpp
%{_bindir}/xsubpp
%{_mandir}/man1/xsubpp*
%{_mandir}/man3/ExtUtils::ParseXS.3*
%{_mandir}/man3/ExtUtils::ParseXS::Constants.3*
%{_mandir}/man3/ExtUtils::ParseXS::Eval.3*
%{_mandir}/man3/ExtUtils::ParseXS::Utilities.3*
%{_mandir}/man3/ExtUtils::Typemaps.3*
%{_mandir}/man3/ExtUtils::Typemaps::Cmd.3*
%{_mandir}/man3/ExtUtils::Typemaps::InputMap.3*
%{_mandir}/man3/ExtUtils::Typemaps::OutputMap.3*
%{_mandir}/man3/ExtUtils::Typemaps::Type.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Fetch
%dir %{privlib}/File
%{privlib}/File/Fetch.pm
%{_mandir}/man3/File::Fetch.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Path
%dir %{privlib}/File
%{privlib}/File/Path.pm
%{_mandir}/man3/File::Path.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Temp
%dir %{privlib}/File
%{privlib}/File/Temp.pm
%{_mandir}/man3/File::Temp.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Filter
%dir %{archlib}/auto/Filter
%{archlib}/auto/Filter/Util
%dir %{archlib}/Filter
%{archlib}/Filter/Util
%{privlib}/pod/perlfilter.pod
%{_mandir}/man1/perlfilter.*
%{_mandir}/man3/Filter::Util::*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Filter-Simple
%dir %{privlib}/Filter
%{privlib}/Filter/Simple.pm
%{_mandir}/man3/Filter::Simple.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Getopt-Long
%dir %{privlib}/Getopt
%{privlib}/Getopt/Long.pm
%{_mandir}/man3/Getopt::Long.3*
%endif

%files IO
%dir %{archlib}/IO
%{archlib}/IO.pm
%{archlib}/IO/Dir.pm
%{archlib}/IO/File.pm
%{archlib}/IO/Handle.pm
%{archlib}/IO/Pipe.pm
%{archlib}/IO/Poll.pm
%{archlib}/IO/Seekable.pm
%{archlib}/IO/Select.pm
%dir %{archlib}/IO/Socket
%{archlib}/IO/Socket/INET.pm
%{archlib}/IO/Socket/UNIX.pm
%{archlib}/IO/Socket.pm
%dir %{archlib}/auto/IO
%{archlib}/auto/IO/IO.so
%{_mandir}/man3/IO.*
%{_mandir}/man3/IO::Dir.*
%{_mandir}/man3/IO::File.*
%{_mandir}/man3/IO::Handle.*
%{_mandir}/man3/IO::Pipe.*
%{_mandir}/man3/IO::Poll.*
%{_mandir}/man3/IO::Seekable.*
%{_mandir}/man3/IO::Select.*
%{_mandir}/man3/IO::Socket::INET.*
%{_mandir}/man3/IO::Socket::UNIX.*
%{_mandir}/man3/IO::Socket.*

%if %{dual_life} || %{rebuild_from_scratch}
%files IO-Compress
# IO-Compress
%{_bindir}/zipdetails
%dir %{privlib}/IO
%dir %{privlib}/IO/Compress
%{privlib}/IO/Compress/FAQ.pod
%{_mandir}/man1/zipdetails.*
%{_mandir}/man3/IO::Compress::FAQ.*
# Compress-Zlib
%dir %{privlib}/Compress
%{privlib}/Compress/Zlib.pm
%{_mandir}/man3/Compress::Zlib*
#IO-Compress-Base
%dir %{privlib}/File
%{privlib}/File/GlobMapper.pm
%dir %{privlib}/IO
%dir %{privlib}/IO/Compress
%{privlib}/IO/Compress/Base
%{privlib}/IO/Compress/Base.pm
%dir %{privlib}/IO/Uncompress
%{privlib}/IO/Uncompress/AnyUncompress.pm
%{privlib}/IO/Uncompress/Base.pm
%{_mandir}/man3/File::GlobMapper.*
%{_mandir}/man3/IO::Compress::Base.*
%{_mandir}/man3/IO::Uncompress::AnyUncompress.*
%{_mandir}/man3/IO::Uncompress::Base.*
# IO-Compress-Zlib
%dir %{privlib}/IO
%dir %{privlib}/IO/Compress
%{privlib}/IO/Compress/Adapter
%{privlib}/IO/Compress/Deflate.pm
%{privlib}/IO/Compress/Bzip2.pm
%{privlib}/IO/Compress/Gzip
%{privlib}/IO/Compress/Gzip.pm
%{privlib}/IO/Compress/RawDeflate.pm
%{privlib}/IO/Compress/Zip
%{privlib}/IO/Compress/Zip.pm
%{privlib}/IO/Compress/Zlib
%dir %{privlib}/IO/Uncompress
%{privlib}/IO/Uncompress/Adapter/
%{privlib}/IO/Uncompress/AnyInflate.pm
%{privlib}/IO/Uncompress/Bunzip2.pm
%{privlib}/IO/Uncompress/Gunzip.pm
%{privlib}/IO/Uncompress/Inflate.pm
%{privlib}/IO/Uncompress/RawInflate.pm
%{privlib}/IO/Uncompress/Unzip.pm
%{_mandir}/man3/IO::Compress::Deflate*
%{_mandir}/man3/IO::Compress::Gzip*
%{_mandir}/man3/IO::Compress::Bzip2*
%{_mandir}/man3/IO::Compress::RawDeflate*
%{_mandir}/man3/IO::Compress::Zip*
%{_mandir}/man3/IO::Uncompress::AnyInflate*
%{_mandir}/man3/IO::Uncompress::Bunzip2*
%{_mandir}/man3/IO::Uncompress::Gunzip*
%{_mandir}/man3/IO::Uncompress::Inflate*
%{_mandir}/man3/IO::Uncompress::RawInflate*
%{_mandir}/man3/IO::Uncompress::Unzip*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IO-Socket-IP
%dir %{privlib}/IO
%dir %{privlib}/IO/Socket
%{privlib}/IO/Socket/IP.pm
%{_mandir}/man3/IO::Socket::IP.*
%endif

%files IO-Zlib
%dir %{privlib}/IO
%{privlib}/IO/Zlib.pm
%{_mandir}/man3/IO::Zlib.*

%if %{dual_life} || %{rebuild_from_scratch}
%files HTTP-Tiny
%dir %{privlib}/HTTP
%{privlib}/HTTP/Tiny.pm
%{_mandir}/man3/HTTP::Tiny*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IPC-Cmd
%dir %{privlib}/IPC
%{privlib}/IPC/Cmd.pm
%{_mandir}/man3/IPC::Cmd.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IPC-SysV
%{archlib}/auto/IPC
%dir %{archlib}/IPC
%{archlib}/IPC/Msg.pm
%{archlib}/IPC/Semaphore.pm
%{archlib}/IPC/SharedMem.pm
%{archlib}/IPC/SysV.pm
%{_mandir}/man3/IPC::Msg.*
%{_mandir}/man3/IPC::Semaphore.*
%{_mandir}/man3/IPC::SharedMem.*
%{_mandir}/man3/IPC::SysV.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files JSON-PP
%{_bindir}/json_pp
%dir %{privlib}/JSON
%{privlib}/JSON/PP
%{privlib}/JSON/PP.pm
%{_mandir}/man1/json_pp.1*
%{_mandir}/man3/JSON::PP.3*
%{_mandir}/man3/JSON::PP::Boolean.3pm*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files libnet
%dir %{privlib}/Net
%{privlib}/Net/Cmd.pm
%{privlib}/Net/Config.pm
%{privlib}/Net/Domain.pm
%{privlib}/Net/FTP
%{privlib}/Net/FTP.pm
%{privlib}/Net/libnetFAQ.pod
%{privlib}/Net/NNTP.pm
%{privlib}/Net/Netrc.pm
%{privlib}/Net/POP3.pm
%{privlib}/Net/SMTP.pm
%{privlib}/Net/Time.pm
%{_mandir}/man3/Net::Cmd.*
%{_mandir}/man3/Net::Config.*
%{_mandir}/man3/Net::Domain.*
%{_mandir}/man3/Net::FTP.*
%{_mandir}/man3/Net::libnetFAQ.*
%{_mandir}/man3/Net::NNTP.*
%{_mandir}/man3/Net::Netrc.*
%{_mandir}/man3/Net::POP3.*
%{_mandir}/man3/Net::SMTP.*
%{_mandir}/man3/Net::Time.*
%endif

%files libnetcfg
%{_bindir}/libnetcfg
%{_mandir}/man1/libnetcfg*

%if %{dual_life} || %{rebuild_from_scratch}
%files Locale-Codes
%dir %{privlib}/Locale
%{privlib}/Locale/Codes
%{privlib}/Locale/Codes.*
%{privlib}/Locale/Country.*
%{privlib}/Locale/Currency.*
%{privlib}/Locale/Language.*
%{privlib}/Locale/Script.*
%{_mandir}/man3/Locale::Codes::*
%{_mandir}/man3/Locale::Codes.*
%{_mandir}/man3/Locale::Country.*
%{_mandir}/man3/Locale::Currency.*
%{_mandir}/man3/Locale::Language.*
%{_mandir}/man3/Locale::Script.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Locale-Maketext
%dir %{privlib}/Locale
%dir %{privlib}/Locale/Maketext
%{privlib}/Locale/Maketext.*
%{privlib}/Locale/Maketext/Cookbook.*
%{privlib}/Locale/Maketext/Guts.*
%{privlib}/Locale/Maketext/GutsLoader.*
%{privlib}/Locale/Maketext/TPJ13.*
%{_mandir}/man3/Locale::Maketext.*
%{_mandir}/man3/Locale::Maketext::Cookbook.*
%{_mandir}/man3/Locale::Maketext::Guts.*
%{_mandir}/man3/Locale::Maketext::GutsLoader.*
%{_mandir}/man3/Locale::Maketext::TPJ13.*
%endif

%files Locale-Maketext-Simple
%dir %{privlib}/Locale
%dir %{privlib}/Locale/Maketext
%{privlib}/Locale/Maketext/Simple.pm
%{_mandir}/man3/Locale::Maketext::Simple.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Math-BigInt
%dir %{privlib}/Math
%{privlib}/Math/BigFloat.pm
%{privlib}/Math/BigInt.pm
%dir %{privlib}/Math/BigInt
%{privlib}/Math/BigInt/Calc.pm
%{privlib}/Math/BigInt/CalcEmu.pm
%{_mandir}/man3/Math::BigFloat.*
%{_mandir}/man3/Math::BigInt.*
%{_mandir}/man3/Math::BigInt::Calc.*
%{_mandir}/man3/Math::BigInt::CalcEmu.*
%endif

%files Math-BigInt-FastCalc
%{archlib}/Math
%{archlib}/auto/Math
%{_mandir}/man3/Math::BigInt::FastCalc.*

%files Math-BigRat
%dir %{privlib}/Math
%{privlib}/Math/BigRat.pm
%{_mandir}/man3/Math::BigRat.*

%files Math-Complex
%dir %{privlib}/Math
%{privlib}/Math/Complex.pm
%{privlib}/Math/Trig.pm
%{_mandir}/man3/Math::Complex.*
%{_mandir}/man3/Math::Trig.*

%files Memoize
%{privlib}/Memoize
%{privlib}/Memoize.pm
%{_mandir}/man3/Memoize::*
%{_mandir}/man3/Memoize.*

%if %{dual_life} || %{rebuild_from_scratch}
%files MIME-Base64
%{archlib}/auto/MIME
%{archlib}/MIME
%{_mandir}/man3/MIME::*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-CoreList
%dir %{privlib}/Module
%{privlib}/Module/CoreList
%{privlib}/Module/CoreList.pm
%{privlib}/Module/CoreList.pod
%{_mandir}/man3/Module::CoreList*

%files Module-CoreList-tools
%{_bindir}/corelist
%{_mandir}/man1/corelist*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Load
%dir %{privlib}/Module
%{privlib}/Module/Load.pm
%{_mandir}/man3/Module::Load.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Load-Conditional
%dir %{privlib}/Module
%{privlib}/Module/Load
%{_mandir}/man3/Module::Load::Conditional*
%endif

%files Module-Loaded
%dir %{privlib}/Module
%{privlib}/Module/Loaded.pm
%{_mandir}/man3/Module::Loaded*

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Metadata
%dir %{privlib}/Module
%{privlib}/Module/Metadata.pm
%{_mandir}/man3/Module::Metadata.3pm*
%endif

%files Net-Ping
%dir %{privlib}/Net
%{privlib}/Net/Ping.pm
%{_mandir}/man3/Net::Ping.*

%if %{dual_life} || %{rebuild_from_scratch}
%files PathTools
%{archlib}/Cwd.pm
%dir %{archlib}/File
%{archlib}/File/Spec*
%{archlib}/auto/Cwd
%{_mandir}/man3/Cwd*
%{_mandir}/man3/File::Spec*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Params-Check
%{privlib}/Params/
%{_mandir}/man3/Params::Check*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Parse-CPAN-Meta
%dir %{privlib}/Parse/
%dir %{privlib}/Parse/CPAN/
%{privlib}/Parse/CPAN/Meta.pm
%{_mandir}/man3/Parse::CPAN::Meta.3*
%endif

%files open
%{privlib}/open.pm
%{_mandir}/man3/open.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files parent
%{privlib}/parent.pm
%{_mandir}/man3/parent.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files perlfaq
%{privlib}/perlfaq.pm
%dir %{privlib}/pod
%{privlib}/pod/perlfaq*
%{privlib}/pod/perlglossary.pod
%{_mandir}/man1/perlfaq*
%{_mandir}/man1/perlglossary.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files PerlIO-via-QuotedPrint
%{privlib}/PerlIO
%{_mandir}/man3/PerlIO::via::QuotedPrint.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Perl-OSType
%dir %{privlib}/Perl
%{privlib}/Perl/OSType.pm
%{_mandir}/man3/Perl::OSType.3pm*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Checker
%{_bindir}/podchecker
%dir %{privlib}/Pod
%{privlib}/Pod/Checker.pm
%{_mandir}/man1/podchecker.*
%{_mandir}/man3/Pod::Checker.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Escapes
%dir %{privlib}/Pod
%{privlib}/Pod/Escapes.pm
%{_mandir}/man3/Pod::Escapes.*
%endif

%files Pod-Html
%doc Pod-Html-license-clarification
%dir %{privlib}/Pod
%{_bindir}/pod2html
%{privlib}/Pod/Html.pm
%{_mandir}/man1/pod2html.1*
%{_mandir}/man3/Pod::Html.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Parser
%{_bindir}/podselect
%dir %{privlib}/Pod
%{privlib}/Pod/Find.pm
%{privlib}/Pod/InputObjects.pm
%{privlib}/Pod/ParseUtils.pm
%{privlib}/Pod/Parser.pm
%{privlib}/Pod/PlainText.pm
%{privlib}/Pod/Select.pm
%{_mandir}/man1/podselect.1*
%{_mandir}/man3/Pod::Find.*
%{_mandir}/man3/Pod::InputObjects.*
%{_mandir}/man3/Pod::ParseUtils.*
%{_mandir}/man3/Pod::Parser.*
%{_mandir}/man3/Pod::PlainText.*
%{_mandir}/man3/Pod::Select.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Perldoc
%{_bindir}/perldoc
%{privlib}/pod/perldoc.pod
%dir %{privlib}/Pod
%{privlib}/Pod/Perldoc
%{privlib}/Pod/Perldoc.pm
%{_mandir}/man1/perldoc.1*
%{_mandir}/man3/Pod::Perldoc*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Usage
%{_bindir}/pod2usage
%dir %{privlib}/Pod
%{privlib}/Pod/Usage.pm
%{_mandir}/man1/pod2usage.*
%{_mandir}/man3/Pod::Usage.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files podlators
%{_bindir}/pod2man
%{_bindir}/pod2text
%{privlib}/pod/perlpodstyle.pod
%dir %{privlib}/Pod
%{privlib}/Pod/Man.pm
%{privlib}/Pod/ParseLink.pm
%{privlib}/Pod/Text
%{privlib}/Pod/Text.pm
%{_mandir}/man1/pod2man.1*
%{_mandir}/man1/pod2text.1*
%{_mandir}/man1/perlpodstyle.1*
%{_mandir}/man3/Pod::Man*
%{_mandir}/man3/Pod::ParseLink*
%{_mandir}/man3/Pod::Text*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Simple
%dir %{privlib}/Pod
%{privlib}/Pod/Simple
%{privlib}/Pod/Simple.pm
%{privlib}/Pod/Simple.pod
%{_mandir}/man3/Pod::Simple*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Scalar-List-Utils
%{archlib}/List
%{archlib}/Scalar
%{archlib}/Sub
%{archlib}/auto/List
%{_mandir}/man3/List::Util*
%{_mandir}/man3/Scalar::Util*
%{_mandir}/man3/Sub::Util*
%endif

%files SelfLoader
%{privlib}/SelfLoader.pm
%{_mandir}/man3/SelfLoader*

%if %{dual_life} || %{rebuild_from_scratch}
%files Sys-Syslog
%dir %{archlib}/Sys
%{archlib}/Sys/Syslog.pm
%dir %{archlib}/auto/Sys
%{archlib}/auto/Sys/Syslog
%{_mandir}/man3/Sys::Syslog.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Socket
%dir %{archlib}/auto/Socket
%{archlib}/auto/Socket/Socket.*
%{archlib}/Socket.pm
%{_mandir}/man3/Socket.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Storable
%{archlib}/Storable.pm
%{archlib}/auto/Storable
%{_mandir}/man3/Storable.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Term-ANSIColor
%dir %{privlib}/Term
%{privlib}/Term/ANSIColor.pm
%{_mandir}/man3/Term::ANSIColor*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Term-Cap
%dir %{privlib}/Term
%{privlib}/Term/Cap.pm
%{_mandir}/man3/Term::Cap.*
%endif

%files Test
%{privlib}/Test.pm
%{_mandir}/man3/Test.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Test-Harness
%{_bindir}/prove
%dir %{privlib}/App
%{privlib}/App/Prove*
%{privlib}/TAP*
%dir %{privlib}/Test
%{privlib}/Test/Harness*
%{_mandir}/man1/prove.1*
%{_mandir}/man3/App::Prove*
%{_mandir}/man3/TAP*
%{_mandir}/man3/Test::Harness*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Test-Simple
%{privlib}/ok*
%dir %{privlib}/Test
%{privlib}/Test/More*
%{privlib}/Test/Builder*
%{privlib}/Test/Tester*
%{privlib}/Test/Simple*
%{privlib}/Test/Tutorial*
%{privlib}/Test/use
%{_mandir}/man3/ok*
%{_mandir}/man3/Test::More*
%{_mandir}/man3/Test::Builder*
%{_mandir}/man3/Test::Tester*
%{_mandir}/man3/Test::Simple*
%{_mandir}/man3/Test::Tutorial*
%{_mandir}/man3/Test::use::*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-Balanced
%dir %{privlib}/Text
%{privlib}/Text/Balanced.pm
%{_mandir}/man3/Text::Balanced.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-ParseWords
%dir %{privlib}/Text
%{privlib}/Text/ParseWords.pm
%{_mandir}/man3/Text::ParseWords.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-Tabs+Wrap
%dir %{privlib}/Text
%{privlib}/Text/Tabs.pm
%{privlib}/Text/Wrap.pm
%{_mandir}/man3/Text::Tabs.*
%{_mandir}/man3/Text::Wrap.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Thread-Queue
%dir %{privlib}/Thread
%{privlib}/Thread/Queue.pm
%{_mandir}/man3/Thread::Queue.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Time-HiRes
%dir %{archlib}/Time
%{archlib}/Time/HiRes.pm
%dir %{archlib}/auto/Time
%{archlib}/auto/Time/HiRes
%{_mandir}/man3/Time::HiRes.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Time-Local
%dir %{privlib}/Time
%{privlib}/Time/Local.pm
%{_mandir}/man3/Time::Local.*
%endif

%files Time-Piece
%dir %{archlib}/Time
%{archlib}/Time/Piece.pm
%{archlib}/Time/Seconds.pm
%dir %{archlib}/auto/Time
%{archlib}/auto/Time/Piece
%{_mandir}/man3/Time::Piece.3*
%{_mandir}/man3/Time::Seconds.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files threads
%dir %{archlib}/auto/threads
%{archlib}/auto/threads/threads*
%{archlib}/threads.pm
%{_mandir}/man3/threads.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files threads-shared
%dir %{archlib}/auto/threads
%{archlib}/auto/threads/shared*
%dir %{archlib}/threads
%{archlib}/threads/shared*
%{_mandir}/man3/threads::shared*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Unicode-Collate
%dir %{archlib}/auto/Unicode
%{archlib}/auto/Unicode/Collate
%dir %{archlib}/Unicode
%{archlib}/Unicode/Collate
%{archlib}/Unicode/Collate.pm
%dir %{privlib}/Unicode
%{privlib}/Unicode/Collate
%{_mandir}/man3/Unicode::Collate.*
%{_mandir}/man3/Unicode::Collate::*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Unicode-Normalize
%dir %{archlib}/auto/Unicode
%{archlib}/auto/Unicode/Normalize
%dir %{archlib}/Unicode
%{archlib}/Unicode/Normalize.pm
%{_mandir}/man3/Unicode::Normalize.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files version
%{privlib}/version.pm
%{privlib}/version.pod
%{privlib}/version/
%{_mandir}/man3/version.3*
%{_mandir}/man3/version::Internals.3*
%endif

%files core
# Nothing. Nada. Zilch. Zarro. Uh uh. Nope. Sorry.

# Old changelog entries are preserved in CVS.
%changelog
* Sun Jul 24 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-375
- Rebuild without bootstrap

* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-374
- Fix a crash in lexical scope warnings (RT#128597)

* Fri Jul 08 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-373
- Fix a crash in "Subroutine redefined" warning (RT#128257)

* Thu Jul 07 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-372
- Fix a crash when vivifying a stub in a deleted package (RT#128532)

* Thu Jul 07 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.24.0-371
- Do not let XSLoader load relative paths (CVE-2016-6185)

* Mon Jul 04 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-370
- Fix line numbers with perl -x (RT#128508)

* Fri Jun 24 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-369
- Do not crash when inserting a non-stash into a stash (RT#128238)

* Wed Jun 22 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-368
- Do not use unitialized memory in $h{\const} warnings (RT#128189)
- Fix precedence in hv_ename_delete (RT#128086)
- Do not treat %: as a stash (RT#128238)

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-367
- Fix compiling regular expressions like /\X*(?0)/ (RT#128109)

* Thu Jun 16 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-366
- Do not mangle errno from failed socket calls (RT#128316)

* Tue Jun 14 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-365
- Fix a memory leak when compiling a regular expression with a POSIX class
  (RT#128313)

* Thu May 19 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-364
- Remove reflexive dependencies
- Use pregenerated dependencies on bootstrapping
- Specify more build-time dependencies

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.24.0-363
- Stop providing old perl(MODULE_COMPAT_5.22.*)
- Update license tags

* Wed May 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.24.0-362
- 5.24.0 bump (see <http://search.cpan.org/dist/perl-5.24.0/pod/perldelta.pod>
  for release notes)
- Update sub-packages; Update or remove patches

* Mon May 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.22.6-361
- 5.22.2 bump (see <http://search.cpan.org/dist/perl-5.22.2/pod/perldelta.pod>
  for release notes)

* Mon Apr 18 2016 Petr Pisar <ppisar@redhat.com> - 4:5.22.1-360
- Weak perl-Encode-devel dependency on perl-devel to Recommends level
  (bug #1129443)
- Remove perl-ExtUtils-ParseXS dependency on perl-devel (bug #1129443)
- Require perl-devel by perl-ExtUtils-MakeMaker
- Provide MM::maybe_command independently (bug #1129443)
- Replace ExtUtils::MakeMaker dependency with ExtUtils::MM::Utils in IPC::Cmd
  (bug #1129443)
- Remove perl-ExtUtils-Install dependency on perl-devel (bug #1129443)
- Remove perl-ExtUtils-Manifest dependency on perl-devel (bug #1129443)

* Tue Mar 15 2016 Petr Pisar <ppisar@redhat.com> - 4:5.22.1-359
- Do not filter FCGI dependency, CGI is non-core now

* Fri Mar 04 2016 Petr Pisar <ppisar@redhat.com> - 4:5.22.1-358
- Remove bundled perl-IPC-SysV (bug #1308527)

* Wed Mar 02 2016 Petr Pisar <ppisar@redhat.com> - 4:5.22.1-357
- Fix CVE-2016-2381 (ambiguous environment variables handling) (bug #1313702)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4:5.22.1-356
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.1-355
- Remove bundled Math-BigInt (bug #1277203)

* Mon Dec 14 2015 Jitka Plesnikova <jplesnik@redhat.com> - 5.22.1-354
- 5.22.1 bump (see <http://search.cpan.org/dist/perl-5.22.1/pod/perldelta.pod>
  for release notes)

* Tue Oct 20 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-353
- Rebuild to utilize perl(:VERSION) dependency symbol

* Tue Oct 13 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-352
- Do not own IO::Socket::IP manual page by perl-IO

* Fri Oct 09 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-351
- Sub-package Attribute-Handlers
- Sub-package Devel-Peek
- Sub-package Devel-SelfStubber
- Sub-package SelfLoader
- Sub-package IO
- Sub-package Errno
- Correct perl-Digest-SHA dependencies
- Correct perl-Pod-Perldoc dependencies
- Move utf8 and dependencies to perl-libs
- Correct perl-devel and perl-CPAN dependencies
- Sub-package IPC-SysV
- Sub-package Test
- Sub-package utilities (splain) into perl-utils
- Provide perl version in perl(:VERSION) dependency symbol

* Fri Aug 07 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-350
- Sub-package Memoize
- Sub-package Net-Ping
- Sub-package Pod-Html

* Thu Jul 16 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-349
- Disable hardening due to some run-time failures (bug #1238804)

* Mon Jul 13 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-348
- Sub-package bignum
- Sub-package Math-BigRat
- Sub-package Math-BigInt-FastCalc
- Sub-package Math-Complex
- Remove bundled perl-Config-Perl-V (bug #1238203)
- Remove bundled perl-MIME-Base64 (bug #1238222)
- Remove bundled perl-PerlIO-via-QuotedPrint (bug #1238229)
- Remove bundled perl-Pod-Escapes (bug #1238237)
- Remove bundled perl-Term-Cap (bug #1238248)
- Remove bundled perl-Text-Balanced (bug #1238269)
- Remove bundled perl-libnet (bug #1238689)
- Remove bundled perl-perlfaq (bug #1238703)
- Remove bundled perl-Unicode-Normalize (bug #1238730)
- Remove bundled perl-Unicode-Collate (bug #1238760)

* Wed Jul 08 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-347
- Store distribution's linker and compiler flags to more Config's options
  in order to apply them when linking executable programs (bug #1238804)
- Sub-package Config-Perl-V (bug #1238203)
- Sub-package MIME-Base64 (bug #1238222)
- Sub-package PerlIO-via-QuotedPrint (bug #1238229)
- Update Pod-Escapes metadata (bug #1238237)
- Sub-package Term-Cap (bug #1238248)
- Sub-package Text-Balanced (bug #1238269)
- Sub-package libnet (bug #1238689)
- Sub-package perlfaq (bug #1238703)
- Sub-package Unicode-Normalize (bug #1238730)
- Sub-package Unicode-Collate (bug #1238760)
- Sub-package Math-BigInt
- Do not provide Net/libnet.cfg (bug #1238689)
- Revert downstream change in Net::Config default configuration
- Move libnetcfg tool from perl-devel into perl-libnetcfg sub-package

* Thu Jun 18 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-346
- Subpackage "open" module in order to keep deprecated "encoding" module
  optional (bug #1228378)
- Control building dual-lived sub-packages by perl_bootstrap macro
- Make PadlistNAMES() lvalue again (bug #1231165)
- Make magic vtable writable as a work-around for Coro (bug #1231165)
- Explain file break-down into RPM packages in perl package description

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.22.0-345
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.22.0-244
- Stop providing old perl(MODULE_COMPAT_5.20.*)

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.22.0-243
- Move ok and Test::Use::ok to perl-Test-Simple

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.22.0-242
- Move bin/encguess to perl-Encode

* Mon Jun 01 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.22.0-241
- 5.22.0 bump (see <http://search.cpan.org/dist/perl-5.22.0/pod/perldelta.pod>
  for release notes)
- Update sub-packages and erase the removed modules from the core
- Clean patches, not needed with new version
- Update patches to work with new version

* Wed Apr 15 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.2-328
- Sub-package perl-CGI-Fast and perl-Module-Build-Deprecated
- Add missing dual-life modules to perl-core

* Thu Apr 02 2015 Petr Šabata <contyk@redhat.com> - 4:5.20.2-327
- Bump to make koji happy

* Thu Apr 02 2015 Petr Šabata <contyk@redhat.com> - 4:5.20.2-326
- Correct license tags of the main package, CGI, Compress-Raw-Zlib,
  Digest-MD5, Test-Simple and Time-Piece
- Package a Pod-Html license clarification email

* Wed Mar 25 2015 Petr Pisar <ppisar@redhat.com> - 4:5.20.2-325
- Sub-package Text-Tabs+Wrap (bug #910798)

* Thu Mar 19 2015 Lubomir Rintel <lkundrak@v3.sk> - 4:5.20.2-324
- Add systemtap probes for new dtrace markers

* Mon Mar 16 2015 Petr Pisar <ppisar@redhat.com> - 4:5.20.2-323
- Move perl(:MODULE_COMPAT_*) symbol and include directories to perl-libs
  package (bug #1174951)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 4:5.20.2-322
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 18 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.2-321
- Provide 5.20.2 MODULE_COMPAT
- Clean list of provided files
- Update names of changed patches

* Tue Feb 17 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.2-320
- 5.20.2 bump (see <http://search.cpan.org/dist/perl-5.20.2/pod/perldelta.pod>
  for release notes)
- Regenerate a2p.c (BZ#1177672)

* Mon Feb 16 2015 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-319
- Improve h2ph fix for GCC 5.0

* Thu Feb 12 2015 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-318
- Fix regressions with GCC 5.0

* Tue Feb 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.1-317
- Sub-package inc-latest module

* Fri Jan 23 2015 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-316
- Delete dual-living programs clashing on debuginfo files (bug #878863)

* Mon Dec 01 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-315
- Report inaccesible file on failed require (bug #1166504)
- Use stronger algorithm needed for FIPS in t/op/taint.t (bug #1128032)

* Wed Nov 19 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-314
- Consider Filter::Util::Call dependency as mandatory (bug #1165183)
- Sub-package encoding module
- Own upper directories by each package that installs a file there and
  remove empty directories (bug #1165013)

* Thu Nov 13 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-313
- Freeze epoch at perl-Pod-Checker and perl-Pod-Usage (bug #1163490)
- Remove bundled perl-ExtUtils-Command (bug #1158536)
- Remove bundled perl-Filter-Simple (bug #1158542)

* Wed Nov 12 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-312
- Do not double-own perl-Pod-Usage' and perl-Pod-Checker' files by
  perl-Pod-Parser on bootstrap
- Sub-package ExtUtils-Command (bug #1158536)
- Sub-package Filter-Simple (bug #1158542)
- Build-require groff-base instead of big groff

* Wed Oct 29 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-311
- Remove bundled perl-Devel-PPPort (bug #1143999)
- Remove bundled perl-B-Debug (bug #1142952)
- Remove bundled perl-ExtUtils-CBuilder (bug #1144033)
- Remove bundled perl-ExtUtils-Install (bug #1144068)

* Thu Oct 23 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-310
- Move all Module-CoreList files into perl-Module-CoreList
- Sub-package corelist(1) into perl-Module-CoreList-tools (bug #1142757)
- Remove bundled perl-Module-CoreList, and perl-Module-CoreList-tools
  (bug #1142757)
- Sub-package Devel-PPPort (bug #1143999)
- Sub-package B-Debug (bug #1142952)
- Use native version for perl-ExtUtils-CBuilder
- Specify all dependencies for perl-ExtUtils-Install (bug #1144068)
- Require perl-ExtUtils-ParseXS by perl-ExtUtils-MakeMaker because of xsubpp

* Tue Sep 16 2014 Petr Šabata <contyk@redhat.com> - 4:5.20.1-309
- Provide 5.20.0 MODULE_COMPAT

* Mon Sep 15 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.1-308
- 5.20.1 bump (see <http://search.cpan.org/dist/perl-5.20.1/pod/perldelta.pod>
  for release notes)
- Sub-package perl-ExtUtils-Miniperl (bug #1141222)

* Wed Sep 10 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.0-307
- Specify all dependencies for perl-CPAN (bug #1090112)
- Disable non-core modules at perl-CPAN when bootstrapping
- Remove bundled perl-CPAN (bug #1090112)

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.0-306
- Stop providing old perl(MODULE_COMPAT_5.18.*)

* Mon Aug 18 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.0-305
- Update to Perl 5.20.0
- Clean patches, not needed with new version
- Update patches to work with new version
- Update version of sub-packages, remove the deleted sub-packages
- Sub-package perl-IO-Socket-IP, perl-experimental
- Disable BR perl(local::lib) for cpan tool when bootstraping

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.18.2-304
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-303
- Declare dependencies for cpan tool (bug #1122498)
- Use stronger algorithm needed for FIPS in t/op/crypt.t (bug #1128032)
- Make *DBM_File desctructors thread-safe (bug #1107543)

* Tue Jul 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.18.2-302
- Sub-package perl-Term-ANSIColor and remove it (bug #1121924)

* Fri Jun 27 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-301
- Remove bundled perl-App-a2p, perl-App-find2perl, perl-App-s2p, and
  perl-Package-Constants
- Correct perl-App-s2p license to ((GPL+ or Artistic) and App-s2p)

* Thu Jun 19 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-300
- Sub-package perl-App-find2perl (bug #1111196)
- Sub-package perl-App-a2p (bug #1111232)
- Sub-package perl-App-s2p (bug #1111242)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.18.2-299
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 10 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-298
- Pass -fwrapv to stricter GCC 4.9 (bug #1082957)

* Fri Apr 04 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-297
- Fix t/comp/parser.t not to load system modules (bug #1084399)

* Mon Feb 03 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-296
- Move macro files into %%{_rpmconfigdir}/macros.d

* Wed Jan 29 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-295
- Provide perl(CPAN::Meta::Requirements) with six decimal places

* Tue Jan 21 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-294
- Drop perl-Test-Simple-tests package is it is not delivered by dual-lived
  version
- Hide dual-lived perl-Object-Accessor

* Tue Jan 14 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-293
- Use a macro to cover all 64-bit PowerPC architectures (bug #1052709)

* Tue Jan 14 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-292
- Use upstream patch to fix a test failure in perl5db.t when TERM=vt100

* Tue Dec 10 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.18.2-291
- 5.18.2 bump (see <http://search.cpan.org/dist/perl-5.18.2/pod/perldelta.pod>
  for release notes)

* Mon Dec 02 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.1-290
- Document Math::BigInt::CalcEmu requires Math::BigInt (bug #959096)

* Tue Oct 22 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.1-289
- perl_default_filter macro does not need to filter private libraries from
  provides (bug #1020809)
- perl_default_filter anchors the filter regular expressions
- perl_default_filter appends the filters instead of redefining them

* Mon Sep 09 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.18.1-288
- Fix rules for parsing numeric escapes in regexes (bug #978233)
- Fix crash with \&$glob_copy (bug #989486)
- Fix coreamp.t's rand test (bug #970567)
- Reap child in case where exception has been thrown (bug #988805)
- Fix using regexes with multiple code blocks (bug #982131)

* Tue Aug 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.18.1-287
- 5.18.1 bump (see <http://search.cpan.org/dist/perl-5.18.1/pod/perldelta.pod>
  for release notes)
- Disable macro %%{rebuild_from_scratch}
- Fix regex seqfault 5.18 regression (bug #989921)
- Fixed interpolating downgraded variables into upgraded (bug #970913)
- SvTRUE returns correct value (bug #967463)
- Fixed doc command in perl debugger (bug #967461)
- Fixed unaligned access in slab allocator (bug #964950)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.18.0-286
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.0-285
- Stop providing old perl(MODULE_COMPAT_5.16.*)

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.0-284
- Perl 5.18 rebuild

* Tue Jul 09 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.0-283
- Define SONAME for libperl.so and move the libary into standard path
- Link XS modules to libperl.so on Linux (bug #960048)

* Mon Jul 08 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.0-282
- Do not load system Term::ReadLine::Gnu while running tests
- Disable ornaments on perl5db AutoTrace tests

* Thu Jul 04 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.18.0-281
- Update to Perl 5.18.0
- Clean patches, not needed with new version

* Wed Jun 26 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-280
- Edit local patch level before compilation

* Fri Jun 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-279
- Do not distribute File::Spec::VMS (bug #973713)
- Remove bundled CPANPLUS-Dist-Build (bug #973041)

* Wed Jun 12 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-278
- Update SystemTap scripts to recognize new phase__change marker and new probe
  arguments (bug #971094)
- Update h2ph(1) documentation (bug #948538)
- Update pod2html(1) documentation (bug #948538)
- Do not double-own archlib directory (bug #894195)

* Tue Jun 11 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-277
- Move CPANPLUS-Dist-Build files from perl-CPANPLUS
- Move CPAN-Meta-Requirements files from CPAN-Meta
- Add perl-Scalar-List-Utils to perl-core dependencies

* Thu Jun 06 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-276
- Require $Config{libs} providers (bug #905482)

* Thu May 30 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-275
- Correct typo in perl-Storable file list (bug #966865)
- Remove bundled Storable (bug #966865)

* Wed May 29 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-274
- Sub-package Storable (bug #966865)

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-273
- Use lib64 directories on aarch64 architecture (bug #961900)

* Fri May 10 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-272
- Make regular expression engine safe in a signal handler (bug #849703)
- Remove bundled ExtUtils-ParseXS, and Time-HiRes

* Fri Apr 26 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-271
- Sub-package Time-HiRes (bug #957048)
- Remove bundled Getopt-Long, Locale-Maketext, and Sys-Syslog

* Wed Apr 10 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-270
- Fix leaking tied hashes (bug #859910)
- Fix dead lock in PerlIO after fork from thread (bug #947444)
- Add proper conflicts to perl-Getopt-Long, perl-Locale-Maketext, and
  perl-Sys-Syslog

* Tue Apr 09 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-269
- Sub-package Sys-Syslog (bug #950057)

* Fri Apr 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-268
- Sub-package Getopt-Long (bug #948855)
- Sub-package Locale-Maketext (bug #948974)

* Fri Apr 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-267
- Remove bundled constant, DB_File, Digest-MD5, Env, Exporter, File-Path,
  File-Temp, Module-Load, Log-Message-Simple, Pod-Simple, Test-Harness,
  Text-ParseWords

* Mon Mar 25 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-266
- Filter provides from *.pl files (bug #924938)

* Fri Mar 22 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-265
- Conflict perl-autodie with older perl (bug #911226)
- Sub-package Env (bug #924619)
- Sub-package Exporter (bug #924645)
- Sub-package File-Path (bug #924782)
- Sub-package File-Temp (bug #924822)

* Thu Mar 21 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-264
- Sub-package constant (bug #924169)
- Sub-package DB_File (bug #924351)

* Tue Mar 19 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-263
- Correct perl-Digest-MD5 dependencies
- Remove bundled Archive-Extract, File-Fetch, HTTP-Tiny,
  Module-Load-Conditional, Time-Local

* Fri Mar 15 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-262
- Correct dependencies of perl-HTTP-Tiny
- Sub-package Time-Local (bug #922054)

* Thu Mar 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-261
- 5.16.3 bump (see <http://search.cpan.org/dist/perl-5.16.3/pod/perldelta.pod>
  for release notes)
- Remove bundled autodie, B-Lint, CPANPLUS, Encode, File-CheckTree, IPC-Cmd,
  Params-Check, Text-Soundex, Thread-Queue

* Tue Mar 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-260
- Fix CVE-2013-1667 (DoS in rehashing code) (bug #918008)

* Mon Feb 18 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-259
- Sub-package autodie (bug #911226)
- Add NAME headings to CPAN modules (bug #908113)

* Thu Feb 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-258
- Fix perl-Encode-devel dependency declaration

* Thu Feb 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-257
- Sub-package Thread-Queue (bug #911062)

* Wed Feb 13 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-256
- Sub-package File-CheckTree (bug #909144)
- Sub-package Text-ParseWords
- Sub-package Encode (bug #859149)

* Fri Feb 08 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-255
- Remove bundled Log-Message
- Remove bundled Term-UI

* Thu Feb 07 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-254
- Correct perl-podlators dependencies
- Obsolete perl-ExtUtils-Typemaps by perl-ExtUtils-ParseXS (bug #891952)

* Tue Feb 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-253
- Sub-package Pod-Checker and Pod-Usage (bugs #907546, #907550)

* Mon Feb 04 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-252
- Remove bundled PathTools

* Wed Jan 30 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-251
- Sub-package B-Lint (bug #906015)

* Wed Jan 30 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-250
- Sub-package Text-Soundex (bug #905889)
- Fix conflict declaration at perl-Pod-LaTeX (bug #904085)
- Remove bundled Module-Pluggable (bug #903624)

* Tue Jan 29 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-249
- Run-require POD convertors by Module-Build and ExtUtils-MakeMaker to
  generate documentation when building other packages

* Fri Jan 25 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-248
- Sub-package Pod-LaTeX (bug #904085)

* Wed Jan 16 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-247
- Remove bundled Pod-Parser

* Fri Jan 11 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-246
- Fix CVE-2012-6329 (misparsing of maketext strings) (bug #884354)

* Thu Jan 10 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-245
- Do not package App::Cpan(3pm) to perl-Test-Harness (bug #893768)

* Tue Dec 18 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-244
- Remove bundled Archive-Tar
- Remove bundled CPAN-Meta-YAML
- Remove bundled Module-Metadata

* Tue Dec 18 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-243
- Remove bundled Filter modules

* Mon Nov 05 2012 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.2-242
- 5.16.2 bump (see
  http://search.cpan.org/dist/perl-5.16.1/pod/perldelta.pod for release
  notes)

* Wed Oct 31 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-241
- Remove bundled podlators (bug #856516)

* Wed Oct 17 2012 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.1-240
- Do not crash when vivifying $| (bug #865296)

* Mon Sep 24 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-239
- Conflict perl-podlators with perl before sub-packaging (bug #856516)

* Fri Sep 21 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-238
- Do not leak with attribute on my variable (bug #858966)
- Allow operator after numeric keyword argument (bug #859328)
- Extend stack in File::Glob::glob (bug #859332)

* Thu Sep 20 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-237
- Put perl-podlators into perl-core list (bug #856516)

* Tue Sep 18 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-236
- Remove bundled perl-ExtUtils-Manifest
- perl-PathTools uses Carp

* Fri Sep 14 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-235
- Override the Pod::Simple::parse_file to set output to STDOUT by default
  (bug #826872)

* Wed Sep 12 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-234
- Sub-package perl-podlators (bug #856516)

* Tue Sep 11 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-233
- Do not access freed memory when cloning thread (bug #825749)
- Match non-breakable space with /[\h]/ in ASCII mode (bug #844919)
- Clear $@ before `do' I/O error (bug #834226)
- Do not truncate syscall() return value to 32 bits (bug #838551)

* Wed Sep 05 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-232
- Move App::Cpan from perl-Test-Harness to perl-CPAN (bug #854577)

* Fri Aug 24 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-231
- Remove perl-devel dependency from perl-Test-Harness and perl-Test-Simple

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-230
- define perl_compat by macro for rebuilds
- sub-packages depend on compat rather than on nvr

* Thu Aug  9 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-229
- apply conditionals for dual life patches

* Thu Aug 09 2012 Jitka Plesnikova <jplesnik@redhat.com> 4:5.16.1-228
- 5.16.1 bump (see
  http://search.cpan.org/dist/perl-5.16.1/pod/perldelta.pod for release
  notes)
- Fixed reopening by scalar handle (bug #834221)
- Fixed tr/// multiple transliteration (bug #831679)
- Fixed heap-overflow in gv_stashpv (bug #826516)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.16.0-227
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Paul Howarth <paul@city-fan.org> 4:5.16.0-226
- Move the rest of ExtUtils-ParseXS into its sub-package, so that the main
  perl package doesn't need to pull in perl-devel (bug #839953)

* Mon Jul 02 2012 Jitka Plesnikova <jplesnik@redhat.com> 4:5.16.0-225
- Fix broken atof (bug #835452)

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-224
- perl-Pod-Perldoc must require groff-base because Pod::Perldoc::ToMan executes
  roff

* Mon Jun 25 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-223
- Test::Build requires Data::Dumper
- Sub-package perl-Pod-Parser

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-222
- Remove MODULE_COMPAT_5.14.* Provides

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-221
- Perl 5.16 rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-220
- perl_bootstrap macro is distributed in perl-srpm-macros now

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-219
- Own zipdetails and IO::Compress::FAQ by perl-IO-Compress

* Fri Jun  1 2012 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.0-218
- Fix find2perl to translate ? glob properly (bug #825701)

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-218
- Shorten perl-Module-Build version to 2 digits to follow upstream

* Fri May 25 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-217
- upload the stable 5.16.0

* Wed May 16 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-RC2-217
- clean patches, not needed with new version
- regen by podcheck list of failed pods. cn, jp, ko pods failed. I can't decide
  whether it's a real problem or false positives.

* Mon Apr 30 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-216
- Enable usesitecustomize

* Thu Apr 19 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-215
- Rebuild perl against Berkeley database version 5 (bug #768846)

* Fri Apr 13 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-214
- perl-Data-Dumper requires Scalar::Util (bug #811239)

* Tue Apr 10 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-213
- Sub-package Data::Dumper (bug #811239)

* Tue Feb 21 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-212
- Sub-package Filter (bug #790349)

* Mon Feb 06 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-211
- Fix searching for Unicode::Collate::Locale data (bug #756118)
- Run safe signal handlers before returning from sigsuspend() and pause()
  (bug #771228)
- Correct perl-Scalar-List-Utils files list
- Stop !$^V from leaking (bug #787613)

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 4:5.14.2-210
- Rebuild again now that perl dependency generator is fixed (#772632, #772699)

* Fri Jan 06 2012 Iain Arnell <iarnell@gmail.com> -4:5.14.2-209
- perl-ExtUtils-MakeMaker sub-package requires ExtUtils::Install

* Fri Jan  6 2012 Paul Howarth <paul@city-fan.org> - 4:5.14.2-208
- Rebuild for gcc 4.7

* Tue Dec 20 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-207
- Fix interrupted reading. Thanks to Šimon Lukašík for reporting this issue
  and thanks to Marcela Mašláňová for finding fix. (bug #767931)

* Wed Dec 14 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-206
- Fix leak with non-matching named captures (bug #767597)

* Tue Nov 29 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-205
- Sub-package ExtUtils::Install
- Sub-package ExtUtils::Manifest
- Do not provide private perl(ExtUtils::MakeMaker::_version)

* Thu Nov 24 2011 Ville Skyttä <ville.skytta@iki.fi> - 4:5.14.2-204
- Add $RPM_LD_FLAGS to lddlflags.

* Wed Nov 23 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-203
- Sub-package Socket

* Mon Nov 21 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-202
- Sub-package Pod::Perldoc

* Fri Nov 18 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-201
- Increase epoch of perl-Module-CoreList to overcome version regression in
  upstream (bug #754641)

* Thu Nov  3 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.2-200
- perl(DBIx::Simple) is not needed in spec requirement in CPANPLUS. It's generated
  automatically.

* Wed Nov 02 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-199
- Provide perl(DB) by perl

* Mon Oct 24 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-198
- Do not warn about missing site directories (bug #732799)

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.2-197
- cleaned spec (thanks to Grigory Batalov)
-  Module-Metadata sub-package contained perl_privlib instead of privlib
-  %%files parent section was repeated twice

* Fri Oct 14 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-196
- Filter false perl(DynaLoader) provide from perl-ExtUtils-MakeMaker
  (bug #736714)
- Change Perl_repeatcpy() prototype to allow repeat count above 2^31
  (bug #720610)
- Do not own site directories located in /usr/local (bug #732799)

* Tue Oct 04 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-195
- Fix CVE-2011-3597 (code injection in Digest) (bug #743010)
- Sub-package Digest and thus Digest::MD5 module (bug #743247)

* Tue Oct 04 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.2-194
- add provide for perl(:MODULE_COMPAT_5.14.2)

* Mon Oct 03 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-193
- 5.14.2 bump (see
  https://metacpan.org/module/FLORA/perl-5.14.2/pod/perldelta.pod for release
  notes).
- Fixes panics when processing regular expression with \b class and /aa
  modifier (bug #731062)
- Fixes CVE-2011-2728 (File::Glob bsd_glob() crash with certain glob flags)
  (bug #742987)

* Mon Oct 03 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-192
- Enable GDBM support again to build against new gdbm 1.9.1

* Fri Sep 30 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-191
- Disable NDBM support temporarily too as it's provided by gdbm package

* Wed Sep 21 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-190
- Disable GDBM support temporarily to build new GDBM

* Thu Sep 15 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-189
- Correct perl-CGI list of Provides
- Make tests optional
- Correct perl-ExtUtils-ParseXS Provides
- Correct perl-Locale-Codes Provides
- Correct perl-Module-CoreList version
- Automate perl-Test-Simple-tests Requires version

* Tue Sep 13 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-188
- Make gdbm support optional to bootstrap with new gdbm
- Split Carp into standalone sub-package to dual-live with newer versions
  (bug #736768)

* Tue Aug 30 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-187
- Split Locale::Codes into standalone sub-package to dual-live with newer
  versions (bug #717863)

* Sun Aug 14 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-186
- perl needs to own vendorarch/auto directory

* Fri Aug 05 2011 Petr Sabata <contyk@redhat.com> - 4:5.14.1-185
- Move xsubpp to ExtUtils::ParseXS (#728393)

* Fri Jul 29 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-184
- fix Compress-Raw-Bzip2 pacakging
- ensure that we never bundle bzip2 or zlib

* Tue Jul 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-183
- remove from provides MODULE_COMPAT 5.12.*

* Fri Jul 22 2011 Paul Howarth <paul@city-fan.org> - 4:5.14.1-182
- Have perl-Module-Build explicitly require perl(CPAN::Meta) >= 2.110420,
  needed for creation of MYMETA files by Build.PL; the dual-life version of
  the package already has this dependency

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 4:5.14.1-181
- Temporarily provide 5.12.* MODULE_COMPAT

* Sat Jul 16 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-180
- fix escaping of the __provides_exclude_from macro

* Wed Jul 13 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-179
- Parse-CPAN-Meta explicitly requires CPAN::Meta::YAML and JSON::PP
- Exclude CPAN::Meta* from CPAN sub-package
- Don't try to normalize CPAN-Meta, JSON-PP, and Parse-CPAN-Meta versions;
  their dual-life packages aren't and have much higher numbers already

* Mon Jun 27 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-178
- update macros -> add %%perl_bootstrap 1 and example for readability
- add into Module::Build dependency on perl-devel (contains macros.perl)
- create new sub-package macros, because we need macros in minimal buildroot

* Thu Jun 23 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-175
- remove from macros BSD, because there exists BSD::Resources

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-174
- remove old MODULE_COMPATs

* Mon Jun 20 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-173
- move ptargrep to Archive-Tar sub-package
- fix version numbers in last two changelog entries

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 4:5.14.1-172
- add provide for perl(:MODULE_COMPAT_5.14.1)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-171
- update to 5.14.1 - no new modules, just serious bugfixes and doc
- switch off fork test, which is failing only on koji

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-170
- try to update to latest ExtUtils::MakeMaker, no luck -> rebuild with current 
  version, fix bug RT#67618 in modules

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-169
- filter even Mac:: requires, polish filter again for correct installation
- add sub-package Compress-Raw-Bzip2, solve Bzip2 conflicts after install
- and add IO::Uncompress::Bunzip2 correctly into IO-Compress

* Mon Jun 13 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-167
- Perl 5.14 mass rebuild, bump release, remove releases in subpackages

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-165
- Perl 5.14 mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-163
- Perl 5.14 mass rebuild

* Thu Jun  9 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-162
- add new sub-packages, remove BR in them

* Wed Jun  1 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-161
- arm can't do parallel builds
- add require EE::MM into IPC::Cmd 711486

* Mon May 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-161
- test build of released 5.14.0
- remove Class::ISA from sub-packages
- patches 8+ are part of new release
- remove vendorarch/auto/Compress/Zlib

* Wed Apr 13 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-160
- add provides UNIVERSAL and DB back into perl

* Thu Apr 07 2011 Petr Pisar <ppisar@redhat.com> - 4:5.12.3-159
- Remove rpath-make patch because we use --enable-new-dtags linker option

* Fri Apr  1 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-158
- 692900 - lc launders tainted flag, RT #87336

* Fri Apr  1 2011 Robin Lee <cheeselee@fedoraproject.org> - 4:5.12.3-157
- Cwd.so go to the PathTools sub-package

* Tue Mar 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-156
- sub-package Path-Tools

* Sat Feb 19 2011 Iain Arnell <iarnell@gmail.com> 4:5.12.3-154
- sub-package Scalar-List-Utils

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.12.3-153
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Petr Pisar <ppisar@redhat.com> - 4:5.12.3-152
- Document ExtUtils::ParseXS upgrade in local patch tracking

* Wed Jan 26 2011 Tom Callaway <spot@fedoraproject.org> - 4:5.12.3-151
- update ExtUtils::ParseXS to 2.2206 (current) to fix Wx build

* Wed Jan 26 2011 Petr Pisar <ppisar@redhat.com> - 4:5.12.3-150
- Make %%global perl_default_filter lazy
- Do not hard-code tapsetdir path

* Tue Jan 25 2011 Lukas Berk <lberk@redhat.com> - 4:5.12.3-149
- added systemtap tapset to make use of systemtap-sdt-devel
- added an example systemtap script

* Mon Jan 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-148
- stable update 5.12.3
- add COMPAT

* Thu Dec  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-146
- 463773 revert change. txt files are needed for example by UCD::Unicode,
 PDF::API2,...

* Thu Dec  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-145
- required systemtap-sdt-devel on request in 661553

* Mon Nov 29 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-144
- create sub-package for CGI 3.49

* Tue Nov 09 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-143
- Sub-package perl-Class-ISA (bug #651317)

* Mon Nov 08 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-142
- Make perl(ExtUtils::ParseXS) version 4 digits long (bug #650882)

* Tue Oct 19 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-141
- 643447 fix redefinition of constant C in h2ph (visible in git send mail,
  XML::Twig test suite)
- remove ifdef for s390

* Thu Oct 07 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-140
- Package Test-Simple tests to dual-live with standalone package (bug #640752)
 
* Wed Oct  6 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-139
- remove removal of NDBM

* Tue Oct 05 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-138
- Consolidate Requires filtering
- Consolidate libperl.so* Provides

* Fri Oct  1 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-137
- filter useless requires, provide libperl.so

* Fri Oct 01 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-136
- Reformat perl-threads description
- Fix threads directories ownership

* Thu Sep 30 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-135
- sub-package threads

* Thu Sep 23 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-134
- add vendor path, clean paths in Configure in spec file
- create sub-package threads-shared

* Tue Sep  7 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-133
- Do not leak when destroying thread (RT #77352, RHBZ #630667)

* Tue Sep  7 2010 Petr Sabata <psabata@redhat.com> - 5:5.12.2-132
- Fixing release number for modules

* Tue Sep  7 2010 Petr Sabata <psabata@redhat.com> - 4:5.12.2-1
- Update to 5.12.2
- Removed one hardcoded occurence of perl version in build process
- Added correct path to dtrace binary
- BuildRequires: systemtap-sdt-devel

* Tue Sep  7 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-131
- run Configure with -Dusedtrace for systemtap support

* Wed Aug 18 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.1-130
- Run tests in parallel
- Add "-Wl,--enable-new-dtags" to linker to allow to override perl's rpath by
  LD_LIBRARY_PATH used in tests. Otherwise tested perl would link to old
  in-system libperl.so.
- Normalize spec file indentation

* Mon Jul 26 2010  Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-129
- 617956 move perlxs* docs files into perl-devel

* Thu Jul 15 2010  Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-128
- 614662 wrong perl-suidperl version in obsolete

* Sun Jul 11 2010 Dan Horák <dan[at]danny.cz> - 4:5.12.1-127
- add temporary compat provides needed on s390(x)

* Fri Jul 09 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.1-126
- Add Digest::SHA requirement to perl-CPAN and perl-CPANPLUS (bug #612563)

* Thu Jul  8 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-125
- 607505 add another dir into Module::Build (thanks to Paul Howarth)

* Mon Jun 28 2010 Ralf Corsépius <corsepiu@fedoraproject.org> -  4:5.12.1-124
- Address perl-Compress-Raw directory ownership (BZ 607881).

* Thu Jun 10 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-123
- remove patch with debugging symbols, which should be now ok without it
- update to 5.12.1
- MODULE_COMPAT

* Tue Apr 27 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-122
- packages in buildroot needs MODULE_COMPAT 5.10.1, add it back for rebuild

* Sun Apr 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-121
- rebuild with tests in test buildroot

* Fri Apr 23 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-120-test
- MODULE_COMPAT 5.12.0
- remove BR man
- clean configure
- fix provides/requires in IO-Compress

* Wed Apr 14 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-119.1
- rebuild 5.12.0 without MODULE_COMPAT

* Wed Apr 14 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-119
- initial 5.12.0 build

* Tue Apr  6 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-118
- 463773 remove useless txt files from installation
- 575842 remove PERL_USE_SAFE_PUTENV, use perl putenv

* Tue Mar 16 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-117
- package tests in their own subpackage

* Mon Mar 15 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-116
- add noarch into correct sub-packages
- move Provides/Obsoletes into correct modules from main perl

* Thu Mar 11 2010 Paul Howarth <paul@city-fan.org> - 4:5.10.1-115
- restore missing version macros for Compress::Raw::Zlib, IO::Compress::Base
  and IO::Compress::Zlib

* Thu Mar 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-114
- clean spec a little more
- rebuild with new gdbm

* Fri Mar  5 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-112
- fix license according to advice from legal
- clean unused patches

* Wed Feb 24 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-111
- update subpackage tests macros to handle packages with an epoch properly

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-110
- add initial EXPERIMENTAL tests subpackage rpm macros to macros.perl

* Tue Dec 22 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-109
- 547656 CVE-2009-3626 perl: regexp matcher crash on invalid UTF-8 characters  
- 549306 version::Internals should be packaged in perl-version subpackage
- Parse-CPAN-Meta updated and separate package is dead

* Mon Dec 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-107
- subpackage parent and Parse-CPAN-Meta; add them to core's dep list

* Fri Dec 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 4:5.10.1-106
- exclude "parent".

* Fri Dec 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 4:5.10.1-105
- exclude Parse-CPAN-Meta.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-104
- do not pack Bzip2 manpages either (#544582)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-103
- do not pack Bzip2 modules (#544582)
- hack: cheat about Compress::Raw::Zlib version (#544582)

* Thu Dec  3 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-102
- switch off check for ppc64 and s390x
- remove the hack for "make test," it is no longer needed

* Thu Dec  3 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-101
- be more careful with the libperl.so compatibility symlink (#543936)

* Wed Dec  2 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-100
- new upstream version
- release number must be high, because of stale version numbers of some
  of the subpackages
- drop upstreamed patches
- update the versions of bundled modules
- shorten the paths in @INC
- build without DEBUGGING
- implement compatibility measures for the above two changes, for a short
  transition period
- provide perl(:MODULE_COMPAT_5.10.0), for that transition period only

* Tue Dec  1 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-87
- fix patch-update-Compress-Raw-Zlib.patch (did not patch Zlib.pm)
- update Compress::Raw::Zlib to 2.023
- update IO::Compress::Base, and IO::Compress::Zlib to 2.015 (#542645)

* Mon Nov 30 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-86
- 542645 update IO-Compress-Base

* Tue Nov 24 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-85
- back out perl-5.10.0-spamassassin.patch (#528572)

* Thu Oct 01 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-84
- add /perl(UNIVERSAL)/d; /perl(DB)/d to perl_default_filter auto-provides
  filtering

* Thu Oct  1 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-83
- update Storable to 2.21

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-82
- update our Test-Simple update to 0.92 (patch by Iain Arnell), #519417
- update Module-Pluggable to 3.9

* Thu Aug 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-81
- fix macros.perl *sigh*

* Mon Aug 24 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-80
- Remove -DDEBUGGING=-g, we are not ready yet.

* Fri Aug 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-79
- add helper filtering macros to -devel, for perl-* package invocation
  (#502402)

* Fri Jul 31 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-78
- Add configure option -DDEBUGGING=-g (#156113)

* Tue Jul 28 2009 arcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-77
- 510127 spam assassin suffer from tainted bug

* Mon Jul 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-76
- 494773 much better swap logic to support reentrancy and fix assert failure (rt #60508)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.10.0-75
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-74
- fix generated .ph files so that they no longer cause warnings (#509676)
- remove PREREQ_FATAL from Makefile.PL's processed by miniperl
- update to latest Scalar-List-Utils (#507378)
- perl-skip-prereq.patch: skip more prereq declarations in Makefile.PL files

* Tue Jul  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-73
- re-enable tests

* Tue Jul  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-72
- move -DPERL_USE_SAFE_PUTENV to ccflags (#508496)

* Mon Jun  8 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-71
- #504386 update of Compress::Raw::Zlib 2.020

* Thu Jun  4 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-70
- update File::Spec (PathTools) to 3.30

* Wed Jun  3 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-69
- fix #221113, $! wrongly set when EOF is reached

* Fri Apr 10 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-68
- do not use quotes in patchlevel.h; it breaks installation from cpan (#495183)

* Tue Apr  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-67
- update CGI to 3.43, dropping upstreamed perl-CGI-escape.patch

* Tue Apr  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-66
- fix CGI::escape for all strings (#472571)
- perl-CGI-t-util-58.patch: Do not distort lib/CGI/t/util-58.t
  http://rt.perl.org/rt3/Ticket/Display.html?id=64502

* Fri Mar 27 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-65
- Move the gargantuan Changes* collection to -devel (#492605)

* Tue Mar 24 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-64
- update module autodie

* Mon Mar 23 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-63
- update Digest::SHA (fixes 489221)

* Wed Mar 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-62
- drop 26_fix_pod2man_upgrade (don't need it)
- fix typo in %%define ExtUtils_CBuilder_version

* Wed Mar 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-61
- apply Change 34507: Fix memory leak in single-char character class optimization
- Reorder @INC, based on b9ba2fadb18b54e35e5de54f945111a56cbcb249
- fix Archive::Extract to fix test failure caused by tar >= 1.21
- Merge useful Debian patches

* Tue Mar 10 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-60
- remove compatibility obsolete sitelib directories
- use a better BuildRoot
- drop a redundant mkdir in %%install
- call patchlevel.h only once; rm patchlevel.bak
- update modules Sys::Syslog, Module::Load::Conditional, Module::CoreList,
  Test::Harness, Test::Simple, CGI.pm (dropping the upstreamed patch),
  File::Path (that includes our perl-5.10.0-CVE-2008-2827.patch),
  constant, Pod::Simple, Archive::Tar, Archive::Extract, File::Fetch,
  File::Temp, IPC::Cmd, Time::HiRes, Module::Build, ExtUtils::CBuilder
- standardize the patches for updating embedded modules
- work around a bug in Module::Build tests bu setting TMPDIR to a directory
  inside the source tree

* Sun Mar 08 2009 Robert Scheck <robert@fedoraproject.org> - 4:5.10.0-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-58
- add /usr/lib/perl5/site_perl to otherlibs (bz 484053)

* Mon Feb 16 2009 Dennis Gilmore <dennis@ausil.us> - 4:5.10.0-57
- build sparc64 without _smp_mflags

* Sat Feb 07 2009 Dennis Gilmore <dennis@ausil.us> - 4:5.10.0-56
- limit sparc builds to -j12

* Tue Feb  3 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-55
- update IPC::Cmd to v 0.42

* Mon Jan 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-54
- 455410 http://rt.perl.org/rt3/Public/Bug/Display.html?id=54934
  Attempt to free unreferenced scalar fiddling with the symbol table
  Keep the refcount of the globs generated by PerlIO::via balanced.

* Mon Dec 22 2008 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-53
- add missing XHTML.pm into Pod::Simple

* Fri Dec 12 2008 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-52
- 295021 CVE-2007-4829 perl-Archive-Tar directory traversal flaws
- add another source for binary files, which test untaring links

* Fri Nov 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-51
- to fix Fedora bz 473223, which is really perl bug #54186 (http://rt.perl.org/rt3//Public/Bug/Display.html?id=54186)
  we apply Changes 33640, 33881, 33896, 33897

* Mon Nov 24 2008 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-50
- change summary according to RFC fix summary discussion at fedora-devel :)

* Thu Oct 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-49
- update File::Temp to 0.20

* Sun Oct 12 2008 Lubomir Rintel <lkundrak@v3.sk> - 4:5.10.0-48
- Include fix for rt#52740 to fix a crash when using Devel::Symdump and
  Compress::Zlib together

* Tue Oct 07 2008 Marcela Mašláňová <mmaslano@redhat.com> 4:5.10.0-47.fc10
- rt#33242, rhbz#459918. Segfault after reblessing objects in Storable.
- rhbz#465728 upgrade Simple::Pod to 3.07

* Wed Oct  1 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-46
- also preserve the timestamp of AUTHORS; move the fix to the recode
  function, which is where the stamps go wrong

* Wed Oct  1 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-45
- give Changes*.gz the same datetime to avoid multilib conflict

* Wed Sep 17 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-44.fc10
- remove Tar.pm from Archive-Extract
- fix version of Test::Simple in spec
- update Test::Simple
- update Archive::Tar to 1.38

* Tue Sep 16 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-43.fc10
- 462444 update Test::Simple to 0.80

* Thu Aug 14 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-42.fc10
- move libnet to the right directory, along Net/Config.pm

* Wed Aug 13 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-41.fc10
- do not create directory .../%%{version}/auto

* Tue Aug  5 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-40.fc10
- 457867 remove required IPC::Run from CPANPLUS - needed only by win32
- 457771 add path

* Fri Aug  1 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-39.fc10
- CGI.pm bug in exists() on tied param hash (#457085)
- move the enc2xs templates (../Encode/*.e2x) to -devel, (#456534)

* Mon Jul 21 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-38
- 455933 update to CGI-3.38
- fix fuzz problems (patch6)
- 217833 pos() function handle unicode characters correct

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-36
- rebuild for new db4 4.7

* Wed Jul  9 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-35
- remove db4 require, it is handled automatically

* Thu Jul  3 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-34
- 453646 use -DPERL_USE_SAFE_PUTENV. Without fail some modules f.e. readline.

* Tue Jul  1 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-33
- 451078 update Test::Harness to 3.12 for more testing. Removed verbose 
test, new Test::Harness has possibly verbose output, but updated package
has a lot of features f.e. TAP::Harness. Carefully watched all new bugs 
related to tests!

* Fri Jun 27 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-32
- bump the release number, so that it is not smaller than in F-9

* Tue Jun 24 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-28
- CVE-2008-2827 perl: insecure use of chmod in rmtree

* Wed Jun 11 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-27
- 447371 wrong access permission rt49003

* Tue Jun 10 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-26
- make config parameter list consistent for 32bit and 64bit platforms,
  add config option -Dinc_version_list=none (#448735)
- use perl_archname consistently
- cleanup of usage of *_lib macros in %%install

* Fri Jun  6 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-25
- 449577 rebuild for FTBFS

* Mon May 26 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-24
- 448392 upstream fix for assertion

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-23
- sparc64 breaks with the rpath hack patch applied

* Mon May 19 2008 Marcela Maslanova <mmaslano@redhat.com>
- 447142 upgrade CGI to 3.37 (this actually happened in -21 in rawhide.)

* Sat May 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-21
- sparc64 fails two tests under mysterious circumstances. we need to get the
  rest of the tree moving, so we temporarily disable the tests on that arch.

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-20
- create the vendor_perl/%%{perl_version}/%%{perl_archname}/auto directory 
  in %%{_libdir} so we own it properly

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-19
- fix CPANPLUS-Dist-Build Provides/Obsoletes (bz 437615)
- bump version on Module-CoreList subpackage

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-18
- forgot to create the auto directory for multilib vendor_perl dirs

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-17
- own multilib vendor_perl directories
- mark Module::CoreList patch in patchlevel.h

* Tue Mar 18 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-16
- 437817: RFE: Upgrade Module::CoreList to 2.14

* Wed Mar 12 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-15
- xsubpp now lives in perl-devel instead of perl.

* Sat Mar  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-14
- back out Archive::Extract patch, causing odd test failure

* Sat Mar  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-13
- add missing lzma test file

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-12
- conditionalize multilib patch report in patchlevel.h
- Update Archive::Extract to 0.26
- Update Module::Load::Conditional to 0.24

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-11
- only do it once, and do it for all our patches

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-10
- note 32891 in patchlevel.h

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-9
- get rid of bad conflicts on perl-File-Temp

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-8
- use /usr/local for sitelib/sitearch dirs
- patch 32891 for significant performance improvement

* Fri Feb 22 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-7
- Add perl-File-Temp provides/obsoletes/conflicts (#433836),
  reported by Bill McGonigle <bill@bfccomputing.com>
- escape the macros in Jan 30 entry

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4:5.10.0-6
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-5
- disable some futime tests in t/io/fs.t because they started failing on x86_64
  in the Fedora builders, and no one can figure out why. :/

* Wed Jan 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-4
- create %%{_prefix}/lib/perl5/vendor_perl/%%{perl_version}/auto and own it
  in base perl (resolves bugzilla 214580)

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-3
- Update Sys::Syslog to 0.24, to fix test failures

* Wed Jan 9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-2
- add some BR for tests

* Tue Jan 8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-1
- 5.10.0 final
- clear out all the unnecessary patches (down to 8 patches!)
- get rid of super perl debugging mode
- add new subpackages

* Thu Nov 29 2007 Robin Norwood <rnorwood@redhat.com> - 4:5.10.0_RC2-0.1
- first attempt at building 5.10.0


