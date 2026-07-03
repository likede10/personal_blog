CREATE DATABASE IF NOT EXISTS personal_blog
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE personal_blog;

CREATE TABLE users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,

  username VARCHAR(50) NOT NULL COMMENT '用户名，用于登录或展示',
  email VARCHAR(255) NOT NULL COMMENT '邮箱，用于登录/找回密码',
  password_hash VARCHAR(255) NOT NULL COMMENT '加密后的密码，不能存明文密码',

  nickname VARCHAR(80) DEFAULT NULL COMMENT '展示昵称',
  avatar_url VARCHAR(500) DEFAULT NULL COMMENT '头像地址',
  bio TEXT DEFAULT NULL COMMENT '个人简介',

  role VARCHAR(20) NOT NULL DEFAULT 'user' COMMENT '角色：admin/author/user',
  status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态：active/disabled/pending',

  email_verified_at DATETIME DEFAULT NULL COMMENT '邮箱验证时间',
  last_login_at DATETIME DEFAULT NULL COMMENT '最后登录时间',

  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  deleted_at DATETIME DEFAULT NULL COMMENT '软删除时间',

  UNIQUE KEY uk_users_username (username),
  UNIQUE KEY uk_users_email (email),
  KEY idx_users_role (role),
  KEY idx_users_status (status),
  KEY idx_users_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';