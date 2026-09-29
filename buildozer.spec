[app]
title = AvaFix Logbook
package.name = avafix
package.domain = org.crew.avafix
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,html,css,js
version = 1.0

# پکیج‌های سبک و استاندارد بدون سربار کامپایل
requirements = python3,kivy,flask,requests,urllib3,jinja2,werkzeug

orientation = portrait
fullscreen = 0

# Android specific
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
# فقط معماری 64 بیتی استاندارد اندرویدهای امروزی (سرعت بیلد ۳ برابر می‌شود)
android.archs = arm64-v8a
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
