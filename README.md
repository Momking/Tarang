# Tarang

A modern GTK4 application launcher built for Wayland compositors.

## Goals

- Native GTK4
- Wayland Layer Shell
- Fast startup
- Beautiful Material You theming
- Plugin architecture

## Structure
```
src/

main.py

models/
    app_info.py

services/
    application_service.py
    search_service.py
    theme_service.py

wayland/
    layer_shell.py

widgets/
    launcher_window.py
    app_grid.py
    app_card.py
    search_bar.py

resources/
    base.css
    generated.css
```
