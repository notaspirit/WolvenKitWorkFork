## 8.18.1 — 2026-05-14

**App**

* *Security*: Patched a vulnerability where temporary extracted files could inherit overly permissive permissions. by @71be0d44-2fa1-4c2e-bf2a-4f18f4a55c72
* *Removed*: Removed unused experimental telemetry settings from the preferences panel. by @f17d8e32-95bb-4e67-b1f0-9cc3d88f7c44
* *Added*: Added workspace tab persistence across application restarts. by @8f14e45f-ea6d-4c8a-9b1d-1d7f0f8c2a11
* *Added*: Added support for importing multiple project files in a single command. by @4cda2f67-7b94-42b4-a15f-58d2f16f9b83

**CLI**

* *Security*: Patched a vulnerability where temporary extracted files could inherit overly permissive permissions. by @71be0d44-2fa1-4c2e-bf2a-4f18f4a55c72
* *Deprecated*: Deprecated the legacy --config-path argument in favor of the new profile system. by @2ac7f8de-54ab-4fd2-9a2f-0d2d5a7ce331
* *Added*: Added support for importing multiple project files in a single command. by @4cda2f67-7b94-42b4-a15f-58d2f16f9b83
* *Fixed*: Fixed an issue where relative file paths were resolved incorrectly on Windows. by @b3c92d1a-6e2f-41f3-8c93-7b5c1e8f4d20

**Nuget Packages**

* *Deprecated*: Deprecated the legacy --config-path argument in favor of the new profile system. by @2ac7f8de-54ab-4fd2-9a2f-0d2d5a7ce331
* *Fixed*: Fixed incorrect cancellation behavior in asynchronous archive loading operations. by @ce91ab6e-3c0a-4c1f-9f4a-2c6be8c97d12
* *Changed*: Improved logging performance by reducing allocations during structured log formatting. by @d94a7c11-1f83-45de-92d7-c6a8b2f0e5a9


---

## 8.18.0 — 2026-05-04

**App**

* *Added*: Import and export flow is now also available in the right click menu by @notaspirit
* *Added*: Sleeves and hair substitution for ArchiveXL by @manavortex
* *Fixed*: AMM prop generation now correctly reads mesh appearances by @manavortex
* *Fixed*: Delete unused materials now uses correct index by @manavortex
* *Fixed*: ArchiveXL item generator will now successfully handle component name uniqueness - various robustness fixes by @manavortex
* *Fixed*: Nested quest phase nodes no longer lose internal socket connections after paste/duplicate operations by @misterchedda
* *Changed*: Filepath handling has been adjusted to handle os and archive paths according to their respective specs. Archive paths are now stricter and os paths looser than the previous combined implementation. by @notaspirit

**CLI**

* *Added*: Sleeves and hair substitution for ArchiveXL by @manavortex
* *Changed*: Filepath handling has been adjusted to handle os and archive paths according to their respective specs. Archive paths are now stricter and os paths looser than the previous combined implementation. by @notaspirit

**Nuget Packages**

* *Deprecated*: SanitizePath in FileHelper, ToFilePath, ToFileName, IsSaneFilePath, and SanitizeFilePath in StringPathExtensions are now deprecated. Use new archive or os path methods in StringPathExtensions and in FilePathValidation tools instead. by @notaspirit
* *Added*: Sleeves and hair substitution for ArchiveXL by @manavortex
* *Changed*: Filepath handling has been adjusted to handle os and archive paths according to their respective specs. Archive paths are now stricter and os paths looser than the previous combined implementation. by @notaspirit
