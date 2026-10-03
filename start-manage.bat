@echo off
chcp 65001 >nul
title 知识库管理服务
cd /d "%~dp0"
echo 正在启动知识库管理服务...
echo 浏览器将自动打开 http://localhost:8877
echo 关闭本窗口即停止服务
start "" http://localhost:8877
node server.js
pause
