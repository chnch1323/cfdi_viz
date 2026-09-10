# Visor de CFDI

Aplicación de Windows que abre archivos `.xml` de CFDI (facturas del SAT) y los
muestra formateados en el navegador, usando la librería
[`satcfdi`](https://github.com/SAT-CFDI/python-satcfdi) para el parseo y
renderizado a HTML.

Diseñada para asociarse como programa predeterminado de `.xml`: doble clic en
un CFDI y se abre ya formateado, sin pasos manuales.

## Cómo funciona

1. Windows invoca `CFDIViewer.exe` pasando la ruta del `.xml` como argumento.
2. `app.py` carga el CFDI con `satcfdi.cfdi.CFDI.from_file()` y lo renderiza
   con `satcfdi.render.html_str()` (soporta Comprobante estándar y
   complementos como Nómina, Pagos, CartaPorte, Retenciones, etc.).
3. El HTML resultante se guarda en una carpeta temporal y se abre con el
   navegador predeterminado del sistema.
4. Si el XML no es válido, se muestra una página de error con el detalle.

## Requisitos (solo para desarrollo/build)

- Python 3.11+
- `pip install -r requirements.txt` (instala `satcfdi` y `pyinstaller`)

## Construir el ejecutable

```powershell
.\build.ps1
```

Genera `dist\CFDIViewer.exe`, un ejecutable independiente (no requiere Python
instalado) con el ícono `CFDIviewer.ico`, empaquetando también los templates
HTML y el catálogo interno de `satcfdi`.

## Uso

Ejecutar directamente pasando la ruta del XML:

```powershell
dist\CFDIViewer.exe ruta\al\cfdi.xml
```

## Asociarlo como app predeterminada para `.xml`

1. Clic derecho en cualquier `.xml` → **Abrir con** → **Elegir otra aplicación**.
2. Buscar y seleccionar `dist\CFDIViewer.exe`.
3. Marcar **"Usar siempre esta aplicación para abrir archivos .xml"**.

Desde ahí, doble clic en cualquier CFDI `.xml` lo abrirá formateado en el
navegador.
