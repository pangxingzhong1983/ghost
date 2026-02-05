# Ghost CI Android Buildozer Percent Fix (2026-02-05)

## 1) 用户需求 / 任务目的 / 背景
- 需求：远程构建失败，要求修复并保证 latest 分支可构建。
- 背景：Android job 在 buildozer 解析配置时失败；随后因缺少 build-tools 导致 Aidl 不可用；再后续因 SDK License 未接受而无法安装 build-tools。

## 2) 本次所有变更点
- 修复 buildozer 配置中 `build_dir` 的 `%BUILDOZER%` 插值导致的解析异常。
- 允许 buildozer 安装所需 SDK 组件，避免 build-tools 缺失。
- 在 Android workflow 中预置 SDK License 文件，避免交互式许可阻塞。

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
+      - name: Accept Android SDK licenses
+        run: |
+          SDK_LICENSE_DIR="$HOME/.buildozer/android/platform/android-sdk/licenses"
+          mkdir -p "$SDK_LICENSE_DIR"
+          echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > "$SDK_LICENSE_DIR/android-sdk-license"
+          echo "84831b9409646a918e30573bab4c9c91346d8abd" > "$SDK_LICENSE_DIR/android-sdk-preview-license"
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
+      - name: Accept Android SDK licenses
+        run: |
+          SDK_LICENSE_DIR="$HOME/.buildozer/android/platform/android-sdk/licenses"
+          mkdir -p "$SDK_LICENSE_DIR"
+          echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > "$SDK_LICENSE_DIR/android-sdk-license"
+          echo "84831b9409646a918e30573bab4c9c91346d8abd" > "$SDK_LICENSE_DIR/android-sdk-preview-license"
```

## 4) 使用方式 / 依赖 / 注意事项
- 触发 GitHub Actions（latest 分支）后 Android 构建将使用本地 `.buildozer` 目录。
- buildozer 将在需要时安装 SDK build-tools 以保证 Aidl 可用。
- workflow 会预置 SDK License 文件，避免 `sdkmanager` 交互式许可阻塞。
- 无新增依赖。

## 5) 风险点与回滚方案
- 风险：若依赖外部环境变量 `%BUILDOZER%` 的构建路径策略将不再生效；构建时会自动下载 SDK 组件（耗时增加）。
- 回滚：将 `build_dir` 恢复为原值或删除；将 `android.skip_update` 改回 `True`；移除 workflow 中 License 预置步骤。

## 6) 后续可扩展与优化建议
- 若确需环境变量路径，改用 buildozer 支持的配置方式，或在 CI 里显式生成 buildozer.spec。

## 7) 记忆更新
- 已同步将本次变更要点写入 MCP Memory Worklog。
