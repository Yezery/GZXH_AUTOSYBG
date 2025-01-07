## MAC
### pyinstaller -D -w --clean --noconfirm --strip --add-data "./source/logo.png:." --add-data "./source/config/config.json:config" -i "./source/logo.icns" -n 'GEN' ./app/main.py --debug all

## MAC打包成dmg
### create-dmg --volname "GEN-installer" --background "./source/bg.svg" --window-pos 400 200 --window-size 660 400 --icon-size 100 --icon "GEN.app" 160 185 --hide-extension "GEN.app" --app-drop-link 500 185 --volicon "source/installer.icns" dist/GEN-darwin.dmg dist/GEN.app

## Windows
### pyinstaller -D -w --clean --noconfirm --add-data ".\\source\\logo.png;." --add-data ".\\source\\config\\config.json;config" -i ".\\source\\logo.ico" -n GEN .\app\main.py

## Windows打包成安装包
### 使用 Inno Setup 见 GENsetupiss.iss

### API_KEY: "gJBWXXcfaIyQ1AXs5b6gyZPp"
### SECRET_KEY: "VAOa3QhPlE3o1tybWHvKfyXiJ85rGYTl"
<!-- sips -z 16 16     logo.png --out icon_16x16.png
sips -z 32 32     logo.png --out icon_16x16@2x.png
sips -z 32 32     logo.png --out icon_32x32.png
sips -z 64 64     logo.png --out icon_32x32@2x.png
sips -z 128 128   logo.png --out icon_128x128.png
sips -z 256 256   logo.png --out icon_128x128@2x.png
sips -z 256 256   logo.png --out icon_256x256.png
sips -z 512 512   logo.png --out icon_256x256@2x.png
sips -z 512 512   logo.png --out icon_512x512.png
cp logo.png icon_512x512@2x.png 
iconutil -c icns logo.iconset   
-->

Makecert -sv gen.pvk -r -n “CN=ZivYE” gen.cer
Cert2spc gen.cer gen.spc
pvk2pfx -pvk gen.pvk -pi '123456789' -spc gen.spc -pfx gen.pfx -f
signtool sign /f gen.pfx /p 123456789 /fd SHA256 C:\Users\11720\Desktop\GEN\GEN.exe
signtool timestamp /tr http://timestamp.digicert.com /td SHA256 C:\Users\11720\Desktop\GEN\GEN.exe

