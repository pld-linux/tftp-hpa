Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(de.UTF-8):	Client für das 'trivial file transfer protocol (TFTP)'
Summary(fr.UTF-8):	Client pour le « trivial file transfer protocol » (TFTP)
Summary(pl.UTF-8):	Klient TFTP (Trivial File Transfer Protocol)
Summary(tr.UTF-8):	İlkel dosya aktarım protokolu (TFTP) için sunucu ve istemci
Name:		tftp-hpa
Version:	5.2
Release:	1
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.kernel.org/pub/software/network/tftp/tftp-hpa/%{name}-%{version}.tar.xz
# Source0-md5:	e86f58164166804e8ae5a46010f29317
Source1:	tftpd-hpa.inetd
Source2:	tftpd-hpa.init
Source3:	tftpd-hpa.sysconfig
URL:		http://freshmeat.net/projects/tftp-hpa/
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Obsoletes:	inetutils-tftp
Obsoletes:	tftp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. This package contains TFTP client.

%description -l de.UTF-8
Das trivial file transfer protocol (TFTP) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -l fr.UTF-8
Le « trivial file transfer protocol » (TFTP) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -l pl.UTF-8
TFTP (Trivial File Transfer Protocol) jest używany głównie do
startowania stacji bezdyskowych z sieci. Pakiet ten zawiera aplikację
TFTP klienta.

%description -l tr.UTF-8
İlkel dosya aktarım protokolu genelde disksiz iş istasyonlarının ağ
üzerinden açılmalarında kullanılır. Güvenlik denetimleri çok az
olduğundan zorunlu kalmadıkça çalıştırılmamalıdır.

%package -n tftpd-hpa-common
Summary:	Daemon for the trivial file transfer protocol (TFTP)
Summary(de.UTF-8):	Dämon für das 'trivial file transfer protocol (TFTP)'
Summary(fr.UTF-8):	Démon pour le « trivial file transfer protocol » (TFTP)
Summary(pl.UTF-8):	Serwer TFTP (Trivial File Transfer Protocol)
Summary(tr.UTF-8):	İlkel dosya aktarım protokolu (TFTP) için sunucu ve istemci
Group:		Networking/Daemons/FTP
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Provides:	group(tftp)
Provides:	user(tftp)

%description -n tftpd-hpa-common
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. The tftp-hpa package provides the user
interface for TFTP, which allows users to transfer files to and from a
remote machine. It provides very little security, and should not be
enabled unless it is needed.

%description -n tftpd-hpa-common -l de.UTF-8
Das trivial file transfer protocol (TFTP) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -n tftpd-hpa-common -l fr.UTF-8
Le « trivial file transfer protocol » (TFTP) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -n tftpd-hpa-common -l pl.UTF-8
TFTP (Trivial File Transfer Protocol) jest używany głównie do
startowania stacji bezdyskowych z sieci. Serwer TFTP powinien być
instalowany tylko wtedy, kiedy zachodzi taka konieczność ponieważ
należy on do aplikacji o niskim poziomie bezpieczeństwa.

%package -n tftpd-hpa-inetd
Summary:	inetd configs for tftpd-hpa
Summary(pl.UTF-8):	Pliki konfiguracyjne do użycia tftpd-hpa poprzez inetd
Group:		Networking/Daemons/FTP
Requires:	tftpd-hpa-common = %{version}-%{release}
Requires:	rc-inetd >= 0.8.1
Provides:	tftpdaemon
Obsoletes:	atftpd
Obsoletes:	inetutils-tftpd
Obsoletes:	tftp-server
Obsoletes:	tftpd
Obsoletes:	tftpd-hpa
Obsoletes:	utftpd

%description -n tftpd-hpa-inetd
tftpd-hpa configs for running from inetd.

%description -n tftpd-hpa-inetd -l pl.UTF-8
Pliki konfiguracyjna tftpd-hpa do startowania demona poprzez inetd.

%package -n tftpd-hpa-standalone
Summary:	Standalone daemon configs for tftpd-hpa
Summary(pl.UTF-8):	Pliki konfiguracyjne do startowania tftpd-hpa w trybie standalone
Group:		Networking/Daemons/FTP
Requires:	tftpd-hpa-common = %{version}-%{release}
Requires:	rc-scripts
Provides:	tftpdaemon
Obsoletes:	atftpd
Obsoletes:	inetutils-tftpd
Obsoletes:	tftp-server
Obsoletes:	tftpd
Obsoletes:	tftpd-hpa
Obsoletes:	utftpd

%description -n tftpd-hpa-standalone
tftpd-hpa configs for running as a standalone daemon.

%description -n tftpd-hpa-standalone -l pl.UTF-8
Pliki konfiguracyjne tftpd-hpa do startowania demona w trybie
standalone.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT{/etc/sysconfig/rc-inetd,/etc/rc.d/init.d} \
	$RPM_BUILD_ROOT/var/lib/tftp

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/tftpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/tftpd-hpa
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/tftpd-hpa

mv -f $RPM_BUILD_ROOT%{_sbindir}/in.tftpd $RPM_BUILD_ROOT%{_sbindir}/tftpd
mv -f $RPM_BUILD_ROOT%{_mandir}/man8/in.tftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/tftpd.8

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n tftpd-hpa-common
%groupadd -P tftpd-hpa -g 59 -r -f tftp
%useradd -P tftpd-hpa -u 15 -r -d /var/lib/tftp -s /bin/false -c "TFTP User" -g tftp tftp

%postun -n tftpd-hpa-common
if [ "$1" = "0" ]; then
	%userremove tftp
	%groupremove tftp
fi

%post -n tftpd-hpa-inetd
%service -q rc-inetd reload

%postun -n tftpd-hpa-inetd
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
fi

%post -n tftpd-hpa-standalone
/sbin/chkconfig --add tftpd-hpa
%service tftpd-hpa restart

%preun -n tftpd-hpa-standalone
if [ "$1" = "0" ]; then
	%service tftpd-hpa stop
	/sbin/chkconfig --del tftpd-hpa
fi

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files -n tftpd-hpa-common
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(750,tftp,root) %dir /var/lib/tftp
%{_mandir}/man8/*

%files -n tftpd-hpa-inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/tftpd

%files -n tftpd-hpa-standalone
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/tftpd-hpa
%attr(754,root,root) /etc/rc.d/init.d/tftpd-hpa
