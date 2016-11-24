-- MySQL dump 10.13  Distrib 5.6.27, for osx10.10 (x86_64)
--
-- Host: amp.pharm.mssm.edu    Database: euclid
-- ------------------------------------------------------
-- Server version	5.5.5-10.0.19-MariaDB-1~wheezy-log

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bio_category`
--

DROP TABLE IF EXISTS `bio_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bio_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `curator`
--

DROP TABLE IF EXISTS `curator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `curator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dataset`
--

DROP TABLE IF EXISTS `dataset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dataset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text,
  `record_type` varchar(32) NOT NULL,
  `organism` varchar(255) DEFAULT NULL,
  `accession` varchar(255) DEFAULT NULL,
  `platform` varchar(32) DEFAULT NULL,
  `summary` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5348 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `enrichment_term`
--

DROP TABLE IF EXISTS `enrichment_term`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enrichment_term` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `combined_score` double DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `enrichr_result_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_enrichr_result` (`enrichr_result_fk`),
  CONSTRAINT `fk_enrichr_result` FOREIGN KEY (`enrichr_result_fk`) REFERENCES `enrichr_result` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9154234 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `enrichr_result`
--

DROP TABLE IF EXISTS `enrichr_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enrichr_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_list_id` int(11) NOT NULL,
  `is_up` tinyint(1) NOT NULL,
  `gene_signature_fk` int(11) DEFAULT NULL,
  `library` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gene_signature_fk` (`gene_signature_fk`),
  CONSTRAINT `enrichr_result_ibfk_1` FOREIGN KEY (`gene_signature_fk`) REFERENCES `gene_signature` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35679 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gene`
--

DROP TABLE IF EXISTS `gene`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gene` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=211721 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gene_list`
--

DROP TABLE IF EXISTS `gene_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gene_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `direction` int(11) DEFAULT NULL,
  `gene_signature_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `extraction_id` (`gene_signature_fk`),
  CONSTRAINT `gene_list_ibfk_1` FOREIGN KEY (`gene_signature_fk`) REFERENCES `gene_signature` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `gene_list_ibfk_2` FOREIGN KEY (`gene_signature_fk`) REFERENCES `gene_signature` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=72571 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gene_signature`
--

DROP TABLE IF EXISTS `gene_signature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gene_signature` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `extraction_id` varchar(10) DEFAULT NULL,
  `resource_fk` int(11) NOT NULL DEFAULT '1',
  `_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `resource_fk` (`resource_fk`),
  CONSTRAINT `gene_signature_ibfk_1` FOREIGN KEY (`resource_fk`) REFERENCES `resource` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23859 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gene_signature_to_report`
--

