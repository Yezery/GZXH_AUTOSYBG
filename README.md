## MAC
### pyinstaller --clean --noconfirm --strip --add-data "./logo.png:." --add-data "./setup/config/config.json:config" --onedir --windowed -i logo.ico -n 'GEN' main.py

## MAC打包成dmg
### create-dmg --volname "GEN-insatller" --background "./source/bg.svg" --window-pos 400 200 --window-size 660 400 --icon-size 100  --icon "GEN.app" 160 185 --hide-extension "GEN.app" --app-drop-link 500 185  --volicon "./source/installer.icns"  dist/GEN-darwin.dmg  dist/GEN.app

## Windows
### pyinstaller --clean --noconfirm --strip --add-data ".\\logo.png;." --add-data ".\\setup\\config\\config.json;config" --onefile --windowed -i ".\\logo.ico" -n GEN main.py

## Windows打包成安装包
### 使用 Inno Setup 见 GENsetupiss.iss

### API_KEY: "gJBWXXcfaIyQ1AXs5b6gyZPp"
### SECRET_KEY: "VAOa3QhPlE3o1tybWHvKfyXiJ85rGYTl"
