# -*- mode: python ; coding: utf-8 -*-

from scripts.bundle_guard import should_exclude_binary


a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

removed_binaries = [entry for entry in a.binaries if should_exclude_binary(entry)]
a.binaries[:] = [entry for entry in a.binaries if not should_exclude_binary(entry)]

for entry in removed_binaries:
    print(f"[bundle-guard] removendo DLL externa: {entry[0]} <- {entry[1]}")

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PesquisaMidias",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="PesquisaMidias",
)
