# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

PROJECT_ROOT = os.path.abspath(os.path.dirname(SPECPATH))

hidden = [
    'kivy',
    'sqlite3',
    'paths',
    'KivyWidgets.SessionPanel',
    'Widgets.notifications',
    'Widgets.notificationMessages',
    'Style.ButtonStyle',
    'Style.ButtonState',
    'Style.Colors',
    'Style.palettes',
]
hidden += collect_submodules('KivyWidgets')
hidden += collect_submodules('Widgets')
hidden += collect_submodules('Style')
hidden += collect_submodules('Models')
hidden += collect_submodules('Database')

a = Analysis(
    ['app.py'],
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=[
        ('translation.json', '.'),
        ('Style', 'Style'),
        ('views', 'views'),
        ('Images', 'Images'),
    ],
    hiddenimports=hidden,
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
    name='StudentPlanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='StudentPlanner',
)
