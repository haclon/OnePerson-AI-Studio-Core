# 常见问题（FAQ）

> 在使用 OnePerson AI Studio Core 过程中遇到问题？这里有答案！

---

## 📋 目录

- [安装相关](#安装相关)
- [使用问题](#使用问题)
- [配置调整](#配置调整)
- [性能与成本](#性能与成本)
- [故障排除](#故障排除)

---

## 🔧 安装相关

### Q1: 安装脚本提示 "No module named 'xxx'"？

**A**: 脚本使用的是 Python 标准库，不需要额外安装依赖。如果仍然报错，请检查：

```bash
# 检查 Python 版本（需要 3.10+）
python --version

# 如果版本过低，尝试使用 python3
python3 install.py --interactive
```

### Q2: 安装后找不到 `.cursorrules` 文件？

**A**: `.cursorrules` 是隐藏文件（以 `.` 开头），在文件管理器中可能不可见。

**Windows**：
```powershell
# 查看隐藏文件
dir /A

# 或在文件资源管理器中：查看 → 显示 → 隐藏的项目
```

**Mac/Linux**：
```bash
# 查看隐藏文件
ls -la

# 或在 Finder 中：Cmd+Shift+. 切换显示隐藏文件
```

### Q3: 能在已有项目中安装吗？

**A**: 可以！但要注意：

1. **如果已有 `.cursorrules`**：会提示是否覆盖
2. **如果已有 `.cursor/rules/`**：新规则会覆盖同名文件

**建议**：先备份现有配置
```bash
cp .cursorrules .cursorrules.backup
cp -r .cursor/rules .cursor/rules.backup
```

### Q4: 支持哪些技术栈？

**A**: 当前内置预设：
- ✅ `python-fastapi-vue3` - Python + FastAPI + Vue 3

**即将支持**：
- 🚧 `nodejs-express-react` - Node.js + Express + React
- 🚧 `golang-gin-vue3` - Go + Gin + Vue 3

**自定义**：参考 [自定义配置指南](customization.md#创建自定义技术栈预设)

---

## 💬 使用问题

### Q5: 诊断模式（`?` 命令）不工作？

**A**: 请按以下步骤排查：

1. **检查 `.cursorrules` 是否存在**：
   ```bash
   ls -la .cursorrules
   ```

2. **检查语法错误**：
   打开 `.cursorrules`，确认没有语法错误（如未闭合的引号）

3. **重新加载 Cursor**：
   - `Ctrl/Cmd+Shift+P` → "Reload Window"

4. **尝试完整问题**：
   ```
   ? 我想实现一个登录功能，应该怎么做？
   ```

5. **查看 AI 回复**：
   如果 AI 没有按格式回复，可能需要调整 `.cursorrules` 中的诊断模式说明

### Q6: 角色没有自动触发？

**A**: 角色触发依赖 `.mdc` 文件中的 `globs` 参数。

**检查步骤**：

1. **确认文件类型匹配**：
   ```yaml
   # 在 .cursor/rules/fe_developer.mdc 中
   globs: frontend/src/**/*.{vue,js,scss}
   ```
   如果你的文件是 `.jsx` 或在其他目录，需要调整 `globs`

2. **查看项目结构**：
   ```bash
   # 确认你的文件路径是否匹配 globs 模式
   ls frontend/src
   ```

3. **测试方法**：
   - 打开一个应该触发规则的文件（如 `.vue`）
   - 询问 AI："你现在是什么角色？"
   - AI 应该回复："我是 XXX 项目的前端开发专家"

### Q7: AI 推荐的模型不符合我的预期？

**A**: 你可以：

1. **明确指定模型**：
   ```
   用 Opus 4.5 帮我分析这个复杂的架构问题
   ```

2. **调整模型选择策略**：
   编辑 `.cursorrules` 第 5-6 节，修改推荐规则

3. **反馈给项目**：
   在 [GitHub Issues](https://github.com/haclon/OnePerson-AI-Studio-Core/issues) 提出改进建议

### Q8: 多个角色同时触发怎么办？

**A**: 这是设计的一部分！AI 会综合考虑所有激活的规则。

**如果不希望重叠**：
1. 调整 `.mdc` 文件的 `globs`，确保路径不重叠
2. 使用更具体的 `globs` 模式

**示例**：
```yaml
# FE 规则只匹配 components/
globs: src/components/**/*.vue

# BE 规则只匹配 api/
globs: src/api/**/*.ts
```

---

## ⚙️ 配置调整

### Q9: 如何修改参数替换后的配置？

**A**: 直接编辑生成的文件即可：

```bash
# 修改全局规则
vi .cursorrules

# 修改某个角色规则
vi .cursor/rules/fe_developer.mdc
```

**修改后**：
- 无需重新运行安装脚本
- 在 Cursor 中重新加载项目即可生效

### Q10: 可以为不同项目使用不同配置吗？

**A**: 当然可以！每个项目的 `.cursorrules` 和 `.cursor/rules/` 都是独立的。

**建议工作流**：
1. 为每种项目类型创建预设
2. 新项目时选择对应预设
3. 根据需要微调

### Q11: 如何禁用某个角色？

**A**: 有两种方法：

**方法 1：删除文件**
```bash
rm .cursor/rules/batch_processor.mdc
```

**方法 2：修改 `globs` 为不可能匹配的模式**
```yaml
# 在 .mdc 文件中
globs: __never_match__
```

### Q12: 团队如何共享配置？

**A**: 将配置纳入版本控制：

```bash
# 添加到 Git
git add .cursorrules .cursor/
git commit -m "feat: 添加 AI 协作规则"
git push

# 团队成员克隆后立即可用
git clone your-repo
cd your-repo
# .cursorrules 和 .cursor/ 已经存在
```

**最佳实践**：
- 在 README 中说明已配置 AI 规则
- 提供简单的使用指南（如 `? 命令`）

---

## 💰 性能与成本

### Q13: 使用这套规则会增加 AI 成本吗？

**A**: 会有**轻微增加**，但通过优化模型选择可以**节省更多**。

**增加的成本**：
- `.cursorrules` 和 `.mdc` 规则会作为上下文发送给 AI
- 约增加 5-10% 的 Token 消耗

**节省的成本**：
- 通过诊断模式推荐合适的模型，避免滥用昂贵模型
- 例如：不用 Opus 做简单任务，可节省 70%+ 成本

**实际效果**：
- 对于一人公司开发者，通常可节省 30-50% 的 AI 费用

### Q14: 如何进一步降低成本？

**A**: 策略建议：

1. **调整模型选择策略**（`.cursorrules` 第 6 节）：
   - 简单任务优先使用 Codex Mini 或 Grok Code
   - 只在复杂推理时使用 Opus

2. **精简规则文件**：
   - 删除不需要的角色
   - 简化规则描述

3. **使用 `?` 诊断**：
   - 养成习惯，让 AI 推荐模型
   - 避免盲目使用默认模型

### Q15: 规则文件会影响 AI 响应速度吗？

**A**: 影响**非常小**（< 0.5秒）。

**原因**：
- 规则文件总共约 6000 行
- 对于现代 LLM，这是很小的输入量

**如果确实在意速度**：
- 删除不常用的角色
- 简化 `.cursorrules` 中的表格和示例

---

## 🔧 故障排除

### Q16: 提示 "找不到模板文件"？

**A**: 检查仓库路径：

```bash
# 确认仓库存在
ls ~/OnePerson-AI-Studio-Core

# 检查模板文件
ls ~/OnePerson-AI-Studio-Core/templates

# 如果不存在，重新克隆
git clone https://github.com/haclon/OnePerson-AI-Studio-Core.git ~/OnePerson-AI-Studio-Core
```

### Q17: 参数没有被替换（还有 `{{}}` 残留）？

**A**: 检查配置文件和参数名是否匹配。

```bash
# 检查未替换的参数
grep -r "{{" .cursorrules .cursor/rules/

# 查看配置文件中的参数
cat ~/OnePerson-AI-Studio-Core/presets/python-fastapi-vue3.json
```

**常见原因**：
- 参数名拼写错误（大小写敏感）
- 配置文件中缺少该参数

**解决**：
1. 手动替换残留的 `{{}}`
2. 或重新运行安装脚本

### Q18: Cursor 提示语法错误？

**A**: 检查生成的文件是否有格式问题。

**常见问题**：
1. **YAML 格式错误**（`.mdc` 文件开头）：
   ```yaml
   # 错误：description 后缺少空格
   description:当进行...
   
   # 正确
   description: 当进行...
   ```

2. **Markdown 格式错误**：
   - 未闭合的代码块
   - 未转义的特殊字符

**调试方法**：
```bash
# 使用 YAML linter 检查 .mdc 文件
python -c "import yaml; yaml.safe_load(open('.cursor/rules/fe_developer.mdc').read())"
```

### Q19: 在 Windows 上路径问题？

**A**: Windows 路径使用反斜杠 `\`，可能导致问题。

**解决方案**：
1. **使用正斜杠**（推荐）：
   ```bash
   python install.py --target=./my-project
   ```

2. **或使用 PowerShell 的路径**：
   ```powershell
   python install.py --target="$(pwd)\my-project"
   ```

3. **或使用绝对路径**：
   ```bash
   python install.py --target=D:/Projects/my-project
   ```

### Q20: 其他问题？

**A**: 寻求帮助的渠道：

1. **查看文档**：
   - [快速开始](quick-start.md)
   - [自定义配置](customization.md)

2. **搜索类似问题**：
   - [GitHub Issues](https://github.com/haclon/OnePerson-AI-Studio-Core/issues)

3. **提交新问题**：
   - [创建 Issue](https://github.com/haclon/OnePerson-AI-Studio-Core/issues/new)
   - 请提供：系统版本、Python 版本、错误信息、完整的命令

4. **参与讨论**：
   - [GitHub Discussions](https://github.com/haclon/OnePerson-AI-Studio-Core/discussions)

---

## 💡 使用技巧

### 技巧 1：快速切换项目

如果你有多个项目使用不同配置：

```bash
# 为每个项目创建独立预设
~/OnePerson-AI-Studio-Core/presets/
├── project-a.json
├── project-b.json
└── project-c.json

# 安装时指定预设
cd ~/project-a
python ~/OnePerson-AI-Studio-Core/scripts/install.py --preset project-a
```

### 技巧 2：保存常用配置

创建一个 "安装命令备忘录"：

```bash
# ~/install-commands.sh
alias install-fe="python ~/OnePerson-AI-Studio-Core/scripts/install.py --preset python-fastapi-vue3"
alias install-be="python ~/OnePerson-AI-Studio-Core/scripts/install.py --preset nodejs-express"
```

### 技巧 3：版本控制最佳实践

```gitignore
# .gitignore
# 如果不想提交 AI 规则，添加：
.cursorrules
.cursor/

# 但建议提交，以便团队统一
```

### 技巧 4：定期更新

```bash
# 每月更新一次模板
cd ~/OnePerson-AI-Studio-Core
git pull

# 检查是否有新功能或修复
git log --oneline -10
```

---

## 📚 相关资源

- [快速开始指南](quick-start.md) - 5 分钟上手
- [自定义配置](customization.md) - 深度定制
- [GitHub 仓库](https://github.com/haclon/OnePerson-AI-Studio-Core) - 源码和更新
- [Issues](https://github.com/haclon/OnePerson-AI-Studio-Core/issues) - 问题报告
- [Discussions](https://github.com/haclon/OnePerson-AI-Studio-Core/discussions) - 社区讨论

---

**还有其他问题？** 

欢迎在 [GitHub Discussions](https://github.com/haclon/OnePerson-AI-Studio-Core/discussions) 提问！

