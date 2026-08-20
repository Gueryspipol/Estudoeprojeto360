import json
import os
from pathlib import Path


class _FilesCompat:
    def __init__(self):
        self._indice = 0

    def upload(self):
        fila = json.loads(os.environ.get("AP360_UPLOAD_QUEUE", "[]"))
        if self._indice >= len(fila):
            return {}
        origem = Path(fila[self._indice])
        self._indice += 1
        if not origem.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {origem.name}")
        destino = Path.cwd() / origem.name
        if origem.resolve() != destino.resolve():
            destino.write_bytes(origem.read_bytes())
        return {destino.name: destino.read_bytes()}

    def download(self, caminho):
        return caminho


files = _FilesCompat()
