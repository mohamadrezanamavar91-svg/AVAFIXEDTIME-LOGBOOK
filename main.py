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

      - name: Set up Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Set up Java 17
        uses: actions/setup-java@v4
        with:
          distribution: "temurin"
          java-version: "17"

      - name: Install System Dependencies
        run: |
          sudo apt update
          sudo apt install -y git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
            libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev build-essential libltdl-dev ccache \
            libjpeg-dev libpng-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

      - name: Install Python Build Tools
        run: |
          python -m pip install --upgrade pip setuptools wheel
          python -m pip install "Cython<3.0.0" buildozer

      - name: Pre-download Android NDK
        run: |
          mkdir -p /home/runner/.buildozer/android/platform
          cd /home/runner/.buildozer/android/platform
          if [ ! -d "android-ndk-r25b" ]; then
            wget -q https://dl.google.com/android/repository/android-ndk-r25b-linux.zip
            unzip -q android-ndk-r25b-linux.zip
          fi

      - name: Build with Buildozer
        run: |
          buildozer -v android debug

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: AvaFix-Crew-APK
          path: bin/*.apk
