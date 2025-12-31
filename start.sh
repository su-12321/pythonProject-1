#!/usr/bin/env bash
# start.sh - Railway 启动脚本

echo "=== 开始部署 Django 应用 ==="

# 1. 检查Python版本
python --version

# 2. 安装依赖
if [ -f "requirements.txt" ]; then
    echo "安装Python依赖..."
    pip install -r requirements.txt
else
    echo "错误: requirements.txt 不存在"
    exit 1
fi

# 3. 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 4. 运行数据库迁移
echo "运行数据库迁移..."
python manage.py migrate

# 5. 启动Gunicorn服务器
echo "启动Gunicorn服务器..."
exec gunicorn myblog.wsgi:application --bind 0.0.0.0:$PORT
