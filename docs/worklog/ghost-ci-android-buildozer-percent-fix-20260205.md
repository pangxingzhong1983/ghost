# Ghost CI Android Buildozer Percent Fix (2026-02-05)

## 1) 用户需求 / 任务目的 / 背景
- 需求：远程构建失败，要求修复并保证 latest 分支可构建。
- 背景：Android job 在 buildozer 解析配置时失败；随后因缺少 build-tools 导致 Aidl 不可用；再后续因 SDK License 未接受而无法安装 build-tools；最后因 SDK 目录存在但缺少 sdkmanager 导致构建中断；并出现 libtool/autoconf 宏缺失错误（LT_SYS_SYMBOL_USCORE）；需要 libltdl-dev 提供宏。

## 2) 本次所有变更点
- 修复 buildozer 配置中 `build_dir` 的 `%BUILDOZER%` 插值导致的解析异常。
- 允许 buildozer 安装所需 SDK 组件，避免 build-tools 缺失。
- 在 Android workflow 中预装 commandline tools 并自动接受 License，确保 sdkmanager 可用。
- Android 依赖补齐 autoconf/automake/libtool 等构建工具，并补充 libltdl-dev 提供 LT_SYS_SYMBOL_USCORE。

## 3) 变更前后差异对照
```diff
--- a/client/android_sources/buildozer-docker.spec
+++ b/client/android_sources/buildozer-docker.spec
@@
-build_dir = %BUILDOZER%
+build_dir = .buildozer
@@
-android.skip_update = True
+android.skip_update = False
```

```diff
--- a/.github/workflows/remote-build.yml
+++ b/.github/workflows/remote-build.yml
@@
       - name: Prepare buildozer spec
         working-directory: client/android_sources
         run: |
           cp -f buildozer-docker.spec buildozer.spec
+
+      - name: Prepare Android SDK tools and licenses
+        run: |
+          export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
+          SDK_ROOT="$HOME/.buildozer/android/platform/android-sdk"
+          TOOLS_ZIP="/tmp/cmdline-tools.zip"
+          TMP_DIR="$(mktemp -d)"
+          mkdir -p "$SDK_ROOT/cmdline-tools"
+          curl -fL --retry 3 "https://dl.google.com/android/repository/commandlinetools-linux-6514223_latest.zip" -o "$TOOLS_ZIP"
+          unzip -q "$TOOLS_ZIP" -d "$TMP_DIR"
+          if [[ -d "$TMP_DIR/cmdline-tools" ]]; then
+            SRC_DIR="$TMP_DIR/cmdline-tools"
+          elif [[ -d "$TMP_DIR/tools" ]]; then
+            SRC_DIR="$TMP_DIR/tools"
+          else
+            echo "cmdline-tools not found in archive"
+            exit 1
+          fi
+          rm -rf "$SDK_ROOT/cmdline-tools/latest"
+          mv "$SRC_DIR" "$SDK_ROOT/cmdline-tools/latest"
+          rm -rf "$TMP_DIR"
+          mkdir -p "$SDK_ROOT/tools/bin"
+          ln -sf "$SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" "$SDK_ROOT/tools/bin/sdkmanager"
+          yes | "$SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" --licenses
```

```diff
--- a/.github/workflows/build.yml
+++ b/.github/workflows/build.yml
@@
       - name: Prepare buildozer spec
         working-directory: client/android_sources
         run: |
           cp -f buildozer-docker.spec buildozer.spec
+
+      - name: Prepare Android SDK tools and licenses
+        run: |
+          export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
+          SDK_ROOT="$HOME/.buildozer/android/platform/android-sdk"
+          TOOLS_ZIP="/tmp/cmdline-tools.zip"
+          TMP_DIR="$(mktemp -d)"
+          mkdir -p "$SDK_ROOT/cmdline-tools"
+          curl -fL --retry 3 "https://dl.google.com/android/repository/commandlinetools-linux-6514223_latest.zip" -o "$TOOLS_ZIP"
+          unzip -q "$TOOLS_ZIP" -d "$TMP_DIR"
+          if [[ -d "$TMP_DIR/cmdline-tools" ]]; then
+            SRC_DIR="$TMP_DIR/cmdline-tools"
+          elif [[ -d "$TMP_DIR/tools" ]]; then
+            SRC_DIR="$TMP_DIR/tools"
+          else
+            echo "cmdline-tools not found in archive"
+            exit 1
+          fi
+          rm -rf "$SDK_ROOT/cmdline-tools/latest"
+          mv "$SRC_DIR" "$SDK_ROOT/cmdline-tools/latest"
+          rm -rf "$TMP_DIR"
+          mkdir -p "$SDK_ROOT/tools/bin"
+          ln -sf "$SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" "$SDK_ROOT/tools/bin/sdkmanager"
+          yes | "$SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" --licenses
```

```diff
--- a/.github/workflows/remote-build.yml
+++ b/.github/workflows/remote-build.yml
@@
-          sudo apt-get install -y build-essential ccache git zip unzip libffi-dev libssl-dev libbz2-dev libncurses5-dev libncursesw5-dev zlib1g-dev openjdk-17-jdk python3 python3-pip python3-dev liblzma-dev
+          sudo apt-get install -y build-essential ccache git zip unzip libffi-dev libssl-dev libbz2-dev libncurses5-dev libncursesw5-dev zlib1g-dev openjdk-17-jdk python3 python3-pip python3-dev liblzma-dev autoconf automake libtool libtool-bin pkg-config libltdl-dev
```

```diff
--- a/.github/workflows/build.yml
+++ b/.github/workflows/build.yml
@@
-          sudo apt-get install -y build-essential ccache git zip unzip libffi-dev libssl-dev libbz2-dev libncurses5-dev libncursesw5-dev zlib1g-dev openjdk-17-jdk python3 python3-pip python3-dev liblzma-dev
+          sudo apt-get install -y build-essential ccache git zip unzip libffi-dev libssl-dev libbz2-dev libncurses5-dev libncursesw5-dev zlib1g-dev openjdk-17-jdk python3 python3-pip python3-dev liblzma-dev autoconf automake libtool libtool-bin pkg-config libltdl-dev
```

## 4) 使用方式 / 依赖 / 注意事项
- 触发 GitHub Actions（latest 分支）后 Android 构建将使用本地 `.buildozer` 目录。
- buildozer 将在需要时安装 SDK build-tools 以保证 Aidl 可用。
- workflow 会预装 commandline tools 并自动接受 License，避免 `sdkmanager` 不存在或交互式许可阻塞。
- 无新增依赖。

## 5) 风险点与回滚方案
- 风险：若依赖外部环境变量 `%BUILDOZER%` 的构建路径策略将不再生效；构建时会自动下载 SDK 组件（耗时增加）；额外下载 commandline tools 增加少量耗时。
- 回滚：将 `build_dir` 恢复为原值或删除；将 `android.skip_update` 改回 `True`；移除 workflow 中 SDK tools/license 步骤。

## 6) 后续可扩展与优化建议
- 若确需环境变量路径，改用 buildozer 支持的配置方式，或在 CI 里显式生成 buildozer.spec。

## 7) 记忆更新
- 已同步将本次变更要点写入 MCP Memory Worklog。
