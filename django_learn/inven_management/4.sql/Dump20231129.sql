-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: invetory_management_new
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add drugs',7,'add_drugs'),(26,'Can change drugs',7,'change_drugs'),(27,'Can delete drugs',7,'delete_drugs'),(28,'Can view drugs',7,'view_drugs'),(29,'Can add in_document',8,'add_in_document'),(30,'Can change in_document',8,'change_in_document'),(31,'Can delete in_document',8,'delete_in_document'),(32,'Can view in_document',8,'view_in_document'),(33,'Can add in_out',9,'add_in_out'),(34,'Can change in_out',9,'change_in_out'),(35,'Can delete in_out',9,'delete_in_out'),(36,'Can view in_out',9,'view_in_out'),(37,'Can add manager',10,'add_manager'),(38,'Can change manager',10,'change_manager'),(39,'Can delete manager',10,'delete_manager'),(40,'Can view manager',10,'view_manager'),(41,'Can add memeber',11,'add_memeber'),(42,'Can change memeber',11,'change_memeber'),(43,'Can delete memeber',11,'delete_memeber'),(44,'Can view memeber',11,'view_memeber'),(45,'Can add provider',12,'add_provider'),(46,'Can change provider',12,'change_provider'),(47,'Can delete provider',12,'delete_provider'),(48,'Can view provider',12,'view_provider'),(49,'Can add user',13,'add_user'),(50,'Can change user',13,'change_user'),(51,'Can delete user',13,'delete_user'),(52,'Can view user',13,'view_user'),(53,'Can add worker',14,'add_worker'),(54,'Can change worker',14,'change_worker'),(55,'Can delete worker',14,'delete_worker'),(56,'Can view worker',14,'view_worker'),(57,'Can add member',15,'add_member'),(58,'Can change member',15,'change_member'),(59,'Can delete member',15,'delete_member'),(60,'Can view member',15,'view_member'),(61,'Can add sell_manage',16,'add_sell_manage'),(62,'Can change sell_manage',16,'change_sell_manage'),(63,'Can delete sell_manage',16,'delete_sell_manage'),(64,'Can view sell_manage',16,'view_sell_manage'),(65,'Can add sales_returning',17,'add_sales_returning'),(66,'Can change sales_returning',17,'change_sales_returning'),(67,'Can delete sales_returning',17,'delete_sales_returning'),(68,'Can view sales_returning',17,'view_sales_returning');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_drugs`
--

DROP TABLE IF EXISTS `demo_drugs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_drugs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `drug_name` varchar(50) NOT NULL,
  `product_id` varchar(100) NOT NULL,
  `product_place` varchar(50) NOT NULL,
  `type` varchar(50) NOT NULL,
  `in_price` double NOT NULL,
  `single_price` double NOT NULL,
  `discount` double NOT NULL,
  `package` int NOT NULL,
  `size` varchar(50) NOT NULL,
  `pro_date` date NOT NULL,
  `valid_date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_drugs`
--

LOCK TABLES `demo_drugs` WRITE;
/*!40000 ALTER TABLE `demo_drugs` DISABLE KEYS */;
INSERT INTO `demo_drugs` VALUES (12,'毒药123','1230032','缅甸','1',25777,123.5,1.2,100,'0','2023-12-01','2044-12-01'),(13,'阿莫西林','1230032','西安','1',25777,25.5,1.2,102,'2','2021-12-01','2044-12-01'),(15,'阿莫西林','1230032','西安','1',25777,25.5,1.2,102,'2','2021-12-01','2044-12-01'),(16,'莲花清瘟','12302','北京','1',25777,15.8,1.2,102,'2','2019-12-01','2044-12-01');
/*!40000 ALTER TABLE `demo_drugs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_in_document`
--

DROP TABLE IF EXISTS `demo_in_document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_in_document` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `in_id` varchar(50) NOT NULL,
  `io_number_id` bigint NOT NULL,
  `provider_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `demo_in_document_io_number_id_cc404310_fk_demo_in_out_id` (`io_number_id`),
  KEY `demo_in_document_provider_id_id_f5270135_fk_demo_provider_id` (`provider_id_id`),
  CONSTRAINT `demo_in_document_io_number_id_cc404310_fk_demo_in_out_id` FOREIGN KEY (`io_number_id`) REFERENCES `demo_in_out` (`id`),
  CONSTRAINT `demo_in_document_provider_id_id_f5270135_fk_demo_provider_id` FOREIGN KEY (`provider_id_id`) REFERENCES `demo_provider` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_in_document`
--

LOCK TABLES `demo_in_document` WRITE;
/*!40000 ALTER TABLE `demo_in_document` DISABLE KEYS */;
/*!40000 ALTER TABLE `demo_in_document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_in_out`
--

DROP TABLE IF EXISTS `demo_in_out`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_in_out` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `io_number` int NOT NULL,
  `drug_id` int NOT NULL,
  `number` int NOT NULL,
  `date` datetime(6) NOT NULL,
  `money` double NOT NULL,
  `type` varchar(50) NOT NULL,
  `user_increment` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10008 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_in_out`
--

LOCK TABLES `demo_in_out` WRITE;
/*!40000 ALTER TABLE `demo_in_out` DISABLE KEYS */;
INSERT INTO `demo_in_out` VALUES (10002,1807,1230032,1,'2023-11-28 23:58:19.611270',123.5,'1',5),(10003,1373,1230032,1,'2023-11-28 23:59:05.475972',123.5,'1',5),(10004,1218,1230032,1,'2023-11-29 00:00:38.382055',123.5,'1',5),(10005,1378,1230032,1,'2023-11-29 00:01:06.102648',123.5,'1',5),(10007,1897,1230032,1,'2023-11-29 00:15:43.247091',25.5,'1',5);
/*!40000 ALTER TABLE `demo_in_out` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_manager`
--

