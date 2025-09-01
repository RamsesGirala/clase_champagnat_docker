import base64, hashlib

from exceptions.tributarios_exception import TributarioException


class FileService:

    def __init__(self):
        self.name = "files"

    def base64_a_bytes(self,b64: str) -> bytes:
        try:
            archivo = base64.b64decode(b64, validate=True)
            return archivo
        except Exception as e:
            raise TributarioException(mensaje=f"Base64 inválido: {e}")

    def sha256_hex(self,data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def tamano_bytes(self,data: bytes) -> int:
        return len(data)