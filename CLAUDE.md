# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于 **FastAPI + LangGraph** 的智能医疗问诊 AI 系统，采用**分层架构**设计，遵循 SOLID 原则和严格的代码质量标准。

### 核心功能

- **智能问诊流程**：基于"一诉五史"（主诉、现病史、既往史、个人史、家族史、生殖史）的结构化数据采集
- **情感支持**：渐进式共情，根据用户情绪等级（NORMAL/MILD/MODERATE/SEVERE）动态调整响应
- **冲突解决**：智能检测用户信息矛盾，触发回溯重新确认
- **紧急检测**：红/黄/绿三级预警系统，自动识别需要紧急就医的症状
- **防幻觉设计**：置信度评分机制，确保 AI 只在数据充分时给出结论
- **输入清洗**：自动脱敏敏感信息（手机号、身份证、姓名等）
- **多症状处理**：优先级排序，并行采集多个症状信息

## 开发环境设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装核心依赖
pip install fastapi uvicorn langgraph

# 安装测试依赖
pip install pytest pytest-cov

# 可选：开发工具
pip install black isort mypy ruff
```

## 常用命令

```bash
# 启动开发服务器（推荐：添加端口和日志）
uvicorn app.main:app --reload --port 8000

# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 代码格式化
black app/ tests/
isort app/ tests/

# Linting
ruff check app/ tests/
```

## API 端点

### 健康检查
- `GET /` - 根端点，返回系统信息
- `GET /health` - 健康检查端点

### 问诊系统
- `POST /api/v1/consultation/chat` - 主对话接口
  - 请求: `{"session_id": "可选", "user_input": "用户输入"}`
  - 响应: 包含 session_id, bot_response, current_phase, collected_fields, emergency_flag 等

- `GET /api/v1/consultation/medical-record/{session_id}` - 获取完整病历
  - 响应: 包含"一诉五史"完整医疗记录

## 项目架构

### 目录结构

```
lesson_02/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口，路由注册
│   ├── config.py            # 配置管理（Pydantic Settings）
│   ├── dependencies.py      # 依赖注入（lifespan, get_db）
│   ├── models/              # 数据模型层
│   │   ├── consultation_state.py  # 会话状态模型
│   │   └── medical_record.py      # 病历数据模型（一诉五史）
│   ├── schemas/             # Pydantic schemas（API 请求/响应）
│   │   └── consultation.py         # 问诊 API schemas
│   ├── services/            # 业务逻辑层
│   │   ├── input_sanitization.py   # 输入清洗服务
│   │   ├── session_manager.py       # 会话管理器
│   │   ├── confidence_scoring.py    # 置信度评分
│   │   ├── emergency_detection.py   # 紧急检测
│   │   ├── intent_classifier.py     # 意图分类
│   │   ├── emotion_support.py       # 情感支持
│   │   ├── conflict_resolution.py   # 冲突解决
│   │   ├── structured_extraction.py # 结构化提取
│   │   └── multi_symptom_handler.py # 多症状处理
│   ├── graph/               # LangGraph 状态机
│   │   └── consultation_graph.py    # 问诊流程图
│   └── api/                 # API 路由层
│       ├── __init__.py
│       ├── health.py        # 健康检查端点
│       └── consultation.py  # 问诊 API 路由
├── tests/                   # 测试文件
│   ├── models/              # 模型测试
│   ├── schemas/             # Schema 测试
│   ├── services/            # 服务测试
│   ├── graph/               # 状态机测试
│   ├── api/                 # API 测试
│   └── integration/         # 端到端集成测试
├── docs/                    # 文档目录
│   └── plans/               # 实施计划
├── .claude/
│   └── skills/              # ZCF Vibe Coding 技能集
├── CLAUDE.md                # 本文档
└── README.md                # 项目说明文档
```

### 架构设计原则

**分层模式**：新功能应遵循以下结构
- `app/api/{feature}.py` - 路由层（FastAPI 路由）
- `app/services/{feature}.py` - 业务逻辑层（如需要）
- `app/models/{feature}.py` - 数据模型层（如需要）
- `app/schemas/{feature}.py` - Pydantic schemas（如需要）
- `app/graph/{feature}.py` - 状态机层（复杂流程）
- `tests/{layer}/test_{feature}.py` - 测试文件

**Lifespan 管理**：使用 `app/dependencies.py:lifespan` 进行启动/关闭事件处理

### 问诊流程状态机

```python
GREETING → CHIEF_COMPLAINT → PRESENT_ILLNESS → PAST_HISTORY
    → PERSONAL_HISTORY → FAMILY_HISTORY → REPRODUCTIVE_HISTORY
    → REVIEW → COMPLETE
