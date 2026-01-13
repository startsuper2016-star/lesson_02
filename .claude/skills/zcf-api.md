# ZCF API Development Skill

FastAPI RESTful API 开发全流程，从接口设计到文档生成的完整解决方案。

## 功能描述

提供完整的 API 开发支持：
- RESTful 接口设计
- 自动化文档生成
- 请求验证
- 错误处理
- 认证授权
- 限流缓存
- 版本管理

---

## 使用方式

### 创建 API 端点
```
你：/zcf:api create /api/users --crud

Claude：创建用户 CRUD API...

【接口设计】
资源：User (用户)
基础路径：/api/users

路由设计：
├── GET    /api/users          # 列表（分页、过滤、排序）
├── POST   /api/users          # 创建
├── GET    /api/users/{id}     # 详情
├── PUT    /api/users/{id}     # 完整更新
├── PATCH  /api/users/{id}     # 部分更新
└── DELETE /api/users/{id}     # 删除

【生成文件】
✓ app/schemas/user.py (85 行)
  ├── UserListQuery (查询参数)
  ├── UserCreate (创建请求)
  ├── UserUpdate (更新请求)
  └── UserResponse (响应模型)

✓ app/api/users.py (145 行)
  ├── get_users() (列表)
  ├── create_user() (创建)
  ├── get_user() (详情)
  ├── update_user() (更新)
  ├── patch_user() (部分更新)
  └── delete_user() (删除)

✓ tests/test_users_api.py (200 行)
  ├── test_list_users()
  ├── test_create_user()
  ├── test_get_user()
  ├── test_update_user()
  ├── test_patch_user()
  ├── test_delete_user()
  └── test_validation_errors()

【功能特性】
✅ 请求验证（Pydantic）
✅ 自动文档（Swagger UI）
✅ 错误处理（HTTPException）
✅ 状态码规范
✅ 响应格式统一

【访问地址】
API 文档：http://localhost:8000/docs
ReDoc：http://localhost:8000/redoc

🎉 API 创建完成！
```

### API 版本管理
```
你：/zcf:api version v2

Claude：创建 API v2...

【版本策略】
URL 路径版本：/api/v2/

【生成结构】
app/
├── api/
│   ├── v1/
│   │   ├── __init__.py
│   │   └── users.py      # v1 用户接口
│   └── v2/
│       ├── __init__.py
│       └── users.py      # v2 用户接口（改进版）

【变更内容】
v1 → v2 改进：
├── 响应格式优化
├── 添加分页默认值
├── 新增过滤字段
└── 性能优化（缓存）

【路由注册】
# app/main.py
app.include_router(v1_router, prefix="/api/v1")
app.include_router(v2_router, prefix="/api/v2")

【向后兼容】
✅ v1 接口保留
✅ 添加弃用警告
⚠️  建议迁移到 v2

【迁移指南】
1. 更新基础路径：/api/v1 → /api/v2
2. 调整响应格式解析
3. 利用新功能（过滤、分页）

版本创建完成！
```

---

## RESTful 设计规范

### HTTP 方法映射
```
┌─────────┬─────────────┬──────────┬────────────┐
│ 方法    │ 路径        │ 操作     │ 幂等性     │
├─────────┼─────────────┼──────────┼────────────┤
│ GET     │ /resources  │ 列表     │ ✅         │
│ POST    │ /resources  │ 创建     │ ❌         │
│ GET     │ /resources/1│ 详情     │ ✅         │
│ PUT     │ /resources/1│ 完整更新 │ ✅         │
│ PATCH   │ /resources/1│ 部分更新 │ ✅         │
│ DELETE  │ /resources/1│ 删除     │ ✅         │
└─────────┴─────────────┴──────────┴────────────┘
```

### 状态码规范
```python
# 成功响应
200 OK          # 查询成功
201 Created     # 创建成功
204 No Content  # 删除成功

# 客户端错误
400 Bad Request         # 请求参数错误
401 Unauthorized        # 未认证
403 Forbidden          # 无权限
404 Not Found          # 资源不存在
409 Conflict           # 资源冲突
422 Unprocessable Entity # 验证失败
429 Too Many Requests   # 请求过多

# 服务器错误
500 Internal Server Error  # 服务器错误
503 Service Unavailable    # 服务不可用
```

