import os
import re
import shutil
import subprocess
import tempfile
import threading
from typing import Optional

from exceptions.tributarios_exception import TributarioException


class WordToPdfConverterService:
    """
    Conversor DOCX -> PDF usando LibreOffice/soffice headless.
    Sincrónico, seguro para concurrencia y con manejo de errores.
    """

    def __init__(
        self,
        soffice_cmd: Optional[str] = None,   # p.ej. "soffice" o "/usr/bin/soffice"
        timeout_seconds: int = 60,           # timeout por conversión
        max_concurrency: int = 2             # para no saturar el host
    ):
        # Resolver binario
        self.soffice = soffice_cmd or shutil.which("soffice") or shutil.which("libreoffice")
        if not self.soffice:
            raise TributarioException(
                "No se encontró 'soffice' (LibreOffice). Verifique que esté instalado en el contenedor/host."
            )

        self.timeout_seconds = timeout_seconds
        if max_concurrency < 1:
            max_concurrency = 1
        self._sem = threading.BoundedSemaphore(max_concurrency)

    def convertir_docx_a_pdf(self, archivo_docx: bytes) -> bytes:
        if not archivo_docx:
            raise TributarioException("No se pudo convertir: el archivo vino vacío.")

        # Limitar concurrencia global del proceso (sin async)
        with self._sem:
            try:
                with tempfile.TemporaryDirectory(prefix="conv_") as tmpdir:
                    path_docx = os.path.join(tmpdir, "entrada.docx")
                    path_pdf = os.path.join(tmpdir, "entrada.pdf")

                    # Perfil de usuario aislado para evitar locks entre procesos
                    user_profile_dir = os.path.join(tmpdir, "lo_profile")
                    os.makedirs(user_profile_dir, exist_ok=True)
                    user_install_arg = f"-env:UserInstallation=file://{user_profile_dir}"

                    # Guardar DOCX
                    with open(path_docx, "wb") as f:
                        f.write(archivo_docx)

                    # Ejecutar conversión
                    # Nota: "writer_pdf_Export" suele ser más estable que el alias "pdf"
                    cmd = [
                        self.soffice,
                        "--headless",
                        "--nologo",
                        "--nolockcheck",
                        user_install_arg,
                        "--convert-to", "pdf:writer_pdf_Export",
                        "--outdir", tmpdir,
                        path_docx,
                    ]

                    completed = subprocess.run(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        check=False,
                        timeout=self.timeout_seconds,
                    )

                    if completed.returncode != 0:
                        # Limpieza de logs (para no volcar paredes de texto)
                        stdout = (completed.stdout or "").strip()
                        stderr = (completed.stderr or "").strip()
                        msg = stderr or stdout or "Fallo desconocido en LibreOffice."
                        msg = self._compactar_mensaje(msg)
                        raise TributarioException(f"Fallo en conversión (rc={completed.returncode}): {msg}")

                    # Validar salida
                    if not os.path.exists(path_pdf):
                        stdout = (completed.stdout or "").strip()
                        stderr = (completed.stderr or "").strip()
                        msg = self._compactar_mensaje(stderr or stdout or "No se generó el PDF.")
                        raise TributarioException(f"Conversión incompleta: {msg}")

                    with open(path_pdf, "rb") as f:
                        pdf_bytes = f.read()

                    if not pdf_bytes:
                        raise TributarioException("El PDF generado está vacío.")
                    if not pdf_bytes.startswith(b"%PDF-"):
                        raise TributarioException("El archivo generado no es un PDF válido.")

                    return pdf_bytes

            except subprocess.TimeoutExpired:
                raise TributarioException(
                    f"Timeout de conversión: LibreOffice excedió {self.timeout_seconds} segundos."
                )
            except OSError as e:
                # Errores del sistema (p.ej., permisos, disco, binario faltante)
                raise TributarioException(f"Error del sistema al convertir: {e}")

    @staticmethod
    def _compactar_mensaje(msg: str, max_len: int = 700) -> str:
        """ Acorta y limpia el mensaje de LO para retornar algo legible. """
        msg = re.sub(r"\s+", " ", msg)
        if len(msg) > max_len:
            msg = msg[: max_len - 3] + "..."
        return msg
