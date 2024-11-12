import platform
import os


# General Note: This folder currently generally excludes GUI stuff, as we (plan to) use a cross-platform GUI framework by default.
# pyright: reportUnusedImport=false

if platform.system() == "Linux":
    from .linux_io import *
elif platform.system() == "Windows":
    from .windows_io import *
elif platform.system() == "Darwin":
    from .mac_io import *
