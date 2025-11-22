# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ghost/cli/ghostsh.py'],
    pathex=[],
    binaries=[],
    datas=[('ghost/library_patches_py3', 'ghost/library_patches_py3'), ('ghost/packages/all', 'ghost/packages/all'), ('ghost/commands', 'ghost/commands')],
    hiddenimports=['ghost.ghostlib.GhostJob', 'ghost.cli', 'ghost.cli.ghostgen', 'pylzma', 'ghost.ghostlib.utils.credentials', 'ghost.ghostlib.PythonCompleter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ghost-macos-arm64',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
