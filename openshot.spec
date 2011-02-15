%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Summary:	GNOME Non-linear video editor 
Name:		openshot
Version:	1.3.0
Release:	1%{?dist}

Group:		Applications/Multimedia
License:	GPLv3
URL:		http://www.openshotvideo.com
Source0:	http://launchpad.net/openshot/1.3/1.3.0/+download/openshot-%{version}.tar.gz
Patch0:		openshot-1.3.0-melt-command.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires:	desktop-file-utils
BuildRequires:	python-devel

Requires:	mlt-python
Requires:	pygoocanvas
Requires:	pyxdg
Requires:	frei0r-plugins

BuildArch:	noarch


%description
OpenShot Video Editor is a free, open-source, non-linear video editor, based on
Python, GTK, and MLT. It can edit video and audio files, composite and 
transition video files, and mix multiple layers of video and audio together and 
render the output in many different formats.


%prep
%setup -q
%patch0 -p1


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT 

# Remove unnecessary file
rm %{buildroot}/usr/lib/mime/packages/openshot

# We strip bad shebangs (/usr/bin/env) instead of fixing them
# since these files are not executable anyways
find %{buildroot}/%{python_sitelib} -name '*.py' \
  -exec grep -q '^#!' '{}' \; -print | while read F
do
  awk '/^#!/ {if (FNR == 1) next;} {print}' $F >chopped
  touch -r $F chopped
  mv chopped $F
done


desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# modify find-lang.sh to deal with gettext .mo files under
# openshot/locale
%{__sed} -e 's|/share/locale/|/%{name}/locale/|' \
 /usr/lib/rpm/find-lang.sh \
 > find-lang-modified.sh

sh find-lang-modified.sh %{buildroot} OpenShot %{name}.lang
find %{buildroot}%{python_sitelib}/%{name}/locale -type d | while read dir
do
 echo "%%dir ${dir#%{buildroot}}" >> %{name}.lang
done


%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :


%postun
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :



%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING AUTHORS 
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/*
%{python_sitelib}/%{name}
%{python_sitelib}/*egg-info
%{_mandir}/man*/* 


%changelog
* Tue Feb 15 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 1.3.0-1
- update to 1.3.0
- update melt patch

* Thu Nov 11 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 1.2.2-3
- really apply melt patch

* Tue Nov  8 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 1.2.2-2
- add R: frei0r-plugins
- fix melt_command

* Mon Sep 27 2010 Jonathan Haskins <jhaskins@killobyte.com> - 1.2.2-1
- Release 1.2.2

* Thu Apr 29 2010 Jonathan Haskins <jhaskins@killobyte.com> - 1.1.3-2
- Add pyxdg as dependency

* Thu Apr 15 2010 Jonathan Haskins <jhaskins@killobyte.com> - 1.1.3-1
- Release 1.1.3

* Sat Mar 17 2010 Jonathan Haskins <jhaskins@killobyte.com> - 1.1.1-1
- Release 1.1.1

* Sat Mar 13 2010 Jonathan Haskins <jhaskins@killobyte.com> - 1.1.0-1
- Release 1.1.0

* Tue Jan 12 2010 Zarko <zarko.pintar@gmail.com> - 1.0.0-1
- Release 1.0.0

* Thu Dec 04 2009 Zarko <zarko.pintar@gmail.com> - 0.9.54-1
- initial release
