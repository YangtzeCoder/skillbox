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

脚本自动扫描仓库 `skills/` 的直接子目录，将每个包含 `SKILL.md` 的目录视为一个可发布技能，并生成 `dist/<目录名>.zip`。每个 ZIP 的根目录直接包含该技能文件夹内的文件，子目录层级保持不变。新技能满足上述目录结构后会自动包含在发布结果中。此项目专用技能位于 `.agents/skills/`，不会作为发布内容打包。

脚本会创建 `dist/` 并覆盖同名 ZIP。所有当前技能打包成功后，会删除 `dist/` 中不再对应当前技能的 ZIP，其他文件保持不变。成功时会输出每个生成的压缩包路径；执行失败时，根据错误信息处理文件或权限问题后重试。
