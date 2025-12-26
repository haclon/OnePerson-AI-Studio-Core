# Proposal: OnePerson-AI-Studio-Core 通用框架

> **提案类型**：新能力 (New Capability)  
> **影响范围**：跨项目通用框架  
> **提案人**：用户 (一人公司开发者)  
> **创建时间**：2025-12-26  
> **状态**：草案 (Draft)

---

## 1. 背景与动机 (Background & Motivation)

### 1.1 当前痛点

在 BOQ-StructuredExtraction-Web 项目中，我们成功建立了一套基于多模型、多角色协作的 AI 辅助开发工作流：

- ✅ **诊断模式 (`?`)**：自动推荐最合适的模型和 Agent 角色
- ✅ **角色分工 (.mdc)**：6 大专家角色各司其职，规则清晰
- ✅ **成本优化**：质量 > 成本 > 时间的模型选择策略
- ✅ **OpenSpec 流程**：大改动前强制走提案审批

**但是**，这套"灵魂"深度耦合在 BOQ 项目中：
- `.cursorrules` 混合了通用规则和 BOQ 业务术语
- `.mdc` 文件中包含了 FastAPI/Vue 3 的具体路径
- 新项目无法快速复用这套工作流

### 1.2 用户诉求

作为一人公司开发者，我希望能够：
1. **在新项目启动时**：1 分钟内一键生成全套 AI 协作规则
2. **在旧项目接手时**：无损注入规则，不破坏现有代码结构
3. **跨技术栈复用**：无论是 Go+React 还是 Python+Vue，都能适配

---

## 2. 解决方案概述 (Solution Overview)

### 2.1 核心设计

**OnePerson-AI-Studio-Core** 是一个**可注入、可配置的 AI 协作框架**，它包含：

```
OnePerson-AI-Studio-Core/
├── core/                           # 核心规则库（通用层）
│   ├── .cursorrules.template       # 通用规则模板
│   ├── rules/                      # 标准角色定义
│   │   ├── prd_analyst.mdc
│   │   ├── spec_architect.mdc
│   │   ├── fe_developer.mdc
│   │   ├── be_developer.mdc
│   │   ├── qa_reviewer.mdc
│   │   └── batch_processor.mdc
│   └── model-matrix.json           # 模型能力与定价矩阵
│
├── adapters/                       # 技术栈适配器（可插拔层）
│   ├── python-fastapi/
│   ├── golang-gin/
│   ├── nodejs-express/
│   └── ...
│
├── cli/                            # 命令行工具
│   ├── init.js                     # 新项目初始化
│   ├── inject.js                   # 旧项目注入
│   └── audit.js                    # 项目现状审计
│
└── README.md                       # 框架使用文档
```

### 2.2 两种工作模式

#### 模式 1：新项目启动 (Init Mode)

**用户操作**：
```bash
npx oneperson-ai-studio init --stack python-fastapi-vue3
```

**AI 自动完成**：
1. 在项目根目录生成 `.cursorrules`
2. 创建 `.cursor/rules/` 目录并注入 6 个 `.mdc` 文件
3. 生成标准化的 `README.md` 和 `docs/` 目录结构
4. 创建 `openspec/` 目录并初始化 `project.md`

#### 模式 2：旧项目注入 (Inject Mode)

**用户操作**：
```bash
? 这是个旧项目，请适配规则
```

**AI 执行流程**：
1. **现状审计**：扫描项目结构，识别技术栈和架构特征
2. **生成报告**：输出"项目现状诊断报告"
3. **规则适配**：根据现状调整 `.mdc` 规则（不强制现有代码符合新规范）
4. **分步注入**：优先注入通用层，逐步引入角色层

---

## 3. 核心机制：项目自适应注入 (Project Adaptive Injection)

### 3.1 现状审计 (Project Audit)

当 AI 检测到"旧项目注入请求"时，执行以下审计流程：

#### 步骤 1：技术栈识别

**扫描目标**：
- `package.json` / `requirements.txt` / `go.mod` → 确定主语言和框架
- 目录结构 (`src/`, `app/`, `backend/`) → 推断项目类型
- 配置文件 (`.gitignore`, `docker-compose.yml`) → 识别部署方式

**输出示例**：
```yaml
技术栈:
  后端: Python 3.10 + FastAPI 0.104
  前端: Vue 2 (非 Composition API)
  数据库: MySQL 5.7
  部署: Docker
```

