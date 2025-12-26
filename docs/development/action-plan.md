# OnePerson-AI-Studio-Core 实施行动计划

> **决策结果**：采用方案4（独立仓库 + 脚本 + 预设配置），公开分享  
> **核心原则**：先验证，再扩展；从简单到完整  
> **预计总耗时**：5-7 天（分散到日常开发中）

---

## 🎯 总体策略：4 个阶段，逐步验证

```
阶段1（1-2天） → 阶段2（1-2天） → 阶段3（2-3天） → 阶段4（1天）
在BOQ中验证    创建独立仓库    编写脚本文档    新项目测试
```

---

## 📅 阶段 1：在 BOQ 项目中提取并验证第一个模板（1-2 天）

### 目标
验证"参数化规则"的可行性，确保 AI 能正确理解替换后的规则。

### 任务清单

#### 1.1 创建临时验证目录
```bash
mkdir -p .ai-studio-temp/templates
mkdir -p .ai-studio-temp/test
```

#### 1.2 提取并参数化 `.cursorrules`
- [ ] 复制当前的 `.cursorrules` 到 `.ai-studio-temp/templates/.cursorrules.template`
- [ ] 用 `{{}}` 替换所有项目特定信息：
  - `BOQ清单数据提取与标准化Web应用` → `{{PROJECT_NAME}}`
  - `BOQSE-Web` → `{{PROJECT_ABBR}}`
  - `Vue 3 + Element Plus + FastAPI + SQLAlchemy + SQLite/PostgreSQL` → `{{TECH_STACK}}`
- [ ] **删除**第 3 节"业务术语表"（完整删除 29-78 行）
- [ ] 保留其他所有内容

**验证点**：替换后的文件总行数应该约 160 行（原 210 行 - 50 行业务术语）

#### 1.3 提取并参数化第一个 `.mdc` 文件（选择 `fe_developer.mdc`）
- [ ] 复制 `.cursor/rules/fe_developer.mdc` 到 `.ai-studio-temp/templates/fe_developer.mdc.template`
- [ ] 替换参数：
  ```yaml
  # 原文件
  description: 当进行前端 Vue 3 页面开发、UI 组件编写、样式调整或 API 调用封装时触发。
  globs: frontend/src/**/*.vue, frontend/src/**/*.js, frontend/src/**/*.scss, docs/frontend-guidelines.md
  
  你现在的角色是 BOQSE-Web 项目的前端开发专家。你精通 Vue 3, Element Plus 和前端工程化。
  
  # 替换后
  description: 当进行前端{{FRONTEND_FRAMEWORK}}页面开发、UI组件编写、样式调整或API调用封装时触发。
  globs: {{FRONTEND_SRC_PATH}}/**/*.{{FRONTEND_EXT}}, docs/frontend-guidelines.md
  
  你现在的角色是 {{PROJECT_ABBR}} 项目的前端开发专家。你精通 {{FRONTEND_FRAMEWORK}}, {{UI_LIBRARY}} 和前端工程化。
  ```

#### 1.4 创建测试配置文件
创建 `.ai-studio-temp/test/boq-config.json`：
```json
{
  "PROJECT_NAME": "BOQ清单数据提取与标准化Web应用",
  "PROJECT_ABBR": "BOQSE-Web",
  "TECH_STACK": "Vue 3 + Element Plus + FastAPI + SQLAlchemy + SQLite/PostgreSQL",
  "FRONTEND_FRAMEWORK": "Vue 3",
  "UI_LIBRARY": "Element Plus",
  "FRONTEND_SRC_PATH": "frontend/src",
  "FRONTEND_EXT": "vue,js,scss",
  "BACKEND_FRAMEWORK": "FastAPI",
  "ORM": "SQLAlchemy 2.0",
  "BACKEND_SRC_PATH": "backend/app",
  "STATE_MANAGEMENT": "Pinia",
  "COMMENT_LANGUAGE": "中文",
  "ENCODING": "UTF-8"
}
```

