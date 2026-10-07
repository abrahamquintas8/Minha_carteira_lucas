[app]
title = My Application
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,gif
source.exclude_dirs = tests, bin, venv, .venv, .git, .github
version = 0.1
requirements = python3,kivy,sqlite3
orientation = portrait
osx.kivy_version = 2.2.0
fullscreen = 0
android.api = 33
android.ndk = 28c
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.branch = develop
p4a.commit = 0382d27de2f7315ed98e74884bafb30365decdee
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
ios.codesign.allowed = false
[buildozer]
log_level = 2
warn_on_root = 1
