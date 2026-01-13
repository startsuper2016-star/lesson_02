# ZCF Feature Development Skill

功能开发的完整工作流，从需求分析到代码实现的一站式解决方案。

## 功能描述

提供结构化的功能开发流程，确保：
- 需求理解准确
- 设计方案合理
- 代码质量高
- 符合项目规范
- 完整可测试

---

## 使用方式

### 标准功能开发
```
你：/zcf:feat 实现用户注册功能

Claude：启动功能开发工作流...

【需求分析】
功能：用户注册
输入：邮箱、密码、用户名
输出：用户对象 + JWT Token
验证：邮箱格式、密码强度、邮箱唯一性

【方案设计】
架构设计：
┌─────────┐    ┌──────────┐    ┌──────────┐
│   API   │───→│ Service  │───→│ Database │
└─────────┘    └──────────┘    └──────────┘
     │              │
     v              v
  Schema          Model

文件结构：
app/api/auth.py          # 注册路由
app/schemas/user.py      # 请求/响应模型
app/models/user.py       # 数据模型
app/services/auth.py     # 业务逻辑

【实施计划】
□ 创建 User 模型
□ 创建 UserCreate Schema
□ 实现 AuthService.register()
□ 创建 POST /api/auth/register 端点
□ 添加邮箱验证
□ 添加密码加密
□ 编写测试

【实施中】
正在创建文件...

【完成】
✓ 创建 4 个文件
✓ 实现注册功能
✓ 添加验证逻辑
✓ 编写 5 个测试用例

测试结果：5/5 通过
访问：POST http://localhost:8000/api/auth/register
```

### 快速原型
```
你：/zcf:feat --quick 快速实现一个登录接口

Claude：快速模式启动...
[跳过详细设计，直接实现基础功能]
```

---

## 工作流程

### 1. 需求澄清
- 功能描述
- 输入输出
- 业务规则
- 边界条件

### 2. 技术设计
- API 接口定义
- 数据模型设计
- 业务逻辑拆分
- 依赖关系分析

### 3. 实施计划
- 任务分解
- 优先级排序
- 风险评估

### 4. 代码实现
- 遵循 SOLID 原则
- 符合文件行数限制
- 保持代码简洁
- 添加必要注释

### 5. 质量保证
- 单元测试
- 集成测试
- 代码审查
- 性能检查

---

## 自动化检查

### 架构约束检查
```python
# 检查项
- 文件行数 < 200 行：✓
- 文件夹文件数 < 8 个：✓
- 单一职责原则：✓
- 依赖方向正确：✓
- 无循环依赖：✓
```

### 代码质量检查
```python
# 坏味道检测
- 僵化性：✓ 易于扩展
- 冗余性：✓ 无重复代码
- 脆弱性：✓ 修改安全
- 晦涩性：✓ 代码清晰
- 过度复杂：✓ 设计简洁
```

---

## 常用模式

### CRUD 功能
```
你：/zcf:feat 创建任务管理 CRUD

Claude：实现标准 CRUD...
├── POST   /api/todos/      # 创建
├── GET    /api/todos/      # 列表
├── GET    /api/todos/{id}  # 详情
├── PUT    /api/todos/{id}  # 更新
└── DELETE /api/todos/{id}  # 删除
```

### 关联查询
```
你：/zcf:feat 实现文章评论关联

Claude：设计关联关系...
Post ←─── Comment
  1          N

自动生成：
- 外键约束
- 级联删除
- 关联查询接口
```

### 分页过滤
```
你：/zcf:feat 为用户列表添加分页和搜索

Claude：实现查询增强...
├── 分页参数：page, page_size
├── 排序参数：sort_by, order
├── 过滤参数：status, created_after
└── 搜索参数：q（全文搜索）

生成：PaginatedResponse Schema
```

---

## 测试驱动

