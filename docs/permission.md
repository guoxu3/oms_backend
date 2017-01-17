##permission规则
```
以数字来定义handler，小数点后为handler子权限,依次类推
0为管理员，1 为拥有handler1的所有权限
```
---
###task:
```
taskhandler: 1
	│ 
	├── get: 1.1
	│  
	├── post: 1.2
	│		├── add: 1.2.1
	│		└── update: 1.2.2
	│
	└── delete: 1.3
```
###task_status:
```
taskhandler: 2
	│ 
	├── get: 2.1
	│  
	└── post: 2.2（预留）
			└── update: NULL,开放对外调用，不做验证
```
###permission:
```
permissionhandler: 3
	│ 
	├── get: 3.1
	│  
	└── post: 3.2
			└── add: 3.2.1
```
###user:
```
userhandler: 4
	│ 
	├── get: 4.1
	│  
	├── post: 4.2
	│		├── add: 4.2.1
	│		└── update: 4.2.2
	│
	└── delete: 4.3
			
```	
###update:
```
updatehandler: 5
	│ 
	├── get: 5.1 (预留)
	│  
	└── post: 5.2
			├── pay: 5.2.1
			├── static: 5.2.2
			├── exp: 5.2.3
			├── exp_v4: 5.2.4
			├── sample_api: 5.2.5
			├── sample_api_v4: 5.2.6
			├── card: 5.2.7
			├── channel: 5.2.8
			├── ground: 5.2.9
			├── api: 5.2.10
			└── stock: 5.2.11		
```	
###machine:
```
machinehandler: 5
	│ 
	├── get: 6.1
	│  
	├── post: 6.2
	│		├── add: 6.2.1
	│		└── update: 6.2.2
	│
	└── delete: 6.3
			
```	
