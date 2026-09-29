[app]

# (string) Title of your application
title = AvaFix Logbook

# (string) Package name
package.name = avafix

# (string) Package domain (needed for android/ios packaging)
package.domain = org.crew.avafix

# (directory) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,kv,atlas,db,html,css,js

# (string) Application versioning
version = 1.0

# (list) Application requirements
# پکیج‌های سبک بدون نیاز به کامپایل سنگین C
requirements = python3,kivy,flask,requests,urllib3,jinja2,werkzeug

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

#
# Android specific
#

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use (همگام با مخزن گوگل)
android.ndk = 25.1.8937393

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for (فقط معماری ۶۴ بیت استاندارد برای سرعت بیلد بالا)
android.archs = arm64-v8a

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
