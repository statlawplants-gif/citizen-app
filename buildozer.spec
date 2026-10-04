[app]
title = شهروند ایج
package.name = citizen_ij
package.domain = org.ij.citizen
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 1.0
requirements = python3,kivy,requests,urllib3,chardet,idna,certifi
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

android.sdk = 33
android.ndk = 25b