DROP TABLE IF EXISTS `demo_manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_manager` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `manager_increment` varchar(500) NOT NULL,
  `user_increment_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `demo_manager_user_increment_id_7ae2a7b0` (`user_increment_id`),
  CONSTRAINT `demo_manager_user_increment_id_7ae2a7b0_fk_demo_user_id` FOREIGN KEY (`user_increment_id`) REFERENCES `demo_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_manager`
--

LOCK TABLES `demo_manager` WRITE;
/*!40000 ALTER TABLE `demo_manager` DISABLE KEYS */;
/*!40000 ALTER TABLE `demo_manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_member`
--

DROP TABLE IF EXISTS `demo_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_member` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_client` varchar(16) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_member`
--

LOCK TABLES `demo_member` WRITE;
/*!40000 ALTER TABLE `demo_member` DISABLE KEYS */;
INSERT INTO `demo_member` VALUES (43,'225','万海东','wanhd@nwpu.edu.cn'),(47,'115','lixuhui','lixuhui123@mail.nwpu.edu.cn'),(48,'116','lixuhui','lixuhui123@mail.nwpu.edu.cn'),(49,'225','万海东123','wanhd@nwpu.edu.cn');
/*!40000 ALTER TABLE `demo_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_provider`
--

DROP TABLE IF EXISTS `demo_provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_provider` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pro_name` varchar(50) NOT NULL,
  `linkman` varchar(50) NOT NULL,
  `linkWay` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `provider_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_provider`
--