#### 1.5 编写简单的 PowerShell 测试脚本
创建 `.ai-studio-temp/test-replace.ps1`：
```powershell
# 读取配置
$config = Get-Content ".ai-studio-temp/test/boq-config.json" | ConvertFrom-Json

# 读取模板
$template = Get-Content ".ai-studio-temp/templates/.cursorrules.template" -Raw

# 替换所有参数
foreach ($key in $config.PSObject.Properties.Name) {
    $value = $config.$key
    $template = $template -replace "{{\s*$key\s*}}", $value
}

# 输出到测试文件
Set-Content -Path ".ai-studio-temp/test/.cursorrules.test" -Value $template

Write-Host "✅ 替换完成！请检查 .ai-studio-temp/test/.cursorrules.test"
Write-Host "📊 原始模板行数: $((Get-Content '.ai-studio-temp/templates/.cursorrules.template').Count)"
Write-Host "📊 替换后行数: $((Get-Content '.ai-studio-temp/test/.cursorrules.test').Count)"
```

#### 1.6 验证结果
- [ ] 运行脚本：`powershell -File .ai-studio-temp/test-replace.ps1`
- [ ] 对比 `.ai-studio-temp/test/.cursorrules.test` 和原始 `.cursorrules`
- [ ] 检查是否有遗漏的 `{{}}` 标记
- [ ] 检查替换后的内容是否语义正确

#### 1.7 AI 理解测试（关键验证）
- [ ] **临时替换**：备份当前 `.cursorrules`，用 `.cursorrules.test` 替换
- [ ] **测试诊断模式**：输入 `? 加个字段` 看 AI 是否能正确推荐
- [ ] **测试角色触发**：打开 `frontend/src/views/xxx.vue`，输入一段代码，看是否触发 FE 规则
- [ ] **恢复原文件**：测试完成后恢复备份

**预期结果**：AI 的行为应该和替换前完全一致。

### 🎯 阶段 1 成功标准
- ✅ 参数替换脚本运行无错误
- ✅ 替换后的规则文件 AI 能正确理解
- ✅ 诊断模式 (`?`) 正常工作
- ✅ 角色触发（打开文件自动激活规则）正常工作

### ⚠️ 如果失败怎么办？
- **问题1**：替换后 AI 行为异常 → 检查是否有 `{{}}` 残留，或参数值有误
- **问题2**：`.mdc` 规则未触发 → 检查 `globs` 路径是否正确
- **问题3**：诊断模式不工作 → 检查 `.cursorrules` 中的示例是否还在

---

## 📅 阶段 2：创建独立 GitHub 仓库并迁移模板（1-2 天）

### 目标
将验证通过的模板迁移到独立仓库，建立标准化的目录结构。

### 任务清单

#### 2.1 创建 GitHub 仓库
- [ ] 登录 GitHub，创建新仓库：`OnePerson-AI-Studio-Core`
- [ ] 选择：公开仓库（Public）
- [ ] 初始化：勾选 "Add a README file"
- [ ] License：建议选择 MIT License
- [ ] `.gitignore`：选择 "None"（我们自己创建）

#### 2.2 克隆到本地
```bash
git clone https://github.com/你的用户名/OnePerson-AI-Studio-Core.git
cd OnePerson-AI-Studio-Core
```

#### 2.3 创建标准目录结构
```bash
mkdir -p templates/.cursor/rules
mkdir -p presets
mkdir -p docs
mkdir -p scripts
```

#### 2.4 迁移验证通过的模板
- [ ] 复制 `.ai-studio-temp/templates/.cursorrules.template` → `templates/.cursorrules.template`
- [ ] 复制 `.ai-studio-temp/templates/fe_developer.mdc.template` → `templates/.cursor/rules/fe_developer.mdc.template`

