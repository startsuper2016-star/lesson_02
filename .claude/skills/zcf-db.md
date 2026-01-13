# ZCF Database Operations Skill

数据库操作全流程管理，包括模型设计、迁移、查询优化和事务处理。

## 功能描述

提供完整的数据库开发支持：
- 数据模型设计
- ORM 配置（SQLAlchemy）
- 数据库迁移（Alembic）
- 查询优化
- 事务管理
- 种子数据

---

## 使用方式

### 创建数据模型
```
你：/zcf:db create model User

Claude：创建 User 模型...

【模型设计】
字段分析：
- id: UUID (主键)
- email: String(255), 唯一, 非空
- username: String(50), 唯一
- password_hash: String(255), 非空
- is_active: Boolean, 默认 True
- created_at: DateTime, 自动生成
- updated_at: DateTime, 自动更新

关系分析：
- User ← Post (一对多)
- User ← Comment (一对多)

【生成文件】
✓ app/models/user.py (67 行)
  └── User 模型
  └── UserCreate Schema
  └── UserUpdate Schema
  └─ UserResponse Schema

✓ alembic/versions/001_create_users.py (45 行)
  └── 迁移脚本

【创建索引】
建议添加：
- idx_user_email (email)
- idx_user_username (username)
- idx_user_created (created_at)

是否应用迁移？[Y/n]
```

### 数据库迁移
```
你：/zcf:db migrate

Claude：检查变更...

检测到变更：
+ 新增：User 模型
~ 修改：Post 模型（添加 author_id 外键）
- 删除：Comment 模型（废弃）

【生成迁移】
✓ alembic/versions/002_add_author_to_posts.py

【迁移内容】
```sql
-- 升级
ALTER TABLE posts ADD COLUMN author_id UUID;
ALTER TABLE posts ADD CONSTRAINT fk_author
  FOREIGN KEY (author_id) REFERENCES users(id);
CREATE INDEX idx_post_author ON posts(author_id);

-- 降级
ALTER TABLE posts DROP COLUMN author_id;
```

【应用迁移】
/zcf:db upgrade
✅ 迁移成功：002_add_author_to_posts

【回滚】
/zcf:db downgrade
✅ 回滚成功：回到版本 001
```

### 查询优化
```
你：/zcf:db optimize app/services/user.py

Claude：分析查询性能...

🔍 检测到问题：

【N+1 查询】
位置：app/services/user.py:89
```python
# ❌ 问题代码
users = db.query(User).all()
for user in users:
    posts = db.query(Post).filter_by(user_id=user.id).all()
```

影响：100 个用户 = 101 次查询

优化方案：
```python
# ✅ 使用 eager loading
users = db.query(User).options(
    joinedload(User.posts)
).all()
```

效果：1 次查询

【缺少索引】
位置：app/models/order.py:23
建议：
```sql
CREATE INDEX idx_order_user_date
ON orders(user_id, created_at);
```

预期提升：查询速度提升 10x

【全表扫描】
位置：app/services/product.py:45
```python
# ❌ 问题
products = db.query(Product).filter(
    Product.name.like(f"%{keyword}%")
).all()
```

优化：
```python
# ✅ 使用全文搜索
products = db.query(Product).filter(
    Product.name.match(keyword)
).all()
```

需要：添加全文索引

【优化报告】
- N+1 查询：3 处
- 缺少索引：5 个
- 全表扫描：2 处
- 预计提升：性能提升 80%

是否应用优化？[Y/n]
```

---

## 数据模型设计

### 基础模型
```python
# app/models/base.py
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class BaseModel:
    """基础模型，提供公共字段"""
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
```

### 用户模型
```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # 关系
    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"<User {self.username}>"
```

### 关联模型
```python
# app/models/post.py
class Post(Base):
    """文章模型"""
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    # 关系
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    # 索引
    __table_args__ = (
        Index("idx_post_author", "author_id"),
        Index("idx_post_created", "created_at"),
    )
```

---

## 事务管理

