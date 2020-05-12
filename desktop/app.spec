# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['C:\\Users\\rzkan\\OneDrive - Institut Teknologi Sepuluh Nopember\\project\\git\\MuktabahSyamilah\\desktop'],
             binaries=[],
             datas=[
                ('data/dataset/kategori.npy', 'data/dataset'),
                ('data/dataset/kitabsave.npy', 'data/dataset'),
                ('data/dataset/namakitab.npy', 'data/dataset'),
                ('data/dataset/sentence_clearsave.npy', 'data/dataset'),
                ('data/model/modelFT.model', 'data/model'),
                ('data/model/modelFT.model.trainables.syn1neg.npy', 'data/model'),
                ('data/model/modelFT.model.trainables.vectors_ngrams_lockf.npy', 'data/model'),
                ('data/model/modelFT.model.trainables.vectors_vocab_lockf.npy', 'data/model'),
                ('data/model/modelFT.model.wv.vectors_ngrams.npy', 'data/model'),
                ('data/model/modelFT.model.wv.vectors_vocab.npy', 'data/model'),
                ('data/model/modelFT.model.wv.vectors.npy', 'data/model')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Muktabah Syamila',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