#### 2.5 提取其余 5 个 `.mdc` 模板
使用同样的参数化逻辑，提取：
- [ ] `prd_analyst.mdc.template`
- [ ] `spec_architect.mdc.template`
- [ ] `be_developer.mdc.template`
- [ ] `qa_reviewer.mdc.template`
- [ ] `batch_processor.mdc.template`

**技巧**：可以复用阶段1的替换脚本，批量处理。

#### 2.6 创建技术栈预设配置
创建 `presets/python-fastapi-vue3.json`（BOQ 项目的配置）：
```json
{
  "name": "Python FastAPI + Vue 3",
  "description": "适用于 Python 后端（FastAPI + SQLAlchemy）和 Vue 3 前端（Element Plus）",
  "params": {
    "TECH_STACK": "Vue 3 + Element Plus + FastAPI + SQLAlchemy + SQLite/PostgreSQL",
    "FRONTEND_FRAMEWORK": "Vue 3",
    "UI_LIBRARY": "Element Plus",
    "FRONTEND_SRC_PATH": "frontend/src",
    "FRONTEND_EXT": "vue,js,scss",
    "BACKEND_FRAMEWORK": "FastAPI",
    "ORM": "SQLAlchemy 2.0",
    "BACKEND_SRC_PATH": "backend/app",
    "STATE_MANAGEMENT": "Pinia",
    "COMMENT_LANGUAGE": "中文",
    "ENCODING": "UTF-8"
  }
}
```

额外创建 1-2 个常见预设（可选）：
- [ ] `presets/nodejs-express-react.json`
- [ ] `presets/golang-gin-vue3.json`

#### 2.7 创建模型定价矩阵
创建 `model-matrix.json`（从 `analysis-standardization.md` 提取）：
```json
{
  "models": [
    {
      "name": "Claude 4.5 Opus",
      "input_cost": 15,
      "output_cost": 75,
      "context": "200k",
      "networking": true,
      "use_cases": ["复杂推理", "需求澄清", "风险评估"]
    },
    {
      "name": "Claude 4.5 Sonnet",
      "input_cost": 3,
      "output_cost": 15,
      "context": "200k (Max: 1M)",
      "networking": true,
      "use_cases": ["理解需求", "写文档", "日常讨论"]
    }
    // ... 其他模型
  ],
  "last_updated": "2025-12-26"
}
```

#### 2.8 提交到 GitHub
```bash
git add .
git commit -m "feat: 初始化模板和预设配置"
git push origin main
```

### 🎯 阶段 2 成功标准
- ✅ GitHub 仓库创建成功，目录结构清晰
- ✅ 所有 7 个模板文件（1个 .cursorrules + 6个 .mdc）已迁移
- ✅ 至少 1 个技术栈预设配置可用
- ✅ 首次提交已推送到 GitHub

---

## 📅 阶段 3：编写安装脚本和使用文档（2-3 天）

### 目标
让用户能够"一键安装"规则到任意项目。

### 任务清单

#### 3.1 编写 Windows 安装脚本
创建 `install.ps1`（PowerShell 脚本）：

```powershell
# OnePerson AI Studio Core - Windows 安装脚本
# 使用方法: powershell -File install.ps1 [-Preset python-fastapi-vue3] [-Interactive]

param(
    [string]$Preset = "",
    [string]$ProjectName = "",
    [string]$ProjectAbbr = "",
    [switch]$Interactive = $false
)

Write-Host "🚀 OnePerson AI Studio Core - 项目初始化" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# 获取脚本所在目录（仓库根目录）
$REPO_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. 选择预设
if (-not $Preset -or $Interactive) {
    Write-Host "`n可用的技术栈预设:" -ForegroundColor Yellow
    $presetFiles = Get-ChildItem "$REPO_DIR/presets/*.json"
    for ($i = 0; $i -lt $presetFiles.Count; $i++) {
        $presetName = [System.IO.Path]::GetFileNameWithoutExtension($presetFiles[$i].Name)
        Write-Host "  $($i+1). $presetName"
    }
    $selection = Read-Host "`n请选择 (1-$($presetFiles.Count))"
    $Preset = [System.IO.Path]::GetFileNameWithoutExtension($presetFiles[$selection - 1].Name)
}

