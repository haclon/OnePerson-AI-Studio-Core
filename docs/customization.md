# 自定义配置指南

> 本指南将帮助你根据项目需求定制 OnePerson AI Studio Core。

---

## 📋 目录

1. [创建自定义技术栈预设](#创建自定义技术栈预设)
2. [调整模型选择策略](#调整模型选择策略)
3. [自定义角色规则](#自定义角色规则)
4. [修改诊断模式](#修改诊断模式)
5. [添加项目特定术语](#添加项目特定术语)

---

## 🔧 创建自定义技术栈预设

如果你的技术栈不在现有预设中，可以创建自己的配置文件。

### 步骤 1：复制现有预设

```bash
cd ~/OnePerson-AI-Studio-Core/presets
cp python-fastapi-vue3.json my-custom-preset.json
```

### 步骤 2：编辑配置文件

打开 `my-custom-preset.json`，修改参数：

```json
{
  "PROJECT_NAME": "",
  "PROJECT_ABBR": "",
  "TECH_STACK": "Node.js + Express + React + PostgreSQL",
  "FRONTEND_FRAMEWORK": "React 18",
  "UI_LIBRARY": "Ant Design",
  "FRONTEND_SRC_PATH": "src",
  "FRONTEND_EXT": "jsx,js,tsx,ts",
  "API_DIR": "src/api/*",
  "BACKEND_FRAMEWORK": "Express",
  "ORM": "Prisma",
  "BACKEND_SRC_PATH": "src",
  "STATE_MANAGEMENT": "Redux Toolkit",
  "COMMENT_LANGUAGE": "中文",
  "ENCODING": "UTF-8",
  "PREFERRED_MODEL_FE": "GPT-5.2",
  "PREFERRED_MODEL_BE": "GPT-5.2"
}
```

### 步骤 3：使用自定义预设

```bash
python ~/OnePerson-AI-Studio-Core/scripts/install.py \
  --preset my-custom-preset \
  --name "我的项目" \
  --abbr "MyApp"
```

### 参数说明

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `TECH_STACK` | string | 完整技术栈描述 | `"Django + Vue 3 + PostgreSQL"` |
| `FRONTEND_FRAMEWORK` | string | 前端框架名称 | `"React 18"`, `"Angular 16"` |
| `UI_LIBRARY` | string | UI 组件库 | `"Ant Design"`, `"Material-UI"` |
| `FRONTEND_SRC_PATH` | string | 前端源码相对路径 | `"src"`, `"frontend/src"` |
| `FRONTEND_EXT` | string | 前端文件扩展名（逗号分隔） | `"jsx,tsx,js,ts"` |
| `API_DIR` | string | API 封装目录 | `"src/api/*"`, `"services/*"` |
| `BACKEND_FRAMEWORK` | string | 后端框架名称 | `"Django"`, `"Gin"`, `"Spring Boot"` |
| `ORM` | string | ORM 框架 | `"Prisma"`, `"TypeORM"`, `"GORM"` |
| `BACKEND_SRC_PATH` | string | 后端源码相对路径 | `"src"`, `"backend/app"` |
| `STATE_MANAGEMENT` | string | 状态管理库 | `"Redux"`, `"MobX"`, `"Zustand"` |
| `COMMENT_LANGUAGE` | string | 注释语言 | `"中文"`, `"English"` |
| `PREFERRED_MODEL_FE` | string | 前端推荐模型 | `"GPT-5.2"`, `"Codex Max"` |
| `PREFERRED_MODEL_BE` | string | 后端推荐模型 | `"GPT-5.2"`, `"Codex Max"` |

---

## 🎯 调整模型选择策略

如果你想修改模型推荐逻辑，编辑 `.cursorrules` 文件。

### 位置

`.cursorrules` 第 5-6 节：模型能力边界和模型选择策略

### 示例：调整成本优先级

**场景**：你想更激进地省钱，优先使用便宜的模型。

**修改前**：
```markdown
| 日常写代码 | **GPT-5.2** | 便宜够用 |
```

**修改后**：
```markdown
| 日常写代码 | **Codex Mini** | 最便宜 |
```

### 示例：调整质量优先级

**场景**：你不在意成本，优先使用最强模型。

**修改前**：
```markdown
| 讨论需求/理清思路 | **Sonnet 4.5** | 理解能力强 |
```

**修改后**：
```markdown
| 讨论需求/理清思路 | **Opus 4.5** | 理解能力最强 |
```

---

## 👤 自定义角色规则

### 修改现有角色

**位置**：`.cursor/rules/*.mdc`

**示例**：为前端开发专家添加特定规则

编辑 `.cursor/rules/fe_developer.mdc`：

```markdown
## 2. 行为禁忌
- 严禁在页面组件中直接书写HTTP请求（必须走API封装层）
- 严禁绕过 Element Plus 变量强行写死样式值
- 禁止在单个文件中编写超过500行的逻辑
+ 禁止使用 any 类型，必须明确定义类型           # 新增
+ 禁止在组件中直接操作 localStorage             # 新增
```

### 创建新角色

**场景**：你想添加一个"DevOps 专家"角色。

**步骤 1**：创建新文件

```bash
touch .cursor/rules/devops_specialist.mdc
```

**步骤 2**：编写规则

```markdown
---
description: 当涉及CI/CD配置、Docker容器化、K8s部署或服务器运维时触发。
globs: **/.github/workflows/*, **/Dockerfile, **/docker-compose.yml, **/k8s/**/*
---

# 角色：DevOps-运维专家

你现在的角色是 MyApp 项目的 DevOps 运维专家。你精通容器化、自动化部署和云原生技术。

## 1. 核心职责
- 编写高效的 CI/CD 流水线
- 优化 Docker 镜像大小和构建速度
- 设计可扩展的 K8s 部署方案
- 监控和日志系统配置

## 2. 行为禁忌
- 严禁在生产环境直接运行未测试的脚本
- 严禁硬编码敏感信息（密码、Token）

## 3. 工作约束
- 优先推荐使用 GPT-5.2
- 所有配置必须使用环境变量
- 必须包含回滚方案
```

**步骤 3**：测试

打开 `Dockerfile` 或 `.github/workflows/*.yml`，AI 应该自动识别为 DevOps 专家。

---

## 🔍 修改诊断模式

### 添加新的任务类型

**位置**：`.cursorrules` 第 3.1 节

**示例**：添加"重构"任务类型

```markdown
**示例**：
- `? 加个字段` → `[写代码] GPT-5.2 + BE-后端开发 (后端字段改动)`
- `? 这个需求怎么拆` → `[讨论] Sonnet 4.5 + Spec-平台架构师 (需求澄清)`
- `? 批量重命名变量` → `[批量] Grok Code + Batch-机械改动 (机械操作)`
+ `? 这段代码需要重构` → `[重构] Opus 4.5 + Spec-平台架构师 (架构优化)`  # 新增
```

### 修改触发符号

如果你不喜欢 `?`，可以改为其他符号：

**修改前**：
```markdown
当用户输入以 **`?`** 或 **`/task`** 开头时
```

**修改后**：
```markdown
当用户输入以 **`!`** 或 **`@task`** 开头时
```

**注意**：修改后需要重新加载 Cursor 项目。

---

## 📚 添加项目特定术语

如果你的项目有特定的业务术语，可以在 `.cursorrules` 中添加。

### 步骤 1：在 `.cursorrules` 末尾添加新节

```markdown
## 11. 项目术语表

### 11.1 核心概念

| 术语 | 英文 | 说明 |
|------|------|------|
| 订单 | Order | 用户下单后生成的记录 |
| SKU | Stock Keeping Unit | 商品的最小库存单元 |
| 库存 | Inventory | 可售商品数量 |

### 11.2 业务流程

- **下单流程**：用户选商品 → 加购物车 → 提交订单 → 支付 → 发货
- **退款流程**：申请退款 → 审核 → 退款 → 更新库存
```

### 步骤 2：更新角色规则（可选）

在相关角色的 `.mdc` 文件中引用这些术语：

```markdown
## 1. 核心职责
- 实现订单管理相关接口（参考 .cursorrules 第 11 节术语表）
- 处理 SKU 库存逻辑
```

---

## 🔄 调整 globs 匹配规则

`globs` 决定哪些文件会触发特定角色。

### 基本语法

- `**/*` - 匹配所有文件
- `*.vue` - 匹配根目录的 .vue 文件
- `**/*.vue` - 递归匹配所有 .vue 文件
- `src/**/*.ts` - 匹配 src 目录下的所有 .ts 文件
- `{*.js,*.ts}` - 匹配 .js 或 .ts 文件

### 示例：调整前端规则触发范围

**修改前**（只匹配 frontend/src）：
```yaml
globs: frontend/src/**/*.vue, frontend/src/**/*.js, frontend/src/**/*.scss
```

**修改后**（匹配多个前端目录）：
```yaml
globs: frontend/**/*.{vue,js,jsx,ts,tsx}, src/components/**/*
```

### 示例：排除特定文件

如果你不想在某些文件中触发规则：

```yaml
globs: backend/app/**/*.py, !backend/app/tests/**/*
```

（`!` 表示排除）

---

## 🎨 自定义输出模板

某些角色有"输出模板"，你可以根据需要调整。

### 示例：修改 PRD 输出模板

**位置**：`.cursor/rules/prd_analyst.mdc` 第 4 节

**修改前**：
```markdown
【背景】业务场景与用户痛点
【目标】要解决什么问题
【范围】包含什么 / 不包含什么
【验收标准】如何判断需求已满足
【优先级】高 / 中 / 低（及理由）
```

**修改后**（添加时间估算）：
```markdown
【背景】业务场景与用户痛点
【目标】要解决什么问题
【范围】包含什么 / 不包含什么
【验收标准】如何判断需求已满足
【优先级】高 / 中 / 低（及理由）
+ 【时间估算】预计开发时间（人天）
```

---

## 💡 高级技巧

### 技巧 1：为不同环境创建不同配置

如果你在多个项目中使用不同的规则：

```bash
# 为开源项目使用宽松规则
python install.py --preset open-source-friendly

# 为企业项目使用严格规则
python install.py --preset enterprise-strict
```

### 技巧 2：版本控制最佳实践

**推荐**：将 `.cursorrules` 和 `.cursor/` 纳入版本控制

```bash
git add .cursorrules .cursor/
git commit -m "feat: 添加 AI 协作规则"
```

**好处**：
- 团队成员克隆后立即拥有统一环境
- 规则变更可追溯
- 可以为不同分支使用不同规则

### 技巧 3：使用环境变量

如果你有敏感信息不想写在配置文件中：

在 `.cursorrules` 中引用环境变量：
```markdown
- **API Base URL**: 使用环境变量 `$API_BASE_URL`
```

---

## 📊 示例：完整的自定义工作流

### 场景：为电商项目定制

**1. 创建预设**（`presets/ecommerce-stack.json`）：
```json
{
  "TECH_STACK": "Next.js + NestJS + PostgreSQL + Redis",
  "FRONTEND_FRAMEWORK": "Next.js 14",
  "BACKEND_FRAMEWORK": "NestJS",
  ...
}
```

**2. 添加术语表**（`.cursorrules`）：
```markdown
## 11. 电商术语表
| 术语 | 说明 |
|------|------|
| SPU | 标准产品单元 |
| SKU | 库存量单位 |
```

**3. 创建专属角色**（`.cursor/rules/ecommerce_specialist.mdc`）：
```markdown
---
description: 处理订单、库存、支付等电商业务逻辑时触发
globs: **/orders/*, **/inventory/*, **/payments/*
---
...
```

**4. 安装并测试**：
```bash
python install.py --preset ecommerce-stack --name "我的电商" --abbr "MyShop"
```

---

## 🆘 故障排除

### 问题1：修改后不生效

**解决**：在 Cursor 中重新加载项目
- Windows/Linux: `Ctrl+Shift+P` → "Reload Window"
- Mac: `Cmd+Shift+P` → "Reload Window"

### 问题2：规则冲突

**现象**：多个角色同时触发

**解决**：调整 `globs` 确保不重叠，或使用更具体的路径

### 问题3：参数替换不完整

**现象**：文件中还有 `{{参数}}`

**解决**：
```bash
# 检查所有未替换的参数
grep -r "{{" .cursorrules .cursor/rules/
```

---

## 📖 更多资源

- [快速开始](quick-start.md) - 基本安装流程
- [常见问题](FAQ.md) - 更多问题解答
- [GitHub Issues](https://github.com/haclon/OnePerson-AI-Studio-Core/issues) - 报告问题或建议

---

**享受定制化的 AI 协作体验！** ✨

