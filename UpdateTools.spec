# -*- mode: python ; coding: utf-8 -*-

import shutil
import os

# 每次打包前清理 dist 和 build 目录
base_dir = os.path.dirname(os.path.abspath(SPECPATH))
for folder in ('dist', 'build'):
    folder_path = os.path.join(base_dir, folder)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f'已清理: {folder_path}')

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
