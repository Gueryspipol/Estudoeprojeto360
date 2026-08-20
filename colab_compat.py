import json
import os
from pathlib import Path

class _FilesCompat:
    def __init__(self):
        self._indice = 0
    def upload(self):
        fila = json.loads(os.environ.get('UPLOAD_QUEUE', '[]'))
        if self._indice >= len(fila):
            return {}
        caminho = Path(fila[self._indice])
        self._indice += 1
        if not caminho.exists():
            raise FileNotFoundError(f'Arquivo de entrada não encontrado: {caminho.name}')
        return {caminho.name: caminho.read_bytes()}
    def download(self, caminho):
        return caminho
files = _FilesCompat()
