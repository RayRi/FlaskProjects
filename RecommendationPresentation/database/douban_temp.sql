

-- ----------------------------
-- Table structure for temp
-- 临时存储表，存储信息包括三个主要信息，影视 id、标题、海报 URL，用于构建推荐系统可视化使用
-- ----------------------------
DROP TABLE IF EXISTS `temp`;
CREATE TABLE `temp` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `series_id` varchar(20) NOT NULL COMMENT '豆瓣影视剧条目 ID',
  `title` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '豆瓣影视标题',
  `cover` varchar(200) DEFAULT NULL COMMENT '豆瓣影视海报链接',
  PRIMARY KEY (`id`),
  UNIQUE KEY `sid` (`series_id`) COMMENT '豆瓣影视实际 ID 作为唯一约束'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='临时存储表构建推荐系统可视化使用';


-- ----------------------------
-- Table structure for similarity
-- 临时存储表，存储信息包括三个主要信息，影视 id1、影视 id2、以及两者相似度值，用于构建推荐系统可视化使用
-- ----------------------------
DROP TABLE IF EXISTS `similarity`;
CREATE TABLE `similarity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sid1` varchar(20) NOT NULL COMMENT '豆瓣影视剧条目 ID',
  `sid2` varchar(20) NOT NULL COMMENT '豆瓣影视剧条目 ID',
  `sim` FLOAT DEFAULT NULL COMMENT 'sid1 和 sid2 的相似度',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='临时存储表用于构建推荐系统可视化使用';