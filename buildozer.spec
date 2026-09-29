[app]
title = AvaFix Logbook
package.name = avafix
package.domain = org.crew.avafix
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,html,css,js
version = 1.0

requirements = python3,kivy,flask,pyjnius,requests,urllib3,chardet,idna,jinja2,werkzeug,itsdangerous,click

orientation = portrait
fullscreen = 0

# Android specific
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
