# Define backup go macros
%if %{rhel} == 8
%global gopkg %package -n %{goname}-devel \
Summary:	%{summary} \
BuildArch:  noarch \
%description -n %{goname}-devel \
%{common_description}
%global generate_buildrequires echo "Need more specific macro on rhel8"
# Specific BuildRequires macro
%global go_generate_buildrequires BuildRequires:	%{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang} golang-github-farsightsec-framestream-devel golang-github-miekg-dns-devel
%endif

%global debug_package %{nil}
# https://github.com/dnstap/golang-dnstap
%global goipath         github.com/dnstap/golang-dnstap
%global common_description %{expand:
Implements an encoding format for DNS server events.}

%global golicences      LICENSE
%global godocs          README

Version:        0.4.0
Release:        1%{?dist}
Summary:        DNS server event encoding format
%gometa
Name:           golang-dnstap
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}

%description
%{common_description}

%go_generate_buildrequires

%gopkg

%prep
%setup -q
%autopatch -p1

%install
for file in $(find . -iname "*.go" \! -iname "*_test.go" \! -iname "main.go" ) ; do
    echo "%%dir %%{gopath}/src/%%{goipath}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{goipath}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{goipath}/$file
    echo "%%{gopath}/src/%%{goipath}/$file" >> devel.file-list
done
sort -u -o devel.file-list devel.file-list

%if %{with check}
%check
%gocheck
%endif

%files devel -f devel.file-list

%changelog
