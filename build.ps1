# Construye CFDIViewer.exe empaquetando app.py junto con los datos de satcfdi
# (templates HTML/CSS y el catálogo sqlite que usa en tiempo de ejecución).
$ErrorActionPreference = "Stop"

pyinstaller --onefile --windowed --name CFDIViewer `
    --icon CFDIviewer.ico `
    --collect-data satcfdi `
    app.py
