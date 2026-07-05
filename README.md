# 高校教室管理系统

## 项目简介

这是一个基于 MySQL 的高校教室管理系统课程设计项目，包含数据库设计、Flask 后端 API、Vue 3 前端页面。项目以“代码共享、数据库本地搭建”为协作模式，避免把敏感信息写入 Git 仓库。

## 目录结构

- `sql/`: SQL 脚本
- `app/`: Python 后端 API（Flask）与数据库连接
- `frontend/`: Vue 3 前端页面
- `docs/`: 文档与设计说明
- `.gitignore`: Git 忽略配置
- `README.md`: 项目说明与协作流程

## 快速启动

完成一次性环境配置后，日常开发只需启动后端和前端两个服务。

### 前置要求

- MySQL 8.x
- Python 3.11+
- Node.js 18+

### 一次性配置（首次克隆后执行）

```bash
# 1. 克隆仓库
git clone 仓库地址
cd classroom-management-system

# 2. 安装 Python 依赖
pip install -r app/requirements.txt

# 3. 配置数据库连接
copy .env.example .env
# 编辑 .env，填入本机 MySQL 账号密码

# 4. 建库建表
mysql -u root -p < sql/create_tables.sql

# 5. 导入测试数据（后需更改为完整数据）
cd app
python seed_data.py
cd ..

# 6. 验证数据库连接
python app/db_connect.py

# 7. 安装前端依赖
cd frontend
npm install
cd ..
```

### 日常启动（两个终端）

**终端 1 — 启动后端 API**

```bash
cd app
python app.py
```

后端地址：`http://localhost:5000`

**终端 2 — 启动前端页面**

```bash
cd frontend
npm run dev
```

前端地址：`http://localhost:5173`

浏览器打开 **http://localhost:5173** 即可使用系统。

### 测试账号

| 账号 | 密码 | 角色 | 进入页面 |
| --- | --- | --- | --- |
| 9001 | 123456 | 管理员 | 管理员端（教室/课程管理、预约审核） |
| 1001 | 123456 | 教师 | 使用者端（查询、预约） |
| 2001 | 123456 | 学生 | 使用者端（查询、预约） |

### 重置测试数据

```bash
cd app
python seed_data.py
```

### 数据库视图

- `View_Reservation_Detail`：聚合预约、用户、教室和审核结果，便于查看预约详情。
- `View_Course_Schedule`：展示课程、教师和教室的排课信息。
- `View_Classroom_Usage`：汇总教室的排课与预约使用情况，便于后续统计分析。

创建方式：
```bash
mysql -u <your_user> -p classroom_management < sql/views.sql
```

## 重要说明

- 不要将 `classrooms.db` 上传到 GitHub。
- 不要将 `.env` 文件提交到仓库。
- 如果你收到 `classrooms.db`，请单独保存并在本地使用，切勿放入仓库目录。

## 共享协作规则

1. 代码、SQL、文档共享到 GitHub。
2. 每位成员在本地搭建 MySQL 数据库。
3. 由共享仓库中的 `sql/create_tables.sql` 建库建表。
4. 本地数据库连接配置写入 `.env`，不提交到仓库。

## 环境准备（详细介绍）

### 1. 克隆仓库

```bash
git clone <仓库地址>
cd classroom-management-system
```

### 2. 创建 Conda 环境并安装依赖

```bash
conda create -n cms-env python=3.11 -y
conda activate cms-env
pip install -r app/requirements.txt
```

### 3. 创建本地数据库和账号

在本机 MySQL 中执行：

```sql
CREATE DATABASE classroom_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

如果你希望创建单独用户，也可以：

```sql
CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON classroom_management.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. 配置本地环境变量

复制 `.env.example` 为 `.env`：

```bash
copy .env.example .env
```