```

**流程中断条件**：
- 紧急症状检测 → 立即就医建议
- 用户情绪严重 → 情感支持优先
- 信息冲突 → 回溯重新确认
- 无关输入 → 礼貌引导回正轨

### 置信度评分规则

| 分数范围 | 等级 | 说明 |
|---------|------|------|
| 0.8 - 1.0 | HIGH | 数据充分，可用于诊断 |
| 0.5 - 0.7 | MEDIUM | 数据部分充分，需补充 |
| 0.0 - 0.4 | LOW | 数据不足，不能下结论 |

### 紧急预警级别

| 级别 | 症状示例 | 建议 |
|------|---------|------|
| RED | 胸痛、呼吸困难、意识模糊、大出血 | 立即急诊 |
| YELLOW | 高热、严重脱水、持续呕吐 | 尽快就医 |
| GREEN | 普通症状 | 常规就诊 |

### ZCF Vibe Coding 技能集

项目包含自定义开发技能，位于 `.claude/skills/`：

| 技能 | 用途 |
|------|------|
| `zcf:workflow` | 六阶段结构化开发流程 |
| `zcf:feat` | 功能开发工作流 |
| `zcf:review` | 代码质量审查 |
| `zcf:tdd` | 测试驱动开发 |
| `zcf:api` | RESTful API 开发 |
| `zcf:db` | 数据库操作 |
| `zcf:init-project` | 项目文档生成 |

### API 端点组织

新增 API 时，在 `app/api/` 创建模块并通过 `app/main.py` 注册：

```python
# app/main.py
from app.api import health, consultation  # 导入新路由

app.include_router(health.router, tags=["health"])
app.include_router(consultation.router, prefix="/api/v1", tags=["consultation"])
```

---

# Code Architecture Guidelines

## 📏 硬性指标（Must-Follow）

### ✅ 文件行数限制
- **Python 文件**：每个代码文件 **不超过 200 行**
- **目的**：提高可读性、可维护性，降低认知负担

### ✅ 文件夹结构限制
- 每个文件夹中 **文件数量不超过 8 个**
- 若超过，需进行 **多层子文件夹拆分**
- **目的**：提升结构清晰度，便于快速定位与扩展

---

## 🧠 架构设计关注点（持续警惕）

以下"坏味道"会严重侵蚀代码质量，**必须时刻警惕并避免**：

### ❌ 1. 僵化（Rigidity）
系统难以变更，微小改动引发连锁反应
- **建议**：引入接口抽象、策略模式、依赖倒置原则

### ❌ 2. 冗余（Redundancy）
相同逻辑重复出现，维护困难
- **建议**：提取公共函数或类，使用组合代替继承

### ❌ 3. 循环依赖（Circular Dependency）
模块相互依赖，形成"死结"
- **建议**：使用接口解耦、事件机制、依赖注入

### ❌ 4. 脆弱性（Fragility）
修改一处，导致看似无关部分出错
- **建议**：遵循单一职责原则、提高模块内聚性

### ❌ 5. 晦涩性（Obscurity）
代码结构混乱，意图不明
- **建议**：命名清晰、注释得当、结构简洁

### ❌ 6. 数据泥团（Data Clump）
多个参数总是一起出现，暗示应封装为对象
- **建议**：封装为数据结构或值对象（Pydantic 模型）

### ❌ 7. 不必要的复杂性（Needless Complexity）
过度设计，小问题用大方案
- **建议**：遵循 YAGNI 原则，KISS 原则，按需设计

---

## 🚨 重要提醒

> **【非常重要】无论编写、阅读还是审核代码，都必须严格遵守上述硬性指标，并时刻关注架构设计质量。**
> **【非常重要】一旦发现"坏味道"，应立即提醒是否需要优化，并提供合理的优化建议。**
