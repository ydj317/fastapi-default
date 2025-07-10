/*
Navicat MariaDB Data Transfer

Source Server         : local dev
Source Server Version : 100338
Source Host           : 192.168.51.104:3307
Source Database       : fastapi-default

Target Server Type    : MariaDB
Target Server Version : 100338
File Encoding         : 65001

Date: 2025-07-10 14:13:43
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for t_logs
-- ----------------------------
DROP TABLE IF EXISTS `t_logs`;
CREATE TABLE `t_logs` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `status` varchar(10) DEFAULT NULL,
  `message` varchar(255) DEFAULT NULL,
  `data` longtext DEFAULT NULL,
  `trace_id` varchar(100) DEFAULT '',
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT '',
  `password` varchar(200) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

