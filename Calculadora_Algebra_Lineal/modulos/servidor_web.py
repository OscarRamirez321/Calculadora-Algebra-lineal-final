"""Servidor local que abre la calculadora como página web en el navegador.
Sirve interfaz/index.html y atiende /api/<acción> con ServicioAlgebra, usando solo la
biblioteca estándar (http.server). Escucha únicamente en 127.0.0.1: nadie más puede entrar.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .servicio_web import ServicioAlgebra

CARPETA_INTERFAZ = Path(__file__).resolve().parent.parent / "interfaz"


class ManejadorHTTP(BaseHTTPRequestHandler):
    """Atiende GET de la página y POST de las operaciones."""

    servicio = ServicioAlgebra()

    def do_GET(self):
        """Entrega la página principal; cualquier otra ruta no existe."""
        if self.path.split("?")[0] not in ("/", "/index.html"):
            self._responder(404, b"No encontrado", "text/plain; charset=utf-8")
            return
        contenido = (CARPETA_INTERFAZ / "index.html").read_bytes()
        self._responder(200, contenido, "text/html; charset=utf-8")

    def do_POST(self):
        """Ejecuta /api/<acción> con el JSON recibido y devuelve el resultado en JSON."""
        if not self.path.startswith("/api/"):
            self._responder(404, b"{}", "application/json")
            return
        largo = int(self.headers.get("Content-Length", 0))
        try:
            datos = json.loads(self.rfile.read(largo) or b"{}")
        except json.JSONDecodeError:
            datos = {}
        resultado = self.servicio.ejecutar(self.path[len("/api/"):], datos)
        self._responder(200, json.dumps(resultado).encode("utf-8"), "application/json; charset=utf-8")

    def _responder(self, codigo, cuerpo, tipo):
        """Escribe la respuesta HTTP completa."""
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def log_message(self, formato, *argumentos):
        """Silencia el registro de cada petición para no ensuciar la terminal."""


class ServidorWeb:
    """Arranca el servidor en el primer puerto libre y abre el navegador."""

    PUERTO_INICIAL = 8765
    INTENTOS = 20

    def _crear_servidor(self):
        """Prueba puertos consecutivos hasta encontrar uno libre."""
        for puerto in range(self.PUERTO_INICIAL, self.PUERTO_INICIAL + self.INTENTOS):
            try:
                return ThreadingHTTPServer(("127.0.0.1", puerto), ManejadorHTTP), puerto
            except OSError:
                continue  # Puerto ocupado: se prueba el siguiente
        raise OSError("No se encontró un puerto libre entre 8765 y 8784")

    def iniciar(self, abrir_navegador=True):
        """Muestra la dirección, abre la pestaña y atiende hasta Ctrl+C."""
        servidor, puerto = self._crear_servidor()
        direccion = f"http://127.0.0.1:{puerto}/"
        print(f"\n  Calculadora de Álgebra Lineal abierta en {direccion}")
        print("  Si no se abre sola, copie esa dirección en su navegador.")
        print("  Para cerrar el programa presione Ctrl+C en esta ventana.\n")
        if abrir_navegador:
            threading.Timer(0.7, webbrowser.open, args=(direccion,)).start()
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\n  Programa finalizado.")
        finally:
            servidor.server_close()
