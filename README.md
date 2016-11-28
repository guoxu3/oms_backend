# 更新系统

## 需要实现的功能

1. 用户登陆
2. 权限管理
3. 提交任务
4. 查看任务
5. 执行任务
6. 统计分析

## 数据库
1. task 表，存储task信息
2. task_status表，存储task的状态
3. user表，存储用户信息
4. permission表，存储权限对照信息

## 接口设计
1. /api/task          task相关操作
2. /api/task_status   task_status相关操作
3. /api/update        执行更新操作
4. /admin/user        用户相关操作