%define debug_package %{nil}
%define __jar_repack  %{nil}
%define wildfly_home  /opt/wildfly

Name:           keycloak
Version:        13.0.1
Release:        1%{?dist}
Summary:        Keycloak is an open source identity and access management solution.

Group:          System Environment/Base
License:        APLv2.0
URL:            http://www.keycloak.org/
Source0:        https://github.com/keycloak/keycloak/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        keycloak.service
Source2:        keycloak.sysconfig
Source3:        LICENSE

BuildRequires: systemd tar gzip

Requires(pre): shadow-utils
Requires:      systemd
Requires:      java-headless

%description
Keycloak is an open source Identity and Access Management solution aimed at
modern applications and services. It makes it easy to secure applications and
services with little to no code.

%prep

%build

%install
install -d %{buildroot}%{wildfly_home}/%{name}-%{version}
tar --strip-components=1 -C %{buildroot}%{wildfly_home}/%{name}-%{version} -xvf %{SOURCE0}
ln -sf %{name}-%{version} %{buildroot}%{wildfly_home}/%{name}
install -D %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -D %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
install -D %{SOURCE3} %{buildroot}/%{_docdir}/%{name}/LICENSE
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name} user" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
case "$1" in
  0)
    # This is an uninstallation.
    getent passwd %{name} >/dev/null && userdel %{name}
    getent group %{name} >/dev/null && groupdel %{name}
  ;;
  1)
    # This is an upgrade.
  ;;
esac
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %attr(-, %{name}, %{name}) %{wildfly_home}/%{name}-%{version}
%attr(-, %{name}, %{name}) %{wildfly_home}/%{name}-%{version}/*
%attr(-, %{name}, %{name}) %{wildfly_home}/%{name}
%attr(644, root, root) %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/sysconfig/%{name}
%doc %{_docdir}/%{name}/LICENSE
%dir %attr(-, %{name}, %{name}) %{_sharedstatedir}/%{name}

%changelog
* Thu Jun 3 2021 Shestopalov Ilya <selfidx@gmail.com> - 13.0.1-1
- Creating a SPEC file

