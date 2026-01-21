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
  `status` enum('completed','pending','failed') NOT NULL,
  `amount` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pm_cliente` (`subscriptionId`),
  CONSTRAINT `fk_pm_cliente` FOREIGN KEY (`subscriptionId`) REFERENCES `SUBSCRIPTION` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `PAYMENT` (`id`, `subscriptionId`, `paymentDate`, `method`, `status`, `amount`) VALUES
('f75afcf7-6268-48f6-9b57-4b0fdf3c548d',	'd9b56de1-756d-425a-9eed-d4df13e36e0b',	'2026-01-21',	'card',	'completed',	14.59);

DROP TABLE IF EXISTS `PROFILE`;
CREATE TABLE `PROFILE` (
  `id` varchar(255) NOT NULL,
  `userUsername` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_profile_user` (`userUsername`),
  CONSTRAINT `PROFILE_ibfk_1` FOREIGN KEY (`userUsername`) REFERENCES `USER` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `PROFILE` (`id`, `userUsername`, `name`) VALUES
('41980cc5-b029-40cb-99bf-63110a995676',	'gabriel',	'antuan');

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
  `userUsername` varchar(255) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `status` enum('pending','active','expired') NOT NULL,
  `type` enum('standard','premium','standard_yearly','premium_yearly') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `userId` (`userUsername`),
  CONSTRAINT `SUBSCRIPTION_ibfk_1` FOREIGN KEY (`userUsername`) REFERENCES `USER` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `SUBSCRIPTION` (`id`, `userUsername`, `startDate`, `endDate`, `status`, `type`) VALUES
('d9b56de1-756d-425a-9eed-d4df13e36e0b',	'gabriel',	'2026-01-21',	'2026-02-21',	'active',	'premium');

DROP TABLE IF EXISTS `SUPERUSER`;
CREATE TABLE `SUPERUSER` (
  `id` varchar(255) NOT NULL,
  `permissions` enum('total','create','edit','read','none') NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_superuser` FOREIGN KEY (`id`) REFERENCES `USER` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `SUPERUSER` (`id`, `permissions`) VALUES
('4add36b1-a9d1-438b-b2c7-d139beb3908e',	'total');

DROP TABLE IF EXISTS `USER`;
CREATE TABLE `USER` (
  `id` varchar(255) NOT NULL,
  `username` varchar(67) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(128) NOT NULL,
  `status` enum('active','inactive') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `USER` (`id`, `username`, `password`, `email`, `status`) VALUES
('38ed5fbe-f916-4d3c-8348-99e4591a2a53',	'string',	'$2b$12$y.WSlo5aPcegFDmzTrY2POpk9UiATjEUuBBgC9anACTzVbfa..N0i',	'string',	'active'),
('4add36b1-a9d1-438b-b2c7-d139beb3908e',	'gabriel',	'$2b$12$SHm3Cg6AWOKV3B8r9hQ4POUMdyzIa9Hyvh07xvoOeMQJumkGVvW4q',	'gabriel',	'active');

-- 2026-01-21 16:36:03 UTC
