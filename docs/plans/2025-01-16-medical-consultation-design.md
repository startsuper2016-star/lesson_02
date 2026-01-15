# 医疗问诊 AI 应用技术设计文档

**创建日期**: 2025-01-16
**版本**: 1.0
**状态**: 设计阶段

---

## 1. 项目概述

### 1.1 核心目标

开发一个基于 FastAPI 和 LangGraph 的医疗问诊 AI 应用，实现以下核心功能：

1. **"一诉五史"数据采集**：结构化收集主诉、现病史、既往史、个人史、家族史、生育史
2. **智能引导机制**：检测无关回答并温和引导回正轨
3. **Graph Agent 实现**：使用 LangGraph 构建有状态的对话流程
4. **预问诊病历生成**：基于采集信息生成结构化医疗记录
5. **防幻觉保障**：确保数据准确性，避免 LLM 编造信息

### 1.2 优化维度决策

| 维度 | 选择方案 | 说明 |
|------|---------|------|
| 对话体验 | A+C | 渐进式情感支持 + 对话节奏控制 |
| 临床准确性 | A+B | 智能回溯机制 + 置信度评分系统 |
| 系统效率 | D | 最小化设计，直接使用 GPT-4 |
| 数据质量 | A | 多模型协同提取 |
| 边界情况 | A | 多症状分叉流程 |
| 紧急识别 | B | AI 动态评估 |

---

## 2. 整体架构设计

### 2.1 技术栈选型

```
Frontend: (可选) 简单 Web 界面 / 移动端 API 集成
Backend:  FastAPI
Graph:    LangGraph (状态机管理)
AI:       GPT-4 (temperature=0 提取, 0.7 对话)
Data:     Pydantic (结构化验证), 内存会话存储
Testing:  pytest + 覆盖率 > 85%
```

### 2.2 分层架构

```
┌─────────────────────────────────────────┐
│         API Layer (FastAPI)             │
│  /consultation - 问诊会话管理            │
│  /medical-record - 病历查询与导出         │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Graph Agent (LangGraph)            │
│  状态机管理、节点路由、条件跳转           │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Core Services Layer              │
│  ┌────────────────────────────────────┐ │
│  │ emotion_support      - 情感支持    │ │
│  │ conflict_resolution  - 冲突解决    │ │
│  │ confidence_scoring   - 置信度评分  │ │
│  │ structured_extraction- 结构化提取  │ │
│  │ emergency_detection  - 紧急检测    │ │
│  └────────────────────────────────────┘ │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Security & Boundary Layer           │
│  input_sanitization   - 输入清洗        │
│  multi_symptom_handler - 多症状处理     │
│  intent_classifier    - 意图识别        │
│  session_manager      - 会话管理        │
└─────────────────────────────────────────┘
```

### 2.3 会话状态模型

```python
ConsultationState:
  - session_id: str               # 会话唯一标识
  - current_phase: Phase           # 当前阶段 (greeting → chief_complaint → ...)
  - collected_data: dict           # 已采集的数据
  - confidence_scores: dict        # 各字段置信度
  - conflict_history: list         # 冲突检测记录
  - emotion_state: str             # 情绪状态 (normal/anxious/distressed)
  - emergency_flag: bool           # 紧急情况标记
  - last_update: datetime          # 最后更新时间
```

---

## 3. 核心组件实现

### 3.1 情感支持服务 (Emotion Support Service)

**职责**: 检测用户情绪状态并提供渐进式共情回应

**实现要点**:
- **情绪检测**: 基于 LLM 分析用户输入的情感倾向（关键词 + 语义分析）
- **分级响应**:
  - Level 1（轻度）: "我理解，这确实让人担心"
  - Level 2（中度）: "看起来这个症状让您很焦虑，我们一起梳理"
  - Level 3（重度）: 暂停提问，优先安抚情绪
- **节奏控制**: 根据用户回复速度调整提问频率（过快则放慢，过慢则催促）

**文件**: `app/services/emotion_support.py` (预期 < 200 行)

### 3.2 冲突解决服务 (Conflict Resolution Service)

**职责**: 检测用户信息冲突并启动智能回溯

**实现要点**:
- **冲突检测**: 比较新输入与 `collected_data` 中已有字段
- **风险评估**:
  - 高风险（药物过敏、重大病史）: 立即回溯确认
  - 中风险（症状描述矛盾）: 温和澄清
  - 低风险（非关键细节）: 记录但不中断
