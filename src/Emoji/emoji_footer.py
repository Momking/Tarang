from gi.repository import Gtk   #noqa


class EmojiFooter(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.END)
        self.add_css_class("footer-navigation-hints")

        # 1. Right Swipe Hint (Go Back Leftwards)
        back_icon = Gtk.Image.new_from_icon_name("gesture-two-finger-swipe-right-symbolic")
        back_icon.set_size_request(24, 24)
        back_label = Gtk.Label(label=" Swipe Right for Back")

        back_layout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        back_layout.append(back_icon)
        back_layout.append(back_label)

        # 2. Left Swipe Hint (Go Forward Rightwards)
        forward_icon = Gtk.Image.new_from_icon_name("gesture-two-finger-swipe-left-symbolic")
        forward_icon.set_size_request(24, 24)
        forward_label = Gtk.Label(label="Swipe Left for Next ")

        forward_layout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        forward_layout.append(forward_label)
        forward_layout.append(forward_icon)

        # Append indicators into the main footer layout strip
        self.append(back_layout)
        self.append(forward_layout)

