-- MySQL dump 10.13  Distrib 5.7.28, for macos10.14 (x86_64)
--
-- Host: localhost    Database: ICP_db
-- ------------------------------------------------------
-- Server version	5.7.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ICP_tbl`
--

DROP TABLE IF EXISTS `ICP_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ICP_tbl` (
  `i_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `p_id` int(10) unsigned NOT NULL,
  `i_date` datetime NOT NULL,
  `i_data` varchar(512) NOT NULL,
  PRIMARY KEY (`i_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ICP_tbl`
--

LOCK TABLES `ICP_tbl` WRITE;
/*!40000 ALTER TABLE `ICP_tbl` DISABLE KEYS */;
/*!40000 ALTER TABLE `ICP_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultation_tbl`
--

DROP TABLE IF EXISTS `consultation_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consultation_tbl` (
  `c_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `p_id` int(10) unsigned NOT NULL,
  `c_date` datetime NOT NULL,
  `symptom` varchar(512) NOT NULL,
  `diagnosis` varchar(512) NOT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultation_tbl`
--

LOCK TABLES `consultation_tbl` WRITE;
/*!40000 ALTER TABLE `consultation_tbl` DISABLE KEYS */;
INSERT INTO `consultation_tbl` VALUES (1,1010,'2020-11-23 15:00:00','无','无'),(2,1010,'2021-04-08 00:00:00','头晕症状减轻','药剂用量减半');
/*!40000 ALTER TABLE `consultation_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor_tbl`
--

DROP TABLE IF EXISTS `doctor_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `doctor_tbl` (
  `d_id` varchar(20) NOT NULL,
  `d_name` varchar(20) NOT NULL,
  `d_tel` varchar(20) NOT NULL,
  `d_pwd` varchar(255) NOT NULL,
  PRIMARY KEY (`d_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_tbl`
--

LOCK TABLES `doctor_tbl` WRITE;
/*!40000 ALTER TABLE `doctor_tbl` DISABLE KEYS */;
INSERT INTO `doctor_tbl` VALUES ('1','test2','1','c4ca4238a0b923820dcc509a6f75849b'),('100000','test','88888888','e10adc3949ba59abbe56e057f20f883e'),('123456','admin','13800000000','e10adc3949ba59abbe56e057f20f883e');
/*!40000 ALTER TABLE `doctor_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_tbl`
--

DROP TABLE IF EXISTS `patient_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient_tbl` (
  `p_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `p_name` varchar(20) NOT NULL,
  `p_age` int(11) NOT NULL,
  `p_gender` varchar(5) NOT NULL,
  `p_pwd` varchar(255) NOT NULL,
  `allergy` varchar(255) DEFAULT NULL,
  `family_history` varchar(255) DEFAULT NULL,
  `height` float DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `blood_type` varchar(5) DEFAULT NULL,
  `p_tel` varchar(20) DEFAULT NULL,
  `past_medical_history` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`p_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1014 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_tbl`
--

LOCK TABLES `patient_tbl` WRITE;
/*!40000 ALTER TABLE `patient_tbl` DISABLE KEYS */;
INSERT INTO `patient_tbl` VALUES (1010,'张三',45,'男','e10adc3949ba59abbe56e057f20f883e','无','无',169,73,'AB','13800000001','高血压'),(1011,'李四',39,'男','e10adc3949ba59abbe56e057f20f883e','青霉素过敏','无',167,67,'B','13800000004','无'),(1012,'李四',38,'男','e10adc3949ba59abbe56e057f20f883e','青霉素过敏','无',167,67,'B','15900000000','无'),(1013,'王五',62,'女','e10adc3949ba59abbe56e057f20f883e','无','无',159,49,'AB','159','无');
/*!40000 ALTER TABLE `patient_tbl` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-21 16:11:14