- **回溯策略**: "刚才您提到 X，现在又说 Y，请问哪个是准确的？"

**文件**: `app/services/conflict_resolution.py` (预期 < 200 行)

### 3.3 置信度评分服务 (Confidence Scoring Service)

**职责**: 为每个提取的字段分配置信度分数

**评分标准**:
- **High (0.8-1.0)**: 用户明确陈述，无歧义
- **Medium (0.5-0.7)**: 需要推断或部分确认
- **Low (0.0-0.4)**: 信息模糊或缺失

**应用场景**:
- 低置信度字段在最终病历中标记为"需确认"
- 指导后续问题聚焦于低置信度领域

**文件**: `app/services/confidence_scoring.py` (预期 < 150 行)

### 3.4 结构化提取服务 (Structured Extraction Service)

**职责**: 将自然语言转换为结构化的"一诉五史"数据

**三层处理流程**:

1. **LLM 提取层** (temperature=0):
   ```python
   prompt = """
   从以下对话中提取医学信息，仅输出 JSON：
   - 主诉、现病史、既往史、个人史、家族史、生育史
   - 如果信息未提及，字段值为 null
   - 不要编造任何信息

   对话: {conversation_history}
   """
   ```

2. **规则引擎层**:
   - 数值范围验证（年龄、体温等）
   - 时间逻辑验证（发病时间不能在未来）
   - 医学术语字典匹配

3. **术语标准化层**:
   - "感冒" → "上呼吸道感染"
   - "打针" → "注射治疗"
   - 基于医学术语本体（ICD-10/SNOMED CT 子集）

**文件**: `app/services/structured_extraction.py` (预期 < 200 行)

### 3.5 紧急检测服务 (Emergency Detection Service)

**职责**: 实时识别需要立即就医的危急症状

**实现要点**:
- **AI 动态评估**: 使用 LLM 判断症状组合的危险程度
- **分级响应**:
  - 红色预警：胸痛、呼吸困难、意识模糊等 → 立即终止，建议急诊
  - 黄色预警：高热持续、严重脱水等 → 建议尽快就医
  - 绿色预警：普通症状 → 继续问诊
- **双路径并行**: 紧急检测与正常问诊流程同时执行，不阻塞主流程

**文件**: `app/services/emergency_detection.py` (预期 < 150 行)

---

## 4. 数据模型定义

### 4.1 医疗记录模型

```python
# app/models/medical_record.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChiefComplaint(BaseModel):
    symptom: str
    duration: str
    severity: Optional[int] = Field(None, ge=1, le=10)
    body_part: Optional[str] = None

class PresentIllness(BaseModel):
    onset_time: Optional[str] = None
    progression: Optional[str] = None
    aggravating_factors: Optional[List[str]] = None
    relieving_factors: Optional[List[str]] = None
    associated_symptoms: Optional[List[str]] = None

class PastHistory(BaseModel):
    chronic_diseases: Optional[List[str]] = None
    surgeries: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None

class PersonalHistory(BaseModel):
    smoking: Optional[str] = None  # never/former/current
    drinking: Optional[str] = None
    occupation: Optional[str] = None

class FamilyHistory(BaseModel):
    hereditary_diseases: Optional[List[str]] = None
    notes: Optional[str] = None

class ReproductiveHistory(BaseModel):
    applicable: bool  # 是否适用
    details: Optional[str] = None

class MedicalRecord(BaseModel):
    session_id: str
    timestamp: datetime
    chief_complaint: Optional[ChiefComplaint] = None
    present_illness: Optional[PresentIllness] = None
    past_history: Optional[PastHistory] = None
    personal_history: Optional[PersonalHistory] = None
    family_history: Optional[FamilyHistory] = None
    reproductive_history: Optional[ReproductiveHistory] = None
    confidence_scores: dict = Field(default_factory=dict)
    emergency_flag: bool = False
    emergency_recommendation: Optional[str] = None
```

### 4.2 会话状态模型

