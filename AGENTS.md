# 仓库贡献指南

## 项目结构与模块组织

本仓库用于维护可复用的智能体技能。每个技能的说明文件位于 `skills/<skill-name>/SKILL.md`：

- `skills/file-backup/`：规定单个文件备份的存储路径与命名规则。
- `skills/md-first-confirm/`：当用户要求修改前审核时，先提供 Markdown 草稿，获得明确确认后再修改。

项目内部使用的技能位于 `.agents/skills/<skill-name>/SKILL.md`：

- `.agents/skills/sync-skills/`：将 `skills/` 中的技能同步到用户技能目录，更新同名文件并保留目标额外内容。




