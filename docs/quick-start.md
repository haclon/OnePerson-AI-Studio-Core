# 快速开始指南

> 本指南将帮助你在 **5 分钟内** 为新项目配置 OnePerson AI Studio Core。

---

## 前置要求

在开始之前，请确保你已安装：

- ✅ [Cursor](https://cursor.sh/) 编辑器
- ✅ Git
- ✅ Python 3.10+ （用于运行安装脚本）

---

## 🚀 方式 1：自动化安装（推荐）

### 步骤 1：克隆仓库

```bash
# 克隆到本地（一次性操作）
git clone https://github.com/haclon/OnePerson-AI-Studio-Core.git ~/OnePerson-AI-Studio-Core
```

### 步骤 2：进入你的项目目录

```bash
# 进入你想配置的项目
cd /path/to/your-project
```

### 步骤 3：运行安装脚本（交互式）

```bash
python ~/OnePerson-AI-Studio-Core/scripts/install.py --interactive
```

**脚本会询问：**
1. 选择技术栈预设（如 python-fastapi-vue3）
2. 输入项目名称（全称）
3. 输入项目缩写（英文）

**脚本会自动：**
- ✅ 生成 `.cursorrules` 文件
- ✅ 创建 `.cursor/rules/` 目录并生成 6 个 `.mdc` 文件
- ✅ 替换所有参数为你的项目信息

### 步骤 4：重新加载 Cursor

在 Cursor 中：
- **Windows/Linux**: `Ctrl+Shift+P` → "Reload Window"
- **Mac**: `Cmd+Shift+P` → "Reload Window"

### 步骤 5：测试诊断模式

在 Cursor 中输入：
```
? 我想加个登录功能
```

如果看到类似输出，说明安装成功：
```
[写代码] GPT-5.2 + BE-后端开发 (后端逻辑实现)
```

---

## 📋 方式 2：手动安装

如果你更喜欢手动控制，或者遇到脚本问题。

### 步骤 1：复制模板文件

```bash
# 克隆仓库（如果还没有）
git clone https://github.com/haclon/OnePerson-AI-Studio-Core.git

# 进入你的项目目录
cd your-project

# 复制 .cursorrules
cp ../OnePerson-AI-Studio-Core/templates/.cursorrules.template .cursorrules

# 复制 .cursor/rules/
mkdir -p .cursor/rules
cp ../OnePerson-AI-Studio-Core/templates/.cursor/rules/*.template .cursor/rules/
```

### 步骤 2：重命名模板文件

```bash
# 在 .cursor/rules/ 目录中，去掉所有 .template 后缀
cd .cursor/rules
for file in *.template; do mv "$file" "${file%.template}"; done
```

### 步骤 3：手动替换参数

打开 `.cursorrules` 和所有 `.cursor/rules/*.mdc` 文件，替换以下参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| `{{PROJECT_NAME}}` | 项目全称 | `我的电商平台` |
| `{{PROJECT_ABBR}}` | 项目缩写 | `MyShop` |
| `{{TECH_STACK}}` | 技术栈 | `Vue 3 + FastAPI` |
| `{{FRONTEND_FRAMEWORK}}` | 前端框架 | `Vue 3` |
| `{{UI_LIBRARY}}` | UI 库 | `Element Plus` |
| `{{FRONTEND_SRC_PATH}}` | 前端源码路径 | `frontend/src` |
| `{{FRONTEND_EXT}}` | 前端文件扩展名 | `vue,js,scss` |
| `{{API_DIR}}` | API 目录 | `src/api/*` |
| `{{BACKEND_FRAMEWORK}}` | 后端框架 | `FastAPI` |
| `{{ORM}}` | ORM 框架 | `SQLAlchemy 2.0` |
| `{{BACKEND_SRC_PATH}}` | 后端源码路径 | `backend/app` |
| `{{STATE_MANAGEMENT}}` | 状态管理 | `Pinia` |
| `{{COMMENT_LANGUAGE}}` | 注释语言 | `中文` |
| `{{ENCODING}}` | 编码格式 | `UTF-8` |
| `{{PREFERRED_MODEL_FE}}` | 前端推荐模型 | `GPT-5.2` |
| `{{PREFERRED_MODEL_BE}}` | 后端推荐模型 | `GPT-5.2` |

**技巧**：使用编辑器的"查找替换"功能批量替换。

### 步骤 4：验证

检查是否还有未替换的 `{{参数}}`：

```bash
# 在项目根目录
grep -r "{{" .cursorrules .cursor/rules/
```

如果没有输出，说明所有参数都已替换。

---

## 🔍 验证安装

### 测试 1：检查文件

确认以下文件存在：
- ✅ `.cursorrules`
- ✅ `.cursor/rules/fe_developer.mdc`
- ✅ `.cursor/rules/be_developer.mdc`
- ✅ `.cursor/rules/prd_analyst.mdc`
- ✅ `.cursor/rules/spec_architect.mdc`
- ✅ `.cursor/rules/qa_reviewer.mdc`
- ✅ `.cursor/rules/batch_processor.mdc`

### 测试 2：诊断模式

在 Cursor 中测试以下命令：

```
? 加个字段
→ 应推荐 GPT-5.2 + BE-后端开发

? 这个需求怎么拆
→ 应推荐 Sonnet 4.5 + PRD-需求分析

? 批量重命名变量
→ 应推荐 Grok Code + Batch-机械改动
```

### 测试 3：角色触发

打开一个前端文件（如 `.vue`），AI 应该自动识别为前端专家。

---

## ❓ 常见问题

### Q1: 安装脚本报错找不到模块？

**A**: 确保使用 Python 3.10+：
```bash
python --version
# 应该显示 Python 3.10 或更高
```

### Q2: 诊断模式不工作？

**A**: 
1. 确认 `.cursorrules` 文件存在且参数已替换
2. 在 Cursor 中重新加载项目
3. 检查是否有语法错误（如未闭合的引号）

### Q3: 角色没有自动触发？

**A**: 
1. 检查 `.cursor/rules/*.mdc` 文件的 `globs` 参数是否与你的项目结构匹配
2. 确认文件扩展名正确（如 `.vue`, `.js`, `.py`）

### Q4: 想修改某个参数怎么办？

**A**: 
1. 直接编辑 `.cursorrules` 或相应的 `.mdc` 文件
2. 无需重新运行安装脚本
3. 修改后重新加载 Cursor 项目

---

## 🎯 下一步

安装完成后，建议：

1. **阅读文档**：
   - [自定义配置](customization.md) - 了解如何调整规则
   - [常见问题](FAQ.md) - 查看更多问题和解决方案

2. **试用功能**：
   - 使用 `?` 诊断不同类型的任务
   - 打开不同类型的文件，观察角色切换

3. **创建自己的预设**：
   - 如果你的技术栈不在预设中
   - 参考 `presets/python-fastapi-vue3.json` 创建新的配置

---

## 💡 小技巧

### 快速切换模型

在对话中明确指定模型：
```
用 Opus 4.5 帮我分析这个复杂的 Bug
```

### 保存工作区配置

如果你的项目有特殊的规则调整，建议：
1. 将 `.cursorrules` 和 `.cursor/` 加入版本控制
2. 团队成员克隆后立即拥有统一的 AI 协作环境

### 定期更新

OnePerson AI Studio Core 会持续更新：
```bash
# 拉取最新模板
cd ~/OnePerson-AI-Studio-Core
git pull

# 在你的项目中重新运行安装脚本（可选）
```

---

**祝你使用愉快！** 🚀

如有问题，请访问 [GitHub Issues](https://github.com/haclon/OnePerson-AI-Studio-Core/issues)

