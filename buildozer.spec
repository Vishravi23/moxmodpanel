[app]
title = Mox Mod Panel
package.name = moxmodpanel
package.domain = org.mox
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.3.1,requests,android,plyer
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
android.permissions = INTERNET,READ_SMS,SEND_SMS,FOREGROUND_SERVICE,WAKE_LOCK
android.debug = True
android.arch = arm64-v8a
[buildozer]
log_level = 2
