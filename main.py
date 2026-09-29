name: Build Android APK

on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Set up Java 17
        uses: actions/setup-java@v4
        with:
          distribution: "temurin"
          java-version: "17"

      - name: Install System Dependencies
        run: |
          sudo apt update
          sudo apt install -y git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev build-essential wget

      - name: Install Buildozer and Cython
        run: |
          pip install --upgrade pip setuptools wheel
          pip install Cython==0.29.36 buildozer

      - name: Pre-download Android NDK (Bypass 404 Error)
        run: |
          mkdir -p /home/runner/.buildozer/android/platform
          cd /home/runner/.buildozer/android/platform
          wget -q https://dl.google.com/android/repository/android-ndk-r25b-linux.zip -O android-ndk-r25b-linux.zip
          unzip -q android-ndk-r25b-linux.zip
          mv android-ndk-r25b android-ndk-r25b

      - name: Build with Buildozer
        run: |
          buildozer -v android debug

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: AvaFix-Crew-APK
          path: bin/*.apk
