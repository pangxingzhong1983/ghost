# Changelog

## [Unreleased]
- Switch Android payload templates to `arm64-v8a` builds and document the new architecture target.
- Add a custom `pyuv` python-for-android recipe with arm64 aware libuv build flags and Python 3.11 fixes.
- Force host-side cffi builds to embed libffi so cryptography can compile on Apple Silicon hosts.
- Extend the Python toolchain configure cache to disable unavailable `get*ent` symbols on Android and pull in `libbz2`.
- Update the Android build scripts/specs to locate the new build output path automatically and package the resulting APK.
