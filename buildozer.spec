[app]

# (str) Title of your application
title = Papiview 

# (str) Package name
package.name = papis.papiview

# (str) Package domain (needed for android/ios packaging)
package.domain = org.papis.papiview

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = md,py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
#source.include_patterns = *.md#assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = bin,art

# (list) List of exclusions using pattern matching
source.exclude_patterns = buildozer.spec,tests/*,log

# (str) Application versioning (method 1)
version = 0.1.1

# (str) Application versioning (method 2)
#version.regex = __version__ = ['\"]([^'\"]*)['\"]
#version.filename = /home/spopoff/dev/KivyMD/kivymd/__init__.py 
#%(source.dir)s/../../kivymd/__init__.py

# (list) Application requirements
# comma seperated e.g. requirements = sqlite3,kivy

# need to install Cython==0.25 and pyOpenSSL on your machine
# for cffi (required for cryptography required for paramiko) problem with ssl (https)
# add to use local install folder of python for android or
# modify cffi recipe once copied into .buildozer folder and remove the 's' from https
# buildozer android clean + rm ./buildozer
requirements = kivy==master,git+https://gitlab.com/kivymd/KivyMD.git,pycrypto,libffi,pyopenssl==16.0.0,ecdsa,requests,easywebdav,hostpython2,android,PyYAML,unidecode,paramiko==1.16.0
#,cryptography,pysftp
#,pysftp
#,libffi,cffi,cryptography
#cryptography
#cryptography==2.1,paramiko
#git+https://github.com/pyca/cryptography.git
# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes = /home/spopoff/dev/python-for-android/pythonforandroid/recipes
#%(source.dir)s/../../gitlab-ci/p4a-recipes/

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
#requirements.source.kivymd = /home/spopoff/dev/KivyMD

# (list) Garden requirements
# garden_requirements =

# (str) Presplash of the application
#presplash.filename = /home/spopoff/dev/KivyMD/kivymd/images/kivymd_logo.png
presplash.filename = /home/spopoff/dev/papiview/art/big_logo.png
#%(source.dir)s/../../kivymd/images/kivymd_logo.png

# (str) Icon of the application
#icon.filename = /home/spopoff/dev/KivyMD/kivymd/images/kivymd_logo.png
icon.filename = /home/spopoff/dev/papiview/art/logo_notext.png 
# (str) Supported orientation (one of landscape, portrait or all)
orientation = all
#all

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to use
#android.api = 19 

# (int) Minimum API required
#android.minapi = 9

# (int) Android SDK version to use
#android.sdk = 25 

# (str) Android NDK version to use
#android.ndk = 10e 
#10e

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path = /home/spopoff/.buildozer2/android/platform/android-ndk-10e/

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path = /home/spopoff/.buildozer2/android/platform/android-sdk-20/

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path = /usr/bin/ant

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#android.p4a.source_dir = /home/spopoff/anaconda3/bin#/home/spopoff/anaconda3/lib/python3.5/site-packages/pythonforandroid
#p4a.branch = master
#p4a.source_dir = /home/spopoff/.local/lib/python2.7/site-packages/pythonforandroid/
p4a.source_dir = /opt/python-for-android
#.local/lib/python2.7/site-packages/pythonforandroid
#android.p4a_dir = /media/zingballyhoo/Media/Code/Repos/python-for-android

# (str) Filename to the hook for p4a
#p4a.hook =
#p4a.requirements= OpenSSL

p4a.force-build = True


# (list) python-for-android whitelist
#android.p4a_whitelist =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
#android.skip_update = True

# (str) Bootstrap to use for android builds (android_new only)
# android.bootstrap = sdl2

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.renpy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (str) python-for-android branch to use, if not master, useful to try
# not yet merged features.
#android.branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (list) Android additionnal libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86
android.arch = armeabi
#-v7a

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
#build_dir = /home/spopoff/.buildozer2

# (str) Path to build output (i.e. .apk, .ipa) storage
bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be translated into:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#


#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug
