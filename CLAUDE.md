# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-file Windows utility (`app.py`) that gets built into `CFDIViewer.exe`
and set as the default handler for `.xml` files. When a user double-clicks a
CFDI (SAT invoice XML), Windows launches the exe with the file path as
`sys.argv[1]`; the app parses it with `satcfdi` and opens a rendered HTML
version in the default browser.

## Commands

```powershell
pip install -r requirements.txt   # satcfdi + pyinstaller
python app.py path\to\cfdi.xml    # run directly during development
.\build.ps1                       # build dist\CFDIViewer.exe
```

There is no test suite or linter configured.

## Architecture

- `app.py` is the entire application. Flow: `main()` reads `sys.argv[1]` →
  `satcfdi.cfdi.CFDI.from_file()` parses the XML → `satcfdi.render.html_str()`
  renders it (this single call handles the base Comprobante plus whatever
  complemento is present — Nómina, Pagos, CartaPorte, Retenciones — satcfdi
  detects the type automatically) → the HTML is written to a temp file and
  opened via `webbrowser.open()`.
- No CLI args or invalid/unparseable XML both produce user-facing output
  instead of a stack trace: a `MessageBoxW` for the no-args case (the exe is
  built `--windowed`, so there's no console to print to), and a generated
  error HTML page (via `error_page()`) for parse/render failures, so the
  failure is visible in the browser rather than silently discarded.
- `build.ps1` must pass `--collect-data satcfdi` to PyInstaller — `satcfdi`
  reads its Jinja HTML templates and a bundled `catalogs.db` sqlite file from
  its own package directory at runtime, and PyInstaller's default analysis
  does not pick those up as they're not plain Python imports. Omitting this
  flag builds successfully but every run fails at import time
  (`sqlite3.OperationalError: unable to open database file`).
- `CFDIviewer.ico` is passed to PyInstaller via `--icon` to set the exe's
  icon; this is unrelated to any favicon shown in the browser tab when the
  generated HTML is opened, since that's controlled by the HTML itself (which
  currently has none).
- Setting the exe as the default `.xml` handler is a manual, per-machine
  Windows Explorer step (right-click → Open with → Choose another app →
  browse to the exe → "Always use this app") — nothing in this repo automates
  Windows file-association registry entries.
