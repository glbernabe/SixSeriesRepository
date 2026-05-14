-- Adminer 5.4.2 MariaDB 12.2.2-MariaDB-ubu2404 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DELIMITER ;;

DROP EVENT IF EXISTS `check_subscriptions_expired`;;
CREATE DEFINER=`myapi`@`%` EVENT `check_subscriptions_expired` ON SCHEDULE EVERY 1 DAY STARTS '2024-01-01 00:00:00' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE SUBSCRIPTION
                                                                                                                                                         SET status = 'EXPIRED'
                                                                                                                                                         WHERE endDate < CURDATE() AND status != 'EXPIRED';;

DELIMITER ;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `CONTENT`;
CREATE TABLE `CONTENT` (
  `id` varchar(255) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `duration` time NOT NULL,
  `ageRating` varchar(10) NOT NULL,
  `coverUrl` varchar(255) DEFAULT NULL,
  `videoUrl` varchar(255) DEFAULT NULL,
  `type` enum('series','movie','documentary') NOT NULL,
  `logoURL` varchar(255) DEFAULT NULL,
  `portraitURL` varchar(255) DEFAULT NULL,
  `uploadDate` date NOT NULL,
  `releaseDate` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `CONTENT` (`id`, `title`, `description`, `duration`, `ageRating`, `coverUrl`, `videoUrl`, `type`, `logoURL`, `portraitURL`, `uploadDate`, `releaseDate`) VALUES
('1000', 'Game of Thrones', 'Nobles familias luchan por el control del Trono de Hierro.', '04:30:00', '18', 'https://static.posters.cz/image/hp/65920.jpg', 'https://streamimdb.ru/embed/tv/tt0944947', 'series', 'https://1000logos.net/wp-content/uploads/2020/09/Game-of-Thrones-logo.png', 'https://static.posters.cz/image/1300/135456.jpg', '2026-05-14', '2011-04-17'),
('1001', 'Avatar', 'Un marine parapléjico viaja al planeta Pandora y se une a los Na’vi.', '02:42:00', '13', 'https://wallpapercave.com/wp/wp9990039.jpg', 'https://streamimdb.ru/embed/movie/tt0499549', 'movie', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Avatar-Logo-avatar.svg/960px-Avatar-Logo-avatar.svg.png', 'https://m.media-amazon.com/images/M/MV5BMDEzMmQwZjctZWU2My00MWNlLWE0NjItMDJlYTRlNGJiZjcyXkEyXkFqcGc@._V1_.jpg', '2026-05-14', '2009-12-18'),
('1002', 'Cosmos', 'Serie documental que explora el universo y los avances científicos.', '00:50:00', '7', 'https://danielmarin.naukas.com/files/2014/03/neil-dg-tyson-cosmos.jpg', 'https://streamimdb.ru/embed/tv/tt2395695', 'documentary', '', 'https://pics.filmaffinity.com/cosmos_possible_worlds-589968652-mmed.jpg', '2026-05-14', '2014-03-09'),
('1003', 'The Witcher', 'Un cazador de monstruos lucha por encontrar su lugar en un mundo brutal.', '04:00:00', '18', 'https://s29288.pcdn.co/wp-content/uploads/2020/01/the-witcher-season-1-poster-750x298-1.jpg', 'https://streamimdb.ru/embed/tv/tt5180504', 'series', 'https://upload.wikimedia.org/wikipedia/en/0/05/The_Witcher_Logo.png', 'https://m.media-amazon.com/images/I/81UJkXjkmyL.jpg', '2026-05-14', '2019-12-20'),
('123', 'The Batman', 'En su segundo año luchando contra el crimen, Batman explora la corrupción existente en la ciudad de Gotham.', '02:56:00', '16', 'https://occ-0-8407-2218.1.nflxso.net/dnm/api/v6/6AYY37jfdO6hpXcMjf9Yu5cnmO0/AAAABRZGKb0WLE_o_W8uv5JFk7IO3NXuPlTCuWJs9lpDeq1cctUSf9dvwFJZMS4stKawVIqkfEqMZlWdTkmoOCTrtk2Hxf6SzXz2LhOx.jpg?r=55f', 'https://streamimdb.ru/embed/movie/tt1877830', 'movie', 'https://upload.wikimedia.org/wikipedia/commons/d/d1/The_Batman_2022_film_logo.png', 'https://es.web.img3.acsta.net/pictures/22/01/27/16/40/2914301.jpg', '2026-05-14', '2022-03-04'),
('333', 'Joker', 'La pasión de Arthur Fleck es hacer reír a la gente, pero la tragedia distorsiona su visión.', '02:02:00', '18', 'https://i0.wp.com/rockandfilms.es/wp-content/uploads/2019/10/1-1.jpg?fit=1280%2C720&ssl=1', 'https://streamimdb.ru/embed/movie/tt7286456', 'movie', 'https://cdn.mos.cms.futurecdn.net/BSs2g8No7CFR7ACu4rbVxL.jpg', 'https://www.tallengestore.com/cdn/shop/products/Joker_-_Joaquin_Phoenix_-_Hollywood_Action_Movie_Poster_2_80c9c6bd-80ec-4670-ac85-c445e17a579f.jpg?v=1573629351', '2026-05-14', '2019-10-04'),
('444', 'Breaking Bad', 'Un profesor de química diagnosticado con cáncer comienza a fabricar metanfetamina.', '05:00:00', '18', 'https://static.wikia.nocookie.net/eswikia/images/8/80/Breaking_Bad.png', 'https://streamimdb.ru/embed/tv/tt0903747', 'series', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Breaking_Bad_logo.svg/500px-Breaking_Bad_logo.svg.png', 'https://www.iamfy.co/cdn/shop/files/m_2Fx1000_2F223dbd30-fb38-4fd1-8724-c1817579e054.jpg?v=1760777206', '2026-05-14', '2008-01-20'),
('555', 'Interstellar', 'Un grupo de exploradores viaja a través de un agujero de gusano en el espacio.', '02:49:00', '13', 'https://img.englishcinemamadrid.com/nKizXKvqQfZzAMBylGXBi7TuU37mFVp7Mb9phhtftSw/resize:fill:800:450:1:0/gravity:sm/aHR0cHM6Ly9leHBhdGNpbmVtYXByb2QuYmxvYi5jb3JlLndpbmRvd3MubmV0L2ltYWdlcy82MGMzNzFhMy0yNzQyLTQwZWYtYTQwOS1kMzE0NmI0YTNlNDQuanBn.jpg', 'https://streamimdb.ru/embed/movie/tt0816692', 'movie', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Interstellar-logo.jpg/250px-Interstellar-logo.jpg', 'https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', '2026-05-14', '2014-11-07'),
('666', 'Planet Earth', 'Serie documental sobre la naturaleza y los ecosistemas del planeta Tierra.', '01:00:00', '7', 'https://hablandoenvidrio.com/wp-content/uploads/2020/03/planet-earth-ii-documental-sobre-el-planeta-1024x576.jpg', 'https://streamimdb.ru/embed/tv/tt0795176', 'documentary', NULL, 'https://pics.filmaffinity.com/planet_earth-535384921-large.jpg', '2026-05-14', '2006-03-05'),
('777', 'Stranger Things', 'Un grupo de niños descubre fenómenos sobrenaturales en su pequeño pueblo.', '04:00:00', '16', 'https://i.ytimg.com/vi/U9W85p8n-mE/maxresdefault.jpg', 'https://streamimdb.ru/embed/tv/tt4574334', 'series', 'https://upload.wikimedia.org/wikipedia/commons/3/38/Stranger_Things_logo.png', 'https://m.media-amazon.com/images/I/81SG03G+g7L._AC_UF894,1000_QL80_.jpg', '2026-05-14', '2016-07-15'),
('888', 'Inception', 'Un ladrón especializado en robar secretos entra en los sueños de sus víctimas.', '02:28:00', '13', 'https://image.tmdb.org/t/p/original/rWDkbJlIyqN8KcqXajh9sZMwGzo.jpg', 'https://streamimdb.ru/embed/movie/tt1375666', 'movie', 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Inception-wordmark.svg/3840px-Inception-wordmark.svg.png', 'https://www.originalfilmart.com/cdn/shop/files/inception_2010_advance_original_film_art_f4801a23-edb3-4db0-b382-1e2aec1dc927_5000x.jpg?v=1715962948', '2026-05-14', '2010-07-16'),
('999', 'The Last Dance', 'Documental sobre Michael Jordan y la histórica temporada de los Chicago Bulls.', '01:00:00', '13', 'https://images.justwatch.com/backdrop/177080914/s640/the-last-dance.jpg', 'https://streamimdb.ru/embed/tv/tt8420184', 'documentary', 'https://upload.wikimedia.org/wikipedia/commons/1/15/Last_Dance_-_logo.png', 'https://i.redd.it/nbwcb0fz5l1d1.jpeg', '2026-05-14', '2020-04-19');

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


DROP TABLE IF EXISTS `PROFILE`;
CREATE TABLE `PROFILE` (
                           `id` varchar(255) NOT NULL,
                           `userUsername` varchar(255) NOT NULL,
                           `name` varchar(255) NOT NULL,
                           `profileColor` varchar(32) DEFAULT NULL,
                           PRIMARY KEY (`id`),
                           KEY `fk_profile_user` (`userUsername`),
                           CONSTRAINT `PROFILE_ibfk_1` FOREIGN KEY (`userUsername`) REFERENCES `USER` (`username`) ON DELETE CASCADE
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
                                `userUsername` varchar(255) NOT NULL,
                                `startDate` date NOT NULL,
                                `endDate` date NOT NULL,
                                `status` enum('pending','active','expired') NOT NULL,
                                `type` enum('standard','premium','standard_yearly','premium_yearly') NOT NULL,
                                PRIMARY KEY (`id`),
                                KEY `userId` (`userUsername`),
                                CONSTRAINT `SUBSCRIPTION_ibfk_1` FOREIGN KEY (`userUsername`) REFERENCES `USER` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `USER`;
CREATE TABLE `USER` (
  `id` varchar(255) NOT NULL,
  `username` varchar(67) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(128) NOT NULL,
  `status` enum('active','inactive') NOT NULL,
  `rol` enum('user','superuser') NOT NULL DEFAULT 'user',
  `permissions` enum('total','create','edit','read','none') NOT NULL DEFAULT 'none',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


-- 2026-05-12 11:34:24 UTC