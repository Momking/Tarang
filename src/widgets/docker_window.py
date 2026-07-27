
from gi.repository import Gtk   #noqa

from widgets.plugin_docker import PluginDock
from wayland.layer_shell import setup_docker as setup_layer_shell


class DockWindow(Gtk.ApplicationWindow):

    def __init__(self, application, plugin_state):
        super().__init__(application=application)

        setup_layer_shell(self)

        self.plugin_dock = PluginDock(plugin_state)

        self.set_child(self.plugin_dock)

        self.add_css_class("dock-window")
