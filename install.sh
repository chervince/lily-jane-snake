#!/usr/bin/env bash
#
# One-time installer for "Lily Jane's Snake" on Edubuntu.
# Run it once from a terminal:
#
#     ./install.sh
#
# It copies the game into your home folder, makes sure Pygame is present, and
# puts a colourful double-click icon on the desktop and in the Applications
# menu. After this, no terminal is needed to play.

set -euo pipefail

APP_NAME="Lily Jane's Snake"
SLUG="lily-jane-snake"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$HOME/Jeux/$SLUG"
CODE_FILES=(main.py snake_core.py graphics.py sound_fx.py icon.py)

echo "Installing ${APP_NAME}..."

# 1. Copy the game code into the user's home. These are always refreshed, so
#    re-running this script is how you update the game.
mkdir -p "$INSTALL_DIR"
for f in "${CODE_FILES[@]}"; do
    cp "$SRC_DIR/$f" "$INSTALL_DIR/"
done

# config.py holds the parent's per-child tuning (speed, mute, death mode). Copy
# it only on a first install; on an update, keep the existing one so those
# settings are never overwritten. To restore the defaults, delete
# "$INSTALL_DIR/config.py" before re-running.
if [ -f "$INSTALL_DIR/config.py" ]; then
    echo "Keeping your existing config.py (your settings are preserved)."
else
    cp "$SRC_DIR/config.py" "$INSTALL_DIR/"
fi

# 2. Make sure Pygame is available (apt first on Edubuntu, then pip).
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "Pygame not found -- installing it..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update && sudo apt-get install -y python3-pygame || true
    fi
    if ! python3 -c "import pygame" 2>/dev/null; then
        python3 -m pip install --user pygame \
            || python3 -m pip install --user --break-system-packages pygame \
            || true
    fi
fi
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "Could not install Pygame automatically."
    echo "Please install it (sudo apt install python3-pygame) and re-run this script."
    exit 1
fi

# 3. Draw the colourful launcher icon.
python3 "$INSTALL_DIR/icon.py" "$INSTALL_DIR/icon.png"

# 4. Write the .desktop launcher.
DESKTOP_FILE_CONTENTS="[Desktop Entry]
Version=1.0
Type=Application
Name=${APP_NAME}
Comment=A gentle, no-fail snake game for Lily Jane
Exec=python3 \"${INSTALL_DIR}/main.py\"
Path=${INSTALL_DIR}
Icon=${INSTALL_DIR}/icon.png
Terminal=false
Categories=Game;
"

APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"
printf '%s' "$DESKTOP_FILE_CONTENTS" > "$APPS_DIR/$SLUG.desktop"
chmod +x "$APPS_DIR/$SLUG.desktop"

# The Desktop folder name is localised (e.g. "Bureau" in French).
if command -v xdg-user-dir >/dev/null 2>&1; then
    DESKTOP_DIR="$(xdg-user-dir DESKTOP)"
else
    DESKTOP_DIR="$HOME/Desktop"
fi
mkdir -p "$DESKTOP_DIR"
cp "$APPS_DIR/$SLUG.desktop" "$DESKTOP_DIR/$SLUG.desktop"
chmod +x "$DESKTOP_DIR/$SLUG.desktop"
# Mark it trusted so GNOME lets her double-click without a warning.
gio set "$DESKTOP_DIR/$SLUG.desktop" metadata::trusted true 2>/dev/null || true

# Best-effort menu refresh.
update-desktop-database "$APPS_DIR" 2>/dev/null || true

echo ""
echo "Done! '${APP_NAME}' is on the desktop and in the Applications menu."
echo "Lily Jane can now double-click the snake icon to play."