### 自动生成测试
```
你：/zcf:feat --tdd 实现邮箱验证功能

Claude：TDD 模式启动...

【Step 1：编写测试】
✓ 创建 tests/test_auth.py
✓ 定义测试用例：
  - test_valid_email()
  - test_invalid_format()
  - test_duplicate_email()

【Step 2：运行测试】
❌ 测试失败：功能未实现

【Step 3：实现功能】
✓ 实现邮箱验证逻辑

【Step 4：验证】
✅ 3/3 测试通过
```

---

## 配置选项

### 实现级别
- `--full`：完整实现（默认）
  - 完整验证
  - 错误处理
  - 日志记录
  - 单元测试

- `--basic`：基础实现
  - 核心功能
  - 基础验证
  - 最简代码

- `--quick`：快速原型
  - 最小可行
  - 跳过测试
  - 占位符实现

### 附加功能
- `--tdd`：测试驱动开发
- `--async`：异步实现
- `--cache`：添加缓存
- `--docs`：生成文档

---

## 示例场景

### 场景 1：用户认证
```
你：/zcf:feat 实现完整的用户认证系统

Claude：功能拆解：
1. 用户注册
2. 邮箱验证
3. 用户登录
4. 密码重置
5. JWT 管理
6. 权限控制

实施顺序：
[1→2→3→4→5→6]

预计文件：
app/api/auth.py          (120 行)
app/schemas/auth.py      (85 行)
app/models/user.py       (65 行)
app/services/auth.py     (180 行)
tests/test_auth.py       (200 行)

是否开始实施？[Y/n]
```

### 场景 2：批量操作
```
你：/zcf:feat 实现批量导入用户

Claude：设计方案：
┌─────────┐    ┌──────────┐    ┌──────────┐
│ 上传文件 │───→│ 解析验证 │───→│ 批量写入 │
└─────────┘    └──────────┘    └──────────┘
                      │
                      v
                 错误报告

支持格式：
- CSV
- Excel
- JSON

验证规则：
- 必填字段
- 数据格式
- 唯一性约束

事务处理：
- 全部成功 or 全部回滚
```

### 场景 3：文件上传
```
你：/zcf:feat 添加头像上传功能

Claude：实现方案：
前端：multipart/form-data
后端：
  - 文件大小限制：5MB
  - 格式验证：jpg, png
  - 存储：本地 / OSS
  - 生成缩略图
  - URL 返回

安全：
- 文件类型检查
- 病毒扫描
- 防止路径穿越
```

---

## 质量报告

每次功能完成后，自动生成：

```
📊 功能开发报告

功能：用户注册
状态：✅ 完成

代码质量：
✓ 架构合理
✓ 符合规范
✓ 测试覆盖 90%
✓ 性能达标

文件统计：
- 新增：4 个文件
- 总行数：350 行
- 平均文件：87.5 行

测试结果：
✅ test_valid_input: PASS
✅ test_duplicate_email: PASS
✅ test_weak_password: PASS
✅ test_invalid_format: PASS
✅ test_success_registration: PASS
5/5 通过

API 文档：
POST /api/auth/register
Request Body:
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "username": "john_doe"
}

Response:
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "john_doe",
  "token": "jwt_token"
}

访问文档：http://localhost:8000/docs
```

---

## 最佳实践

1. **需求明确**：不清楚的地方先询问
2. **小步迭代**：复杂功能分步实现
3. **持续验证**：每步都运行测试
4. **文档同步**：代码和文档一起更新
5. **代码审查**：完成后自我审查

---

## 故障排除

### 常见问题
```
Q: 如何处理复杂业务逻辑？
A: 拆分为多个小功能，逐个实现

Q: 代码超过 200 行怎么办？
A: 拆分为多个文件/模块，保持单一职责

Q: 测试写不完怎么办？
A: 优先测试核心逻辑，边界条件后补

Q: 性能不达标？
A：分析瓶颈，针对性优化（缓存、索引、异步）
```
