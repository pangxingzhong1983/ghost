# Ghost CI Android Buildozer Percent Fix (2026-02-05)

## 1) 用户需求 / 任务目的 / 背景
- 需求：远程构建失败，要求修复并保证 latest 分支可构建。
- 背景：Android job 在 buildozer 解析配置时失败。

## 2) 本次所有变更点
- 修复 buildozer 配置中 `build_dir` 的 `%BUILDOZER%` 插值导致的解析异常。

## 3) 变更前后差异对照
```diff
--- a/client/android_sources/buildozer-docker.spec
+++ b/client/android_sources/buildozer-docker.spec
@@
-build_dir = %BUILDOZER%
+build_dir = .buildozer
```

## 4) 使用方式 / 依赖 / 注意事项
- 触发 GitHub Actions（latest 分支）后 Android 构建将使用本地 `.buildozer` 目录。
- 无新增依赖。

## 5) 风险点与回滚方案
- 风险：若依赖外部环境变量 `%BUILDOZER%` 的构建路径策略将不再生效。
- 回滚：将该行恢复为原值或直接删除 `build_dir` 让 buildozer 使用默认值。

## 6) 后续可扩展与优化建议
- 若确需环境变量路径，改用 buildozer 支持的配置方式，或在 CI 里显式生成 buildozer.spec。

## 7) 记忆更新
- 已同步将本次变更要点写入 MCP Memory Worklog。