LOCK TABLES `demo_provider` WRITE;
/*!40000 ALTER TABLE `demo_provider` DISABLE KEYS */;
/*!40000 ALTER TABLE `demo_provider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_sales_returning`
--

DROP TABLE IF EXISTS `demo_sales_returning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_sales_returning` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_returning` int NOT NULL,
  `id_sell_id` bigint NOT NULL,
  `io_number_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `demo_sales_returning_id_sell_id_a4410450_fk_demo_sell_manage_id` (`id_sell_id`),
  KEY `demo_sales_returning_io_number_id_21cf7416_fk_demo_in_out_id` (`io_number_id`),
  CONSTRAINT `demo_sales_returning_id_sell_id_a4410450_fk_demo_sell_manage_id` FOREIGN KEY (`id_sell_id`) REFERENCES `demo_sell_manage` (`id`),
  CONSTRAINT `demo_sales_returning_io_number_id_21cf7416_fk_demo_in_out_id` FOREIGN KEY (`io_number_id`) REFERENCES `demo_in_out` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_sales_returning`
--

LOCK TABLES `demo_sales_returning` WRITE;
/*!40000 ALTER TABLE `demo_sales_returning` DISABLE KEYS */;
/*!40000 ALTER TABLE `demo_sales_returning` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_sell_manage`
--

DROP TABLE IF EXISTS `demo_sell_manage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_sell_manage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_sell` int NOT NULL,
  `id_client_id` bigint NOT NULL,
  `io_number_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `demo_sell_manage_id_client_id_c44e2843_fk_demo_member_id` (`id_client_id`),
  KEY `demo_sell_manage_io_number_id_e7b965dd_fk_demo_in_out_id` (`io_number_id`),
  CONSTRAINT `demo_sell_manage_id_client_id_c44e2843_fk_demo_member_id` FOREIGN KEY (`id_client_id`) REFERENCES `demo_member` (`id`),
  CONSTRAINT `demo_sell_manage_io_number_id_e7b965dd_fk_demo_in_out_id` FOREIGN KEY (`io_number_id`) REFERENCES `demo_in_out` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_sell_manage`
--

LOCK TABLES `demo_sell_manage` WRITE;
/*!40000 ALTER TABLE `demo_sell_manage` DISABLE KEYS */;
/*!40000 ALTER TABLE `demo_sell_manage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_user`
--

DROP TABLE IF EXISTS `demo_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_increment` varchar(500) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `pwd` varchar(50) NOT NULL,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_user`
--

LOCK TABLES `demo_user` WRITE;
/*!40000 ALTER TABLE `demo_user` DISABLE KEYS */;
INSERT INTO `demo_user` VALUES (1,'1','lixuhui','qwe20031221','admin'),(2,'2','root','root666','admin');
/*!40000 ALTER TABLE `demo_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_worker`
--

DROP TABLE IF EXISTS `demo_worker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_worker` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `worker_id` int NOT NULL,
  `worker_name` varchar(50) NOT NULL,
  `telephone` varchar(500) NOT NULL,
  `user_increment_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `demo_worker_user_increment_id_3d362ff6` (`user_increment_id`),
  CONSTRAINT `demo_worker_user_increment_id_3d362ff6_fk_demo_user_id` FOREIGN KEY (`user_increment_id`) REFERENCES `demo_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_worker`
--

LOCK TABLES `demo_worker` WRITE;
/*!40000 ALTER TABLE `demo_worker` DISABLE KEYS */;
/*!40000 ALTER TABLE `demo_worker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'demo','drugs'),(8,'demo','in_document'),(9,'demo','in_out'),(10,'demo','manager'),(15,'demo','member'),(11,'demo','memeber'),(12,'demo','provider'),(17,'demo','sales_returning'),(16,'demo','sell_manage'),(13,'demo','user'),(14,'demo','worker'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-11-25 02:33:46.716453'),(2,'auth','0001_initial','2023-11-25 02:33:47.000453'),(3,'admin','0001_initial','2023-11-25 02:33:47.075454'),(4,'admin','0002_logentry_remove_auto_add','2023-11-25 02:33:47.083454'),(5,'admin','0003_logentry_add_action_flag_choices','2023-11-25 02:33:47.089455'),(6,'contenttypes','0002_remove_content_type_name','2023-11-25 02:33:47.134453'),(7,'auth','0002_alter_permission_name_max_length','2023-11-25 02:33:47.168452'),(8,'auth','0003_alter_user_email_max_length','2023-11-25 02:33:47.185454'),(9,'auth','0004_alter_user_username_opts','2023-11-25 02:33:47.191455'),(10,'auth','0005_alter_user_last_login_null','2023-11-25 02:33:47.222453'),(11,'auth','0006_require_contenttypes_0002','2023-11-25 02:33:47.224454'),(12,'auth','0007_alter_validators_add_error_messages','2023-11-25 02:33:47.231455'),(13,'auth','0008_alter_user_username_max_length','2023-11-25 02:33:47.267453'),(14,'auth','0009_alter_user_last_name_max_length','2023-11-25 02:33:47.304453'),(15,'auth','0010_alter_group_name_max_length','2023-11-25 02:33:47.320453'),(16,'auth','0011_update_proxy_permissions','2023-11-25 02:33:47.328463'),(17,'auth','0012_alter_user_first_name_max_length','2023-11-25 02:33:47.370478'),(18,'demo','0001_initial','2023-11-25 02:33:47.461454'),(19,'sessions','0001_initial','2023-11-25 02:33:47.482453'),(20,'demo','0002_member_delete_memeber','2023-11-25 02:52:05.168940'),(21,'demo','0003_alter_drugs_package_alter_drugs_sup_id_and_more','2023-11-25 16:55:20.457778'),(22,'demo','0004_rename_productor_id_drugs_product_id_and_more','2023-11-27 07:15:45.603191'),(23,'demo','0005_remove_drugs_sup_id_alter_in_out_date_and_more','2023-11-27 08:19:43.633857'),(24,'demo','0006_alter_in_out_user_increment','2023-11-28 15:38:50.079751'),(25,'demo','0007_alter_in_out_user_increment','2023-11-28 15:42:41.486059'),(26,'demo','0008_alter_drugs_pro_date_alter_drugs_valid_date_and_more','2023-11-28 15:55:44.474494');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('522citr77fyekz4uaq9c0v7if75up1yd','eyJpbmZvIjoibGl4dWh1aSJ9:1r7vGt:LeomfRUPScIVzaK8avVtY8SP48Wf3-zHF1I1t9kmc0c','2023-12-12 10:24:51.083864'),('ya0cnm8glfgfarnmonnqpi97y4bsfuai','eyJpbmZvIjoicm9vdCJ9:1r7GNo:U5-HYym5vz-q5TsRQQ__n8ojXnlYAf9qI8N1yZ7Qvq8','2023-12-10 14:45:16.950067');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-29  0:24:49
