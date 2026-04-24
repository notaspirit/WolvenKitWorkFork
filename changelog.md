## 8.17.5 — 2026-04-24

### App

#### Added

* Added dark mode support to the main interface by @alice

#### Changed

* Bumped minimum required runtime version to 3.0 by @carol

#### Fixed

* Fixed crash on startup when config file is missing by @dave
* Fixed tooltip misalignment on high-DPI displays by @grace
* Fixed memory leak when closing project tabs rapidly by @heidi

### CLI

#### Added

* Added dark mode support to the main interface by @alice

#### Changed

* Bumped minimum required runtime version to 3.0 by @carol
* Unified error message formatting across all command outputs

#### Removed

* Dropped deprecated --legacy-output flag by @frank

### Core

#### Added

* Introduced plugin lifecycle hooks for init and teardown by @bob

#### Changed

* Bumped minimum required runtime version to 3.0 by @carol
* Unified error message formatting across all command outputs

#### Fixed

* Resolved race condition in the async task scheduler by @eve

#### Security

* Patched path traversal vulnerability in archive loader by @ivan

### Common

#### Changed

* Bumped minimum required runtime version to 3.0 by @carol

#### Removed

* Removed unused internal StringPool utility class

### ModKit

#### Added

* Bundled starter templates for new mod projects

#### Changed

* Bumped minimum required runtime version to 3.0 by @carol

### RED4

#### Changed

* Bumped minimum required runtime version to 3.0 by @carol

#### Fixed

* Corrected offset calculations for RED4 archive headers

### Launcher

#### Added

* Added auto-update check on launch for the Launcher component by @judy

### General

#### Changed

* Adjusted default log verbosity from INFO to WARNING

#### Fixed

* Fixed incorrect line endings in generated output files by @karl