#### 步骤 2：架构模式分析

**扫描目标**：
- 是否有分层结构 (`models/`, `services/`, `api/`)
- 是否使用 ORM (`sqlalchemy`, `gorm`)
- 是否有测试目录 (`tests/`, `__test__/`)

**输出示例**：
```yaml
架构特征:
  分层架构: ✅ 有明确的 MVC 分层
  数据库迁移: ❌ 未发现迁移脚本
  单元测试: ⚠️  仅覆盖 30% 的核心逻辑
  API 文档: ❌ 无 OpenAPI/Swagger 配置
```

#### 步骤 3：代码规范评估

**扫描目标**：
- 命名风格 (`camelCase`, `snake_case`)
- 注释密度和语言（中文/英文）
- 是否有 Linter 配置 (`.eslintrc`, `pyproject.toml`)

**输出示例**：
```yaml
代码规范:
  命名风格: snake_case (Python 标准)
  注释语言: 中文为主 (80%)
  代码规范工具: ✅ 已配置 black + flake8
```

#### 步骤 4：风险点识别

**输出示例**：
```yaml
潜在冲突:
  - ⚠️  现有代码在 API 路由中直接写 SQL，与 BE-Developer 规则冲突
  - ⚠️  前端使用 Vue 2，部分 FE-Developer 规则需调整
  - ✅ 数据库命名已符合 snake_case 规范
```

---

### 3.2 规则适配方案生成 (Rule Adaptation)

基于审计结果，AI 生成"无损注入方案"：

#### 策略 1：兼容性优先

**原则**：规则不强制改造现有代码，只约束新增代码。

**示例**：
```markdown
# BE-Developer 规则适配

## 原规则
"严禁在 API 路由中直接写数据库 SQL（必须走 Service/CRUD 层）"

## 适配后
"**新增接口**必须走 Service 层。现有接口若需改动，建议逐步重构。"
```

#### 策略 2：渐进式引入

**阶段划分**：
- **第 1 阶段**：仅注入 `.cursorrules` 和 `?` 诊断模式
- **第 2 阶段**：注入 PRD、Spec、QA 三个"辅助角色"
- **第 3 阶段**：根据用户反馈，逐步启用 FE/BE 开发规则

#### 策略 3：双轨制运行

**旧代码区**：
- 不触发严格的 `.mdc` 规则
- AI 只做"提示"不做"阻止"

**新代码区**：
- 严格遵循新规则
- 通过 `globs` 精确匹配新增文件

---

### 3.3 输出物：项目适配报告

审计完成后，AI 生成一份 Markdown 报告：

```markdown
# 项目现状审计报告

## 1. 项目基本信息
- 项目名称: Legacy-ERP-System
- 技术栈: Python 3.8 + Flask + jQuery
- 代码行数: ~50,000 行
- 团队规模: 1 人（你）

## 2. 现状评估
### 2.1 技术栈分析
- ✅ 后端框架: Flask 2.0 (成熟稳定)
- ⚠️  前端技术: jQuery (建议未来迁移至 Vue/React)
- ❌ 数据库迁移: 无 (高风险)

### 2.2 架构质量
- 分层清晰度: 60/100
- 测试覆盖率: 20%
- 文档完整度: 30%

## 3. AI 协作规则注入方案
### 3.1 推荐注入策略
**建议采用"渐进式注入"**：
1. 立即注入: `.cursorrules` + `?` 诊断 + PRD/Spec 角色
2. 观察 2 周后: 注入 BE-Developer (Flask 适配版)
3. 前端重构时: 启用 FE-Developer

### 3.2 规则适配调整
- BE-Developer: 已调整为兼容 Flask 的路由写法
- FE-Developer: 暂不启用（等前端迁移至 Vue）

## 4. 行动建议
### 高优先级
- [ ] 建立数据库迁移机制 (Alembic)
- [ ] 补充核心业务逻辑的单元测试

### 中优先级
- [ ] 逐步将 SQL 从路由迁移至 Service 层
- [ ] 为 API 添加 Swagger 文档

## 5. 预期收益
- 🚀 开发效率: 提升 30%（通过 AI 辅助）
- 💰 AI 成本: 预计每月 $20-30
- 🛡️ 代码质量: 逐步提升至 80/100
```

---

## 4. 技术实现要点 (Technical Details)

### 4.1 审计脚本核心逻辑

