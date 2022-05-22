import os
from distutils.util import strtobool  # Importing this because without it values are always evaluated as True

# Settings

SETTINGS = {

    # Login

    "HOST": os.getenv("QB_HOST", "localhost"),  # Hostname of qBitTorrent's Web-UI
    "PORT": os.getenv("QB_PORT", 8080),  # Port of qBitTorrent's Web-UI (default:8080)
    "USERNAME": os.getenv("QB_USER", "admin"),  # Username qBitTorrent's Web-UI
    "PASSWORD": os.getenv("QB_PASS", "password"),  # Password of qBitTorrent's Web-UI

    # Options

    # Force start the torrent if it has private tracker
    "FORCE_START": bool(strtobool(os.getenv("QT_FORCE_START", "True"))),

    # Adds tag to torrents with private trackers to organize torrents
    "ADD_TAG": bool(strtobool(os.getenv("QT_ADD_TAG", "True"))),

    # Removes tag from torrents
    "REMOVE_TAG": bool(strtobool(os.getenv("QT_REMOVE_TAG", "False"))),

    # Leave that as 'False' if you don't know what it is. More info on README.md
    "SUPER_SEED": bool(strtobool(os.getenv("QT_SUPER_SEED", "False"))),

    # Name of the tag to add to torrents or remove from torrents
    "TAG_NAME": os.getenv("QT_TAG_NAME", "Private")
}

# Aliases

host = SETTINGS["HOST"]
port = SETTINGS["PORT"]
username = SETTINGS["USERNAME"]
password = SETTINGS["PASSWORD"]

force_start = SETTINGS["FORCE_START"]
add_tag = SETTINGS["ADD_TAG"]
remove_tag = SETTINGS["REMOVE_TAG"]
tag_name = SETTINGS["TAG_NAME"]
super_seed = SETTINGS["SUPER_SEED"]

# Debug
qt_debug = bool(strtobool(os.getenv("QT_DEBUG", "False")))

# Version and Author Info
qt_version = os.getenv("QT_VERSION", "v3.0")
qt_author = os.getenv("QT_AUTHOR", "jaw3l")