DROP TABLE IF EXISTS `gene_signature_to_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gene_signature_to_report` (
  `gene_signature_fk` int(11) NOT NULL,
  `report_fk` int(11) NOT NULL,
  KEY `gene_signature_fk` (`gene_signature_fk`,`report_fk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gene_signature_to_tag`
--

DROP TABLE IF EXISTS `gene_signature_to_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gene_signature_to_tag` (
  `gene_signature_fk` int(11) DEFAULT NULL,
  `tag_fk` int(11) DEFAULT NULL,
  KEY `gene_signatures_to_tags_ibfk_3` (`gene_signature_fk`),
  KEY `gene_signatures_to_tags_ibfk_4` (`tag_fk`),
  CONSTRAINT `gene_signature_to_tag_ibfk_3` FOREIGN KEY (`gene_signature_fk`) REFERENCES `gene_signature` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `gene_signature_to_tag_ibfk_4` FOREIGN KEY (`tag_fk`) REFERENCES `tag` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `heat_map`
--

DROP TABLE IF EXISTS `heat_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `heat_map` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `network` longtext,
  `link` text NOT NULL,
  `viz_type` varchar(255) NOT NULL,
  `enrichr_library` varchar(255) DEFAULT NULL,
  `report_fk` int(11) NOT NULL,
  `target_app_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `target_app_fk` (`target_app_fk`),
  KEY `report_fk` (`report_fk`),
  CONSTRAINT `heat_map_ibfk_1` FOREIGN KEY (`report_fk`) REFERENCES `report` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `heat_map_ibfk_2` FOREIGN KEY (`target_app_fk`) REFERENCES `target_app_link` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3045 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `l1000cds2_result`
--

DROP TABLE IF EXISTS `l1000cds2_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `l1000cds2_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `share_id` varchar(255) NOT NULL,
  `is_up` tinyint(1) NOT NULL,
  `gene_signature_fk` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gene_signature_fk` (`gene_signature_fk`),
  CONSTRAINT `l1000cds2_result_ibfk_1` FOREIGN KEY (`gene_signature_fk`) REFERENCES `gene_signature` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9516 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `optional_metadata`
--

DROP TABLE IF EXISTS `optional_metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `optional_metadata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `gene_signature_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `optional_metadata_ibfk_1` (`gene_signature_fk`),
  CONSTRAINT `optional_metadata_ibfk_1` FOREIGN KEY (`gene_signature_fk`) REFERENCES `gene_signature` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=49742 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pca_plot`
--

DROP TABLE IF EXISTS `pca_plot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pca_plot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data` blob NOT NULL,
  `report_fk` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_fk` (`report_fk`),
  KEY `report_fk_2` (`report_fk`),
  CONSTRAINT `pca_plot_ibfk_1` FOREIGN KEY (`report_fk`) REFERENCES `report` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=559 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `perturbation`
--

DROP TABLE IF EXISTS `perturbation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perturbation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `score` double DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `l1000cds2_result_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_l1000cds2_result` (`l1000cds2_result_fk`),
  CONSTRAINT `fk_l1000cds2_result` FOREIGN KEY (`l1000cds2_result_fk`) REFERENCES `l1000cds2_result` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=399851 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranked_gene`
--

DROP TABLE IF EXISTS `ranked_gene`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranked_gene` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` float DEFAULT NULL,
  `gene_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gene_id` (`gene_fk`),
  CONSTRAINT `ranked_gene_ibfk_1` FOREIGN KEY (`gene_fk`) REFERENCES `gene` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=267965211 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranked_gene_to_gene_list`
--

DROP TABLE IF EXISTS `ranked_gene_to_gene_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranked_gene_to_gene_list` (
  `ranked_gene_fk` int(11) DEFAULT NULL,
  `gene_list_fk` int(11) DEFAULT NULL,
  KEY `rankedgene_id` (`ranked_gene_fk`),
  KEY `genelist_id` (`gene_list_fk`),
  CONSTRAINT `ranked_gene_to_gene_list_ibfk_1` FOREIGN KEY (`ranked_gene_fk`) REFERENCES `ranked_gene` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ranked_gene_to_gene_list_ibfk_2` FOREIGN KEY (`gene_list_fk`) REFERENCES `gene_list` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_approved` tinyint(1) NOT NULL DEFAULT '0',
  `name` varchar(255) DEFAULT NULL,
  `contact` varchar(255) DEFAULT NULL,
  `tag_fk` int(11) NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tag_fk` (`tag_fk`),
  CONSTRAINT `report_ibfk_1` FOREIGN KEY (`tag_fk`) REFERENCES `tag` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=356 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `required_metadata`
--

DROP TABLE IF EXISTS `required_metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `required_metadata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gene_signature_fk` int(11) DEFAULT NULL,
  `diff_exp_method` varchar(255) DEFAULT NULL,
  `ttest_correction_method` varchar(255) DEFAULT NULL,
  `cutoff` int(11) DEFAULT NULL,
  `threshold` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `diff_exp_method_fk` (`diff_exp_method`),
  KEY `ttest_correction_method_fk` (`ttest_correction_method`),
  KEY `required_metadata_ibfk_4` (`gene_signature_fk`),
  CONSTRAINT `required_metadata_ibfk_4` FOREIGN KEY (`gene_signature_fk`) REFERENCES `gene_signature` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23840 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `resource`
--

DROP TABLE IF EXISTS `resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `soft_file`
--

DROP TABLE IF EXISTS `soft_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `soft_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gene_signature_fk` int(11) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `platform` varchar(200) DEFAULT NULL,
  `is_geo` tinyint(1) DEFAULT NULL,
  `normalize` tinyint(1) DEFAULT NULL,
  `text_file` varchar(200) DEFAULT NULL,
  `actual_text_file` blob,
  `dataset_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `extraction_id` (`gene_signature_fk`),
  KEY `dataset_fk` (`dataset_fk`),
  CONSTRAINT `soft_file_ibfk_1` FOREIGN KEY (`gene_signature_fk`) REFERENCES `gene_signature` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `soft_file_ibfk_2` FOREIGN KEY (`dataset_fk`) REFERENCES `dataset` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21756 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `soft_file_sample`
--

DROP TABLE IF EXISTS `soft_file_sample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `soft_file_sample` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `soft_file_fk` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `is_control` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `soft_file_sample_ibfk_1` (`soft_file_fk`),
  CONSTRAINT `soft_file_sample_ibfk_1` FOREIGN KEY (`soft_file_fk`) REFERENCES `soft_file` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=84377 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `curator_fk` int(11) DEFAULT NULL,
  `is_restricted` tinyint(1) NOT NULL DEFAULT '0',
  `bio_category_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `curator_fk` (`curator_fk`),
  KEY `bio_category_fk` (`bio_category_fk`),
  CONSTRAINT `tag_ibfk_1` FOREIGN KEY (`curator_fk`) REFERENCES `curator` (`id`),
  CONSTRAINT `tag_ibfk_2` FOREIGN KEY (`bio_category_fk`) REFERENCES `bio_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=416 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `target_app`
--

DROP TABLE IF EXISTS `target_app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `target_app` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `target_app_link`
--

DROP TABLE IF EXISTS `target_app_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `target_app_link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `target_app_fk` int(11) DEFAULT NULL,
  `gene_list_fk` int(11) DEFAULT NULL,
  `link` text,
  PRIMARY KEY (`id`),
  KEY `target_app_fk` (`target_app_fk`),
  KEY `target_app_link_ibfk_2` (`gene_list_fk`),
  CONSTRAINT `target_app_link_ibfk_1` FOREIGN KEY (`target_app_fk`) REFERENCES `target_app` (`id`),
  CONSTRAINT `target_app_link_ibfk_2` FOREIGN KEY (`gene_list_fk`) REFERENCES `gene_list` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=100791 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `salt` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-23 14:48:24
