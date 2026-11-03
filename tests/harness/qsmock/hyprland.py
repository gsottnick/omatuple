"""Stand-ins for the `Quickshell.Hyprland` QML module: just what Commons/Ui touch.

Real monitor data needs a compositor; the harness runs offscreen, so
`monitors` stays empty and `focusedMonitor` null — both consumers (Ui/OverlayWindow,
Ui/PopupCard) handle those cases. Loading the module at all is what matters.
"""

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlAnonymous, QmlElement, QmlSingleton

QML_IMPORT_NAME = "Quickshell.Hyprland"
QML_IMPORT_MAJOR_VERSION = 1


@QmlAnonymous
class MonitorSet(QObject):
    """Shape of Quickshell's ObjectModel for monitors: a `.values` list."""

    def values(self):
        return []


@QmlElement
@QmlSingleton
class Hyprland(QObject):
    rawEvent = Signal("QVariant")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._monitors = MonitorSet(self)

    @Property(QObject, constant=True)
    def monitors(self):
        return self._monitors

    @Property(QObject, constant=True)
    def focusedMonitor(self):
        return None

    @Slot()
    def refreshMonitors(self):
        pass


@QmlElement
class HyprlandFocusGrab(QObject):
    """Accepts the declaration so PopupCard loads; no input is grabbed offscreen."""

    cleared = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._active = False
        self._windows = []

    def _get_active(self):
        return self._active

    def _set_active(self, value):
        self._active = bool(value)

    active = Property(bool, _get_active, _set_active)

    def _get_windows(self):
        return self._windows

    def _set_windows(self, value):
        self._windows = list(value or [])

    windows = Property("QVariantList", _get_windows, _set_windows)
