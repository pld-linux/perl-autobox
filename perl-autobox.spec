#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	autobox
Summary:	autobox - call methods on native types
Summary(pl.UTF-8):	autobox - wywoływanie metod na rodzimych typach
Name:		perl-autobox
Version:	2.70
Release:	2
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://search.cpan.org/CPAN/authors/id/C/CH/CHOCOLATE/autobox-%{version}.tar.gz
# Source0-md5:	2399312bfffbf91e8fdce306f0357e86
URL:		http://search.cpan.org/dist/autobox/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Scope-Guard >= 0.03
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The autobox pragma allows methods to be called on integers, floats,
strings, arrays, hashes, and code references in exactly the same
manner as blessed references.

The autoboxing is transparent: boxed values are not blessed into their
(user-defined) implementation class (unless the method elects to
bestow such a blessing) - they simply use its methods as though they
are.

The classes (packages) into which the native types are boxed are fully
configurable. By default, a method invoked on a non-object is assumed
to be defined in a class whose name corresponds to the ref() type of
that value - or SCALAR if the value is a non-reference.

This mapping can be overriden by passing key/value pairs to the use
autobox statement, in which the keys represent native types, and the
values their associated classes.

As with regular objects, autoboxed values are passed as the first
argument of the specified method. Consequently, given a vanilla use
autobox:

# %description -l pl.UTF-8
# TODO

%prep
%setup -q -n %{pdir}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorarch}/autobox.pm
%dir %{perl_vendorarch}/autobox
%{perl_vendorarch}/autobox/*.pm
%dir %{perl_vendorarch}/auto/autobox
%{perl_vendorarch}/auto/autobox//*.bs
%attr(755,root,root) %{perl_vendorarch}/auto/autobox//*.so
%{_mandir}/man3/*
