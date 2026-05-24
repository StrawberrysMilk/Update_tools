# 更新管理工具 (Update Tools)

单机桌面应用，用于集中管理多套系统的运维信息和更新台账。

## 功能（规划）

- [x] 主密码加密存储（AES-256-GCM + PBKDF2）
- [x] SQLite 本地数据库
- [x] 系统/连接入口管理（CRUD）
- [x] 一键打开：RDP（mstsc）、SSH（终端）、浏览器
- [x] 更新方式管理（SSH命令/SFTP/手动等）+ 一键执行
- [x] 更新历史台账（谁、何时、什么版本、状态）
- [x] 导入现有 Excel
- [x] PyInstaller 打包成单文件 exe
- [x] 现代化 UI 界面（渐变蓝色工具栏 + 圆角卡片风格）

## 运行方式（开发）

需要 Python 3.10+。

```bash
pip install -r requirements.txt
python main.py
```

首次启动会要求设置一个主密码，**请务必牢记**——它用于派生加密密钥，丢失后已加密的密码字段无法恢复。

## 打包成 exe

方式一（推荐，Windows 上运行）：
```bash
build.bat
```

方式二（手动）：
```bash
pip install pyinstaller
pyinstaller update_tools.spec
```

产出在 `dist/UpdateTools.exe`，双击即可运行，无需安装 Python。

## 界面预览

- 工具栏：渐变蓝色，白色文字按钮
- 左侧：系统列表，选中高亮
- 右侧 Tab 页：
  - **连接条目**：表格 + 一键打开按钮
  - **更新方式**：表格 + ▶执行按钮（执行后自动提示记录台账）
  - **更新历史**：时间线式台账

## 数据存放位置

- Windows: `%APPDATA%\UpdateTools\`
- Linux/macOS: `~/.config/UpdateTools/`

包含：
- `data.db` —— SQLite 数据库
- `meta.json` —— 加密盐 + 校验密文（不含主密码本身）

⚠️ 这两个文件请勿提交到 Git。

## Excel 导入格式

| 列 | 内容 |
|----|------|
| A  | 系统名称 |
| B  | 远程地址（RDP） |
| C  | 浏览器运维地址 |
| D  | 运维账号 |
| E  | 运维密码 |
| F  | 远程账号 |
| G  | 远程密码 |
| H  | 系统账号 |
| I  | 系统密码 |

第 1 行为表头（自动跳过），从第 2 行开始导入。
