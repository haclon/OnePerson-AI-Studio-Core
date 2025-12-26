# OnePerson AI Studio Core

> 一人公司开发者的 AI 协作框架 - 让 AI 助手更懂你的项目

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 这是什么？

一套**可配置、可复用的 Cursor AI 规则框架**，让你在任何新项目中 **1 分钟内** 配置好 AI 协作环境。

### 核心特性

✅ **诊断模式** (`?`命令) - 自动推荐最合适的模型和 Agent 角色  
✅ **多角色分工** - 6 大专家角色各司其职（PRD/Spec/FE/BE/QA/Batch）  
✅ **成本优化** - 质量 > 成本 > 时间的模型选择策略  
✅ **跨技术栈** - 支持 Python/Node.js/Go + Vue/React/Angular  
✅ **开箱即用** - 提供常见技术栈预设配置

### 为什么需要它？

如果你是一人公司或小团队开发者，可能会遇到：
- ❌ 每次新项目都要重新配置 Cursor 规则
- ❌ AI 不知道该用哪个模型，经常用贵的模型做简单任务
- ❌ 缺乏统一的代码规范，AI 生成的代码风格不一致

这个框架帮你一次配置，处处复用。

---

## 🚀 快速开始

### 前置要求

- [Cursor](https://cursor.sh/) 编辑器
- Git
- Python 3.10+ 或 Node.js 18+（用于运行安装脚本）

### 方式 1：手动配置（当前可用）

```bash
# 1. 克隆仓库
git clone https://github.com/haclon/OnePerson-AI-Studio-Core.git

# 2. 进入你的项目目录
cd 你的项目目录

# 3. 复制模板文件
cp ../OnePerson-AI-Studio-Core/templates/.cursorrules.template .cursorrules
cp -r ../OnePerson-AI-Studio-Core/templates/.cursor .

# 4. 编辑 .cursorrules，替换所有 {{参数}}
# 参考 presets/python-fastapi-vue3.json 查看参数示例

# 5. 编辑 .cursor/rules/*.mdc，同样替换参数

# 6. 重新加载 Cursor 项目
```

### 方式 2：自动化安装脚本（开发中...）

```bash
# 未来将支持
python scripts/install.py --preset python-fastapi-vue3
```

---

## 📚 核心概念

### 1. 诊断模式 (`?` 命令)

在 Cursor 中输入 `?` 开头的问题，AI 会自动分析任务类型并推荐：

```
? 加个登录功能
→ [写代码] GPT-5.2 + BE-后端开发 (后端逻辑实现)

? 这个需求怎么拆
→ [讨论] Sonnet 4.5 + PRD-需求分析 (需求澄清)

? 批量重命名变量
→ [批量] Grok Code + Batch-机械改动 (机械操作)
```

### 2. 六大角色分工

| 角色 | 职责 | 推荐模型 |
|------|------|----------|
| **PRD-需求分析** | 用户痛点、需求拆解、业务边界 | Sonnet 4.5 |
| **Spec-平台架构师** | 系统架构、数据库方案、API 定义 | Sonnet/Opus 4.5 |
| **FE-前端开发** | Vue/React 组件、样式、API 调用 | GPT-5.2 |
| **BE-后端开发** | API 接口、Service 逻辑、数据库 | GPT-5.2 |
| **QA-回归审查** | Bug 定位、性能分析、代码审查 | GPT-5.2/Opus |
| **Batch-机械改动** | 批量重命名、格式化、样板代码 | Grok Code |

### 3. 模型选择策略

遵循 **质量 > 成本 > 时间** 原则：

| 任务类型 | 推荐模型 | 原因 |
|---------|----------|------|
| 讨论需求 | Sonnet 4.5 | 理解能力强，成本适中 |
| 写代码 | GPT-5.2 | 便宜够用 |
| 复杂 Bug | Opus 4.5 | 推理能力最强 |
| 批量操作 | Grok Code | 最便宜 |

---

## 🔧 技术栈预设

目前支持的预设配置：

### `python-fastapi-vue3` ✅
- **后端**：Python 3.10+ + FastAPI + SQLAlchemy
- **前端**：Vue 3 + Element Plus + Pinia
- **适用场景**：企业管理系统、数据平台

### 即将支持
- `nodejs-express-react` - Node.js + Express + React 18
- `golang-gin-vue3` - Go + Gin + Vue 3
- `django-vue` - Django + Vue 3

---

## 📖 文档

- [快速开始指南](docs/quick-start.md) _(开发中)_
- [自定义配置](docs/customization.md) _(开发中)_
- [常见问题](docs/FAQ.md) _(开发中)_
- [贡献指南](docs/contributing.md) _(开发中)_

---

## 🛠️ 项目结构

```
OnePerson-AI-Studio-Core/
├── templates/              # 核心模板文件
│   ├── .cursorrules.template
│   └── .cursor/rules/      # 6个角色规则文件
├── presets/                # 技术栈预设配置
│   └── python-fastapi-vue3.json
├── scripts/                # 安装和工具脚本
│   └── replace-template.py
├── docs/                   # 文档
└── README.md
```

---

## 🤝 贡献

欢迎贡献新的技术栈预设或改进建议！

### 如何贡献

1. Fork 本仓库
2. 创建新分支：`git checkout -b feature/my-preset`
3. 提交更改：`git commit -m "feat: 添加 XXX 预设"`
4. 推送分支：`git push origin feature/my-preset`
5. 提交 Pull Request

### 贡献类型

- ✨ 新增技术栈预设
- 📝 完善文档
- 🐛 修复 Bug
- 💡 提出改进建议

---

## 📝 开发状态

| 功能 | 状态 |
|------|------|
| 核心模板 | ✅ 已完成 |
| Python+Vue 预设 | ✅ 已完成 |
| 自动化安装脚本 | 🚧 开发中 |
| 完整文档 | 🚧 开发中 |
| Node.js 预设 | 📋 计划中 |
| Go 预设 | 📋 计划中 |

---

## 📜 License

MIT License - 自由使用、修改和分享

查看 [LICENSE](LICENSE) 文件了解详情。

---

## 💬 反馈与支持

- **Issues**: [GitHub Issues](https://github.com/haclon/OnePerson-AI-Studio-Core/issues)
- **Discussions**: [GitHub Discussions](https://github.com/haclon/OnePerson-AI-Studio-Core/discussions)

---

## 🌟 Star History

如果这个项目对你有帮助，欢迎给个 Star ⭐️

---

**由一人公司开发者，为一人公司开发者打造。**

> 在 AI 时代，一个人也可以是一支军队。