### 统一响应格式
```python
# 成功响应
{
    "success": true,
    "data": {...},
    "message": "操作成功"
}

# 列表响应
{
    "success": true,
    "data": {
        "items": [...],
        "total": 100,
        "page": 1,
        "page_size": 20,
        "pages": 5
    }
}

# 错误响应
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "验证失败",
        "details": {
            "email": "邮箱格式不正确"
        }
    }
}
```

---

## 请求验证

### Pydantic Schema
```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """用户基础模型"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    """创建用户请求"""
    password: str = Field(..., min_length=8, max_length=100)

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含大写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含数字')
        return v

class UserUpdate(BaseModel):
    """更新用户请求（部分更新）"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(UserBase):
    """用户响应"""
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class UserListQuery(BaseModel):
    """用户列表查询参数"""
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    search: Optional[str] = None
    is_active: Optional[bool] = None
    sort_by: Optional[str] = "created_at"
    order: Optional[str] = Field("desc", regex="^(asc|desc)$")
```

### 路由验证
```python
# app/api/users.py
from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_active: Optional[bool] = Query(None, description="激活状态"),
    sort_by: str = Query("created_at", description="排序字段"),
    order: str = Query("desc", regex="^(asc|desc)$"),
):
    """获取用户列表"""
    # 业务逻辑
    pass

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """创建用户"""
    # 验证邮箱唯一性
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail={"code": "EMAIL_EXISTS", "message": "邮箱已存在"}
        )

    # 创建用户
    user = User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
```

---

## 错误处理

### 全局异常处理
```python
# app/api/exceptions.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP 异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.detail.get("code") if isinstance(exc.detail, dict) else "HTTP_ERROR",
                "message": exc.detail.get("message") if isinstance(exc.detail, dict) else str(exc.detail),
                "details": exc.detail.get("details") if isinstance(exc.detail, dict) else None
            }
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """值错误处理"""
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(exc)
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "服务器内部错误"
            }
        }
    )
```

### 自定义异常
```python
# app/core/exceptions.py
class APIException(Exception):
    """API 异常基类"""
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundException(APIException):
    """资源不存在"""
    def __init__(self, resource: str = "资源"):
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource}不存在",
            status_code=404
        )

class ConflictException(APIException):
    """资源冲突"""
    def __init__(self, message: str = "资源冲突"):
        super().__init__(
            code="CONFLICT",
            message=message,
            status_code=409
        )

# 使用
@router.get("/users/{user_id}")
async def get_user(user_id: UUID):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("用户")
    return user
```

---

## 认证授权

### JWT 认证
```python
# app/core/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """验证令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据"
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    return user

# 使用
@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    return current_user
```

### 权限控制
```python
# app/core/permissions.py
from functools import wraps
from fastapi import HTTPException

def require_permission(permission: str):
    """权限检查装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if not current_user.has_permission(permission):
                raise HTTPException(
                    status_code=403,
                    detail="权限不足"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# 使用
@router.delete("/users/{user_id}")
@require_permission("user.delete")
async def delete_user(user_id: UUID, current_user: User = Depends(get_current_user)):
    """删除用户（需要权限）"""
    pass
```

---

## 限流与缓存

### 速率限制
```python
# app/core/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# app/main.py
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 使用
from app.core.rate_limit import limiter

@router.post("/auth/login")
@limiter.limit("5/minute")  # 每分钟 5 次
async def login(request: Request, credentials: LoginSchema):
    """用户登录（限流）"""
    pass
```

### 响应缓存
```python
# app/core/cache.py
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

# 初始化
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# 使用
@router.get("/users/{user_id}")
@cache(expire=60)  # 缓存 60 秒
async def get_user(user_id: UUID):
    """获取用户（缓存）"""
    pass
```

---

## API 文档

