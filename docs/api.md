# 接口描述

--------
##接口返回定义
```
200, 正常情况，通过返回的json中ok字段判断接口错误
403, 权限错误，认证失败或者没有相应操作权限
500, 内部错误，联系相应开发人员和管理人员处理

返回均以json字符串返回，其中以下字段是公共字段，所有接口共享:
1. ok      ->  True | False
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
    有 task_id 时不读取start和count值

return:
{
    'ok': True,
    'info': {
        'data': [
            {
                'id': 1, 
                'task_id': '0358c3c78f5211e685855cf9389306a2',
                'creator': 'xxxx'
                'ip': '192.168.1.1',
                'action': 'update',
                'create_time': 1480471675,
                'content': '/path/to/file',
                'description': '更新xxx功能',
                'executor': 'xxxx'
                'start_time': 1480471675,
                'revert_time': 1480471675,
                'status': 0,
                'percent': 0,
                'revert': 0
            },
             {
                'id': 2, 
                'task_id': '0358c3c78f5211e685855cf9389306a2',
                'creator': 'xxxx'
                'ip': '192.168.1.1',
                'action': 'update',
                'create_time': 1480471675,
                'content': '/path/to/file',
                'description': '更新xxx功能',
                'executor': 'xxxx'
                'start_time': 1480471675,
                'revert_time': 1480471675,
                'status': 0,
                'percent': 0,
                'revert': 0
            }
        ],
        'count': 100
}
```

### 新增task
```
POST /api/task

argument:
{  
    'action': 'add'
	'data': {
    			'ip' : '192.168.1.1'
    			'creator': 'xxx',
       		    'action': 'update_db',
       		    'target': 'db_name'
       		    'version': '1234'
       		    'content': '/path/to/file',
       		    'description': '更新xxx功能'      		   
       		}
}

argument explain:
    ip (string, 必须) 执行命令的机器IP
    action (string, 必须) 执行的指令
    creator （string, 必须）创建任务人
    target（string，必须）更新目标（目录名、数据库名等）
    version（string，非必需）svn或其他版本管理工具的版本号
    content (string, 必须) 变更的内容，文件名
    description (string, 必须) 变更的描述
    
TIPS:

return:
{
    'ok': True,
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
    'ok': True,
    'info': 'delete task ok'
}
```

##服务器信息接口( /api/machine )
### 获取machine信息
```
GET /api/machine

argument:
    start = 0
    count = 10
    machine_name

argument explain:
    start (int, 非必须) 开始查询的id
    count (int, 非必须) 返回的条数
    machine_name (string, 非必须) 机器名称
    
TIPS:
    有 machine_name 时不读取start和count值

return:
{  
    'ok': True
	'info':
	    'data':[
            {
                'id'：1，
                'machine_name' : 'web01'
                'inside_ip' : '10.2.2.1',
                'outside_ip' : '111.111.11.1',
                'userage': 'web 服务器1',
                'is_initialized': 0,
                'location': '阿里云'		 
            },
            {
                'id'：2，
                'machine_name' : 'web02'
                'inside_ip' : '10.2.2.2',
                'outside_ip' : '111.111.11.2',
                'userage': 'web 服务器2',
                'is_initialized': 0,
                'location': '阿里云'		 
            }
        ]
        'count':100
}
```

### 新增machine
```
POST /api/machine

argument:
{  
    'action': 'add'
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
    'ok': True,
    'info': 'add machine info ok'
}
```

### 更新machine
```
POST /api/machine

argument:
{  
    'action': 'update'
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
    'ok': True,
    'info': 'update machine info ok'
}
```

### 删除machine
```
DELETE /api/machine

argument:
    machine_name = 'web01'

argument explain:
    machine_name (string, 必须) 需要删除的机器名

return:
{
    'ok': True,
    'info': 'delete machin info ok'
}
```

## 执行更新接口( /api/update )
### 执行更新
```
POST /api/machine

argument:
{  
    'action': 'update'
	'data': {
    			'executor' : 'username'
    			'task_id' : '0358c3c78f5211e685855cf9389306a2'
       	    }
}

argument explain:
    action (操作，必须) 更新或者回退
    executor (string, 必须) 执行更新的人
    task_id (string, 必须) 执行的任务id
    
TIPS:
    

return:
{
    'ok': True,
    'info': 'executor task ok'
}
```


