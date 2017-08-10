%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global	gem_name	json
%global gem_extdir %{gem_extdir_mri}
%{!?gem_extdir: %global gem_extdir %{gem_instdir}/extdir}

Summary: JSON Implementation for Ruby
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.0.2
Release: 2%{?dist}
Group: Development/Languages
License: Ruby
URL: http://flori.github.com/json
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix}ruby(release)
Requires: %{?scl_prefix}ruby(rubygems)
Requires: %{?scl_prefix}ruby
BuildRequires: %{?scl_prefix}rubygems-devel
BuildRequires: %{?scl_prefix}ruby-devel >= 2.0
BuildRequires: %{?scl_prefix}ruby-devel < 3
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
This is a implementation of the JSON specification according
to RFC 4627 in Ruby.
You can think of it as a low fat alternative to XML,
if you want to store data to disk or transmit it over
a network rather than use a verbose markup language.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation

Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}
%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build

# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/lib/%{gem_name}
# this isn't working and I don't know why :-(
# cp -a .%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}/
# cp -a .%{gem_extdir_mri}/%{gem_name}/ext/*.so %{buildroot}%{gem_extdir_mri}/%{gem_name}/ext/
# I installed the json-2.0.2 gem on centos7 and found out where the files are copied,
# then just applied that logic here
# in the build root:
# + find -name '*.so'
# ./usr/share/gems/gems/json-2.0.2/lib/json/ext/generator.so
# ./usr/share/gems/gems/json-2.0.2/lib/json/ext/parser.so
# ./usr/share/gems/gems/json-2.0.2/ext/json/ext/parser/parser.so
# ./usr/share/gems/gems/json-2.0.2/ext/json/ext/generator/generator.so
# on the file system
# %{gem_extdir_mri}/%{gem_name}/lib
#./usr/local/lib64/gems/ruby/json-2.0.2/lib/json/ext/parser.so
#./usr/local/lib64/gems/ruby/json-2.0.2/lib/json/ext/generator.so
# these files are also in the file system, but they don't seem to
# be used, and including them in the rpm caused warnings doing rpmbuild
#./usr/local/share/gems/gems/json-2.0.2/ext/json/ext/parser/parser.so
#./usr/local/share/gems/gems/json-2.0.2/ext/json/ext/generator/generator.so

# move to the location for binaries
mv %{buildroot}%{gem_libdir}/%{gem_name}/ext %{buildroot}%{gem_extdir_mri}/lib/%{gem_name}

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}%{gem_instdir}/ext

find %{buildroot}%{gem_instdir} -name \*.rb -print0 | \
	xargs --null chmod 0644

# We don't need those files anymore.
rm -rf %{buildroot}%{gem_instdir}/ext
rm -rf %{buildroot}%{gem_instdir}/install.rb
rm -rf %{buildroot}%{gem_instdir}/lib/json/ext/.keep
rm -rf %{buildroot}%{gem_docdir}/rdoc/classes/.src
rm -rf %{buildroot}%{gem_docdir}/rdoc/classes/.html

rm -rf %{buildroot}%{gem_instdir}/java/

# remove pure
rm -fr %{buildroot}%{gem_instdir}/lib/json/pure*

%files
%dir %{gem_instdir}
%dir %{gem_libdir}
%dir %{gem_libdir}/%{gem_name}
%{gem_extdir_mri}
%{gem_instdir}/README*
%{gem_instdir}/tools
%{gem_libdir}/%{gem_name}.rb
%{gem_libdir}/%{gem_name}/add
%{gem_libdir}/%{gem_name}/common.rb
%{gem_libdir}/%{gem_name}/ext.rb
%{gem_libdir}/%{gem_name}/version.rb
%{gem_libdir}/%{gem_name}/generic_object.rb
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/.*
%{gem_instdir}/*gemspec
%{gem_instdir}/[A-Z]*
%{gem_instdir}/Rakefile
%{gem_instdir}/data
%{gem_instdir}/diagrams
%{gem_instdir}/references
%{gem_instdir}/tests


%changelog
* Wed Sep 21 2016 Rich Megginson <rmeggins@redhat.com> - 2.0.2-2
- bump rev to rebuild for rhlog
- hand hack shared library paths

* Thu Aug 18 2016 Satoe Imaishi <simaishi@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Thu Sep 10 2015 Satoe Imaishi <simaishi@redhat.com> - 1.8.2-9
- Follow ruby packaging guideline to build/install

* Thu Aug 27 2015 Satoe Imaishi <simaishi@redhat.com> - 1.8.2-8
- Copy .so to extensions directory

* Tue Aug 25 2015 Joe VLcek <jvlcek@redhat.com> - 1.8.2-7
- Fix missing ext/json contents

* Tue Aug 25 2015 Joe VLcek <jvlcek@redhat.com> - 1.8.2-6
- Install so in new location

* Tue Aug 25 2015 Joe VLcek <jvlcek@redhat.com> - 1.8.2-5
- Fixed gem install command.

* Tue Aug 25 2015 Joe VLcek <jvlcek@redhat.com> - 1.8.2-4
- Leave arch dependent files where gem install put them and put them where the SCL expect to find them.

* Fri Aug 21 2015 Satoe Imaishi <simaishi@redhat.com> - 1.8.2-3
- Rebuild for rh-ruby22

* Fri Apr 17 2015 Joe VLcek <jvlcek@redhat.com> - 1.8.2-2
- Leave arch dependent files where gem install put them.

* Wed Dec 10 2014 Joe VLcek <jvlcek@redhat.com> - 1.8.2-1
- Update to version 1.8.2

* Wed Dec 10 2014 Joe VLcek <jvlcek@redhat.com> - 1.8.0-5
- Use gem_extdir_mri macro

* Fri Dec 05 2014 Joe VLcek <jvlcek@redhat.com> - 1.8.0-4
- Remove the rubyabi macro

* Tue Jul 30 2013 John Eckersberg <jeckersb@redhat.com> - 1.8.0-3
- Fix usage of gem_extdir macro

* Fri Jul 26 2013 Steve Linabery <slinaber@redhat.com> - 1.8.0-2
- various scl-related specfile fixes

* Mon Jul 22 2013 Mo Morsi <mmorsi@redhat.com> - 1.8.0-1
- New upstream release
- Updated for rhel

* Tue Mar 26 2013 Josef Stribny <jstribny@redhat.com> - 1.7.7-100
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to JSON 1.7.7

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Xavier Lamien <laxathom@lxtnow.net> - 1.7.5-1
- Update to Upstream release.
- Add mtasaka changes request.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 21 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.6.5-1
- 1.6.5

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.4.6-2
- Rebuilt for gcc bug 634757

* Sat Sep 18 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.6-1
- Update release.
- Enabled test stage.

* Fri Jun 11 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-3
- Move ruby's site_lib editor to ruby-json-gui.

* Mon May 10 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-2
- Move editor out of ruby-json sub-package.

* Sun May 09 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-1
- Update release.
- Split-out json editor.

* Thu Oct 29 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.9-1
- Update release.

* Wed Aug 12 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-3
- Fix gem scripts and install_dir.
- Enable %%check stage.

* Wed Aug 05 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-2
- Rebuild in correct buildir process.
- Add sub packages.

* Mon Aug 03 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-1
- Update release.

* Sat Jun 06 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.6-1
- Update release.

* Tue May 12 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.5-1
- Update release.

* Thu Apr 02 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.4-1
- Update release.

* Sat Jul 12 2008 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.3-1
- Initial RPM release.
