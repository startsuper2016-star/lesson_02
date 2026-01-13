# ZCF Code Review Skill

智能代码审查工具，自动化检测代码质量、架构违规和潜在问题。

## 功能描述

提供全方位的代码审查服务，包括：
- 架构约束检查
- 代码质量分析
- 潜在问题检测
- 最佳实践建议
- 性能优化提示

---

## 使用方式

### 全面审查
```
你：/zcf:review

Claude：正在执行代码审查...

🔍 扫描代码库...
✓ 分析 12 个文件
✓ 检查 450 行代码

📊 审查报告

【架构约束】
✅ 文件行数：平均 67 行（限制：200）
✅ 文件夹结构：清晰（最多 6 个文件/目录）
✅ 模块职责：单一职责原则遵守
⚠️  app/services/user.py:185 行，接近限制

【代码质量】
✅ DRY：无重复代码
✅ KISS：代码简洁易懂
✅ 命名：符合规范
⚠️  硬编码配置：app/config.py:15
⚠️  魔法数字：app/services/payment.py:78

【潜在问题】
🔴 严重：
   - SQL 注入风险：app/repository/user.py:45
   - 密码明文存储：app/models/user.py:23

🟡 警告：
   - 未处理的异常：app/api/auth.py:67
   - 缺少类型注解：app/utils/helper.py:12

【性能优化】
💡 建议：
   - N+1 查询：app/services/order.py:90
   - 缺少索引：app/models/product.py:15
   - 可添加缓存：app/api/product.py:34

【安全检查】
🔒 发现：
   - CORS 配置过于宽松：app/main.py:28
   - 缺少速率限制：app/api/auth.py:12
   - 敏感信息日志：app/services/payment.py:45

【建议修复】
优先级 P0（立即修复）：
1. SQL 注入漏洞
2. 密码加密存储

优先级 P1（本周修复）：
3. 异常处理完善
4. 类型注解补充

优先级 P2（下个迭代）：
5. 性能优化
6. 代码重构
```

### 单文件审查
```
你：/zcf:review app/services/user.py

Claude：审查 app/services/user.py...

📄 文件：app/services/user.py (185 行)
⚠️  行数接近限制，建议拆分

【结构分析】
- 函数数量：8 个
- 平均函数长度：18 行
- 最大函数：update_user() (45 行) ⚠️

【代码质量】
✅ 单一职责：清晰
✅ 命名规范：符合
⚠️  复杂度：update_user() 圈复杂度 12

【问题发现】
🔴 P0:
   - 缺少输入验证：line 67
   - 事务未回滚：line 134

🟡 P1:
   - 重复代码：line 89-97 vs line 145-153
   - 硬编码角色：line 178

【重构建议】
1. 拆分为 UserService + UserValidator
2. 提取公共逻辑到私有方法
3. 添加输入验证装饰器
```

### Git Diff 审查
```
你：/zcf:review --diff

Claude：审查变更...

📝 变更概览：
+ 新增文件：2 个
~ 修改文件：5 个
- 删除文件：1 个
+ 新增行数：234 行
- 删除行数：89 行

【关键变更】
⚠️  app/models/user.py:
   - 移除了 email_unique 约束
   - 影响：可能导致重复邮箱

✅ app/services/auth.py:
   - 添加了速率限制
   - 改进：安全性提升

🔴 发现问题：
   - 缺少数据库迁移脚本
   - 未更新相关测试

【建议】
1. 恢复 email_unique 约束
2. 创建 Alembic 迁移
3. 更新测试用例
```

---

## 审查维度

### 1. 架构约束

#### 文件行数检查
```python
# 硬性指标
MAX_LINES_PYTHON = 200
MAX_LINES_JAVA = 250
MAX_LINES_JS = 200

# 检测
if line_count > MAX_LINES:
    warning(f"文件 {file} 超过 {MAX_LINES} 行，当前 {line_count} 行")
    suggest("拆分为多个文件/模块")
```

#### 文件夹结构检查
```python
# 硬性指标
MAX_FILES_PER_DIR = 8

# 检测
file_count = count_files(directory)
if file_count > MAX_FILES_PER_DIR:
    warning(f"目录 {dir} 文件过多：{file_count} 个")
    suggest("创建子目录分类组织")
```

#### 依赖方向检查
```python
# 正确依赖方向
api → services → models
     ↓
  schemas

# 错误依赖方向
models → services  ❌ 违反依赖倒置
```

### 2. SOLID 原则

#### S - 单一职责
```python
# ❌ 违反
class UserService:
    def create_user(self): ...
    def send_email(self): ...     # 应该独立
    def generate_report(self): ... # 应该独立

# ✅ 符合
class UserService:
    def create_user(self): ...

class EmailService:
    def send_email(self): ...

class ReportService:
    def generate_report(self): ...
```

