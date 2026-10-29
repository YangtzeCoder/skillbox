---
name: publish-skills
description: 将仓库中所有技能分别打包到 dist/，适用于发布或重新生成技能 ZIP 包。
version: "1.0.0"
display_name: "发布技能"
display_name_en: "Publish Skills"
description_zh: "将仓库中所有技能分别打包到 dist/。"
description_en: "Package every skill in the repository into a separate ZIP archive under dist/."
---

# 发布技能

当用户要求打包、发布或重新生成本仓库的技能 ZIP 时，运行本技能脚本：

```text
python "<skill-directory>/scripts/package_skills.py"
```

将 `<skill-directory>` 替换为本技能目录的实际路径。脚本会根据自身位置定位仓库，不依赖当前工作目录，也不需要传入技能名称。

脚本自动扫描仓库 `skills/` 的直接子目录，将每个包含 `SKILL.md` 的目录视为一个可发布技能，并使用该技能 front matter 中的 `version` 生成 `dist/<目录名>-<版本号>.zip`，例如 `dist/file-backup-1.0.1.zip`。版本号必须非空，以字母或数字开头和结尾，中间仅允许字母、数字、`.`、`_`、`+` 和 `-`；可以使用单引号或双引号包裹。打包前会检查所有技能的版本号，缺失或无效时停止，不清理已有压缩包。每个 ZIP 的根目录直接包含该技能文件夹内的文件，子目录层级保持不变。新技能满足上述目录结构后会自动包含在发布结果中。此项目专用技能位于 `.agents/skills/`，不会作为发布内容打包。

脚本会创建 `dist/` 并覆盖同名 ZIP。所有当前技能打包成功后，会删除 `dist/` 中不属于当前版本的 ZIP，包括旧版本和不带版本号的压缩包，其他文件保持不变。成功时会输出每个生成的压缩包路径；执行失败时，根据错误信息处理文件或权限问题后重试。
