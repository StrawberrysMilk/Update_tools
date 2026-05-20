# 更新管理工具 (Update Tools)

单机桌面应用，用于集中管理多套系统的运维信息和更新台账。

## 功能（规划）

- [x] 主密码加密存储（AES-256-GCM + PBKDF2）
- [x] SQLite 本地数据库
- [ ] 系统 / 连接条目管理（CRUD）
- [ ] 一键打开：RDP（mstsc）、SSH（终端）、浏览器
- [ ] 更新方式管理（SSH 命令 / SFTP / 手工等）
- [ ] 更新历史台账（谁、何时、什么版本、状态）
- [ ] 导入现有 Excel
- [ ] PyInstaller 打包成单文件 exe

当前进度：**骨架版本**，可以启动、设置主密码、添加系统名称。

## 运行方式（开发）

需要 Python 3.10+。

```bash
pip install -r requirements.txt
python main.py
```

首次启动会要求设置一个主密码，**请务必牢记**——它用于派生加密密钥，丢失后已加密的密码字段无法恢复。

## 数据存放位置

- Windows: `%APPDATA%\UpdateTools\`
- Linux/macOS: `~/.config/UpdateTools/`

包含：
- `data.db` —— SQLite 数据库
- `meta.json` —— 加密盐 + 校验密文（不含主密码本身）

⚠️ 这两个文件请勿提交到 Git。