然后打开 `.env`，将其中的值替换为你自己的 MySQL 连接信息。例如：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的密码
DB_NAME=classroom_management
```

### 5. 验证数据库连接

```bash
python app/db_connect.py
```

如果显示 `数据库连接成功`，则表示本地连接正常。

### 6. 执行建表脚本

```bash
mysql -u <your_user> -p classroom_management < sql/create_tables.sql
```

如果你使用 `root`，也可以：

```bash
mysql -u root -p classroom_management < sql/create_tables.sql
```

### 7. 导入测试数据

**Windows（推荐）：**

```bash
cd app
python seed_data.py
```

**Linux / macOS：**

```bash
mysql -u <your_user> -p classroom_management < sql/insert_test_data.sql
```

### 8. 安装并启动前端（首次）

```bash
cd frontend
npm install
npm run dev
```

### 9. 启动后端 API

```bash
cd app
python app.py
```

### 10. 如果需要重置数据库

```bash
mysql -u <your_user> -p classroom_management < sql/drop_tables.sql
mysql -u <your_user> -p < sql/create_tables.sql
cd app && python seed_data.py
```

## 小组协作全流程

### 1. 拉取最新代码

```bash
git checkout main
git pull origin main
```

### 2. 创建功能分支

```bash
git checkout -b feature/<你的功能名>
```

例如：

```bash
git checkout -b feature/sql
```

### 3. 开发你负责的部分

#### 如果你负责数据库结构
- 修改或补全 `sql/create_tables.sql`
- 更新 `sql/insert_test_data.sql`
- 完善 `sql/triggers.sql`、`sql/views.sql`、`sql/queries.sql`

#### 如果你负责 Python 后端
- 维护 `app/app.py` 中的 REST API
- 使用 `app/db_connect.py` 获取连接
- 参考 `docs/后端协作说明.md` 与前端对接
- 不要把 `.env` 提交到仓库

#### 如果你负责前端
- 在 `frontend/` 中开发页面
- 参考 `docs/前端实现文档.md`
- API 基地址配置在 `frontend/.env.development`

#### 如果你负责文档
- 更新 `docs/数据库设计说明.md`
- 完善 `docs/数据字典.md`

### 4. 本地测试

- 运行 `python app/db_connect.py` 验证数据库连接
- 运行 `python app/app.py` 启动后端，确认 `http://localhost:5000` 可访问
- 运行 `cd frontend && npm run dev` 启动前端，确认 `http://localhost:5173` 可登录
- 使用测试账号（9001 / 1001 / 2001，密码均为 123456）验证各角色功能

### 5. 提交并推送

```bash
git add .
git commit -m "完成 <功能描述>"
git push origin feature/<你的功能名>
```

### 6. 发起 Pull Request

- 说明本次修改内容
- 明确测试方式
- 请组员 review 代码

### 7. 合并到主分支

由组长或指定审核人 review 后合并。

## 其他注意事项

- 不要在仓库中提交真实密码或私密配置。
- 不要把 `classrooms.db` 放到仓库里。
- 如果你本地有 `.env`，请确认 `.gitignore` 已忽略。
- 每次协作前先 `git pull`，避免冲突。

## 文档索引

| 文档 | 说明 |
| --- | --- |
| `docs/后端协作说明.md` | 后端 API 约定、联调方式（后端同学必读） |
| `docs/前端实现文档.md` | 前端页面与接口设计（前端同学必读） |
| `docs/数据库设计说明.md` | 表关系、触发器、视图设计 |
| `docs/数据字典.md` | 各表字段含义 |

## 项目发展建议

- `sql/create_tables.sql`：主要建表结构。
- `sql/insert_test_data.sql`：测试数据。
- `sql/triggers.sql`：预约冲突检测与审核同步触发器。
- `sql/views.sql`：预约详情、课程安排、利用率统计视图。
- `sql/queries.sql`：空闲教室、热门教室、教师统计等常用查询。

如果你收到 `classrooms.db`，请先在本地使用它进行数据迁移，切勿直接上传数据库文件。