#### O - 开闭原则
```python
# ❌ 违反
def process_payment(payment_type):
    if payment_type == 'wechat':
        # 微信支付逻辑
    elif payment_type == 'alipay':
        # 支付宝逻辑

# ✅ 符合
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self): pass

class WechatPay(PaymentProcessor): ...
class Alipay(PaymentProcessor): ...
```

### 3. 代码坏味道

#### 僵化性检测
```python
# 检测点：
- 修改一处需要改多处
- 硬编码配置
- 紧耦合的模块
```

#### 冗余性检测
```python
# 检测点：
- 重复的代码块
- 相似的函数
- 重复的验证逻辑

# 自动建议
def extract_common_logic():
    suggest("提取为独立函数/类")
```

#### 循环依赖检测
```python
# 检测
app/api/users.py → app/services/user.py
app/services/user.py → app/api/users.py  ❌

# 建议
→ app/interfaces/user_interface.py
```

### 4. 安全检查

#### 常见漏洞
```python
# SQL 注入
❌ query = f"SELECT * FROM users WHERE id = {user_id}"
✅ query = "SELECT * FROM users WHERE id = ?"

# XSS
❌ return f"<div>{user_input}</div>"
✅ return escape(user_input)

# 敏感信息
❌ logger.info(f"Password: {password}")
✅ logger.info("Password updated")

# 密码存储
❌ password = "plaintext"
✅ hashed = bcrypt.hash(password)
```

### 5. 性能检查

#### N+1 查询
```python
# ❌ N+1 问题
users = db.query(User).all()
for user in users:
    orders = db.query(Order).filter_by(user_id=user.id).all()

# ✅ 预加载
users = db.query(User).options(joinedload(User.orders)).all()
```

#### 缺少索引
```python
# 检测慢查询
db.query(User).filter_by(email=email).first()

# 建议
# 添加索引：CREATE INDEX idx_user_email ON users(email);
```

### 6. 测试覆盖

```python
# 检测
- 未测试的函数
- 缺少边界测试
- 缺少异常测试

# 建议
tests = analyze_coverage()
if tests.coverage < 80:
    suggest("测试覆盖率低于 80%，建议补充测试")
```

---

## 审查配置

### 严格级别
```bash
# 严格模式
/zcf:review --strict
# 启用所有检查，零容忍

# 适中模式（默认）
/zcf:review --moderate
# 核心检查，适度灵活

# 宽松模式
/zcf:review --loose
# 仅关键问题
```

### 检查范围
```bash
# 全项目
/zcf:review

# 指定目录
/zcf:review app/services/

# 指定文件
/zcf:review app/services/user.py

# Git 变更
/zcf:review --diff
/zcf:review --staged
```

### 排除项
```bash
# 排除测试文件
/zcf:review --exclude "tests/"

# 排除生成文件
/zcf:review --exclude "**/*generated.py"

# 排除多个
/zcf:review --exclude "tests/,migrations/"
```

---

## 自动修复

```
你：/zcf:review --fix

Claude：正在审查并自动修复...

【自动修复】
✓ 格式化代码：app/services/user.py
✓ 添加类型注解：app/api/auth.py
✓ 移除未使用导入：app/models/user.py
✓ 提取重复代码：app/utils/helper.py

【需要手动修复】
⚠️  SQL 注入风险：app/repository/user.py:45
   建议使用参数化查询

⚠️  缺少验证：app/services/auth.py:67
   建议添加 Pydantic 验证

修复完成：
- 自动：4 项
- 手动：2 项
```

---

## 报告格式

### Markdown（默认）
```markdown
# 代码审查报告

## 概览
- 文件数：12
- 总行数：450
- 问题数：8

## 问题清单
### 🔴 严重 (2)
1. SQL 注入风险
2. 密码明文存储

### 🟡 警告 (4)
...

### 💡 建议 (2)
...
```

### JSON
```json
{
  "summary": {
    "files": 12,
    "lines": 450,
    "issues": 8
  },
  "issues": [
    {
      "severity": "critical",
      "file": "app/repository/user.py",
      "line": 45,
      "message": "SQL注入风险",
      "suggestion": "使用参数化查询"
    }
  ]
}
```

---

## 最佳实践

1. **定期审查**：每次提交前
2. **持续改进**：修复问题后再次审查
3. **团队协作**：共享审查标准
4. **记录决策**：重大决策添加注释
5. **学习提升**：从错误中学习

---

## 集成 CI/CD

```yaml
# .github/workflows/review.yml
name: Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run AI Review
        run: claude /zcf:review --diff --json > report.json
      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            const report = require('./report.json')
            github.rest.issues.createComment({...})
```
