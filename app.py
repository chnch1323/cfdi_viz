"""Visor de CFDI: recibe la ruta de un XML del SAT y lo abre formateado en el navegador."""
import ctypes
import html
import os
import sys
import tempfile
import traceback
import webbrowser


def show_message(text: str) -> None:
    if sys.platform == "win32":
        ctypes.windll.user32.MessageBoxW(0, text, "Visor de CFDI", 0x40)
    else:
        print(text)


def write_and_open(html_content: str, base_name: str) -> None:
    out_path = os.path.join(tempfile.gettempdir(), f"{base_name}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    webbrowser.open(f"file://{out_path}")


def error_page(xml_path: str, exc: Exception) -> str:
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Error al procesar CFDI</title></head>
<body style="font-family: sans-serif; padding: 2rem;">
<h1>No se pudo procesar el archivo</h1>
<p><b>Archivo:</b> {html.escape(xml_path)}</p>
<pre style="background:#f4f4f4; padding:1rem; white-space:pre-wrap;">{html.escape(traceback.format_exc())}</pre>
</body></html>"""


def main() -> None:
    if len(sys.argv) < 2:
        show_message(
            "Este programa se usa abriendo un archivo .xml de CFDI con él.\n\n"
            "Clic derecho en un .xml -> Abrir con -> Elegir otra aplicación -> "
            "selecciona este programa y marca 'Usar siempre esta aplicación'."
        )
        return

    xml_path = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(xml_path))[0]

    try:
        from satcfdi.cfdi import CFDI
        from satcfdi.render import html_str

        cfdi = CFDI.from_file(xml_path)
        content = html_str(cfdi)
    except Exception as exc:  # noqa: BLE001 - mostrar cualquier error al usuario
        content = error_page(xml_path, exc)

    write_and_open(content, base_name)


if __name__ == "__main__":
    main()
