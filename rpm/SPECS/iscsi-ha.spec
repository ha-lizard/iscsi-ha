%define version      __VERSION__
%define release      __RELEASE__
%define buildarch    noarch
%define name         iscsi-ha

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Hyperconverged storage for 2-node XenServer and Xen Cloud Platform environments
Requires:       scsi-target-utils, drbd84-utils
Packager:       iscsi-ha
Group:          Productivity/Clustering/HA
BuildArch:      noarch
License:        GPLv3+
URL:            https://www.ha-lizard.com
Source0:        iscsi-ha.tar.gz

%description
iSCSI-HA is a specialized add-on for two-node pools in XenServer and Xen Cloud Platform (XCP) environments, enabling highly available, hyperconverged storage solutions using local disks. By integrating DRBD for synchronous block replication and TGT as the iSCSI target framework, iSCSI-HA eliminates the need for shared storage hardware, enhancing storage reliability and availability while maintaining advanced pool functionalities like live migration.

Key Features:

* Provides a robust, cost-effective alternative to traditional shared storage in two-node setups.
* Utilizes DRBD for real-time block-level data replication between nodes.
* Leverages TGT for scalable and efficient iSCSI target management.
* Supports high-availability failover mechanisms for seamless operation during node failures.
* Designed for compatibility with XenServer, XCP, and other XAPI-based environments.
* Lightweight and efficient, ensuring minimal resource overhead.
* Facilitates hyperconverged infrastructure setups, combining compute and storage on the same nodes.
* This tool is ideal for organizations seeking to optimize two-node cluster setups with redundancy, performance, and simplicity in mind.

%prep
echo "Preparing build environment."
%setup -q -c

%build
# No build steps required, placeholder section
echo "Building skipped."

%install
# Install files into the buildroot
mkdir -p %{buildroot}%{_sysconfdir}/iscsi-ha
cp -Par * %{buildroot}%{_sysconfdir}/iscsi-ha
rm -rf %{buildroot}%{_sysconfdir}/iscsi-ha/rpm

%pre
# Placeholder for pre-install actions
exit 0

%post
#!/bin/bash
set -e
echo "Setting up iscsi-ha..."

# Set executable permissions
find %{_sysconfdir}/iscsi-ha -type f -name "*.sh" -exec chmod +x {} \;
find %{_sysconfdir}/iscsi-ha/scripts -type f -exec chmod +x {} \;
# Add CLI link
ln -sf %{_sysconfdir}/iscsi-ha/scripts/iscsi-ha /usr/bin/iscsi-ha || true

# Tab completion for CLI
# TODO: change filename extension
cp %{_sysconfdir}/iscsi-ha/scripts/iscsi-cfg.tab /etc/bash_completion.d/iscsi-cfg || true
chmod +x /etc/bash_completion.d/iscsi-cfg || true

# Enable init scripts for systemd
# TODO: migrate to systemctl
cp %{_sysconfdir}/iscsi-ha/init/iscsi-ha /etc/init.d/
cp %{_sysconfdir}/iscsi-ha/init/iscsi-ha-watchdog /etc/init.d/

# Enable the services to start on boot
if command -v systemctl &> /dev/null; then
    systemctl daemon-reload
    systemctl enable iscsi-ha iscsi-ha-watchdog
else
    chkconfig iscsi-ha on
    chkconfig iscsi-ha-watchdog on
fi

# Create DB Keys
%{_sysconfdir}/iscsi-ha/scripts/iscsi-cfg insert &>/dev/null

# TODO: Update installation version
# BUG: This generate a error when the system is not connected to internet
#/usr/libexec/iscsi-ha/post_version.py IHA-__VERSION__-__RELEASE__

echo "iscsi-ha setup complete."

%preun
#!/bin/bash
if [ $1 -eq 0 ]; then
    systemctl stop iscsi-ha || true
    systemctl stop iscsi-ha-watchdog || true
    systemctl disable iscsi-ha || true
    systemctl disable iscsi-ha-watchdog || true
fi

%postun
#!/bin/bash
if [ $1 -eq 0 ]; then
    rm -f /usr/bin/iscsi-ha
    rm -f %{_sysconfdir}/bash_completion.d/ha-cfg
    rm -f %{_sysconfdir}/systemd/system/iscsi-ha.service
    rm -f %{_sysconfdir}/systemd/system/iscsi-ha-watchdog.service
    rm -f %{_sysconfdir}/init.d/iscsi-ha-watchdog
    rm -f %{_sysconfdir}/init.d/iscsi-ha-watchdog
    systemctl daemon-reload || true
fi

%files
%defattr(-,root,root,-)

# Root directory files
%{_sysconfdir}/iscsi-ha/iscsi-ha.sh

# Configuration files
%config(noreplace) %{_sysconfdir}/iscsi-ha/iscsi-ha.conf
%config(noreplace) %{_sysconfdir}/iscsi-ha/iscsi-ha.conf.defaults

# Scripts and binaries
%{_sysconfdir}/iscsi-ha/scripts
%{_sysconfdir}/iscsi-ha/iscsi-ha.func
%{_sysconfdir}/iscsi-ha/iscsi-ha.init

# Init and systemd service files
%{_sysconfdir}/iscsi-ha/init/iscsi-ha
%{_sysconfdir}/iscsi-ha/init/iscsi-ha.mon
%{_sysconfdir}/iscsi-ha/init/iscsi-ha-watchdog


# Documentation
# TODO: use doc macro to handle the documentation files
%doc doc/COPYING doc/INSTALL doc/RELEASE
%doc %{_sysconfdir}/iscsi-ha/doc/COPYING
%doc %{_sysconfdir}/iscsi-ha/doc/INSTALL
%doc %{_sysconfdir}/iscsi-ha/doc/RELEASE

# State files
# TODO: change it to {_localstatedir}/lib/ to manage the state files
%{_sysconfdir}/iscsi-ha/state/status

# TODO: Add the CHANGELOG file following the RPM spec format
#%changelog