## 用户信息接口( /api/user )
### 获取user信息
```
GET /api/user

argument:
    start = 0
    count = 10
    username = xxxx
   
argument explain:
    start (int, 非必须) 开始查询的id
    count (int, 非必须) 返回的条数
    username (string, 非必须) 用户名

TIPS:
    有 username 时不读取start和count值

return:
{
	'ok': True,
	'info': {
				'id': 11,
				'mail': 'user@example.com'
				'username': 'xxx',
				'nickname': '二狗子',
				'department': 'dev',
				'permissions': '1,2,3'
			  }
}
 
```

### 新增user
```
POST /api/user

argument:
{  
    'action': 'add'
	'data': [
	    {
            'mail' : 'user@example.com'
            'username' : 'xxx',
            'passwd' : '123456',
            'department': 'dev',
            'permissions': '1,2,3'		 
       	},
       	{
            'mail' : 'user@example.com'
            'username' : 'xxx',
            'passwd' : '123456',
            'department': 'dev',
            'permissions': '1,2,3'		 
       	}
    ]
}

argument explain:
    mail (string, 必须) 用户邮箱
    username (string, 必须) 用户名
    passwd (string, 必须) 密码
    department (string, 必须) 所属部门 
    permissions (string, 必须) 权限组
    
TIPS:
    

return:
{
    'ok': True,
    'info': 'add user ok'
}
```

### 更新user
```
POST /api/user

argument:
{  
    'action': 'update'
	'data': {
	            'username': 'xxxx';
    			'mail' : 'user@example.com'
    			'old_passwd' : '123456'
    			'new_passwd' : '654321',
       		    'department': 'dev',
       		    'permissions': '1,2,3'		 
       	  }
}

argument explain:
    username (string, 必须) 要修改信息的用户的用户名
    mail (string, 非必须) 用户邮箱
    old_passwd (string, 非必须) 旧密码
    new_passwd (string, 非必须) 新密码
    department (string, 非必须) 所属部门 
    permissions (string, 非必须) 权限组
    
TIPS:
    根据username匹配用户进行信息修改

return:
{
    'ok': True,
    'info': 'update user ok'
}
```

### 删除user
```
DELETE /api/user

argument:
    username = xxxx

argument explain:
    username (string, 必须) 需要删除的用户名

return:
{
    'ok': True,
    'info': 'delete user ok'
}
```

## 登陆接口( /api/login )
### 登陆认证
```
GET /api/login

argument:
    username

argument explain:
    username (string, 必须) 用户名
    
TIPS:
    返回用户是否登陆或者是否登陆超时
return:
{  
    'ok': True
	'info': login timeout
}
```

### 登陆认证
```
POST /api/login

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
    'ok': True,
    'info': {'access_token': 'xxxxxxx'}
}
```

## 权限接口( /api/permission )
### 获取权限列表
```
Get /api/permission

argument:
    count = 10
    username = xxxx
   
argument explain:
    start (int, 非必须) 开始查询的id
    count (int, 非必须) 返回的条数

TIPS:

return:
{
	'ok': True,
	'info': 
	    'data': [
	        {
				'permission': 'adduser',
				'permission_desc': '新增用户'
				'permission_code': 2,
			}
		]
		'count': 100
}
 
```

## ssh-key 管理接口( /api/ssh_key_manage )
### 获取ssh-key信息
```
Get /api/ssh_key_manage

argument:
    mode = ip/user
    username = xxxx
    ip = 192.168.1.1
   
argument explain:
    mode (string, 必须) 查询的方式，以用户名查询或以IP查询
    username (strig, 必须) 需要查询的用户名
    ip (strig, 必须) 需要查询的ip

TIPS:

return:
{
	'ok': True,
	'info': 
	    'data': [
	        {
				'username': 'xxxx',
				'ip': '192.168.1.1'
				'system_user': 'root',
			}
		]
}
 