```python
# app/models/consultation_state.py
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime

class Phase(Enum):
    GREETING = "greeting"
    CHIEF_COMPLAINT = "chief_complaint"
    PRESENT_ILLNESS = "present_illness"
    PAST_HISTORY = "past_history"
    PERSONAL_HISTORY = "personal_history"
    FAMILY_HISTORY = "family_history"
    REPRODUCTIVE_HISTORY = "reproductive_history"
    REVIEW = "review"
    COMPLETE = "complete"

class ConsultationState(BaseModel):
    session_id: str
    current_phase: Phase = Phase.GREETING
    collected_data: Dict = Field(default_factory=dict)
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
    conflict_history: List[Dict] = Field(default_factory=list)
    emotion_state: str = "normal"  # normal/anxious/distressed
    emergency_flag: bool = False
    emergency_assessment: Optional[str] = None
    conversation_history: List[str] = Field(default_factory=list)
    last_update: datetime = Field(default_factory=datetime.now)
```

### 4.3 API 请求/响应模型

```python
# app/schemas/consultation.py
from pydantic import BaseModel

class ConsultationRequest(BaseModel):
    session_id: Optional[str] = None  # None = 新会话
    user_input: str

class ConsultationResponse(BaseModel):
    session_id: str
    bot_response: str
    current_phase: str
    collected_fields: List[str]
    missing_fields: List[str]
    is_complete: bool
    emergency_flag: bool
    medical_record: Optional[dict] = None
```

---

## 5. Graph Agent 实现

### 5.1 LangGraph 状态机设计

```python
# app/graph/consultation_graph.py
from langgraph.graph import StateGraph, END
from app.models.consultation_state import ConsultationState, Phase

# 节点定义
async def greeting_node(state: ConsultationState) -> ConsultationState:
    """欢迎节点，建立初步信任"""
    return state

async def collect_chief_complaint_node(state: ConsultationState) -> ConsultationState:
    """收集主诉"""
    # 调用 emotion_support + structured_extraction
    return state

async def collect_present_illness_node(state: ConsultationState) -> ConsultationState:
    """收集现病史"""
    return state

async def emergency_check_node(state: ConsultationState) -> ConsultationState:
    """紧急情况检查（并行执行）"""
    if state.emergency_flag:
        return {**state, "current_phase": Phase.COMPLETE}
    return state

async def review_node(state: ConsultationState) -> ConsultationState:
    """回顾总结，确认信息"""
    return state

# 条件边
def should_trigger_emergency(state: ConsultationState) -> str:
    return "emergency" if state.emergency_flag else "continue"

def has_more_phases(state: ConsultationState) -> str:
    return "next_phase" if state.current_phase != Phase.COMPLETE else END

# 构建图
workflow = StateGraph(ConsultationState)
workflow.add_node("greeting", greeting_node)
workflow.add_node("collect_chief_complaint", collect_chief_complaint_node)
# ... 其他节点

workflow.set_entry_point("greeting")
workflow.add_conditional_edges(
    "collect_chief_complaint",
    should_trigger_emergency,
    {"emergency": "emergency_response", "continue": "collect_present_illness"}
)
# ... 其他边

app = workflow.compile()
```

### 5.2 FastAPI 路由

```python
# app/api/consultation.py
from fastapi import APIRouter, HTTPException
from app.schemas.consultation import ConsultationRequest, ConsultationResponse
from app.graph.consultation_graph import app as consultation_app
from app.services.session_manager import SessionManager

router = APIRouter(prefix="/api/v1/consultation", tags=["consultation"])
session_manager = SessionManager()

@router.post("/chat", response_model=ConsultationResponse)
async def chat(request: ConsultationRequest):
    """主对话接口"""
    # 获取或创建会话
    state = session_manager.get_or_create(request.session_id)

    # 添加用户输入
    state.conversation_history.append(request.user_input)

    # 执行 Graph Agent
    result = await consultation_app.ainvoke(state)

    # 更新会话
    session_manager.update(result.session_id, result)

    return ConsultationResponse(
        session_id=result.session_id,
        bot_response=last_bot_message(result),
        current_phase=result.current_phase.value,
        collected_fields=list(result.collected_data.keys()),
        missing_fields=get_missing_fields(result),
        is_complete=result.current_phase == Phase.COMPLETE,
        emergency_flag=result.emergency_flag,
        medical_record=result.collected_data if result.current_phase == Phase.COMPLETE else None
    )

@router.get("/medical-record/{session_id}")
async def get_medical_record(session_id: str):
    """获取预问诊病历"""
    state = session_manager.get(session_id)
    if not state or state.current_phase != Phase.COMPLETE:
        raise HTTPException(status_code=404, detail="会话未完成")
    return state.collected_data
```

---

