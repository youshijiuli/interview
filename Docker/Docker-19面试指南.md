## 16 Docker 面试题

### Q76: Docker 核心概念？

| 概念 | 说明 | 类比 |
|------|------|------|
| **镜像（Image）** | 只读模板，包含运行环境和代码 | 类（Class） |
| **容器（Container）** | 镜像的运行实例 | 对象（Object） |
| **仓库（Registry）** | 存储镜像的地方（DockerHub） | GitHub |
| **Dockerfile** | 构建镜像的脚本 | Makefile |
| **docker-compose** | 管理多容器应用 | 容器编排脚本 |

---

### Q77: Dockerfile 常用指令？

```dockerfile
FROM python:3.11-slim          # 基础镜像
WORKDIR /app                    # 设置工作目录
COPY requirements.txt .         # 复制文件到容器
RUN pip install -r requirements.txt  # 构建时执行
COPY . .                        # 复制所有代码
ENV PYTHONUNBUFFERED=1         # 设置环境变量
EXPOSE 8000                     # 暴露端口（声明性）
CMD ["uwsgi", "--ini", "uwsgi.ini"]  # 启动命令
```

**COPY vs ADD：** COPY 只复制本地文件；ADD 还支持远程 URL 和解压 tar 包，推荐优先用 COPY。

**CMD vs ENTRYPOINT：** CMD 可被 `docker run` 后面的命令覆盖；ENTRYPOINT 作为固定入口，传的参数作为 ENTRYPOINT 的参数。

---

### Q78: docker-compose 常用指令？

```yaml
version: '3.8'
services:
  web:
    build: .                    # 用 Dockerfile 构建
    image: myapp:latest         # 或直接用镜像
    ports:
      - "8000:8000"             # 宿主机:容器
    volumes:
      - ./code:/app             # 挂载卷
      - static_volume:/app/static
    environment:
      - DEBUG=False             # 环境变量
    depends_on:
      - mysql                    # 启动依赖
      - redis
    networks:
      - app_network
    restart: always              # 自动重启

  mysql:
    image: mysql:8.0
    volumes:
      - mysql_data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_PASSWORD}  # 从 .env 读取

volumes:
  static_volume:
  mysql_data:

networks:
  app_network:
```

```bash
docker-compose up -d           # 后台启动
docker-compose down             # 停止并删除容器
docker-compose build            # 重新构建
docker-compose logs -f web      # 查看日志
docker-compose exec web bash    # 进入容器
```

---
