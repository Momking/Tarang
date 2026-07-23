# Tarang Launcher

<div align="center">

**A modern, extensible application launcher for Wayland desktops built with GTK4 and Python.**

*Fast. Plugin-driven. Designed for Linux power users.*

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GTK4](https://img.shields.io/badge/GTK4-4.x-7FE719?style=for-the-badge&logo=gtk&logoColor=black)
![Wayland](https://img.shields.io/badge/Wayland-Native-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## Overview

Tarang is a **Wayland-native launcher** focused on speed, extensibility, and clean architecture.

Unlike traditional launchers that only search installed applications, Tarang provides a unified search experience through a plugin system capable of searching:

- Applications
- Files
- Clipboard history
- Commands
- Future plugins

The project is built around a service-oriented architecture, making it easy to extend without modifying the core launcher.

---

## Features

### Current

- Wayland native (GTK4 + Layer Shell)
- Plugin-based search architecture
- Fuzzy search
- Application launcher
- File search
- Clipboard history
- Command execution
- Usage-based ranking
- Background file indexing
- File system monitoring
- Persistent file index cache
- Keyboard-first workflow
- Dependency Injection container

### Planned

- Window switcher
- Recent files
- Favorites
- Plugin SDK
- Theme engine
- Image thumbnails
- PDF previews
- Plugin marketplace
- Calculator
- Web search
- Emoji picker
- AI plugins

---

# Screenshots

> Screenshots coming soon.

---

# Architecture

```
User
 │
 ▼
SearchBar
 │
 ▼
SearchController
 │
 ▼
PluginManager
 │
 ├──────────────┐
 ▼              ▼
Application     File
Plugin          Plugin
 │              │
 ▼              ▼
Services     Services
 │              │
 └──────┬───────┘
        ▼
 Search Results
        ▼
     App Grid
```

---

# Project Structure

```
src/
│
├── controllers/
│   └── search_controller.py
│
├── models/
│   ├── app_info.py
│   ├── file_info.py
│   ├── clipboard_item.py
│   └── search_result.py
│
├── plugins/
│   ├── manager.py
│   ├── builtin/
│   │   ├── application_plugin.py
│   │   ├── file_plugin.py
│   │   ├── clipboard_plugin.py
│   │   └── command_plugin.py
│
├── services/
│   ├── application_service.py
│   ├── clipboard_service.py
│   ├── command_service.py
│   ├── file_index_service.py
│   ├── usage_service.py
│   └── thumbnail_service.py
│
├── widgets/
│   ├── launcher_window.py
│   ├── app_grid.py
│   ├── app_card.py
│   └── search_bar.py
│
├── core/
│   └── container.py
│
└── main.py
```

---

# Search Pipeline

```
User Types
      │
      ▼
Search Controller
      │
      ▼
Plugin Manager
      │
      ├──────────────┐
      ▼              ▼
Applications      Files
Clipboard         Commands
      │              │
      └──────┬───────┘
             ▼
      Merge Results
             ▼
       Sort by Score
             ▼
         Display UI
```

---

# Ranking

Tarang combines multiple signals to rank results.

Current scoring includes:

- Exact match
- Prefix match
- Subsequence match
- Usage frequency
- Recency bonus

---

# File Indexing

Unlike scanning the filesystem every search, Tarang maintains an indexed database.

Startup flow:

```
Load cache

↓

Launcher usable immediately

↓

Background indexing

↓

Update cache
```

This provides instant search results while keeping the index up to date.

---

# Plugin System

Every search provider is implemented as a plugin.

Example:

```python
class Plugin:

    def search(
        self,
        query: str,
        limit: int,
    ):
        ...
```

Current plugins:

- Application Plugin
- File Plugin
- Clipboard Plugin
- Command Plugin

Adding new plugins requires no changes to the launcher itself.

---

# Services

Services encapsulate reusable functionality.

Current services include:

| Service | Purpose |
|----------|---------|
| ApplicationService | Installed applications |
| FileIndexService | Background file indexing |
| ClipboardService | Clipboard history |
| UsageService | Ranking history |
| CommandService | Command execution |
| ThumbnailService | File thumbnails |
| SearchService | Fuzzy searching |

---

# Dependency Injection

Tarang uses a lightweight dependency injection container.

```python
container.register(
    ApplicationService,
    ApplicationService(),
)

service = container.resolve(
    ApplicationService
)
```

This keeps plugins loosely coupled and easy to test.

---

# Caching

Tarang stores persistent caches inside

```
~/.cache/tarang/
```

Current caches:

```
files.json
```

Future:

```
usage.json
clipboard.json
thumbnails/
```

---

# Performance

Design goals:

- Startup under **100 ms**
- Incremental background indexing
- Lazy loading
- Memory caching
- Non-blocking search
- Threaded services
- Minimal UI latency

---

# Technologies

- Python
- GTK4
- GObject Introspection
- Wayland
- Layer Shell
- GLib
- Gio
- threading
- JSON
- Freedesktop specifications

---

# Building

Clone the repository

```bash
git clone https://github.com/Momking/Tarang.git

cd Tarang
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python src/main.py
```

---

# Development Goals

Tarang aims to become more than an application launcher.

The long-term vision is to build a desktop command palette for Linux.

Potential capabilities include:

- Launch applications
- Open files
- Focus existing windows
- Clipboard management
- System actions
- Calculator
- Unit conversion
- AI integrations
- Package management
- Plugin ecosystem

---

# Roadmap

## Phase 1

- Application launcher
- Plugin architecture
- File indexing
- Clipboard
- Commands

**Status:** ✅ Complete

---

## Phase 2

- Thumbnail service
- Window switcher
- Favorites
- Recent files
- Theme improvements

**Status:** 🚧 In Progress

---

## Phase 3

- Plugin SDK
- Plugin marketplace
- Theme engine
- Calculator
- Web search

---

## Phase 4

- AI plugins
- Voice commands
- Cloud sync
- Workspace integration

---

# Contributing

Contributions are welcome.

If you'd like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

Please ensure code follows the existing architecture and style.

---

# Inspiration

Tarang is inspired by projects such as:

- Wofi
- Rofi
- GNOME Shell Search
- Raycast
- Alfred
- Ulauncher
- Walker
- KRunner

while focusing on a clean architecture and a native Wayland experience.

---

# License

MIT License

---

<div align="center">

**Tarang** — *A modern command palette for the Linux desktop.*

</div>
