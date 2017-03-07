-- task 表，存储task信息
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `task_id` VARCHAR(40) NOT NULL UNIQUE,
  `creator` VARCHAR(40) NOT NULL,
  `ip` VARCHAR(30) NOT NULL,
  `target` VARCHAR(30) NOT NULL,
  `version` INT(30),
  `type` VARCHAR(30) NOT NULL,
  `create_time` INT(10) NOT NULL,
  `content` VARCHAR(1000) NOT NULL,
  `description` VARCHAR(1000) NOT NULL,
  `executor` VARCHAR(40),
  `start_time` INT(10) DEFAULT '0',
  `revert_time` INT(10) DEFAULT '0',
  `status` BOOLEAN DEFAULT FALSE ,
  `percent` INT(2) DEFAULT '0',
  `revert` BOOLEAN DEFAULT FALSE ,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- machine  存储机器的信息
DROP TABLE IF EXISTS `machine`;
CREATE TABLE `machine` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `machine_name` VARCHAR(40) NOT NULL UNIQUE,
  `inside_ip` VARCHAR(40) NOT NULL,
  `outside_ip` VARCHAR(40) NOT NULL,
  `usage` VARCHAR(40) NOT NULL,
  `is_initialized` BOOLEAN DEFAULT FALSE,
  `location` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- user 表 存储用户信息
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `mail` VARCHAR(40) NOT NULL UNIQUE,
  `username` VARCHAR(40) NOT NULL UNIQUE,
  `nickname` VARCHAR(40) NOT NULL UNIQUE,
  `passwd` VARCHAR(40) NOT NULL,
  `salt` VARCHAR(10) NOT NULL,
  `department` VARCHAR(40) NOT NULL,
  `permissions` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- permissions表  权限对应关系
DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `permission` VARCHAR(40) NOT NULL,
  `permission_desc` VARCHAR(40) NOT NULL,
  `permission_code` VARCHAR (10),
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- session表  权限对应关系
DROP TABLE IF EXISTS `session`;
CREATE TABLE `session` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(40) NOT NULL UNIQUE,
  `access_token` VARCHAR(100) NOT NULL UNIQUE,
  `action_time` INT(10) NOT NULL,
  `expire_time` INT(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;