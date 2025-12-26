# 贡献指南

> 感谢你对 OnePerson AI Studio Core 的关注！我们欢迎所有形式的贡献。

---

## 🌟 贡献方式

你可以通过以下方式贡献：

- ✨ **新增技术栈预设** - 为你使用的技术栈创建配置
- 📝 **完善文档** - 改进说明、添加示例
- 🐛 **报告 Bug** - 发现问题并提交 Issue
- 💡 **提出想法** - 分享改进建议
- 🔧 **修复问题** - 提交 Pull Request

---

## 📋 提交 Issue

在提交 Issue 前，请：

1. **搜索现有 Issues** - 避免重复
2. **使用清晰的标题** - 简明扼要描述问题
3. **提供详细信息**：
   - 系统版本（Windows/Mac/Linux）
   - Python 版本
   - 完整的错误信息
   - 复现步骤

### Issue 模板

```markdown
**问题描述**
简要描述你遇到的问题

**复现步骤**
1. 运行命令 `xxx`
2. 打开文件 `xxx`
3. 看到错误 `xxx`

**预期行为**
你期望发生什么

**实际行为**
实际发生了什么

**环境信息**
- OS: Windows 11
- Python: 3.11.0
- Cursor: 版本号

**截图**
（如果适用）
```

---

## 🔀 提交 Pull Request

### 步骤 1：Fork 仓库

点击 GitHub 页面右上角的 "Fork" 按钮。

### 步骤 2：克隆你的 Fork

```bash
git clone https://github.com/你的用户名/OnePerson-AI-Studio-Core.git
cd OnePerson-AI-Studio-Core
```

### 步骤 3：创建新分支

```bash
# 功能分支
git checkout -b feature/my-new-preset

# 修复分支
git checkout -b fix/installation-error

# 文档分支
git checkout -b docs/improve-readme
```

### 步骤 4：进行修改

遵循项目的代码风格和约定（见下文）。

### 步骤 5：测试修改

```bash
# 测试安装脚本
python scripts/install.py --interactive

# 测试在实际项目中的效果
cd ~/test-project
python ~/OnePerson-AI-Studio-Core/scripts/install.py --preset your-preset
```

### 步骤 6：提交更改

```bash
git add .
git commit -m "feat: 添加 Go + Gin + Vue 3 预设"
```

**提交信息规范**：

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加 Node.js + React 预设` |
| `fix` | Bug 修复 | `fix: 修复 Windows 路径问题` |
| `docs` | 文档更新 | `docs: 完善快速开始指南` |
| `style` | 代码格式 | `style: 统一缩进为 4 空格` |
| `refactor` | 代码重构 | `refactor: 简化参数替换逻辑` |
| `test` | 测试相关 | `test: 添加安装脚本单元测试` |
| `chore` | 构建/工具 | `chore: 更新 .gitignore` |

### 步骤 7：推送到你的 Fork

```bash
git push origin feature/my-new-preset
```

### 步骤 8：创建 Pull Request

1. 访问你的 Fork 页面
2. 点击 "Compare & pull request"
3. 填写 PR 描述：
   - 说明做了什么修改
   - 为什么需要这个修改
   - 如何测试

**PR 模板**：

```markdown
## 修改内容

简要描述你的修改

## 动机

为什么需要这个修改？

## 测试

如何测试这个修改？

- [ ] 已在本地测试
- [ ] 已测试安装脚本
- [ ] 已测试在实际项目中的效果

## 相关 Issue

Closes #123
```

---

## 📐 代码规范

### Python 代码

- 使用 4 空格缩进
- 遵循 PEP 8 规范
- 添加文档字符串

```python
def load_preset(preset_name):
    """加载预设配置
    
    Args:
        preset_name: 预设名称（不含 .json 后缀）
    
    Returns:
        dict: 预设配置字典
    
    Raises:
        FileNotFoundError: 预设文件不存在
    """
    ...
```

### Markdown 文档

- 使用标题层级（# ## ###）
- 代码块指定语言
- 提供实际可运行的示例

### JSON 配置

- 使用 2 空格缩进
- 保持键的顺序一致
- 添加注释说明（如果必要，使用 `_comment` 字段）

```json
{
  "_comment": "这是一个注释示例",
  "TECH_STACK": "...",
  "FRONTEND_FRAMEWORK": "..."
}
```

---

## 🎯 贡献重点领域

我们特别欢迎以下方面的贡献：

### 1. 技术栈预设 ⭐

创建新的技术栈配置，例如：

- `nodejs-express-react.json`
- `golang-gin-vue3.json`
- `django-vue3.json`
- `spring-boot-angular.json`

**步骤**：
1. 复制 `presets/python-fastapi-vue3.json`
2. 修改参数
3. 测试安装
4. 提交 PR

### 2. 文档改进 📝

- 添加更多示例
- 翻译文档（英文、日文等）
- 改进现有说明

### 3. 安装脚本增强 🔧

- 支持更多参数
- 添加验证逻辑
- 改进错误提示

### 4. 模板优化 ✨

- 改进 `.cursorrules` 的模型推荐逻辑
- 优化 `.mdc` 规则的触发条件
- 添加新的角色

---

## 🧪 测试指南

在提交 PR 前，请确保：

### 基本测试

```bash
# 1. 测试安装脚本语法
python -m py_compile scripts/install.py

# 2. 测试交互式安装
python scripts/install.py --interactive

# 3. 测试命令行安装
python scripts/install.py --preset python-fastapi-vue3 --name "Test" --abbr "TEST"
```

### 完整测试

1. 在一个测试项目中运行安装脚本
2. 检查生成的文件是否正确
3. 在 Cursor 中测试诊断模式（`?` 命令）
4. 测试角色自动触发

---

## 📜 许可证

本项目采用 MIT License。

提交贡献即表示你同意：
- 你的贡献将以 MIT License 发布
- 你拥有提交内容的版权或已获得授权

---

## 💬 社区准则

我们致力于创建一个友好、包容的社区。请：

- ✅ 尊重他人
- ✅ 使用清晰、专业的语言
- ✅ 接受建设性批评
- ✅ 关注项目的最佳利益

请避免：
- ❌ 人身攻击或侮辱性言论
- ❌ 发布与项目无关的内容
- ❌ 垃圾信息或广告

---

## 🎁 致谢

感谢所有贡献者！你们的帮助让这个项目变得更好。

### 如何被列入贡献者名单

你的 PR 被合并后，会自动添加到 GitHub 的贡献者列表。

---

## 📧 联系方式

有问题或建议？

- **GitHub Issues**: https://github.com/haclon/OnePerson-AI-Studio-Core/issues
- **GitHub Discussions**: https://github.com/haclon/OnePerson-AI-Studio-Core/discussions

---

**再次感谢你的贡献！** 🙏

让我们一起让 AI 协作变得更美好！