```javascript
// cli/audit.js (伪代码)

async function auditProject(projectPath) {
  const report = {
    stack: await detectStack(projectPath),
    architecture: await analyzeArchitecture(projectPath),
    codeStyle: await evaluateCodeStyle(projectPath),
    risks: []
  };
  
  // 与标准规则对比，找出冲突点
  report.risks = compareWithStandardRules(report);
  
  // 生成适配方案
  const adaptationPlan = generateAdaptationPlan(report);
  
  return { report, adaptationPlan };
}
```

### 4.2 规则模板系统

**模板变量**：
```yaml
# .cursorrules.template
项目缩写: {{PROJECT_ABBR}}
技术栈: {{TECH_STACK}}
后端框架: {{BACKEND_FRAMEWORK}}
前端框架: {{FRONTEND_FRAMEWORK}}
```

**实例化**：
```bash
oneperson-ai-studio init --abbr BOQSE --stack python-fastapi-vue3
# 自动替换所有 {{}} 占位符
```

---

## 5. 验收标准 (Acceptance Criteria)

### 5.1 新项目启动

- [ ] 运行 `init` 命令后，1 分钟内生成完整的规则文件
- [ ] 生成的 `.cursorrules` 包含项目特定信息（名称、技术栈）
- [ ] 6 个 `.mdc` 文件中的 `globs` 自动适配项目目录结构
- [ ] `?` 诊断模式立即可用

### 5.2 旧项目注入

- [ ] AI 能够正确识别 5 种以上常见技术栈（Python/Node/Go/Java/PHP）
- [ ] 审计报告包含"技术栈"、"架构质量"、"风险点"三大模块
- [ ] 适配后的规则不会对现有代码产生误报（Linter 不报错）
- [ ] 用户可以选择"仅注入诊断模式"或"全量注入"

### 5.3 跨项目复用

- [ ] 同一开发者在 3 个不同项目中使用该框架，都能正常工作
- [ ] 规则更新后，所有项目通过 `update` 命令一键升级

---

## 6. 风险与挑战 (Risks & Challenges)

### 6.1 技术风险

| 风险项 | 影响 | 缓解措施 |
|--------|------|----------|
| 审计准确率不足 | 中 | 提供手动修正机制 |
| 规则冲突导致 AI 混乱 | 高 | 严格的优先级和作用域控制 |
| 不同 Cursor 版本兼容性 | 低 | 定期测试最新版本 |

### 6.2 用户体验风险

| 风险项 | 影响 | 缓解措施 |
|--------|------|----------|
| 学习成本高 | 中 | 提供交互式教程 |
| 配置过于复杂 | 高 | 提供"快速模式"和"专家模式" |

---

## 7. 里程碑规划 (Milestones)

### Phase 1: 核心框架搭建 (2 周)
- [ ] 设计并实现 `core/` 目录结构
- [ ] 完成 `.cursorrules.template` 和 6 个 `.mdc` 模板
- [ ] 实现 `init` 命令（支持新项目）

### Phase 2: 审计引擎开发 (2 周)
- [ ] 实现技术栈识别逻辑
- [ ] 实现架构模式分析逻辑
- [ ] 生成标准化的审计报告

### Phase 3: 旧项目适配 (1 周)
- [ ] 实现 `inject` 命令
- [ ] 实现规则冲突检测与自动调整
- [ ] 完成"双轨制运行"机制

### Phase 4: 测试与文档 (1 周)
- [ ] 在 3 个不同类型的项目中测试
- [ ] 编写用户手册和 API 文档
- [ ] 发布 v1.0.0

---

## 8. 讨论问题 (Open Questions)

1. **CLI 工具的技术选型**：Node.js (跨平台) 还是 Python (用户熟悉)？
2. **规则更新机制**：用户如何获取最新的模型定价表和规则模板？
3. **社区化可能性**：是否开源？是否允许用户贡献自定义适配器？
4. **与 Cursor 官方的关系**：这套框架是否应该作为 Cursor 的一个"最佳实践"提交给官方？

---

## 9. 下一步行动 (Next Steps)

1. **需求确认**：用户审阅本 Proposal，确认核心功能优先级
2. **技术选型**：确定 CLI 工具的实现语言
3. **原型开发**：先在 BOQ 项目中验证"审计引擎"的可行性
4. **正式立项**：通过 OpenSpec 审批，进入 Design 阶段

---

**备注**：本 Proposal 仅为初步规划，具体实现细节将在 `design.md` 和 `tasks.md` 中进一步细化。