## 6. 安全与边界处理

### 6.1 输入清洗服务

```python
# app/services/input_sanitization.py
import re

class InputSanitizationService:
    """敏感信息脱敏与输入清洗"""

    PATTERNS = {
        "name": r"[\u4e00-\u9fa5]{2,4}(?:先生|女士|女士|先生)",
        "id_card": r"\d{15}|\d{17}[\dXx]",
        "phone": r"1[3-9]\d{9}",
        "email": r"\w+@\w+\.\w+",
    }

    def sanitize(self, text: str) -> tuple[str, dict]:
        """
        清洗输入文本
        返回: (清洗后文本, 检测到的敏感信息)
        """
        detected = {}
        for key, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                detected[key] = matches
                text = re.sub(pattern, f"[{key}_已脱敏]", text)
        return text, detected

    def validate_input(self, text: str) -> bool:
        """检测注入攻击"""
        dangerous_patterns = [
            r"<script>", r"javascript:", r"onerror=",
            r"ignore instructions", r"print.*length",
        ]
        return not any(re.search(p, text, re.I) for p in dangerous_patterns)
```

### 6.2 多症状处理器

```python
# app/services/multi_symptom_handler.py
from typing import List, Dict
import asyncio

class MultiSymptomHandler:
    """多症状分叉流程处理"""

    SYMPTOM_PRIORITY = {
        "胸痛": 1,
        "呼吸困难": 1,
        "意识模糊": 1,
        "头痛": 2,
        "腹痛": 2,
        "发热": 3,
        "咳嗽": 3,
    }

    async def extract_symptoms(self, text: str) -> List[str]:
        """从用户输入中提取多个症状"""
        # 调用 LLM 提取症状列表
        pass

    async def prioritize(self, symptoms: List[str]) -> List[str]:
        """按优先级排序症状"""
        return sorted(
            symptoms,
            key=lambda s: self.SYMPTOM_PRIORITY.get(s, 99)
        )

    async def create_fork(self, state: ConsultationState, symptoms: List[str]):
        """创建多症状采集分支"""
        # 主症状 → 次症状依次处理
        # 每个症状完整采集后再处理下一个
        pass
```

### 6.3 意图分类器

```python
# app/services/intent_classifier.py
from enum import Enum

class Intent(Enum):
    RELEVANT_INFO = "relevant_info"      # 提供相关信息
    IRRELEVANT_CHAT = "irrelevant_chat"  # 无关聊天
    QUESTION = "question"                # 提问
    COMPLAINT = "complaint"              # 抱怨
    EMOTIONAL = "emotional"              # 情绪宣泄

class IntentClassifier:
    """用户意图分类"""

    async def classify(self, user_input: str) -> Intent:
        """
        使用 LLM 分类用户意图
        指导后续响应策略（继续提问 / 引导回正轨 / 安抚情绪）
        """
        prompt = f"""
        将以下用户输入分类为以下意图之一：
        - relevant_info: 提供症状或病史相关信息
        - irrelevant_chat: 与问诊无关的聊天
        - question: 用户提问（如"为什么要问这个"）
        - complaint: 抱怨或表达不满
        - emotional: 情绪宣泄或焦虑表达

        输入: {user_input}
        输出意图类别（仅输出类别名称）:
        """
        # 调用 LLM
        pass
```

### 6.4 会话管理器

```python
# app/services/session_manager.py
from datetime import datetime, timedelta
from typing import Dict
from app.models.consultation_state import ConsultationState

class SessionManager:
    """内存会话管理（30分钟超时）"""

    def __init__(self, timeout_minutes: int = 30):
        self.sessions: Dict[str, ConsultationState] = {}
        self.timeout = timedelta(minutes=timeout_minutes)

    def get_or_create(self, session_id: str = None) -> ConsultationState:
        """获取或创建会话"""
        self._cleanup_expired()

        if session_id and session_id in self.sessions:
            self.sessions[session_id].last_update = datetime.now()
            return self.sessions[session_id]

        new_id = session_id or self._generate_id()
        new_state = ConsultationState(session_id=new_id)
        self.sessions[new_id] = new_state
        return new_state

    def update(self, session_id: str, state: ConsultationState):
        """更新会话状态"""
        self.sessions[session_id] = state

    def _cleanup_expired(self):
        """清理超时会话"""
        now = datetime.now()
        expired = [
            sid for sid, state in self.sessions.items()
            if now - state.last_update > self.timeout
        ]
        for sid in expired:
            del self.sessions[sid]

    def _generate_id(self) -> str:
        """生成唯一会话ID"""
        import uuid
        return str(uuid.uuid4())
```

