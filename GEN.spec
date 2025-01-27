# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs

# 添加动态链接库
binaries = collect_dynamic_libs('llama_cpp')

a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=binaries,  # 添加动态链接库
    datas=[('./app/resource/', '.')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='GEN',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['packResource/logo.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='GEN',
)
app = BUNDLE(
    coll,
    name='GEN.app',
    icon='./packResource/logo.icns',
    bundle_identifier=None,
)
