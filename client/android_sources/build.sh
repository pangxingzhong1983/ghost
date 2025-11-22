#!/bin/sh
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH:$HOME/.local/bin"
export PKG_CONFIG_PATH=/opt/homebrew/opt/libffi/lib/pkgconfig:${PKG_CONFIG_PATH:-}
export CFLAGS="${CFLAGS:+$CFLAGS }-I/opt/homebrew/opt/libffi/include"
export CPPFLAGS="${CPPFLAGS:+$CPPFLAGS }-I/opt/homebrew/opt/libffi/include"
export LDFLAGS="${LDFLAGS:+$LDFLAGS }-L/opt/homebrew/opt/libffi/lib"

pip install --user --upgrade buildozer==1.5.0
[ -f buildozer.spec ] || ln -sf buildozer.spec.example buildozer.spec
buildozer android release
DIST_ROOT=.buildozer/android/platform
ARM64_BUILD_DIR=$DIST_ROOT/build-arm64-v8a
APK_PATH=$(find "$ARM64_BUILD_DIR" -name "*-release-unsigned.apk" | head -n 1)
[ -n "$APK_PATH" ] || { echo "Unable to locate built APK" >&2; exit 1; }
mv "$APK_PATH" ../../ghost/payload_templates/ghost.apk || exit 1
rm -rf "$ARM64_BUILD_DIR"
rm -rf ~/.buildozer/android/platform/*.tar.gz
rm -rf ~/.buildozer/android/platform/*.tgz
rm -rf ~/.buildozer/android/platform/*.tar.bz2
