# ZCF Test-Driven Development Skill

测试驱动开发（TDD）工作流，通过红-绿-重构循环确保代码质量。

## 功能描述

提供完整的 TDD 支持，包括：
- 测试用例生成
- 测试运行与验证
- 代码实现指导
- 重构建议

---

## TDD 循环

### 红灯（Red）- 编写失败的测试
```python
# 1. 先写测试
def test_user_registration():
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 201
    assert "token" in response.json()

# 2. 运行测试（红灯失败）
❌ pytest tests/test_auth.py
   FAILED: 404 Not Found
```

### 绿灯（Green）- 实现最少代码
```python
# 3. 实现功能（最简代码）
@app.post("/api/auth/register")
async def register(user_data: UserCreate):
    return {"status": "created", "token": "fake_token"}

# 4. 运行测试（绿灯通过）
✅ pytest tests/test_auth.py
   PASSED test_user_registration
```

### 重构（Refactor）- 优化代码
```python
# 5. 重构改进
class AuthService:
    async def register(self, data: UserCreate) -> AuthToken:
        # 完整实现
        ...

# 6. 确保测试仍然通过
✅ pytest tests/test_auth.py
   PASSED test_user_registration
```

---

## 使用方式

### 标准 TDD 流程
```
你：/zcf:tdd 实现用户登录功能

Claude：启动 TDD 流程...

【Step 1：需求分析】
功能：用户登录
输入：邮箱 + 密码
输出：JWT Token 或错误信息
验证：
- 邮箱存在
- 密码正确
- 返回有效 token

【Step 2：编写测试（红灯）】
创建：tests/test_auth_login.py

测试用例：
✓ test_valid_credentials()
✓ test_invalid_email()
✓ test_wrong_password()
✓ test_missing_fields()
✓ test_token_format()

运行测试：
❌ 5/5 失败（预期 - 功能未实现）

【Step 3：实现功能（绿灯）】
创建：app/services/auth.py
实现：login() 方法

运行测试：
✅ 5/5 通过

【Step 4：重构优化】
- 提取验证逻辑
- 添加错误处理
- 优化性能

运行测试：
✅ 5/5 通过

【Step 5：边界测试】
补充测试：
✓ test_account_locked()
✓ test_too_many_attempts()
✓ test_expired_token()

最终结果：
✅ 8/8 通过
覆盖率：95%

📊 TDD 循环完成！
```

### 仅生成测试
```
你：/zcf:tdd --test-only 创建用户管理的测试

Claude：生成测试用例...

创建：tests/test_users.py

测试套件：
【CRUD 测试】
✓ test_create_user()
✓ test_get_user()
✓ test_update_user()
✓ test_delete_user()
✓ test_list_users()

【验证测试】
✓ test_email_unique()
✓ test_password_required()
✓ test_invalid_email_format()

【权限测试】
✓ test_unauthorized_access()
✓ test_admin_only_operations()

【边界测试】
✓ test_pagination()
✓ test_filtering()
✓ test_sorting()

总计：15 个测试用例
覆盖率预估：85%
```

---

## 测试类型

### 1. 单元测试
```python
# 测试单个函数/类
class TestUserService:
    def test_hash_password(self):
        service = UserService()
        hashed = service.hash_password("mypassword")
        assert hashed != "mypassword"
        assert service.verify_password("mypassword", hashed)

    def test_validate_email(self):
        service = UserService()
        assert service.validate_email("user@example.com") == True
        assert service.validate_email("invalid") == False
```

### 2. 集成测试
```python
# 测试模块交互
class TestAuthFlow:
    def test_complete_registration_flow(self):
        # 1. 注册
        response = client.post("/api/auth/register", json=...)
        assert response.status_code == 201

        # 2. 验证邮箱
        token = extract_token(response)
        verify_response = client.post(f"/api/auth/verify?token={token}")
        assert verify_response.status_code == 200

        # 3. 登录
        login_response = client.post("/api/auth/login", json=...)
        assert login_response.status_code == 200
        assert "token" in login_response.json()
```

### 3. API 测试
```python
# 测试 HTTP 端点
class TestUserAPI:
    def test_create_user_endpoint(self):
        response = client.post("/api/users", json={
            "email": "test@example.com",
            "username": "testuser"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data
```

### 4. 性能测试
```python
# 测试性能指标
class TestPerformance:
    def test_query_performance(self):
        start = time.time()
        result = db.query(User).all()
        duration = time.time() - start

        assert duration < 0.1  # 100ms 以内
        assert len(result) > 0

    def test_concurrent_requests(self):
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_user(session, i) for i in range(100)]
            results = await asyncio.gather(*tasks)

        assert all(r.status == 200 for r in results)
```

---

## 测试覆盖

