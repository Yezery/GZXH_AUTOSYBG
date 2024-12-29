# pyinstaller --clean --noconfirm --strip --add-data "./logo.png:." --add-data "./config.json:config" --onedir --windowed -i logo.ico -n 'GEN' main.py
<!-- {
    "NAME": "叶正睿",
    "ID": "22054181",
    "COURSE": "22数媒6",
    "API_KEY": "gJBWXXcfaIyQ1AXs5b6gyZPp",
    "SECRET_KEY": "VAOa3QhPlE3o1tybWHvKfyXiJ85rGYTl",
    "SAVE_PATH": "/Users/yezery/Desktop"
} -->
# create-dmg --volname "GEN Installer" --window-pos 200 200 --window-size 800 600 --icon-size 128 --icon "GEN.app" 150 150 --app-drop-link 600 150  dist/GEN_installer.dmg  dist/GEN.app