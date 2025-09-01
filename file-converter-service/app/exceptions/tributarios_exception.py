class TributarioException(Exception):
    def __init__(self, mensaje: str, mensaje_original: str = "", clase_original: str = ""):
        self.mensaje = mensaje
        self.mensaje_original = mensaje_original
        self.clase_original = clase_original
        super().__init__(mensaje)
