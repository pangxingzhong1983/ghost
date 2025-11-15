#!/bin/bash
# -*- coding: UTF8 -*-

python3 -m pip install pyoxidizer

# so let's copy important files necessary for the build
cp -r ../../ghost/agent lib/ghost/
cp -r ../../ghost/network lib/ghost/
cp -r ../../ghost/library_patches_py3 .

docker run -ti -v $(pwd):/ghost --rm n1nj4sec/pyoxidizer-builder:linux-x86_64 /bin/bash -c 'export PATH="/build/python/bin:$PATH"; cd /ghost; python3 -m pip install pyoxidizer; pyoxidizer build --release'

strip -s build/x86_64-unknown-linux-gnu/release/install/pyoxydizer_ghost
echo "saving built template to ~/.ghost/payload_templates/ ..."
mkdir -p ~/.ghost/payload_templates
cp ./build/x86_64-unknown-linux-gnu/release/install/pyoxydizer_ghost ~/.ghost/payload_templates/ghostx64-310.pyoxidizer.lin


# not working, missing msvc on windows
#docker run --rm -v $(pwd):/opt/win/drive_c/tools/ghost -ti wine 'set PATH=%PATH%;C:\\Program Files\\PyOxidizer && C: && cd C:\\tools\\ghost && pyoxidizer build --release'
