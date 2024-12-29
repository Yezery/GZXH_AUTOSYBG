## MAC
### pyinstaller --clean --noconfirm --strip --add-data "./logo.png:." --add-data "./config.json:config" --onedir --windowed -i logo.ico -n 'GEN' main.py
## MAC打包成dmg
# create-dmg --volname "GEN Installer" --window-pos 200 200 --window-size 800 600 --icon-size 128 --icon "GEN.app" 150 150 --app-drop-link 600 150  dist/GEN_installer.dmg  dist/GEN.app

## Windows
### pyinstaller --clean --noconfirm --strip --add-data ".\\logo.png;." --add-data ".\\config.json;config" --upx-dir c:\Users\11720\Desktop\AUTOSYBG\.conda\Scripts\upx.exe  --onefile --windowed -i ".\\logo.ico" -n GEN main.py
## Windows打包成安装包
### 使用 Inno Setup 见 GENsetupiss.iss

### API_KEY: "gJBWXXcfaIyQ1AXs5b6gyZPp"
### SECRET_KEY: "VAOa3QhPlE3o1tybWHvKfyXiJ85rGYTl"