### 简单事务
```python
from sqlalchemy.orm import Session

def create_user_with_post(db: Session, user_data: dict, post_data: dict):
    """创建用户和文章（事务）"""
    try:
        # 开始事务
        with db.begin():
            # 创建用户
            user = User(**user_data)
            db.add(user)
            db.flush()  # 获取 user.id

            # 创建文章
            post = Post(**post_data, author_id=user.id)
            db.add(post)

        # 提交事务
        return user, post

    except Exception as e:
        # 自动回滚
        raise e
```

### 嵌套事务
```python
from contextlib import contextmanager

@contextmanager
def transaction_scope(db: Session):
    """事务作用域"""
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise

# 使用
def complex_operation(db: Session):
    with transaction_scope(db):
        # 多个操作
        user = create_user(db, ...)
        post = create_post(db, ...)
        send_email(user.email)  # 外部服务
```

### 分布式事务
```python
async def transfer_money(
    db1: Session,
    db2: Session,
    from_account: int,
    to_account: int,
    amount: float
):
    """跨数据库转账（两阶段提交）"""
    try:
        # 阶段 1：准备
        db1.begin_nested()
        db2.begin_nested()

        account1 = db1.query(Account).get(from_account)
        account2 = db2.query(Account).get(to_account)

        account1.balance -= amount
        account2.balance += amount

        # 阶段 2：提交
        db1.commit()
        db2.commit()

    except Exception:
        db1.rollback()
        db2.rollback()
        raise
```

---

## 查询模式

### 基础查询
```python
# 查询所有
users = db.query(User).all()

# 条件查询
active_users = db.query(User).filter(User.is_active == True).all()

# 单个对象
user = db.query(User).filter(User.email == "test@example.com").first()

# 复杂条件
users = db.query(User).filter(
    User.is_active == True,
    User.created_at >= datetime(2024, 1, 1)
).order_by(User.created_at.desc()).limit(10).all()
```

### 关联查询
```python
# Eager Loading（避免 N+1）
users = db.query(User).options(
    joinedload(User.posts)
).all()

# 选择性加载
users = db.query(User).options(
    joinedload(User.posts).load_only(Post.id, Post.title)
).all()

# 筛选关联
posts = db.query(Post).join(User).filter(
    User.is_active == True
).all()
```

### 聚合查询
```python
from sqlalchemy import func

# 统计
count = db.query(func.count(User.id)).scalar()

# 分组
stats = db.query(
    User.created_at.cast(Date),
    func.count(User.id)
).group_by(
    User.created_at.cast(Date)
).all()

# 窗口函数
from sqlalchemy import over

ranked = db.query(
    User,
    func.rank().over(order_by=User.created_at.desc()).label('rank')
).all()
```

---

## 性能优化

### 索引策略
```python
# 单列索引
class User(Base):
    email = Column(String(255), index=True)  # 简单索引

# 复合索引
class Order(Base):
    __table_args__ = (
        Index('idx_order_user_date', 'user_id', 'created_at'),
    )

# 唯一索引
class User(Base):
    __table_args__ = (
        UniqueConstraint('email', name='uq_user_email'),
    )

# 表达式索引
from sqlalchemy import text, Index

class User(Base):
    __table_args__ = (
        Index('idx_user_lower_email', text('lower(email)')),
    )
```

### 查询优化
```python
# 1. 只查询需要的字段
users = db.query(User.id, User.username).all()

# 2. 使用 EXISTS 代替 IN
# ❌ 慢
subq = db.query(User.id).filter(User.is_active == True)
posts = db.query(Post).filter(Post.author_id.in_(subq)).all()

# ✅ 快
posts = db.query(Post).filter(
    db.query(User.id).filter(
        User.id == Post.author_id,
        User.is_active == True
    ).exists()
).all()

# 3. 批量操作
# ❌ 慢（循环插入）
for data in users_data:
    user = User(**data)
    db.add(user)
    db.commit()

# ✅ 快（批量插入）
db.bulk_insert_mappings(User, users_data)
db.commit()

# 4. 使用连接池
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # 自动重连
)
```

