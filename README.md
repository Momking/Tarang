# Tarang Launcher

> A fast, extensible Wayland application launcher written in Python using GTK4 and Layer Shell.

Tarang is a modern launcher designed around a plugin architecture. Instead of hardcoding application search, clipboard history, files, or other sources, every search provider is implemented as a plugin.

The project aims to be:

- ⚡ Fast and responsive
- 🧩 Easily extensible
- 🎨 Fully themeable with CSS
- 🐧 Native Wayland application
- 🏗 Clean architecture suitable for contributors

---

# Features

- Application launcher
- Plugin-based search system
- GTK4 GridView interface
- Wayland Layer Shell support
- Icon caching
- Thumbnail generation
- File indexing
- Clipboard integration
- Keyboard-first workflow
- Calculator
- Commands

Planned features:

- Emoji search
- Browser history
- Recent documents
- AI plugins
- Window switcher
- Plugin marketplace

---

# Screenshots

![](/src/resources/image.png)

---

# Installation

## Requirements

- Python 3.12+
- GTK4
- PyGObject
- gtk4-layer-shell
- Wayland compositor

Fedora example:

```bash
sudo dnf install \
    python3-gobject \
    gtk4 \
    gtk4-layer-shell \
    desktop-file-utils
```

Clone the repository:

```bash
git clone https://github.com/Momking/tarang.git
cd tarang
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
./run.sh
```

---

# Project Structure

```
src/
│
├── controllers/
│
├── core/
│
├── models/
│
├── plugins/
│
├── services/
│
├── widgets/
│
├── wayland/
│
└── main.py
```

---

# Architecture

Tarang follows a simple layered architecture.

```
User Input
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
      ▼
Plugins
      │
      ▼
SearchResult
      │
      ▼
AppGrid
      │
      ▼
LauncherWindow
```

Responsibilities are intentionally separated:

- UI widgets never search.
- Plugins never touch GTK.
- Controllers never know plugin implementation details.

---

# Components

## LauncherWindow

The main application window.

Responsible for:

- Window creation
- Layer Shell setup
- Keyboard shortcuts
- Dependency registration
- Widget layout

---

## SearchController

Coordinates searching.

Responsibilities:

- Debounced searching
- Background worker threads
- Updating UI safely using GLib
- Navigation
- Activation

---

## PluginManager

Discovers and manages plugins.

Responsibilities:

- Load plugins
- Execute searches
- Merge results
- Activate selected result

---

## AppGrid

Displays search results.

Uses:

- Gtk.GridView
- Gtk.SingleSelection
- Gio.ListStore

Responsibilities:

- Rendering results
- Keyboard navigation
- Selection
- Activation

---

## Services

Services provide reusable functionality.

Current services:

- ApplicationService
- UsageService
- ClipboardService
- FileIndexService
- ThumbnailService
- IconCache

Services never depend on GTK.

---

# Search Pipeline

```
User types
      │
      ▼
SearchController
      │
      ▼
PluginManager.search()
      │
      ▼
Each Plugin.search()
      │
      ▼
Combined results
      │
      ▼
Gtk.GridView
```

Searching happens in a worker thread to keep the UI responsive.

UI updates are performed through:

```python
GLib.idle_add(...)
```

---

# Plugin System

Each plugin implements the same interface.

Example:

```python
class Plugin:

    def search(self, query):
        ...

    def activate(self, result):
        ...
```

A plugin returns a list of `SearchResult` objects.

Example:

```python
SearchResult(
    title="Firefox",
    subtitle="Web Browser",
    icon=icon,
    data=desktop_file,
)
```

Plugins should never import GTK widgets.

---

# Dependency Injection

Tarang uses a lightweight dependency container.

Example:

```python
container.register(
    ApplicationService,
    ApplicationService(),
)

service = container.resolve(ApplicationService)
```

This keeps plugins loosely coupled.

---

# Styling

The entire interface is themeable using CSS.

Example:

```css
.launcher {
    border-radius: 18px;
}

.app-card.selected {
    background-color: #0a4239;
}
```

No styling should be hardcoded inside widgets.

---

# Keyboard Navigation

Current shortcuts:

| Key | Action |
|------|--------|
| Enter | Launch selected item |
| Tab | Toggle search/results |
| Escape | Exit launcher |
| ↑ ↓ | Navigate |
| Mouse | Select and launch |

---

# Threading Model

Searching never blocks GTK.

```
Search Request
       │
       ▼
Background Thread
       │
       ▼
Plugin Search
       │
       ▼
GLib.idle_add()
       │
       ▼
Main GTK Thread
```

GTK widgets are only accessed from the main thread.

---

# Creating a Plugin

Example:

```python
class HelloPlugin:

    name = 

    description = 

    author = 

    version = 

    def search(self, query):

        if "hello".startswith(query):

            return [
                SearchResult(
                    title="Hello",
                    subtitle="Example Plugin",
                    icon=None,
                    data=None,
                    query=query,
                )
            ]

        return []

    def activate(self, result):
        print("Hello!")
```

Register it inside the PluginManager.

---

# Design Goals

Tarang follows a few core principles:

- Plugins should be independent.
- Widgets should only display data.
- Controllers coordinate logic.
- Services provide reusable functionality.
- UI should never block.
- Features should be easy to extend.

---

# Roadmap

- [x] Calculator
- [ ] Emoji search
- [ ] Clipboard history
- [ ] Browser history
- [ ] Recent documents
- [ ] File search improvements
- [ ] Plugin discovery
- [ ] Theme manager
- [ ] Configuration file
- [ ] Settings UI
- [ ] Fuzzy matching improvements

---

# Contributing

Contributions are welcome.

Before opening a pull request:

- Follow the existing project structure.
- Keep plugins independent of GTK.
- Avoid blocking the UI thread.
- Document new services and plugins.
- Format code consistently.

---

# License

MIT License
