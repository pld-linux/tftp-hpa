Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(de):	Client für das 'trivial file transfer protocol (TFTP)'
Summary(fr):	Client pour le « trivial file transfer protocol » (TFTP)
Summary(pl):	Klient TFTP (Trivial File Transfer Protocol)
Summary(tr):	Ýlkel dosya aktarým protokolu (TFTP) için sunucu ve istemci
Name:		tftp-hpa
Version:	0.41
Release:	1
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.kernel.org/pub/software/network/tftp/%{name}-%{version}.tar.bz2
# Source0-md5:	db286f988b040ba3e2e83e5df9f8ef38
Source1:	tftpd-hpa.inetd
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Obsoletes:	inetutils-tftp
Obsoletes:	tftp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. This package contains TFTP client.

%description -l de
Das trivial file transfer protocol (TFTP) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -l fr
Le « trivial file transfer protocol » (TFTP) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -l pl
TFTP (Trivial File Transfer Protocol) jest u¿ywany g³ównie do
startowania stacji bezdyskowych z sieci. Pakiet ten zawiera aplikacjê
TFTP klienta.

%description -l tr
Ýlkel dosya aktarým protokolu genelde disksiz iþ istasyonlarýnýn að
üzerinden açýlmalarýnda kullanýlýr. Güvenlik denetimleri çok az
olduðundan zorunlu kalmadýkça çalýþtýrýlmamalýdýr.

%package -n tftpd-hpa
Summary:	Daemon for the trivial file transfer protocol (TFTP)
Summary(de):	Dämon für das 'trivial file transfer protocol (TFTP)'
Summary(fr):	Démon pour le « trivial file transfer protocol » (TFTP)
Summary(pl):	Serwer TFTP (Trivial File Transfer Protocol)
Summary(tr):	Ýlkel dosya aktarým protokolu (TFTP) için sunucu ve istemci
Group:		Networking/Daemons
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	inetdaemon
Requires:	rc-inetd >= 0.8.1
Provides:	group(tftp)
Provides:	tftpdaemon
Provides:	user(tftp)
Obsoletes:	atftpd
Obsoletes:	inetutils-tftpd
Obsoletes:	tftp-server
Obsoletes:	tftpd
Obsoletes:	utftpd

%description -n tftpd-hpa
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. The tftp-hpa package provides the user
interface for TFTP, which allows users to transfer files to and from a
remote machine. It provides very little security, and should not be
enabled unless it is needed.

%description -n tftpd-hpa -l de
Das trivial file transfer protocol (TFTP) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -n tftpd-hpa -l fr
Le « trivial file transfer protocol » (TFTP) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -n tftpd-hpa -l pl
TFTP (Trivial File Transfer Protocol) jest u¿ywany g³ównie do
startowania stacji bezdyskowych z sieci. Serwer TFTP powinien byæ
instalowany tylko wtedy, kiedy zachodzi taka konieczno¶æ poniewa¿
nale¿y on do aplikacji o niskim poziomie bezpieczeñstwa.

%prep
%setup -q

mv -f aclocal.m4 acinclude.m4

%build
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},/etc/sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT{%{_mandir}/man{1,8},/var/lib/tftp}

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/tftpd

mv -f $RPM_BUILD_ROOT%{_sbindir}/in.tftpd $RPM_BUILD_ROOT%{_sbindir}/tftpd
mv -f $RPM_BUILD_ROOT%{_mandir}/man8/in.tftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/tftpd.8

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n tftpd-hpa
%groupadd -P tftpd-hpa -g 59 -r -f tftp
%useradd -P tftpd-hpa -u 15 -r -d /var/lib/tftp -s /bin/false -c "TFTP User" -g tftp tftp

%post -n tftpd-hpa
%service -q rc-inetd reload

%postun -n tftpd-hpa
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
	%userremove tftp
	%groupremove tftp
fi

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files -n tftpd-hpa
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/tftpd
%attr(750,tftp,root) %dir /var/lib/tftp
%{_mandir}/man8/*
