# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None
adbauto_data = collect_data_files('adbauto')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('res', 'res'),
        ('config.ini', '.'),
        ('icon.icns', '.'),
        ('src', 'src'),
        *adbauto_data,
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
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
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.icns',
)

app = BUNDLE(
    exe,
    name='AFKArenaAutomator.app',
    icon='icon.icns',
    bundle_identifier='com.thoteman.afkarenautomator',
)
