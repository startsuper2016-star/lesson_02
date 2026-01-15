# 医疗问诊 AI 系统

基于 **FastAPI + LangGraph** 的智能医疗问诊系统，实现"一诉五史"结构化数据采集，具备情感支持、冲突解决、紧急检测等核心功能。

## 功能特性

### 核心功能
- **智能问诊流程**：基于"一诉五史"（主诉、现病史、既往史、个人史、家族史、生殖史）
- **情感支持**：渐进式共情，根据用户情绪动态调整响应
- **冲突解决**：智能检测信息矛盾，触发回溯重新确认
- **紧急检测**：红/黄/绿三级预警，自动识别紧急症状
- **防幻觉设计**：置信度评分机制，确保数据充分性
- **输入清洗**：自动脱敏敏感信息（手机号、身份证等）
- **多症状处理**：优先级排序，并行采集多个症状

### 技术架构
- **Web 框架**：FastAPI
- **状态机**：LangGraph
- **数据验证**：Pydantic
- **测试框架**：pytest

## 快速开始

### 环境要求
- Python 3.10+
- pip

### 安装步骤

1. **克隆仓库**
```bash
git clone <repository-url>
cd lesson_02
```

2. **创建虚拟环境**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install fastapi uvicorn langgraph pydantic pytest
```

4. **启动开发服务器**
```bash
uvicorn app.main:app --reload --port 8000
```

5. **访问 API 文档**
打开浏览器访问：`http://localhost:8000/docs`

## API 使用示例

### 开始问诊

```bash
curl -X POST "http://localhost:8000/api/v1/consultation/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "你好"}'
```

**响应示例：**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "bot_response": "您好！我是您的智能问诊助手。请问您今天有什么不适？",
  "current_phase": "greeting",
  "collected_fields": {},
  "is_complete": false,
  "emergency_flag": false
}
```

### 继续问诊（描述症状）

```bash
curl -X POST "http://localhost:8000/api/v1/consultation/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_input": "我头痛三天了"
  }'
```

### 获取完整病历

```bash
curl "http://localhost:8000/api/v1/consultation/medical-record/550e8400-e29b-41d4-a716-446655440000"
```

## 测试

### 运行所有测试
```bash
pytest
```

### 运行测试并生成覆盖率报告
```bash
pytest --cov=app --cov-report=html
```

### 运行特定测试
```bash
# 单元测试
pytest tests/services/

# 集成测试
pytest tests/integration/

# API 测试
pytest tests/api/
```

## 项目结构

```
lesson_02/
├── app/
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置管理
│   ├── models/              # 数据模型
│   ├── schemas/             # API schemas
│   ├── services/            # 业务逻辑
│   ├── graph/               # 状态机
│   └── api/                 # 路由
├── tests/                   # 测试
└── docs/                    # 文档
```

## 问诊流程

```
GREETING
    ↓
CHIEF_COMPLAINT (主诉)
    ↓
PRESENT_ILLNESS (现病史)
    ↓
PAST_HISTORY (既往史)
    ↓
PERSONAL_HISTORY (个人史)
    ↓
FAMILY_HISTORY (家族史)
    ↓
REPRODUCTIVE_HISTORY (生殖史)
    ↓
REVIEW (回顾)
    ↓
COMPLETE (完成)
```

## 开发指南

### 代码质量标准
- Python 文件不超过 200 行
- 每个文件夹不超过 8 个文件
- 遵循 SOLID 原则
- TDD 开发模式

### 代码格式化
```bash
# 格式化代码
black app/ tests/
isort app/ tests/

# 代码检查
ruff check app/ tests/
```

## 配置

系统使用 Pydantic Settings 进行配置管理，可通过环境变量或 `.env` 文件配置：

```bash
# 示例配置
SESSION_TIMEOUT_MINUTES=30
CONFIDENCE_THRESHOLD=0.8
```

## 安全特性

- **输入清洗**：自动检测并移除敏感信息
- **XSS 防护**：检测并拒绝恶意脚本注入
- **Prompt 注入防护**：检测并拒绝提示词注入攻击
- **会话管理**：30 分钟自动过期，防止会话劫持

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
