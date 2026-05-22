# -*- mode: python ; coding: utf-8 -*-

import shutil
import os

# 每次打包前清理 dist2 目录
dist_path = os.path.join(os.path.dirname(os.path.abspath(SPECPATH)), 'dist2')
if os.path.exists(dist_path):
    shutil.rmtree(dist_path)
    print(f'已清理: {dist_path}')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['xlrd'],
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
    name='UpdateTools',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
