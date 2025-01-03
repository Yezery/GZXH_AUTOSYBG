# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=[('./source/logo.png', '.'), ('./source/config/config.json', 'config')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    exclude_binaries=True,
    name='GEN',
    debug=True,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['source/logo.icns'],
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
    icon='./source/logo.icns',
    bundle_identifier=None,
)
