# Sensible Perl-specific RPM build macros.
#
# Note that these depend on the generic filtering system being in place in
# rpm core; but won't cause a build to fail if they're not present.
#
# Chris Weyl <cweyl@alumni.drew.edu> 2009
# Marcela Mašláňová <mmaslano@redhat.com> 2011

# This macro unsets several common vars used to control how Makefile.PL (et
# al) build and install packages.  We also set a couple to help some of the
# common systems be less interactive.  This was blatantly stolen from
# cpanminus, and helps building rpms locally when one makes extensive use of
# local::lib, etc.
#
# Usage, in %build, before "%{__perl} Makefile.PL ..."
#
#   %{?perl_ext_env_unset}

%@scl@perl_ext_env_unset %{expand:
unset PERL_MM_OPT MODULEBUILDRC PERL5INC
export PERL_AUTOINSTALL="--defaultdeps"
export PERL_MM_USE_DEFAULT=1
}

#############################################################################
# Filtering macro incantations

# keep track of what "revision" of the filtering we're at.  Each time we
# change the filter we should increment this.

%@scl@perl_default_filter_revision 3

# Perl provides/requeries are generated by external generators.
%global @scl@__perl_provides /usr/lib/rpm/perl.prov
%global @scl@__perl_requires /usr/lib/rpm/perl.req

# By default, for perl packages we want to filter all files in _docdir from 
# req/prov scanning, as well as filtering out any provides caused by private 
# libs in vendorarch/archlib (vendor/core).
#
# Note that this must be invoked in the spec file, preferably as 
# "%{?perl_default_filter}", before any %description block.

%@scl@perl_default_filter %{expand: \
%global __provides_exclude_from %{perl_vendorarch}/auto/.*\\\\.so$|%{perl_archlib}/.*\\\\.so$|%{_docdir}
%global __requires_exclude_from %{_docdir}
%global __provides_exclude perl\\\\(VMS|perl\\\\(Win32|perl\\\\(DB\\\\)|perl\\\\(UNIVERSAL\\\\)
%global __requires_exclude perl\\\\(VMS|perl\\\\(Win32
}

#############################################################################
# Macros to assist with generating a "-tests" subpackage in a semi-automatic
# manner.
#
# The following macros are still in a highly experimental stage and users
# should be aware that the interface and behaviour may change. 
#
# PLEASE, PLEASE CONDITIONALIZE THESE MACROS IF YOU USE THEM.
#
# See http://gist.github.com/284409

# These macros should be invoked as above, right before the first %description
# section, and conditionalized.  e.g., for the common case where all our tests
# are located under t/, the correct usage is:
#
#   %{?perl_default_subpackage_tests}
#
# If custom files/directories need to be specified, this can be done as such:
#
#   %{?perl_subpackage_tests:%perl_subpackage_tests t/ one/ three.sql}
#
# etc, etc.

%@scl@perl_version   %(eval "`%{__perl} -V:version`"; echo $version)
%@scl@perl_testdir   %{_libexecdir}/perl5-tests
%@scl@cpan_dist_name %(eval echo %{name} | %{__sed} -e 's/^perl-//')

# easily mark something as required by -tests and BR to the main package
%@scl@tests_req() %{expand:\
BuildRequires: %*\
%%@scl@tests_subpackage_requires %*\
}

# fixup (and create if needed) the shbang lines in tests, so they work and
# rpmlint doesn't (correctly) have a fit
%@scl@fix_shbang_line() \
TMPHEAD=`mktemp`\
TMPBODY=`mktemp`\
for file in %* ; do \
    head -1 $file > $TMPHEAD\
    tail -n +2 $file > $TMPBODY\
    %{__perl} -pi -e '$f = /^#!/ ? "" : "#!%{__perl}$/"; $_="$f$_"' $TMPHEAD\
    cat $TMPHEAD $TMPBODY > $file\
done\
%{__perl} -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(qw{%*})"\
%{__rm} $TMPHEAD $TMPBODY\
%{nil}

# additional -tests subpackage requires, if any
%@scl@tests_subpackage_requires() %{expand: \
%global @scl@__tests_spkg_req %{?@scl@__tests_spkg_req} %* \
}

# additional -tests subpackage provides, if any
%@scl@tests_subpackage_provides() %{expand: \
%global @scl@__tests_spkg_prov %{?@scl@__tests_spkg_prov} %* \
}

#
# Runs after the body of %check completes.
#

%@scl@__perl_check_pre %{expand: \
%{?__spec_check_pre} \
pushd %{buildsubdir} \
%define @scl@perl_br_testdir %{buildroot}%{@scl@perl_testdir}/%{@scl@cpan_dist_name} \
%{__mkdir_p} %{@scl@perl_br_testdir} \
%{__tar} -cf - %{__perl_test_dirs} | ( cd %{@scl@perl_br_testdir} && %{__tar} -xf - ) \
find . -maxdepth 1 -type f -name '*META*' -exec %{__cp} -vp {} %{@scl@perl_br_testdir} ';' \
find %{@scl@perl_br_testdir} -type f -exec %{__chmod} -c -x {} ';' \
T_FILES=`find %{@scl@perl_br_testdir} -type f -name '*.t'` \
%@scl@fix_shbang_line $T_FILES \
%{__chmod} +x $T_FILES \
%{_fixperms} %{@scl@perl_br_testdir} \
popd \
}

#
# The actual invoked macro
#

%@scl@perl_subpackage_tests() %{expand: \
%global __perl_package 1\
%global __perl_test_dirs %* \
%global __spec_check_pre %{expand:%{@scl@__perl_check_pre}} \
%package tests\
Summary: Test suite for package %{name}\
Group: Development/Debug\
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}\
Requires: /usr/bin/prove \
%{?@scl@__tests_spkg_req:Requires: %@scl@__tests_spkg_req}\
%{?@scl@__tests_spkg_prov:Provides: %@scl@__tests_spkg_prov}\
AutoReqProv: 0 \
%description tests\
This package provides the test suite for package %{name}.\
%files tests\
%defattr(-,root,root,-)\
%{@scl@perl_testdir}\
}

# shortcut sugar
%@scl@perl_default_subpackage_tests %@scl@perl_subpackage_tests t/