---

## 7. 验证与测试计划

### 7.1 测试策略分层

采用**四层测试金字塔**确保系统可靠性：

1. **单元测试层**：对每个核心服务（情感支持、冲突解决、置信度评分、结构化提取、紧急检测）编写独立测试，覆盖正常路径、边界条件和异常情况。

2. **集成测试层**：验证 LangGraph 状态机的节点转换逻辑是否正确，特别是多症状分叉、冲突回溯、意图分类等关键流程。

3. **端到端测试层**：模拟真实问诊场景，从用户输入到病历生成的完整流程验证。

4. **医疗准确性验证层**：与专业医生协作，使用真实问诊案例对生成的病历进行盲测评估，确保临床可用性。

### 7.2 关键测试用例

#### 紧急识别测试
- **输入**: "我感觉胸口很疼，呼吸困难"
- **预期**: 触发红色预警，立即生成急诊建议，终止常规问诊流程

#### 冲突解决测试
- **场景**: 用户先说"无过敏史"，后说"我对青霉素过敏"
- **预期**: 检测到冲突，触发回溯确认，温和询问哪个信息准确

#### 多症状处理测试
- **输入**: "我头痛，还有点肚子不舒服"
- **预期**: 优先处理头痛（完整采集主诉、现病史），再处理腹痛

#### 幻觉防护测试
- **输入**: 模糊输入如"就是不太舒服"
- **预期**: 返回低置信度标记，而非编造具体症状

### 7.3 性能与安全验证

- **并发测试**: 100个同时进行的问诊会话，验证内存占用和超时清理
- **隐私保护测试**: 输入包含姓名、身份证号、手机号，验证脱敏效果
- **注入攻击测试**: SQL注入、XSS、提示词注入等攻击向量验证
- **温度参数验证**: 确认提取类使用 temperature=0，对话类使用 temperature=0.7

---

## 8. 部署与运维

### 8.1 环境配置

```bash
# .env 示例
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4
SESSION_TIMEOUT_MINUTES=30
MAX_CONVERSATION_LENGTH=50
```

### 8.2 启动命令

```bash
# 开发环境
uvicorn app.main:app --reload --port 8000

# 生产环境
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 9. 架构约束合规性

| 约束 | 要求 | 设计 |
|------|------|------|
| Python 文件行数 | < 200 行 | 每个服务文件独立设计，预期 < 200 行 |
| 文件夹文件数 | < 8 个 | 按功能分层：services/, models/, schemas/, api/, graph/ |
| 测试覆盖率 | > 85% | 四层测试策略，关键路径全覆盖 |

### 文件组织结构

```
app/
├── __init__.py
├── main.py                    (< 100 行)
├── dependencies.py            (< 50 行)
├── api/
│   ├── __init__.py
│   ├── consultation.py        (< 150 行)
│   └── health.py              (已存在)
├── services/
│   ├── __init__.py
│   ├── emotion_support.py     (< 200 行)
│   ├── conflict_resolution.py (< 200 行)
│   ├── confidence_scoring.py  (< 150 行)
│   ├── structured_extraction.py (< 200 行)
│   ├── emergency_detection.py (< 150 行)
│   ├── input_sanitization.py  (< 100 行)
│   ├── multi_symptom_handler.py (< 180 行)
│   ├── intent_classifier.py   (< 100 行)
│   └── session_manager.py     (< 120 行)
├── models/
│   ├── __init__.py
│   ├── medical_record.py      (< 150 行)
│   └── consultation_state.py  (< 80 行)
├── schemas/
│   ├── __init__.py
│   └── consultation.py        (< 50 行)
└── graph/
    ├── __init__.py
    └── consultation_graph.py  (< 200 行)
```

---

## 10. 后续扩展方向

1. **语音输入支持**: 集成 STT/TTS 服务
2. **多模态输入**: 支持图片上传（如皮疹照片）
3. **知识库增强**: 集成医学指南库辅助诊断
4. **医生协作模式**: 支持医生介入修正 AI 生成的病历
5. **数据分析**: 匿名化后的流行病学分析

---

**文档版本**: 1.0
**最后更新**: 2025-01-16
