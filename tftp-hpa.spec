Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(de):	Client f�r das 'trivial file transfer protocol (TFTP)'
Summary(fr):	Client pour le � trivial file transfer protocol � (TFTP)
Summary(pl):	Klient TFTP (Trivial File Transfer Protocol)
Summary(tr):	�lkel dosya aktar�m protokolu (TFTP) i�in sunucu ve istemci
Name:		tftp-hpa
Version:	0.40
Release:	1
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.kernel.org/pub/software/network/tftp/%{name}-%{version}.tar.bz2
# Source0-md5:	bfcdd49bf94900e610f2cc937d8980ef
Source1:	tftpd-hpa.inetd
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.159
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
Le � trivial file transfer protocol � (TFTP) est normalement utilis�
uniquement pour d�marrer les stations de travail sans disque. Il offre
tr�s peu de s�curit� et ne devrait pas �tre activ� sauf si c'est
n�cessaire.

%description -l pl
TFTP (Trivial File Transfer Protocol) jest u�ywany g��wnie do
startowania stacji bezdyskowych z sieci. Pakiet ten zawiera aplikacj�
TFTP klienta.

%description -l tr
�lkel dosya aktar�m protokolu genelde disksiz i� istasyonlar�n�n a�
�zerinden a��lmalar�nda kullan�l�r. G�venlik denetimleri �ok az
oldu�undan zorunlu kalmad�k�a �al��t�r�lmamal�d�r.

%package -n tftpd-hpa
Summary:	Daemon for the trivial file transfer protocol (TFTP)
Summary(de):	D�mon f�r das 'trivial file transfer protocol (TFTP)'
Summary(fr):	D�mon pour le � trivial file transfer protocol � (TFTP)
Summary(pl):	Serwer TFTP (Trivial File Transfer Protocol)
Summary(tr):	�lkel dosya aktar�m protokolu (TFTP) i�in sunucu ve istemci
Group:		Networking/Daemons
PreReq:		rc-inetd >= 0.8.1
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires:	inetdaemon
Provides:	group(tftp)
Provides:	tftpdaemon
Provides:	user(tftp)
Obsoletes:	atftpd
Obsoletes:	inetutils-tftpd
Obsoletes:	tftpd
Obsoletes:	tftp-server
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
Le � trivial file transfer protocol � (TFTP) est normalement utilis�
uniquement pour d�marrer les stations de travail sans disque. Il offre
tr�s peu de s�curit� et ne devrait pas �tre activ� sauf si c'est
n�cessaire.

%description -n tftpd-hpa -l pl
TFTP (Trivial File Transfer Protocol) jest u�ywany g��wnie do
startowania stacji bezdyskowych z sieci. Serwer TFTP powinien by�
instalowany tylko wtedy, kiedy zachodzi taka konieczno�� poniewa�
nale�y on do aplikacji o niskim poziomie bezpiecze�stwa.

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

if [ -n "`getgid tftp`" ]; then
	if [ "`getgid tftp`" != "59" ]; then
		echo "Error: group tftp doesn't have gid=59. Correct this before installing tftp-hpa." 1>&2
		exit 1
	fi
else
	echo "Adding group tftp GID=59."
	/usr/sbin/groupadd -g 59 -r -f tftp
fi

if [ -n "`id -u tftp 2>/dev/null`" ]; then
	if [ "`id -u tftp`" != "15" ]; then
		echo "Error: user tftp doesn't have uid=15. Correct this before installing tftpd." 1>&2
		exit 1
	fi
else
	echo "Adding user tftp UID=15."
	/usr/sbin/useradd -u 15 -r -d /var/lib/tftp -s /bin/false -c "TFTP User" -g tftp tftp 1>&2
fi

%post -n tftpd-hpa
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server." 1>&2
fi

%postun -n tftpd-hpa
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi
if [ "$1" = "0" ]; then
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
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/tftpd
%attr(750,tftp,root) %dir /var/lib/tftp
%{_mandir}/man8/*
