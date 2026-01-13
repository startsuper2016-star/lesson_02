# ZCF Vibe Coding Skills

专业的 AI 辅助开发技能集，为 FastAPI 项目提供完整的工作流支持。

## 📋 技能列表

| 技能 | 文件 | 描述 |
|------|------|------|
| **工作流管理** | `zcf-workflow.md` | 六阶段结构化开发流程 |
| **项目初始化** | `zcf-init-project.md` | 项目上下文与文档生成 |
| **功能开发** | `zcf-feat.md` | 完整的功能开发工作流 |
| **代码审查** | `zcf-review.md` | 智能代码质量分析 |
| **测试驱动** | `zcf-tdd.md` | TDD 测试驱动开发 |
| **数据库** | `zcf-db.md` | 数据库操作与优化 |
| **API 开发** | `zcf-api.md` | RESTful API 开发 |

---

## 🚀 快速开始

### 基本用法

```
# 启动结构化工作流
/zcf:workflow 实现用户认证系统

# 初始化项目文档
/zcf:init-project

# 开发新功能
/zcf:feat 创建文章管理功能

# 代码审查
/zcf:review

# 测试驱动开发
/zcf:tdd 实现登录功能

# 数据库操作
/zcf:db create model User

# API 开发
/zcf:api create /api/posts --crud
```

---

## 📚 技能详解

### 1. 工作流管理 (`zcf:workflow`)

**适用场景**：复杂功能的完整开发流程

**六个阶段**：
```
Research（研究）→ Conception（构思）→ Planning（计划）
     ↓
Execution（执行）→ Optimization（优化）→ Review（评审）
```

**示例**：
```
你：/zcf:workflow 实现完整的用户系统

Claude：启动六阶段工作流...
[依次执行所有阶段，确保代码质量]
```

---

### 2. 项目初始化 (`zcf:init-project`)

**适用场景**：新项目或项目结构变更后

**功能**：
- 分析项目结构
- 生成 CLAUDE.md 文档
- 检测技术栈
- 评估代码质量

**示例**：
```
你：/zcf:init-project

Claude：
📊 项目分析报告
技术栈：FastAPI + PostgreSQL
架构：分层架构
质量：符合规范

✓ 生成文档完成
```

---

### 3. 功能开发 (`zcf:feat`)

**适用场景**：实现具体功能

**支持模式**：
- `--full`：完整实现（默认）
- `--basic`：基础实现
- `--quick`：快速原型
- `--tdd`：测试驱动

**示例**：
```
你：/zcf:feat 实现用户注册功能

Claude：
【需求分析】功能：用户注册
【方案设计】API → Service → Model
【实施计划】5 个任务
【实施中】创建文件...
【完成】✓ 4 个文件，测试覆盖 90%
```

---

### 4. 代码审查 (`zcf:review`)

**适用场景**：提交代码前或定期检查

**检查维度**：
- 架构约束（文件行数、文件夹结构）
- SOLID 原则
- 代码坏味道
- 安全漏洞
- 性能问题
- 测试覆盖

**示例**：
```
你：/zcf:review

Claude：
📊 审查报告
✅ 架构合理
🔴 SQL 注入风险：app/user.py:45
⚠️  缺少索引：app/models.py:23
💡 建议：添加缓存

优先级 P0（立即修复）：1 项
优先级 P1（本周修复）：3 项
```

---

### 5. 测试驱动 (`zcf:tdd`)

**适用场景**：需要高质量测试的功能

**TDD 循环**：
```
Red（红灯）→ 写测试
Green（绿灯）→ 实现功能
Refactor（重构）→ 优化代码
```

**示例**：
```
你：/zcf:tdd 实现密码重置

Claude：
【红灯】创建 5 个测试 ❌ 失败
【绿灯】实现功能 ✅ 通过
【重构】优化代码 ✅ 仍然通过
【补充】添加边界测试 ✅ 8/8 通过

覆盖率：92%
```

---

### 6. 数据库 (`zcf:db`)

**适用场景**：数据库相关操作

**功能**：
- 创建数据模型
- 数据库迁移
- 查询优化
- 事务管理

**示例**：
```
你：/zcf:db create model Post

Claude：
【模型设计】字段、关系、索引
【生成文件】app/models/post.py
【迁移脚本】alembic/versions/001_create_posts.py
【应用迁移】✅ 成功
```