Write-Host "`n✅ 使用预设: $Preset" -ForegroundColor Green

# 2. 读取预设配置
$presetPath = "$REPO_DIR/presets/$Preset.json"
if (-not (Test-Path $presetPath)) {
    Write-Host "❌ 错误: 预设文件不存在: $presetPath" -ForegroundColor Red
    exit 1
}
$config = Get-Content $presetPath | ConvertFrom-Json

# 3. 获取项目信息
if (-not $ProjectName) {
    $ProjectName = Read-Host "`n项目名称（全称）"
}
if (-not $ProjectAbbr) {
    $ProjectAbbr = Read-Host "项目缩写（英文，如 MyApp）"
}

# 4. 替换并生成 .cursorrules
Write-Host "`n📝 正在生成 .cursorrules..." -ForegroundColor Yellow
$cursorrules = Get-Content "$REPO_DIR/templates/.cursorrules.template" -Raw

# 替换项目信息
$cursorrules = $cursorrules -replace "{{\s*PROJECT_NAME\s*}}", $ProjectName
$cursorrules = $cursorrules -replace "{{\s*PROJECT_ABBR\s*}}", $ProjectAbbr

# 替换技术栈参数
foreach ($key in $config.params.PSObject.Properties.Name) {
    $value = $config.params.$key
    $cursorrules = $cursorrules -replace "{{\s*$key\s*}}", $value
}

# 检查是否有未替换的参数
if ($cursorrules -match "{{\s*\w+\s*}}") {
    Write-Host "⚠️  警告: 发现未替换的参数，请检查模板和配置" -ForegroundColor Yellow
}

Set-Content -Path ".cursorrules" -Value $cursorrules -Encoding UTF8
Write-Host "   ✅ .cursorrules 已生成" -ForegroundColor Green

# 5. 生成 .cursor/rules/ 目录和 .mdc 文件
Write-Host "`n📁 正在生成 .cursor/rules/..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path ".cursor/rules" | Out-Null

$mdcFiles = Get-ChildItem "$REPO_DIR/templates/.cursor/rules/*.mdc.template"
foreach ($mdcFile in $mdcFiles) {
    $mdcContent = Get-Content $mdcFile.FullName -Raw
    
    # 替换参数（同样的逻辑）
    $mdcContent = $mdcContent -replace "{{\s*PROJECT_NAME\s*}}", $ProjectName
    $mdcContent = $mdcContent -replace "{{\s*PROJECT_ABBR\s*}}", $ProjectAbbr
    foreach ($key in $config.params.PSObject.Properties.Name) {
        $value = $config.params.$key
        $mdcContent = $mdcContent -replace "{{\s*$key\s*}}", $value
    }
    
    # 生成目标文件名（去掉 .template 后缀）
    $targetName = $mdcFile.Name -replace ".template$", ""
    Set-Content -Path ".cursor/rules/$targetName" -Value $mdcContent -Encoding UTF8
    Write-Host "   ✅ $targetName 已生成" -ForegroundColor Green
}

# 6. 创建文档目录（可选）
if (-not (Test-Path "docs")) {
    Write-Host "`n📚 正在创建 docs/ 目录..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path "docs" | Out-Null
    Write-Host "   ✅ docs/ 已创建（建议添加 frontend-guidelines.md, backend-guidelines.md）" -ForegroundColor Green
}

# 7. 创建 openspec/ 目录（可选）
if (-not (Test-Path "openspec")) {
    $createOpenSpec = Read-Host "`n是否初始化 OpenSpec 目录？(Y/n)"
    if ($createOpenSpec -ne "n") {
        Write-Host "📋 正在初始化 OpenSpec..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Force -Path "openspec/changes" | Out-Null
        New-Item -ItemType Directory -Force -Path "openspec/specs" | Out-Null
        Set-Content -Path "openspec/project.md" -Value "# 项目约定`n`n待补充..." -Encoding UTF8
        Write-Host "   ✅ OpenSpec 已初始化" -ForegroundColor Green
    }
}

