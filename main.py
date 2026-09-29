name: Build Android APK

on:
  push:
    branches:
      - main
      - master
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"

      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            git \
            zip \
            unzip \
            wget \
            curl \
            autoconf \
            automake \
            libtool \
            pkg-config \
            cmake \
            gettext \
            libncurses5-dev \
            libncursesw5-dev \
            libtinfo5 \
            zlib1g-dev \
            libffi-dev \
            libssl-dev \
            build-essential

      - name: Install Buildozer
        run: |
          python -m pip install --upgrade pip setuptools wheel
          python -m pip install "Cython==0.29.36"
          python -m pip install buildozer

      - name: Install Android SDK components
        run: |
          SDKMANAGER="${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager"

          yes | "${SDKMANAGER}" --licenses >/dev/null || true

          "${SDKMANAGER}" \
            "platform-tools" \
            "platforms;android-33" \
            "build-tools;33.0.2"

      - name: Install Android NDK r25b manually
        run: |
          NDK_VERSION="25.1.8937393"
          NDK_DIR="${ANDROID_HOME}/ndk/${NDK_VERSION}"
          NDK_ZIP="/tmp/android-ndk-${NDK_VERSION}-linux.zip"

          mkdir -p "${ANDROID_HOME}/ndk"

          wget -O "${NDK_ZIP}" \
            "https://dl.google.com/android/repository/android-ndk-r25b-linux.zip"

          unzip -q "${NDK_ZIP}" -d /tmp

          mv /tmp/android-ndk-r25b "${NDK_DIR}"

          echo "ANDROID_NDK_HOME=${NDK_DIR}" >> "${GITHUB_ENV}"
          echo "ANDROID_NDK_ROOT=${NDK_DIR}" >> "${GITHUB_ENV}"

          test -f "${NDK_DIR}/source.properties"
          echo "Installed NDK:"
          cat "${NDK_DIR}/source.properties"

      - name: Accept Android SDK licenses
        run: |
          yes | sdkmanager --licenses >/dev/null || true

      - name: Build APK
        run: |
          buildozer android clean || true
          buildozer -v android debug

      - name: Upload APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: AvaFix-Crew-APK
          path: bin/*.apk
          if-no-files-found: error
