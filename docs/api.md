# 接口描述

--------
##接口返回定义
```
200, 正常情况，通过返回的json中ok字段判断接口错误
403, 权限错误，认证失败或者没有相应操作权限
500, 内部错误，联系相应开发人员和管理人员处理

返回均以json字符串返回，其中以下字段是公共字段，所有接口共享:
1. code    ->  200 | 400 | 500等 
2. info    ->  返回信息，正确时为数据，错误时为错误信息
```


##任务接口( /api/task )
#### 获取task信息
```
GET /api/task

argument:
    start = 0
    count = 10
    task_id = 0358c3c78f5211e685855cf9389306a2

argument explain:
    start (int, 非必须) 开始查询的id
    count (int, 非必须) 返回的条数
    task_id (string, 非必须) 查询单条task_id 对应的消息

TIPS:
    默认按照id排序

return:
{
    'code': 200,
    'info': [
        {
            'id': 1, 
            'task_id': '0358c3c78f5211e685855cf9389306a2'
            'ip': '192.168.1.1',
            'action': 'update',
            'create_time': 1480471675,
            'content': '/path/to/file',
            'description': '更新xxx功能'
        }
    ]
}
```

### 新增task
```
POST /api/task

argument:
{  'action': 'add'
	'data': {
    			'ip' : '192.168.1.1'
       		'action': 'update',
       		'content': '/path/to/file',
       		'description': '更新xxx功能'			 }
}
argument explain:
    ip (string, 必须) 执行命令的机器IP
    action (string, 必须) 执行的指令
    content (string, 必须) 变更的内容，文件名
    description (string, 必须) 变更的描述
    
TIPS:
    新增task是会同步新增task_status

return:
{
    'code': 200,
    'info': { 'task_id': '0358c3c78f5211e685855cf9389306a2' } 
}
```

### 删除task
```
DELETE /api/task

argument:
    task_id = 0358c3c78f5211e685855cf9389306a2

argument explain:
       task_id (string, 必须) 需要删除的task id

TIPS:
    删除task会同步删除task_status

return:
{
    'code': 200,
    'info': 'delete task ok'
}
```


##任务信息接口( /api/task_status )
#### 获取task信息
```
GET /api/task_status

argument:
    start = 0
    count = 10
    task_id = 0358c3c78f5211e685855cf9389306a2

argument explain:
    start (int, 非必须) 开始查询的id
    count (int, 非必须) 返回的条数
    task_id (string, 非必须) 查询单条task_id 对应的消息

TIPS:
    默认按照id排序

return:
{
    'code': 200,
    'info': [
        {
            'id': 1, 
            'task_id': '0358c3c78f5211e685855cf9389306a2'
            'start_time': 1480471675,
            'revert_time': 1480471675,
            'status': 0,
            'percent': 0,
            'revert': 0
        }
    ]
}
```

### 更新task_status
```
POST /api/task_status

argument:
{  'action': 'update'
	'data': {
    			'task_id' : '0358c3c78f5211e685855cf9389306a2'
    			'start_time' : 1480471675,
    			'revert_time' : 1480471675,
       		'percent': 10,
       		'status': 1,
       		'revert': 1			 
       	  }
}
argument explain:
    task_id (string, 必须) 需要修改的task id
    start_time (int, 非必须) 执行的任务开始时间
    revert_time (int, 非必须) 回退文件的时间
    percent (int, 必须) 更新进度比例 
    status (int, 必须) 是否开始更新 
    revert (int, 必须) 是否回退
    
TIPS:
    

return:
{
    'code': 200,
    'info': 'update task status ok'
}
```

##服务器信息接口( /api/machine_info )
### 获取machine_info信息
```
GET /api/machine_info

argument:
    start = 0
    count = 10
    machine_name

argument explain:
    start (int, 非必须) 开始查询的id
    count (int, 非必须) 返回的条数
    machine_name (string, 非必须) 机器名称
TIPS:
     

return:
 
```

