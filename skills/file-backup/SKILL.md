---
name: file-backup
description: 备份项目中的单个文件。
---

# 文件备份

## 备份目录

- 用户已指定备份目录时，使用用户指定的目录。
- 否则，遵循适用的 AGENTS.md 中关于备份目录的明确规定。
- 没有明确规定时，询问用户备份目录，默认选项为项目根目录下的 backup/；等待用户选择或接受默认目录后再使用。
- 用户选择或接受默认目录后，将该约定记录到项目根目录的 AGENTS.md；文件不存在时创建。
- 记录时仅新增或更新备份目录约定，保留其他内容，避免重复记录。
- 后续任务读取该约定，不再重复询问；用户要求更换目录时同步更新。
- 已有备份不自动迁移；已明确配置的备份目录继续按配置使用。

## 执行备份

使用环境中可用的 Python 3 命令（如 `python` 或 `python3`）调用 [scripts/backup.py](scripts/backup.py)，由脚本生成目录和文件名；正常使用直接执行，无需读取源码。

```text
python "<skill-directory>/scripts/backup.py" --project-root "<project-root>" --backup-dir "<backup-directory>" --source "src/config.yaml" --description "modify-config" --tag configuration --tag backend
```

- 将 `<skill-directory>` 替换为本技能的实际目录；`--project-root` 使用项目根目录的绝对路径。
- `--backup-dir` 使用上述规则确定的目录；它与 `--source` 均可使用绝对路径或相对于项目根目录的路径。源文件必须位于项目内。
- `--description` 必填且不得为空；`--tag` 可省略、可重复。参数只传描述或标签本身，分隔符由脚本添加。

成功时退出码为 `0`，仅输出实际备份路径；失败时根据错误信息修正参数或处理文件操作问题后再调用。同名备份不会被覆盖。

## 存储布局

每个源文件对应一个备份目录，`<source-relative-path>` 包含源文件名，例如 `src/config.yaml`：

```text
<backup-directory>/files/<source-relative-path>/
```

## 备份文件名

备份文件名必须使用以下一种格式：

```text
<timestamp>--<description><extension>
<timestamp>--<description>+<tag>[+<tag>...]<extension>
```

- `<timestamp>` 使用本机当地时间，格式为 `YYYYMMDD-HHmmss`，例如 `20260730-153000`。
- `<description>` 描述本次操作，便于按备份目的查找；`<tag>` 标记类别或模块，便于筛选。
- 描述前使用 `--`，每个标签前使用 `+`；描述和标签不得为空，也不得包含保留分隔符 `--` 或 `+`。
- 名称字段中的 `\ / : * ? " < > |` 替换为 `-` 后，必须采用小写 kebab-case，并匹配 `[a-z0-9]+(?:-[a-z0-9]+)*`。
- `<extension>` 保留源文件的扩展名。

例如，`src/config.yaml` 的备份位于 `<backup-directory>/files/src/config.yaml/`，文件名可以是：

```text
20260730-153000--modify-config.yaml
20260730-153000--modify-config+configuration+backend.yaml
```