---

### 7. API 开发 (`zcf:api`)

**适用场景**：创建 RESTful API

**功能**：
- CRUD 接口生成
- 请求验证
- 错误处理
- 认证授权
- 自动文档

**示例**：
```
你：/zcf:api create /api/users --crud

Claude：
【接口设计】6 个端点
【生成文件】schemas + api + tests
【功能特性】验证、文档、错误处理
✓ 访问文档：http://localhost:8000/docs
```

---

## 🎯 典型工作流

### 场景 1：新功能开发

```
1. /zcf:feat 实现用户评论
   ↓
2. /zcf:tdd 编写测试
   ↓
3. /zcf:review 代码审查
   ↓
4. /zcf:db add migration
   ↓
5. 完成提交
```

### 场景 2：项目初始化

```
1. /zcf:init-project
   ↓
2. /zcf:db init --type postgresql
   ↓
3. /zcf:api create /api/health
   ↓
4. 启动开发
```

### 场景 3：Bug 修复

```
1. /zcf:review app/services/user.py
   ↓
2. 修复问题
   ↓
3. /zcf:tdd --test-only
   ↓
4. 验证通过
```

---

## ⚙️ 配置选项

### 全局配置

创建 `.claude/config.json`：
```json
{
  "defaults": {
    "test_framework": "pytest",
    "database": "postgresql",
    "api_version": "v2"
  },
  "constraints": {
    "max_file_lines": {
      "python": 200,
      "javascript": 200
    },
    "max_files_per_dir": 8
  }
}
```

### 技能级别

```bash
# 严格模式（零容忍）
/zcf:review --strict

# 适中模式（默认）
/zcf:review --moderate

# 宽松模式（仅关键问题）
/zcf:review --loose
```

---

## 📊 质量指标

### 架构约束

| 指标 | 限制 | 状态 |
|------|------|------|
| Python 文件行数 | < 200 | ✅ |
| 文件夹文件数 | < 8 | ✅ |
| 测试覆盖率 | > 85% | ⚠️ |

### 设计原则

- ✅ **SOLID**：单一职责、开闭原则、里氏替换、接口隔离、依赖倒置
- ✅ **DRY**：不重复自己
- ✅ **KISS**：保持简单
- ✅ **YAGNI**：不需要的不做

---

## 🔧 故障排除

### 问题 1：技能未生效

```
确保技能文件在正确位置：
.claude/skills/

检查文件名格式：
zcf-{name}.md
```

### 问题 2：文档不同步

```
重新生成文档：
/zcf:init-project --update
```

### 问题 3：测试失败

```
仅运行相关测试：
pytest -k "test_user"

详细输出：
pytest -v
```

---

## 📖 最佳实践

1. **功能开发前**：先规划，再执行
   ```
   /zcf:workflow → /zcf:feat
   ```

2. **代码提交前**：必须审查
   ```
   /zcf:review
   ```

3. **重要功能**：使用 TDD
   ```
   /zcf:tdd 实现功能
   ```

4. **定期维护**：保持文档同步
   ```
   /zcf:init-project --update
   ```

---

## 🎓 学习路径

```
Week 1: 基础技能
├─ /zcf:init-project  # 理解项目结构
├─ /zcf:feat          # 学习功能开发
└─ /zcf:review        # 了解代码质量

Week 2: 进阶技能
├─ /zcf:workflow      # 掌握完整流程
├─ /zcf:tdd           # 测试驱动开发
└─ /zcf:api           # API 开发

Week 3: 高级技能
├─ /zcf:db            # 数据库优化
├─ 性能调优
└─ 架构设计
```

---

## 🌟 核心理念

> **"专业的 AI 辅助开发，让编程更高效、更优雅"**

- **结构化**：遵循成熟的开发流程
- **规范化**：严格遵守代码质量标准
- **自动化**：让 AI 处理繁琐工作
- **智能化**：持续优化和改进

---

## 📞 使用帮助

遇到问题时：

```
# 查看技能帮助
/zcf:{skill-name} --help

# 查看示例
/zcf:{skill-name} --example

# 详细模式
/zcf:{skill-name} --verbose
```

---

**开始您的 Vibe Coding 之旅！** 🚀
