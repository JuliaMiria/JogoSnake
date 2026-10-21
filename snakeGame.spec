# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['snakeGame.py'],
    pathex=[],
    binaries=[],
    datas=[('fundo.png', '.'), ('morango.png', '.'), ('corpoBloco.png', '.'), ('cabeca_direita.png', '.'), ('cabeca_esquerda.png', '.'), ('cabeca_cima.png', '.'), ('cabeca_baixo.png', '.'), ('mordida.mp3', '.'), ('gameOver.mp3', '.'), ('musica.mp3', '.')],
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
    name='snakeGame',
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
    icon=['icone.ico'],
)
