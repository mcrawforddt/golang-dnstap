%global debug_package %{nil}

# https://github.com/dnstap/golang-dnstap
%global goipath         github.com/dnstap/golang-dnstap
Version:                0.4.0

%gometa

%global common_description %{expand:
Implements an encoding format for DNS server events.}

%global golicences      LICENSE
%global godocs          README

Name:           golang-dnstap
Release:        1%{?dist}
Summary:        DNS server event encoding format

License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang-github-farsightsec-framestream-devel golang-github-miekg-dns-devel

%description
%{common_description}

%package -n %{goname}-devel
Summary:	%{summary}
BuildArch:  noarch
%description -n %{goname}-devel
%{common_description}

%prep
%setup -q
%autopatch -p1

%install
find .
for file in $(find . -iname "*.go" \! -iname "*_test.go" \! -iname "main.go" ) ; do
    echo "%%dir %%{gopath}/src/%%{goipath}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{goipath}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{goipath}/$file
    echo "%%{gopath}/src/%%{goipath}/$file" >> devel.file-list
done
sort -u -o devel.file-list devel.file-list

%if %{rhel} != 8
%if %{with check}
%check
%gocheck
%endif
%endif

%files -n %{goname}-devel -f devel.file-list

%changelog
