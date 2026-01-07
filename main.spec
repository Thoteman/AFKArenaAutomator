# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
import sys

block_cipher = None
adbauto_data = collect_data_files('adbauto')

icon_file = 'icon.ico'
if sys.platform == 'darwin':
    icon_file = 'icon.icns'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('res', 'res'),
        ('config.ini', '.'),
        (icon_file, '.'),
        ('src', 'src'),
        *adbauto_data,
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    optimize=0,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AFKArenaAutomator',
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
    icon=['icon.ico'],
)