### 覆盖率目标
```
总体目标：85%

关键模块：
├── 认证授权：95%
├── 支付逻辑：100%
├── 数据验证：90%
└── 一般业务：80%
```

### 覆盖率报告
```
你：/zcf:tdd --coverage

Claude：生成覆盖率报告...

📊 测试覆盖率报告

总体：87.3% ⭐

模块详情：
app/api/auth.py          95.2%  ✅
app/services/user.py     82.1%  ⚠️
app/models/user.py       100.0% ✅
app/utils/validator.py   68.4%  🔴

未覆盖代码：
app/services/user.py:
  - line 145: 异常处理分支
  - line 178: 边界条件

建议：
1. 补充异常测试
2. 添加边界用例
```

---

## Mock 与 Fixture

### Pydantic Fixture
```python
# tests/conftest.py
@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "username": "testuser"
    }

@pytest.fixture
def authenticated_client(user_data):
    # 注册并登录
    client.post("/api/auth/register", json=user_data)
    response = client.post("/api/auth/login", json=user_data)
    token = response.json()["token"]

    # 返回带认证的客户端
    client.headers["Authorization"] = f"Bearer {token}"
    return client
```

### 数据库 Mock
```python
@pytest.fixture
async def db_session():
    # 使用测试数据库
    async with TestDatabase() as db:
        yield db
    # 清理
    await db.cleanup()

@pytest.fixture
def mock_external_api(monkeypatch):
    async def fake_call(*args, **kwargs):
        return {"status": "success"}

    monkeypatch.setattr(
        "app.services.external.call_api",
        fake_call
    )
```

---

## 测试最佳实践

### ✅ 应该做的
```python
# 1. 测试独立性
def test_one_thing():
    assert function() == expected  # 一个测试一个断言

# 2. 描述性命名
def test_user_cannot_register_with_duplicate_email():
    ...

# 3. 测试边界
def test_password_min_length():
    with pytest.raises(ValidationError):
        UserCreate(password="short")

# 4. 测试异常
def test_invalid_input_raises_error():
    with pytest.raises(ValueError, match="Invalid email"):
        service.validate_email("invalid")
```

### ❌ 不应该做的
```python
# 1. 不要测试实现细节
❌ def test_function_calls_database():
     # 关注结果，不是过程

# 2. 不要写脆弱的测试
❌ def test_exact_string_match():
     assert message == "User created at 2024-01-13 10:30:00"
     # 时间变化导致失败

# 3. 不要忽略测试
❌ @pytest.mark.skip
   def test_important_feature():
       pass

# 4. 不要测试第三方库
❌ def test_fastapi_works():
     # 框架已测试
```

---

## 配置选项

### 测试框架
```bash
# pytest（推荐）
/zcf:tdd --framework pytest

# unittest
/zcf:tdd --framework unittest

# 自定义
/zcf:tdd --framework custom
```

### 测试级别
```bash
# 快速测试（仅单元）
/zcf:tdd --fast

# 完整测试（含集成）
/zcf:tdd --full

# 压力测试
/zcf:tdd --stress
```

### 输出格式
```bash
# 详细输出
/zcf:tdd --verbose

# 简洁输出
/zcf:tdd --quiet

# JSON 报告
/zcf:tdd --json
```

---

## CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with TDD
        run: |
          claude /zcf:tdd --full --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 常见问题

### Q1: 测试太慢？
```
解决方案：
1. 使用 mock 隔离外部依赖
2. 并行测试：pytest -n auto
3. 仅运行相关测试：pytest -k "test_user"
```

### Q2: 测试数据库污染？
```
解决方案：
1. 使用事务回滚
2. 每个测试独立数据库
3. fixture 清理

@pytest.fixture(autouse=True)
async def rollback(db):
    async with db.transaction():
        yield
        await db.rollback()
```

### Q3: 异步代码测试？
```
解决方案：
使用 pytest-asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

---

## 示例：完整 TDD 会话

```
你：/zcf:tdd 实现密码重置功能

Claude：【红灯阶段】
创建测试：
tests/test_password_reset.py

测试用例：
✓ test_request_reset()
✓ test_invalid_email()
✓ test_expired_token()
✓ test_valid_reset()
✓ test_weak_password()

运行：pytest
❌ 5/5 失败

Claude：【绿灯阶段】
实现功能：
app/services/password.py
├── request_reset()
├── verify_token()
├── reset_password()
└── validate_password()

运行：pytest
✅ 5/5 通过

Claude：【重构阶段】
优化：
- 提取 TokenService
- 添加速率限制
- 优化数据库查询

运行：pytest
✅ 5/5 通过

Claude：【补充测试】
添加：
✓ test_too_many_requests()
✓ test_token_reuse()
✓ test_same_password()

最终：pytest
✅ 8/8 通过
覆盖率：92%

📊 功能完成！
```
