## 8.17.5 — 2026-04-25

**App**

* *Security*: Sanitize user-supplied file paths to prevent directory traversal by @a3f8c2d1-7e4b-4a90-bc12-5f6e8d3c1a02
* *Removed*: Drop support for .redmod bundles created before version 0.9.0 by @e5a8d2f6-1c4b-4e54-bf87-4d1a3c7e9f02
* *Added*: Add dark-mode toggle to the settings panel by @f2c1e9b4-7a3d-4f43-9c21-5e8b0d6f3a14
* *Fixed*: Fix crash when opening a project that contains an empty archive folder by @c9d2e5a8-3f1b-4c76-8d43-2b9e6f4a1c57
* *Fixed*: Correct UV channel index off-by-one error during glTF mesh import by @e5a8d2f6-1c4b-4e54-bf87-4d1a3c7e9f02
* *Changed*: Project explorer now sorts entries case-insensitively by @f2c1e9b4-7a3d-4f43-9c21-5e8b0d6f3a14

**CLI**

* *Deprecated*: The --legacy-resolve flag is deprecated and will be removed in 2.0.0 by @c9d2e5a8-3f1b-4c76-8d43-2b9e6f4a1c57
* *Removed*: Drop support for .redmod bundles created before version 0.9.0 by @e5a8d2f6-1c4b-4e54-bf87-4d1a3c7e9f02
* *Added*: New `wkit pack --dry-run` flag prints resolved output paths without writing files by @a3f8c2d1-7e4b-4a90-bc12-5f6e8d3c1a02
* *Fixed*: Resolve incorrect exit code returned when pack fails due to missing redscript by @d1f4b7c3-8e2a-4d65-ae90-3c0f5e8b2d79
* *Changed*: Progress output is now written to stderr so stdout remains machine-parseable by @a3f8c2d1-7e4b-4a90-bc12-5f6e8d3c1a02

**Nuget Packages**

* *Security*: Upgrade System.Text.Json to 8.0.4 to address CVE-2024-30105 by @b7e1d4f9-2c3a-4b87-9e56-1a8f7c2d0e34
* *Deprecated*: WolvenKit.Core.Compat.LegacyReader is deprecated in favour of WolvenKit.Core.Reader by @d1f4b7c3-8e2a-4d65-ae90-3c0f5e8b2d79
* *Added*: Expose MeshImportSettings.NormalRecalculation on the public API by @b7e1d4f9-2c3a-4b87-9e56-1a8f7c2d0e34
* *Fixed*: Correct UV channel index off-by-one error during glTF mesh import by @e5a8d2f6-1c4b-4e54-bf87-4d1a3c7e9f02
* *Changed*: CR2WReader.ReadFile now returns a result type instead of throwing on malformed input by @b7e1d4f9-2c3a-4b87-9e56-1a8f7c2d0e34
