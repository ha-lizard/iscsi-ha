# Changelog

<!-- markdownlint-disable line-length no-duplicate-heading -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.5.0-rc] - 2024-12-17

- Enhanced directory structure by relocating configuration, documentation, and runtime files to align with standard Linux practices.
- Refactored scripts to improve readability, maintainability, and error handling.
- Addressed ShellCheck warnings, enhancing script quality and robustness:
  - Fixed quoting issues to prevent word splitting and glob expansion.
  - Replaced legacy backticks with modern `$(...)` command substitution.
  - Transitioned to well-defined constructs for logical expressions.
  - Optimized scripts using tools like `pgrep`, `find`, and `grep -c`.
- Improved RPM packaging with architecture-specific builds and updated file handling.
- Added new system configuration for TGTD override customization.
- Created Linux man page for `iscsi-cfg` and updated documentation paths.

## [2.3.0] - 2024-12-01

- Initial release for GitHub.

## [2.2.7] - 2024-11-01

- Code preparation for moving project to GitHub.
- No logic changes, only comments added/removed.

## [2.2.6] - 2024-08-01

- Bug Fix: Resolved race condition with DRBD and `multipathd` introduced in XCP 8.2.1 release.
- Bug Fix: IFS was not restored before calling `replication_link_check`, causing interface looping to break.

## [2.2.5] - 2021-02-01

- Bug Fix: Manual mode tracking could produce a "unary operator expected" error if the state file was missing or empty.
- Added DRBD disk state tracking and alerting.
- Added DRBD split-brain alerting via XenCenter/XCP-ng Center. The alert script can be found in `/etc/iscsi-ha/scripts/drbd-split-brain-alert`.

## [2.2.4] - 2019-11-01

- Bug Fix: Updated `manage_db_manual_mode` to better handle missing parameters when installed over older versions of HA-Lizard.

## [2.2.3] - 2019-10-01

- Bug Fix: Resolved parsing error in `replication_link_check` for bonded interfaces with more than two interfaces.
- Updated `restore_replication_link` for improved handling of bonded interfaces.

## [2.2.2] - 2019-10-01

- Removed dependency on `networkctl` as it is no longer included in XCP/XenServer v8 default dom0.

## [2.2.1] - 2019-10-01

- Improved logic to detect and correct ARP failures on replication interfaces using bonded links inside Linux bridges.
- Updated `fw_init` for backward compatibility with pre-version 7 hosts using SystemV.
- Added SSL support to the email handler.

## [2.2.0] - 2018-10-01

- Added stateful configuration manager to preserve all settings in a 2-node hyperconverged pool.
- Removed manual patching requirements for iptables for replication networks.
- Enhanced service startup logic to ensure proper initialization after a dom0 upgrade.
- Resolved printf display bugs in status monitoring.

## [2.1.5] - 2017-08-01

- Bug Fix: Resolved a race condition in XenServer 7.x deployments where `DRBD` could start before the network was ready.

## [2.1.4] - 2017-01-01

- Bug Fix: Addressed incorrect run state displayed for iSCSI targets in manual mode.
- Enhanced DRBD daemon startup retries for stability.
- Reverted ARP update logic to pre-version 2 method for improved compatibility.

## [2.1.3] - 2016-12-01

- Bug Fix: Resolved invalid characters in TGT drop-in configuration causing delays.
- Improved backward compatibility for daemon controller.

## [2.1.2] - 2016-12-01

- Merged version 1.5.7 for backward compatibility.
- Updated init for compatibility with XenServer 6 and 7 environments.

## [2.1.1] - 2016-11-01

- Added frequent ARP updates for storage hosts on replication networks.
- Introduced DRBD split-brain recovery tools.
- CLI updated with version-check option (`-v`).

## [2.1.0] - 2016-11-01

- Multiple bug fixes for daemon runtime behavior.
- Added support for `daemon-reload` on drop-in file creation.

## [2.0.2_beta] - 2016-07-01

- Introduced XenServer 7 compatibility (not backward compatible with 6.x).
- Added stateful updates for manual mode validations.

## [2.0.0] - 2016-07-01

- Initial version 2 release.

## [1.5.7] - 2016-05-01

- Bug Fix: Ensured DRBD primary role is asserted before iSCSI target starts.
- Added DRBD kernel module for the latest XenServer 6.2 kernel.
- Enabled seamless transition of the pool master into maintenance mode.

## [1.5.6] - 2015-09-01

- Improved switchover times during failure or role reversal in manual mode.
- Resolved issues with `replug_pbd` for handling multiple iSCSI SRs.

## [1.5.5] - 2015-08-01

- Added compiled DRBD modules for XenServer kernel version 2.6.32.43-0.4.1.xs1.8.0.861.170802xen.

## [1.5.4] - 2015-04-01

- Added support for DRBD 8.4.3.
- Updated installer for `noSAN` installer support.
- Improved email handler, centralizing email settings.

## [1.4.5] - 2014-09-01

- Fixed CLI display bug for replication IPs when using custom interfaces.
- Added DRBD kernel module for XenServer 6.2 updates.

## [1.4.4] - 2014-07-01

- Added DRBD kernel module to support updated XenServer 6.2 kernel.

## [1.4.3] - 2014-06-01

- Resolved `replug_pbd` bug for environments with multiple iSCSI SRs.
- Fixed IP display bugs in manual mode.

## [1.4.2] - 2014-04-01

- Introduced manual operating mode for managing storage manually.
- Improved installation and initialization scripts for better usability.

## [1.3.7] - 2013-12-01

- Improved logger process management in unclean exits.
- Updated scripts for XenServer 6.2 SP1 kernel compatibility.

## [1.3.1] - 2013-10-01

- Addressed race conditions in slow `dom0s`.
- Updated email alert logic to prevent network-related hanging.

## [1.2.15] - 2013-09-01

- Resolved email alert truncation issues.
- Enhanced installer to retain configurations during upgrades.

## [1.2.14] - 2013-09-01

- Improved PBD replugging for better SR management after reboots.
- Enhanced environment configuration handling.

## [1.2.12] - 2013-08-06

- Added DRBD RPMs for XenServer 6.2 compatibility.

## [1.2.11] - 2013-06-01

- Introduced auto-plugging of iSCSI SRs for better XenServer integration.