---

## 数据种子

### 固定数据
```python
# app/db/seed.py
def seed_permissions(db: Session):
    """初始化权限数据"""
    permissions = [
        Permission(name="read", description="读取权限"),
        Permission(name="write", description="写入权限"),
        Permission(name="delete", description="删除权限"),
    ]

    db.add_all(permissions)
    db.commit()

# 使用
/zcf:db seed permissions
✓ 创建 3 条权限记录
```

### 测试数据
```python
def seed_test_data(db: Session, count: int = 100):
    """生成测试数据"""
    from faker import Faker

    fake = Faker()

    users = [
        User(
            email=fake.email(),
            username=fake.user_name(),
            password_hash=hash_password("password123")
        )
        for _ in range(count)
    ]

    db.bulk_save_objects(users)
    db.commit()

    print(f"✓ 创建 {count} 条测试用户")

# 使用
/zcf:db seed test --count 1000
✓ 创建 1000 条测试用户
```

---

## 备份与恢复

### 数据备份
```bash
# PostgreSQL
pg_dump -U user -d database > backup.sql

# 带压缩
pg_dump -U user -d database | gzip > backup.sql.gz

# 仅结构
pg_dump -U user -d database --schema-only > schema.sql

# 仅数据
pg_dump -U user -d database --data-only > data.sql
```

### 数据恢复
```bash
# PostgreSQL
psql -U user -d database < backup.sql

# 从压缩恢复
gunzip -c backup.sql.gz | psql -U user -d database
```

### 自动备份脚本
```python
# app/db/backup.py
import subprocess
from datetime import datetime

def backup_database(db_url: str, output_dir: str):
    """自动备份数据库"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/backup_{timestamp}.sql.gz"

    cmd = f"pg_dump {db_url} | gzip > {output_file}"
    subprocess.run(cmd, shell=True, check=True)

    print(f"✓ 备份完成：{output_file}")

# 定时任务
# /zcf:db backup --schedule "0 2 * * *"  # 每天凌晨 2 点
```

---

## 配置选项

### 数据库类型
```bash
# PostgreSQL（推荐）
/zcf:db init --type postgresql

# MySQL
/zcf:db init --type mysql

# SQLite（开发）
/zcf:db init --type sqlite
```

### 连接配置
```python
# app/db/config.py
DATABASE_CONFIG = {
    "postgresql": {
        "url": "postgresql://user:pass@localhost/db",
        "pool_size": 10,
        "max_overflow": 20,
        "pool_recycle": 3600,
        "echo": False,  # 生产环境设为 False
    }
}
```

---

## 最佳实践

1. **始终使用事务**：确保数据一致性
2. **合理使用索引**：提升查询性能
3. **避免 N+1 查询**：使用 eager loading
4. **批量操作**：减少数据库往返
5. **定期备份**：保护重要数据
6. **监控性能**：使用慢查询日志
7. **使用连接池**：复用数据库连接
8. **软删除**：保留数据历史记录

---

## 常见问题

### Q1: 如何处理并发更新？
```python
# 使用乐观锁
class Product(Base):
    version = Column(Integer, default=1)

    def update_with_version_check(self, db: Session, **kwargs):
        current_version = self.version
        self.__dict__.update(kwargs)
        self.version += 1

        result = db.execute(
            update(Product)
            .where(Product.id == self.id)
            .where(Product.version == current_version)
            .values(version=self.version)
        )

        if result.rowcount == 0:
            raise StaleDataError("数据已被其他用户修改")
```

### Q2: 如何实现分页？
```python
def paginate(query: Query, page: int = 1, page_size: int = 20):
    """分页查询"""
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )
```

### Q3: 如何实现软删除？
```python
class SoftDeleteMixin:
    """软删除混入类"""
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now()

# 查询时过滤
def get_active_users(db: Session):
    return db.query(User).filter(User.deleted_at.is_(None)).all()
```
