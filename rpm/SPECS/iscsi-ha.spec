%define version      __VERSION__
%define release      __RELEASE__
%define docdir        %{_datadir}/doc/%{name}

Name:           iscsi-ha
Version:        %{version}
Release:        %{release}
Summary:        Hyperconverged storage for 2-node XenServer and Xen Cloud Platform environments
Requires:       ha-lizard, scsi-target-utils, drbd84-utils, gawk, coreutils, util-linux, iproute, net-tools
Packager:       iscsi-ha
Group:          Productivity/Clustering/HA
BuildArch:      x86_64
License:        GPLv3
URL:            https://www.ha-lizard.com
Source0:        iscsi-ha.tar.gz

%description
iSCSI-HA is a specialized add-on for two-node pools in XenServer and Xen Cloud
Platform (XCP) environments, enabling highly available, hyperconverged storage
solutions using local disks. By integrating DRBD for synchronous block
replication and TGT as the iSCSI target framework, iSCSI-HA eliminates the need
for shared storage hardware, enhancing storage reliability and availability
while maintaining advanced pool functionalities like live migration.

Key Features:
* Provides a robust, cost-effective alternative to traditional shared storage
  in two-node setups.
* Utilizes DRBD for real-time block-level data replication between nodes.
* Leverages TGT for scalable and efficient iSCSI target management.
* Supports high-availability failover mechanisms for seamless operation during
  node failures.
* Designed for compatibility with XenServer, XCP, and other XAPI-based
  environments.
* Lightweight and efficient, ensuring minimal resource overhead.
* Facilitates hyperconverged infrastructure setups, combining compute and storage
  on the same nodes.
* Ideal for organizations seeking to optimize two-node cluster setups with
  redundancy, performance, and simplicity.

%prep
# Preparing the build environment by unpacking the source tarball
echo "Preparing build environment."
%setup -q -c

%build
# No build steps required, placeholder section
echo "Building skipped."

%install
# Install files into the buildroot directory, ensuring proper file structure
mkdir -p %{buildroot}%{_sysconfdir}/iscsi-ha
# states and logs
mkdir -p %{buildroot}%{_localstatedir}/lib/iscsi-ha/state
mkdir -p %{buildroot}%{_localstatedir}/log/iscsi-ha
# documentation
mkdir -p %{buildroot}%{docdir}
# TODO: legacy scripts
mkdir -p %{buildroot}%{_libexecdir}/iscsi-ha/scripts