### 新增machine_info
```
POST /api/machine_info

argument:
{  'action': 'add'
	'data': {
    			'machine_name' : 'web01'
    			'inside_ip' : '10.2.2.2',
    			'outside_ip' : '111.111.11.1',
       		'userage': 'web 服务器1',
       		'is_initialized': 0,
       		'location': '阿里云'		 
       	  }
}
argument explain:
    machine_name (string, 必须) 服务器名字，标识
    inside_ip (string, 必须) 服务器内网ip
    outside_ip (string, 必须) 服务器外网ip
    usage (string, 必须) 机器用途 
    is_initialized (int, 必须) 是否初始化了 
    location (string, 必须) 机器所在机房
    
TIPS:
    

return:
{
    'code': 200,
    'info': 'add machine info ok'
}
```

### 更新machine_info
```
POST /api/machine_info

argument:
{  'action': 'update'
	'data': {
    			'machine_name' : 'web01'
    			'inside_ip' : '10.2.2.2',
    			'outside_ip' : '111.111.11.1',
       		'userage': 'web 服务器1',
       		'is_initialized': 0,
       		'location': '阿里云'		 
       	  }
}
argument explain:
    machine_name (string, 必须) 服务器名字，标识
    inside_ip (string, 必须) 服务器内网ip
    outside_ip (string, 必须) 服务器外网ip
    usage (string, 必须) 机器用途 
    is_initialized (int, 必须) 是否初始化了 
    location (string, 必须) 机器所在机房
    
TIPS:
    

return:
{
    'code': 200,
    'info': 'update machine info ok'
}
```

### 删除machine_info
```
DELETE /api/machine_info

argument:
    machine_name = 'web01'

argument explain:
       machine_name (string, 必须) 需要删除的机器名

return:
{
    'code': 200,
    'info': 'delete machin info ok'
}
```

## 执行更新接口( /api/update )
```
	待开发
```

## 用户信息接口( /admin/user )
### 获取user信息
```
GET /admin/user

argument:
   start = 0
   count = 10
   username = xxxx
   
argument explain:
   start (int, 非必须) 开始查询的id
   count (int, 非必须) 返回的条数
   username (string, 非必须) 用户名

TIPS:
     

return:
{
	'code': 200,
	'info': {
				'id': 11,
				'mail': 'user@example.com'
				'name': 'xxx',
				'department': 'dev',
				'permissions': '1,2,3'
			  }
}
 
```

### 新增user
```
POST /admin/user

argument:
{  'action': 'add'
	'data': {
    			'mail' : 'user@example.com'
    			'name' : 'xxx',
    			'passwd' : '123456',
       		'department': 'dev',
       		'permissions': '1,2,3'		 
       	  }
}
argument explain:
    mail (string, 必须) 用户邮箱
    name (string, 必须) 用户名
    passwd (string, 必须) 密码
    department (string, 必须) 所属部门 
    permissions (string, 必须) 权限组
    
TIPS:
    

return:
{
    'code': 200,
    'info': 'add user ok'
}
```

### 更新user
```
POST /admin/user

argument:
{  'action': 'update'
	'data': {
    			'mail' : 'user@example.com'
    			'old_passwd' : '123456'
    			'new_passwd' : '654321',
       		'department': 'dev',
       		'permissions': '1,2,3'		 
       	  }
}
argument explain:
    mail (string, 非必须) 用户邮箱
    old_passwd (string, 非必须) 旧密码
    new_passwd (string, 非必须) 新密码
    department (string, 非必须) 所属部门 
    permissions (string, 非必须) 权限组
    
TIPS:
    

return:
{
    'code': 200,
    'info': 'update user ok'
}
```

### 删除user
```
DELETE /admin/user

argument:
    name = 'xxxx'

argument explain:
       name (string, 必须) 需要删除的用户名

return:
{
    'code': 200,
    'info': 'delete user ok'
}
```

## 登陆接口( /admin/user_login )
### 登陆认证
```
POST /admin/user_login
argument:
 	{
 		'name': 'xxxx',
 		'password': 'xxxx'
 	}

argument explain:
       username (string, 必须) 用户名
       password (string, 必须) 密码

return:
{
    'code': 200,
    'info': {'access_token': 'xxxxxxx'}
}
```