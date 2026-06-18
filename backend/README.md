# 法律咨询平台 - 后端

基于 FastAPI 的法律咨询平台后端服务。

## 功能特性

- 用户认证与授权（JWT）
- 律师管理与审核
- 在线咨询
- 预约服务
- 文书模板
- 知识库
- 后台管理

## 快速开始

### 方式一：使用启动脚本

chmod +x start.sh
./start.sh

### 方式二：手动启动

1. 安装依赖

pip install -r requirements.txt

2. 创建上传目录

mkdir -p uploads

3. 配置环境变量（可选）

cp .env.example .env

4. 初始化种子数据

python3 -m app.seed

5. 启动服务

uvicorn app.main:app --reload --port 8000

## 数据库配置

默认使用 SQLite 数据库（legal_platform.db），无需额外配置。

如需使用 PostgreSQL，请修改 .env 文件中的 DATABASE_URL。

## 默认账号

### 管理员
- 用户名: admin
- 密码: admin123

### 律师账号
- lawyer1 / lawyer123 (民事律师)
- lawyer2 / lawyer123 (婚姻家庭律师)
- lawyer3 / lawyer123 (刑事律师)

### 普通用户
- user1 / user123
- user2 / user123
- user3 / user123

## API 文档

启动服务后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

backend/
├── app/
│   ├── api/              # API 路由
│   ├── models/           # 数据模型
│   ├── main.py           # 应用入口
│   ├── config.py         # 配置
│   ├── database.py       # 数据库连接
│   ├── schemas.py        # Pydantic 模型
│   ├── security.py       # 安全相关
│   ├── crud.py           # 数据操作
│   └── seed.py           # 种子数据
├── uploads/              # 上传文件目录
├── requirements.txt      # 依赖
├── start.sh              # 启动脚本 
## 项目结构