# Specifically install each one of the files
install -D -m 644 etc/bash_completion.d/iscsi-cfg %{buildroot}%{_sysconfdir}/bash_completion.d/iscsi-cfg
install -D -m 644 etc/iscsi-ha/iscsi-ha.conf %{buildroot}%{_sysconfdir}/iscsi-ha/iscsi-ha.conf
install -D -m 644 etc/iscsi-ha/iscsi-ha.conf.defaults %{buildroot}%{_sysconfdir}/iscsi-ha/iscsi-ha.conf.defaults
install -D -m 644 etc/iscsi-ha/iscsi-ha.init %{buildroot}%{_sysconfdir}/iscsi-ha/iscsi-ha.init
install -D -m 644 etc/iscsi-ha/install.params %{buildroot}%{_sysconfdir}/iscsi-ha/install.params
install -D -m 755 etc/init.d/iscsi-ha %{buildroot}%{_sysconfdir}/init.d/iscsi-ha
install -D -m 755 etc/init.d/iscsi-ha-watchdog %{buildroot}%{_sysconfdir}/init.d/iscsi-ha-watchdog
install -D -m 755 etc/systemd/system/tgtd.service.d/iscsi-ha.local %{buildroot}%{_sysconfdir}/systemd/system/tgtd.service.d/iscsi-ha.local
install -D -m 755 usr/lib64/iscsi-ha/iscsi-ha.func %{buildroot}%{_libdir}/iscsi-ha/iscsi-ha.func
install -D -m 755 usr/bin/iscsi-cfg %{buildroot}%{_bindir}/iscsi-cfg
install -D -m 755 usr/libexec/iscsi-ha/become_primary %{buildroot}%{_libexecdir}/iscsi-ha/become_primary
install -D -m 755 usr/libexec/iscsi-ha/config_manager %{buildroot}%{_libexecdir}/iscsi-ha/config_manager
install -D -m 755 usr/libexec/iscsi-ha/drbd-sb-tool %{buildroot}%{_libexecdir}/iscsi-ha/drbd-sb-tool
install -D -m 755 usr/libexec/iscsi-ha/drbd-split-brain-alert %{buildroot}%{_libexecdir}/iscsi-ha/drbd-split-brain-alert
install -D -m 755 usr/libexec/iscsi-ha/email_alert.py %{buildroot}%{_libexecdir}/iscsi-ha/email_alert.py
install -D -m 755 usr/libexec/iscsi-ha/fw_init %{buildroot}%{_libexecdir}/iscsi-ha/fw_init
install -D -m 755 usr/libexec/iscsi-ha/iscsi-ha.mon %{buildroot}%{_libexecdir}/iscsi-ha/iscsi-ha.mon
install -D -m 755 usr/libexec/iscsi-ha/iscsi-ha.sh %{buildroot}%{_libexecdir}/iscsi-ha/iscsi-ha.sh
install -D -m 755 usr/libexec/iscsi-ha/log %{buildroot}%{_libexecdir}/iscsi-ha/log
install -D -m 755 usr/libexec/iscsi-ha/post_version.py %{buildroot}%{_libexecdir}/iscsi-ha/post_version.py
install -D -m 755 usr/libexec/iscsi-ha/replug_pbd %{buildroot}%{_libexecdir}/iscsi-ha/replug_pbd
install -D -m 755 usr/libexec/iscsi-ha/status %{buildroot}%{_libexecdir}/iscsi-ha/status
install -D -m 755 usr/libexec/iscsi-ha/timeout %{buildroot}%{_libexecdir}/iscsi-ha/timeout
# Documentation
install -D -m 644 LICENSE %{buildroot}%{docdir}/
install -D -m 644 CHANGELOG.md %{buildroot}%{docdir}/
install -D -m 644 usr/share/doc/iscsi-ha/INSTALL %{buildroot}%{docdir}/
install -D -m 644 usr/share/man/man8/iscsi-cfg.8 %{buildroot}%{_mandir}/man8/iscsi-cfg.8
# TODO: legacy scripts
install -D -m 755 usr/libexec/iscsi-ha/scripts/* %{buildroot}%{_libexecdir}/iscsi-ha/scripts/


%pre
# Check if the system is XenServer or XCP-ng using lsb_release
if command -v lsb_release &>/dev/null; then
    DISTRO_NAME=$(lsb_release -i | awk -F: '{print $2}' | xargs)

    # Check for XenServer or XCP-ng in the Distributor ID
    if [[ "$DISTRO_NAME" != "XenServer" && "$DISTRO_NAME" != "XCP-ng" ]]; then
        echo "This package is designed for XenServer or XCP-ng systems only."
        exit 1
    fi
else
    echo "lsb_release command not found. This package can only be installed on XenServer or XCP-ng."
    exit 1
fi

%post
set -e
echo "Setting up iscsi-ha..."

# Disable scsi-target-utils service if it exists
if systemctl list-units --type=service --quiet --all scsi-target.service; then
    systemctl disable scsi-target.service
    systemctl stop scsi-target.service
fi

# Disable drbd84-utils service if it exists
if systemctl list-units --type=service --quiet --all drbd.service; then
    systemctl disable drbd.service
    systemctl stop drbd.service
fi

# Enable the services to start on boot
if command -v systemctl &> /dev/null; then
    systemctl daemon-reload
    systemctl enable iscsi-ha iscsi-ha-watchdog
else
    chkconfig iscsi-ha on
    chkconfig iscsi-ha-watchdog on
fi

# Insert any required pool DB params
%{_bindir}/iscsi-cfg insert &>/dev/null

# TODO: Update installation version
# BUG: This generate a error when the system is not connected to internet
#/usr/libexec/iscsi-ha/post_version.py IHA-__VERSION__-__RELEASE__

echo "iscsi-ha setup complete."

%preun
# Pre-uninstallation cleanup (stop services before removal)
# NOTE: $1 = 0 when uninstalling (package removal), $1 = 1 when upgrading
if [ $1 -eq 0 ]; then
    systemctl stop iscsi-ha || true
    systemctl stop iscsi-ha-watchdog || true
    systemctl disable iscsi-ha || true
    systemctl disable iscsi-ha-watchdog || true
    systemctl daemon-reload || true
fi

%files
%defattr(-,root,root,-)

# Configuration files (this will NOT be replaced during upgrades)
%config(noreplace) %{_sysconfdir}/iscsi-ha/iscsi-ha.conf
%config(noreplace) %{_sysconfdir}/iscsi-ha/iscsi-ha.conf.defaults
%config(noreplace) %{_sysconfdir}/iscsi-ha/iscsi-ha.init
# Configuration files (this WILL be replaced during upgrades)
%config %{_sysconfdir}/iscsi-ha/install.params
%config %{_sysconfdir}/systemd/system/tgtd.service.d/iscsi-ha.local
# bash completion
%config %{_sysconfdir}/bash_completion.d/iscsi-cfg
# Libraries
%{_libdir}/iscsi-ha/iscsi-ha.func

# Init and systemd service files
%{_sysconfdir}/init.d/iscsi-ha
%{_sysconfdir}/init.d/iscsi-ha-watchdog

# Documentation
%doc %{docdir}/LICENSE
%doc %{docdir}/INSTALL
%doc %{docdir}/CHANGELOG.md
%{_mandir}/man8/iscsi-cfg.8.gz

# Create /var/lib/iscsi/state directory
%dir %{_localstatedir}/lib/iscsi-ha/state
%ghost %attr(644,root,root) %{_localstatedir}/lib/iscsi-ha/state/status

# Include the python and bash script in /usr/bin/
%{_bindir}/iscsi-cfg

# Application-specific executable files
%{_libexecdir}/iscsi-ha/become_primary
%{_libexecdir}/iscsi-ha/config_manager
%{_libexecdir}/iscsi-ha/drbd-sb-tool
%{_libexecdir}/iscsi-ha/drbd-split-brain-alert
%{_libexecdir}/iscsi-ha/email_alert.py
%{_libexecdir}/iscsi-ha/fw_init
%{_libexecdir}/iscsi-ha/iscsi-ha.mon
%{_libexecdir}/iscsi-ha/iscsi-ha.sh
%{_libexecdir}/iscsi-ha/log
%{_libexecdir}/iscsi-ha/post_version.py
%{_libexecdir}/iscsi-ha/replug_pbd
%{_libexecdir}/iscsi-ha/status
%{_libexecdir}/iscsi-ha/timeout

# TODO: legacy scripts
%{_libexecdir}/iscsi-ha/scripts/*

# TODO: add a logrotate
# Create /var/log/ha-lizard directory
%dir %{_localstatedir}/log/iscsi-ha

# INFO: Do not put anything after the changelog macro. github actions will add the changelog there.
%changelog
