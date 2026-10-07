# Skillbox

可复用的智能体技能集合。

- [file-backup](skills/file-backup/SKILL.md)：约定单个文件备份的目录与命名规则。
- [md-first-confirm](skills/md-first-confirm/SKILL.md)：用户要求修改前审核时，先提供 Markdown 草稿，确认后再执行。

## 安装

可以使用 [`npx skills`](https://github.com/vercel-labs/skills) 安装本仓库中的技能。以下命令会交互式选择安装目标 Agent。

### GitHub（默认）

单独安装某个技能：

```bash
npx skills add YangtzeCoder/skillbox --skill file-backup
npx skills add YangtzeCoder/skillbox --skill md-first-confirm
```

安装全部技能：

```bash
npx skills add YangtzeCoder/skillbox --skill '*'
```

### CNB

也可以从 CNB 安装：

```bash
npx skills add https://cnb.cool/xiong/skillbox.git --skill file-backup
npx skills add https://cnb.cool/xiong/skillbox.git --skill md-first-confirm
```

安装全部技能：

```bash
npx skills add https://cnb.cool/xiong/skillbox.git --skill '*'
```

### 更新

更新已安装的技能（包括从 GitHub 或 CNB 安装的技能）：

```bash
npx skills update
```