# 8. 完成
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🎉 完成！AI 协作规则已安装" -ForegroundColor Green
Write-Host "`n下一步:" -ForegroundColor Yellow
Write-Host "  1. 打开 Cursor，加载当前项目"
Write-Host "  2. 试试诊断模式: ? 我想加个登录功能"
Write-Host "  3. 查看文档: https://github.com/你的用户名/OnePerson-AI-Studio-Core"
Write-Host ""
```

#### 3.2 编写 Linux/Mac 安装脚本（可选）
创建 `install.sh`（基本逻辑同 PowerShell 版本）

#### 3.3 编写主 README.md
创建仓库根目录的 `README.md`：

```markdown
# OnePerson AI Studio Core

> 一人公司开发者的 AI 协作框架 - 让 AI 助手更懂你的项目

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

### 方式 1：一键安装（推荐）

```bash
# 1. 克隆仓库到本地（一次性）
git clone https://github.com/你的用户名/OnePerson-AI-Studio-Core.git ~/OnePerson-AI-Studio-Core

# 2. 进入你的项目目录
cd 你的项目目录

# 3. 运行安装脚本
powershell -File ~/OnePerson-AI-Studio-Core/install.ps1 -Interactive
```

### 方式 2：指定预设快速安装

```bash
# Python + FastAPI + Vue 3
powershell -File ~/OnePerson-AI-Studio-Core/install.ps1 -Preset python-fastapi-vue3 -ProjectName "我的项目" -ProjectAbbr "MyApp"

# Node.js + Express + React
powershell -File ~/OnePerson-AI-Studio-Core/install.ps1 -Preset nodejs-express-react
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

### `python-fastapi-vue3`
- 后端：Python 3.10+ + FastAPI + SQLAlchemy
- 前端：Vue 3 + Element Plus + Pinia
- 适用：企业管理系统、数据平台

### `nodejs-express-react`（待补充）
- 后端：Node.js + Express + Prisma
- 前端：React 18 + Ant Design + Redux

### `golang-gin-vue3`（待补充）
- 后端：Go + Gin + GORM
- 前端：Vue 3 + Naive UI

---

## 📖 使用文档

- [快速开始](docs/quick-start.md)
- [自定义配置](docs/customization.md)
- [常见问题](docs/faq.md)
- [贡献指南](docs/contributing.md)

---

## 🤝 贡献

欢迎贡献新的技术栈预设！

1. Fork 本仓库
2. 在 `presets/` 下添加你的配置文件
3. 更新 README 的"技术栈预设"部分
4. 提交 Pull Request

---

## 📝 License

MIT License - 自由使用、修改和分享

---

## 💬 反馈与支持

- Issues: [GitHub Issues](https://github.com/你的用户名/OnePerson-AI-Studio-Core/issues)
- Discussions: [GitHub Discussions](https://github.com/你的用户名/OnePerson-AI-Studio-Core/discussions)

---

**由一人公司开发者，为一人公司开发者打造。**
```

#### 3.4 编写子文档
- [ ] `docs/quick-start.md` - 详细的安装和使用步骤
- [ ] `docs/customization.md` - 如何自定义参数和创建新预设
- [ ] `docs/faq.md` - 常见问题解答

#### 3.5 提交所有文档
```bash
git add .
git commit -m "docs: 添加安装脚本和使用文档"
git push origin main
```

### 🎯 阶段 3 成功标准
- ✅ `install.ps1` 脚本能正常运行
- ✅ 主 README.md 清晰易懂，有示例和截图
- ✅ 至少 2 篇子文档（quick-start + customization）

---

