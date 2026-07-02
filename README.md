# 高校教室管理系统

## 项目简介

这是一个基于 MySQL 的高校教室管理系统课程设计项目，包含数据库设计、建表 SQL、测试数据、触发器与视图的初步实现。项目以“代码共享、数据库本地搭建”为协作模式，避免把敏感信息写入 Git 仓库。

## 目录结构

- `sql/`: SQL 脚本
- `app/`: Python 连接脚本与后续演示代码
- `docs/`: 文档与设计说明
- `design.md`: 数据库设计说明
- `plan.md`: 项目开发计划
- `.gitignore`: Git 忽略配置
- `README.md`: 项目说明与协作流程

## 重要说明

- 不要将 `classrooms.db` 上传到 GitHub。
- 不要将 `.env` 文件提交到仓库。
- 如果你收到 `classrooms.db`，请单独保存并在本地使用，切勿放入仓库目录。

## 共享协作规则

1. 代码、SQL、文档共享到 GitHub。
2. 每位成员在本地搭建 MySQL 数据库。
3. 由共享仓库中的 `sql/create_tables.sql` 建库建表。
4. 本地数据库连接配置写入 `.env`，不提交到仓库。

## 环境准备

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

```bash
mysql -u <your_user> -p classroom_management < sql/insert_test_data.sql
```

### 8. 如果需要重置数据库

```bash
mysql -u <your_user> -p classroom_management < sql/drop_tables.sql
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

#### 如果你负责 Python 代码
- 在 `app/` 中添加或修改演示脚本
- 使用 `app/db_connect.py` 获取连接
- 不要把 `.env` 提交到仓库

#### 如果你负责文档
- 更新 `docs/数据库设计说明.md`
- 完善 `docs/数据字典.md`
- 补充 `design.md` 与 `plan.md`

### 4. 本地测试

- 运行 `app/db_connect.py` 验证连接
- 运行 SQL 脚本验证建表、插入数据是否正常
- 如果修改了 SQL，建议先在本地执行 `sql/create_tables.sql` 和 `sql/insert_test_data.sql`

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

## 项目发展建议

- `sql/create_tables.sql`：主要建表结构。
- `sql/insert_test_data.sql`：测试数据。
- `sql/triggers.sql`：预约冲突检测与审核同步触发器。
- `sql/views.sql`：预约详情、课程安排、利用率统计视图。
- `sql/queries.sql`：空闲教室、热门教室、教师统计等常用查询。

如果你收到 `classrooms.db`，请先在本地使用它进行数据迁移，切勿直接上传数据库文件。
