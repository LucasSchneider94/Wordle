# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['wordleBotApp.py'],
    pathex=[],
    binaries=[],
    datas=[('colors_dict_2.pkl', '.'), ('saved_dictionary_all.pkl', '.'), ('saved_dictionary_ans.pkl', '.')],
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
    a.binaries,
    a.datas,
    [],
    name='WordleSolver',
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
    icon=['stupidicon.icns'],
)
app = BUNDLE(
    exe,
    name='WordleSolver.app',
    icon='stupidicon.icns',
    bundle_identifier=None,
)
