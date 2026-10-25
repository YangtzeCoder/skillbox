# 仓库贡献指南

## 项目结构与模块组织

本仓库用于维护可复用的智能体技能。可发布技能位于 `skills/<skill-name>/`，项目专用 Codex 技能位于 `.agents/skills/<skill-name>/`：

- `skills/file-backup/`：规定单个文件备份的存储路径与命名规则。
- `skills/md-first-confirm/`：当用户要求修改前审核时，先提供 Markdown 草稿，获得明确确认后再修改。
- `.agents/skills/publish-skills/`：自动发现并分别打包 `skills/` 中的可发布技能到 `dist/`。




