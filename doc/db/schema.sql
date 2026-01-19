-- Adminer 5.4.0 MariaDB 12.0.2-MariaDB-ubu2404 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

USE `myapi`;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `CONTENT`;
CREATE TABLE `CONTENT` (
  `id` varchar(255) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `duration` int(11) NOT NULL,
  `ageRating` varchar(10) NOT NULL,
  `coverUrl` varchar(255) DEFAULT NULL,
  `videoUrl` varchar(255) DEFAULT NULL,
  `type` enum('series','movie','documentary') NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `CONTENT_GENRE`;
CREATE TABLE `CONTENT_GENRE` (
  `contentId` varchar(255) NOT NULL,
  `genreId` varchar(255) NOT NULL,
  PRIMARY KEY (`contentId`,`genreId`),
  KEY `fk_cg_genre` (`genreId`),
  CONSTRAINT `fk_cg_content` FOREIGN KEY (`contentId`) REFERENCES `CONTENT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cg_genre` FOREIGN KEY (`genreId`) REFERENCES `GENRE` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `FAVORITE`;
CREATE TABLE `FAVORITE` (
  `profileId` varchar(255) NOT NULL,
  `contentId` varchar(255) NOT NULL,
  `addedDate` date NOT NULL,
  PRIMARY KEY (`profileId`,`contentId`),
  KEY `fk_fav_content` (`contentId`),
  CONSTRAINT `fk_fav_content` FOREIGN KEY (`contentId`) REFERENCES `CONTENT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_fav_profile` FOREIGN KEY (`profileId`) REFERENCES `PROFILE` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `GENRE`;
CREATE TABLE `GENRE` (
  `id` varchar(255) NOT NULL,
  `name` varchar(67) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `HISTORY`;
CREATE TABLE `HISTORY` (
  `profileId` varchar(255) NOT NULL,
  `contentId` varchar(255) NOT NULL,
  `lastWatched` datetime NOT NULL,
  `timeViewed` int(11) NOT NULL,
  PRIMARY KEY (`profileId`,`contentId`),
  KEY `fk_hist_content` (`contentId`),
  CONSTRAINT `fk_hist_content` FOREIGN KEY (`contentId`) REFERENCES `CONTENT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_hist_profile` FOREIGN KEY (`profileId`) REFERENCES `PROFILE` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `PAYMENT`;
CREATE TABLE `PAYMENT` (
  `id` varchar(255) NOT NULL,
  `subscriptionId` varchar(255) NOT NULL,
  `paymentDate` date NOT NULL,
  `method` enum('card','paypal') NOT NULL,
  `status` enum('pending','completed','failed') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pm_cliente` (`subscriptionId`),
  CONSTRAINT `fk_pm_cliente` FOREIGN KEY (`subscriptionId`) REFERENCES `SUBSCRIPTION` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `PROFILE`;
CREATE TABLE `PROFILE` (
  `id` varchar(255) NOT NULL,
  `userId` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_profile_user` (`userId`),
  CONSTRAINT `fk_profile_user` FOREIGN KEY (`userId`) REFERENCES `USER` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `RATING`;
CREATE TABLE `RATING` (
  `profileId` varchar(255) NOT NULL,
  `contentId` varchar(255) NOT NULL,
  `rating` enum('like','dislike','unrated') NOT NULL DEFAULT 'unrated',
  PRIMARY KEY (`profileId`,`contentId`),
  KEY `fk_rating_content` (`contentId`),
  CONSTRAINT `fk_rating_content` FOREIGN KEY (`contentId`) REFERENCES `CONTENT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_rating_profile` FOREIGN KEY (`profileId`) REFERENCES `PROFILE` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `SUBSCRIPTION`;
CREATE TABLE `SUBSCRIPTION` (
  `id` varchar(255) NOT NULL,
  `userId` varchar(255) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `status` enum('active','expired') NOT NULL,
  `type` enum('standard','premium','standard_yearly','premium_yearly') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `userId` (`userId`),
  CONSTRAINT `SUBSCRIPTION_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `SUBSCRIPTION` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `SUPERUSER`;
CREATE TABLE `SUPERUSER` (
  `id` varchar(255) NOT NULL,
  `permissions` enum('total','create','edit','read','none') NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_superuser` FOREIGN KEY (`id`) REFERENCES `USER` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `USER`;
CREATE TABLE `USER` (
  `id` varchar(255) NOT NULL,
  `username` varchar(67) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(128) NOT NULL,
  `status` enum('active','inactive') NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


-- 2026-01-16 19:47:19 UTC
