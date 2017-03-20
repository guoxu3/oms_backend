##permission规则
```
以数字来定义handler，小数点后为handler子权限,依次类推
0为管理员，拥有所有权限
1 为拥有handler number 为1的所有操作权限
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

###task_statistic:
```
task_statistic_handler: 2
	│
	└──  get: 2.1
```

###permission:
```
permissionhandler: 3
	│ 
	├── get: 3.1
	│  
	├── post: 3.2
	│		└── add: 3.2.1
	│		└── update: 3.2.2
	│
	└── delete: 3.3
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
			├── update_file: 5.2.1
			└── update_db: 5.2.2		
```	

###machine:
```
machinehandler: 6
	│ 
	├── get: 6.1
	│  
	├── post: 6.2
	│		├── add: 6.2.1
	│		└── update: 6.2.2
	│
	└── delete: 6.3
```