## 📅 阶段 4：在新项目中完整测试（1 天）

### 目标
验证整个流程在真实场景中的可用性。

### 任务清单

#### 4.1 创建测试项目
```bash
# 创建一个空项目（模拟全新项目）
mkdir test-new-project
cd test-new-project
npm init -y  # 或 python -m venv venv
```

#### 4.2 使用安装脚本
```bash
powershell -File ~/OnePerson-AI-Studio-Core/install.ps1 -Preset python-fastapi-vue3 -ProjectName "测试新项目" -ProjectAbbr "TestApp"
```

#### 4.3 验证生成的文件
- [ ] 检查 `.cursorrules` 是否正确生成
- [ ] 检查 `.cursor/rules/` 下是否有 6 个 `.mdc` 文件
- [ ] 打开文件，确认所有 `{{}}` 都已替换

#### 4.4 Cursor AI 功能测试
打开 Cursor，加载测试项目：
- [ ] 测试诊断模式：`? 我想加个用户模块`
- [ ] 测试角色触发：创建一个 `.vue` 文件，输入代码，看是否触发 FE 规则
- [ ] 测试模型推荐：问不同类型的问题，看是否推荐合适的模型

#### 4.5 修复发现的问题
根据测试结果，回到仓库修复：
- 模板中的 Bug
- 脚本中的逻辑错误
- 文档中的不清晰之处

#### 4.6 在 BOQ 项目中"重新安装"测试
- [ ] 备份 BOQ 项目的 `.cursorrules` 和 `.cursor/rules/`
- [ ] 使用脚本重新生成规则
- [ ] 对比生成的文件和原始文件，确认一致性

### 🎯 阶段 4 成功标准
- ✅ 在全新项目中成功安装并运行
- ✅ 所有 AI 功能正常工作
- ✅ 没有残留的 `{{}}` 或报错
- ✅ 在 BOQ 项目中重新安装后行为一致

---

## 🎉 完成后的状态

完成所有 4 个阶段后，你将拥有：

### ✅ 一个公开的 GitHub 仓库
```
OnePerson-AI-Studio-Core/
├── README.md                       # 精美的项目说明
├── templates/                      # 7 个模板文件
│   ├── .cursorrules.template
│   └── .cursor/rules/*.mdc.template
├── presets/                        # 至少 1 个预设配置
│   └── python-fastapi-vue3.json
├── scripts/                        # 安装脚本
│   └── install.ps1
├── docs/                           # 使用文档
│   ├── quick-start.md
│   └── customization.md
└── model-matrix.json               # 模型定价矩阵
```

### ✅ 一套经过验证的工作流
1. 新项目启动时，运行一行命令
2. 1 分钟内完成 AI 规则配置
3. 立刻可以用诊断模式和角色分工

### ✅ 可分享的开源项目
- 其他一人公司开发者可以直接使用
- 可以接受社区贡献新的技术栈预设
- 可以作为你的"开源作品"展示

---

## 📊 时间与优先级建议

### 如果时间紧张，可以分批完成：

**第 1 优先级**（必须完成）：
- 阶段 1：验证参数化可行性
- 阶段 2 前半部分：创建仓库和迁移模板

**第 2 优先级**（尽快完成）：
- 阶段 3：编写安装脚本
- 阶段 4：测试验证

**第 3 优先级**（逐步完善）：
- 补充更多技术栈预设
- 完善文档和示例
- 添加高级功能（如旧项目审计）

---

## 💡 我的建议

**现在立刻开始"阶段 1"**，因为：
1. 可以在 BOQ 项目中直接操作，风险低
2. 1-2 小时就能看到结果
3. 验证了可行性，后续工作才有意义

你现在要我：
- **A**：立刻开始阶段 1，帮你创建 `.ai-studio-temp/` 目录和测试脚本？
- **B**：先看看这个行动计划，有问题再开始？
- **C**：调整计划，有些步骤你想改一下？

