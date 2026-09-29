[app]
# (str) Title of your application
title = AvaFix Logbook

# (str) Package name
package.name = avafix

# (str) Package domain (to satisfy packaging rules)
package.domain = org.crew.avafix

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db,html,css,js

# (str) Application version
version = 1.0

# (list) Application requirements
# پیش‌نیازهای استاندارد و کامل جهت اجرای بدون خطای Kivy, KivyMD و شبکه/فلاسک
requirements = python3,openssl,certifi,kivy==2.3.0,kivymd,flask,requests,urllib3,jinja2,werkzeug,charset-normalizer,idna

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Fullscreen or not
fullscreen = 0

# --------------------------------------------------
# Android specific
# --------------------------------------------------

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25.2.9519653

# (int) Android NDK API to use
android.ndk_api = 21

# (list) Architectures to build for (64-bit modern androids)
android.archs = arm64-v8a

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# --------------------------------------------------
# Buildozer
# --------------------------------------------------

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