### 自动化文档
```python
# app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Lesson 02 API",
    description="FastAPI 后端接口文档",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

def custom_openapi():
    """自定义 OpenAPI 配置"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Lesson 02 API",
        version="2.0.0",
        description="完整的 API 文档",
        routes=app.routes,
    )

    # 添加认证配置
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### 文档注释
```python
@router.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=201,
    summary="用户注册",
    description="创建新用户账号，注册成功后返回用户信息和 JWT Token",
    responses={
        201: {"description": "注册成功"},
        409: {"description": "邮箱已存在"},
        422: {"description": "验证失败"},
    },
    tags=["认证"],
)
async def register(
    user_data: UserCreate,
    request: Request,
):
    """
    用户注册接口

    **请求示例：**
    ```json
    {
        "email": "user@example.com",
        "username": "john_doe",
        "password": "SecurePass123!"
    }
    ```

    **响应示例：**
    ```json
    {
        "id": "uuid",
        "email": "user@example.com",
        "username": "john_doe",
        "is_active": true,
        "created_at": "2024-01-13T10:30:00Z"
    }
    ```

    **验证规则：**
    - 邮箱必须是有效格式
    - 用户名长度 3-50 字符
    - 密码至少 8 字符，包含大小写字母和数字
    """
    pass
```

---

## 测试 API

### API 测试套件
```python
# tests/test_users_api.py
from fastapi.testclient import TestClient

client = TestClient(app)

class TestUsersAPI:
    """用户 API 测试"""

    def test_list_users(self):
        """测试获取用户列表"""
        response = client.get("/api/users")
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert "items" in data["data"]
        assert isinstance(data["data"]["items"], list)

    def test_create_user(self):
        """测试创建用户"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "SecurePass123!"
        }

        response = client.post("/api/users", json=user_data)
        assert response.status_code == 201

        data = response.json()
        assert data["email"] == user_data["email"]
        assert "id" in data
        assert "password" not in data  # 不返回密码

    def test_validation_error(self):
        """测试验证错误"""
        invalid_data = {
            "email": "invalid-email",
            "username": "ab",  # 太短
            "password": "short"  # 太弱
        }

        response = client.post("/api/users", json=invalid_data)
        assert response.status_code == 422

        errors = response.json()["detail"]
        assert any("email" in str(e).lower() for e in errors)
```

---

## 配置选项

### API 配置
```python
# app/config.py
class APIConfig:
    """API 配置"""
    API_PREFIX: str = "/api"
    VERSION: str = "v2"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # 分页默认值
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # 限流配置
    RATE_LIMIT: str = "100/minute"

    # 缓存配置
    CACHE_TTL: int = 60  # 秒

    # CORS 配置
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "https://example.com"
    ]
```

---

## 最佳实践

1. **RESTful 设计**：遵循资源导向的 URL 设计
2. **版本管理**：从第一版就考虑版本控制
3. **统一响应**：保持响应格式一致
4. **充分验证**：使用 Pydantic 严格验证输入
5. **清晰文档**：为每个端点编写详细文档
6. **安全第一**：认证、授权、限流一个都不能少
7. **性能优化**：合理使用缓存和分页
8. **测试覆盖**：确保每个端点都有测试

---

## 常见问题

### Q1: 如何处理大文件上传？
```python
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """文件上传（流式处理）"""
    # 验证文件大小
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, "文件过大")

    # 保存文件
    filename = f"{uuid.uuid4()}{file.filename}"
    with open(f"uploads/{filename}", "wb") as f:
        f.write(content)

    return {"filename": filename}
```

### Q2: 如何实现异步任务？
```python
from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379")

@router.post("/reports/generate")
async def generate_report():
    """生成报告（异步任务）"""
    task = celery_app.send_task("generate_report")
    return {"task_id": task.id}

@router.get("/reports/status/{task_id}")
async def get_report_status(task_id: str):
    """获取任务状态"""
    result = celery_app.AsyncResult(task_id)
    return {
        "status": result.state,
        "result": result.result if result.ready() else None
    }
```
