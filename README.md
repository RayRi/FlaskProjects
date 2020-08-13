# 说明
利用 Flask 创建的一些测试 Flask 项目

## 项目
1. [recommendation](./recommendation) 根据 flask 官网博客项目整理的相关内容。主要是作为理解 Flask 基本应用的目的

   * 运行 flask 服务之前需要调用注册的 `flask init-tb` 命令安装依赖的的数据库
   * 设置运行的应用 `export FLASK_APP=recommendation`，如果需要开发模式开启需要通过命令启动 `export FLASK_ENV=development`
   * 启动 flask 服务器 `flask run`

2. [RecommendationPresentation](./RecommendationPresentation) 

   依赖 Flask 和 Flask-SQLAlchemy 搭建推荐系统展示页面

   **Requirement**

   * Flask
   * Flask-SQLAlchemy
   
3. [sentimentAPI](./sentimentAPI)

   依赖 Flask 搭建 `sentiment` 的 API，相关的内容说明参考 [README.md](./sentimentAPI/README.md)

   