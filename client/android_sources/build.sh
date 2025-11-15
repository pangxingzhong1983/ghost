#!/bin/sh
export PATH=$PATH:$HOME/.local/bin

pip install --user --upgrade git+https://github.com/kivy/buildozer
[ -f buildozer.spec ] || ln -sf buildozer.spec.example buildozer.spec
buildozer android release
mv .buildozer/android/platform/build/dists/ghost/bin/Wi-Fi-0.1-release-unsigned.apk \
 ../../ghost/payload_templates/ghost.apk || exit 1
rm -rf .buildozer/android/platform/build
rm -rf ~/.buildozer/android/platform/*.tar.gz
rm -rf ~/.buildozer/android/platform/*.tgz
rm -rf ~/.buildozer/android/platform/*.tar.bz2
