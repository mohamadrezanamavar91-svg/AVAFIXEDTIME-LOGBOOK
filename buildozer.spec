[app]
title = AvaFix Logbook
package.name = avafix
package.domain = org.crew.avafix
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db,html,css,js
version = 1.0

requirements = python3,kivy,flask,requests,urllib3,jinja2,werkzeug,certifi


orientation = portrait
fullscreen = 0

# Android specific
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
