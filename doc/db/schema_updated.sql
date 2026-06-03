-- Adminer 5.4.1 MariaDB 12.1.2-MariaDB-ubu2404 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `CONTENT`;
CREATE TABLE `CONTENT` (
  `id` varchar(255) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `duration` time DEFAULT NULL,
  `ageRating` varchar(10) NOT NULL,
  `coverUrl` varchar(255) DEFAULT NULL,
  `videoUrl` varchar(255) DEFAULT NULL,
  `type` enum('series','movie','documentary') NOT NULL,
  `uploadDate` date DEFAULT NULL,
  `releaseDate` date DEFAULT NULL,
  `logoURL` varchar(255) DEFAULT NULL,
  `portraitURL` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `CONTENT` (`id`, `title`, `description`, `duration`, `ageRating`, `coverUrl`, `videoUrl`, `type`, `uploadDate`, `releaseDate`, `logoURL`, `portraitURL`) VALUES
('1000',	'Game of Throsss',	'Nobles familias luchan por el control del Trono de Hierro.',	'04:30:00',	'18',	'https://static.posters.cz/image/hp/65920.jpg',	'https://streamimdb.ru/embed/tv/tt0944947',	'series',	NULL,	NULL,	'https://1000logos.net/wp-content/uploads/2020/09/Game-of-Thrones-logo.png',	'https://static.posters.cz/image/1300/135456.jpg'),
('1001',	'Avatar',	'Un marine parapléjico viaja al planeta Pandora y se une a los Na’vi.',	'02:42:00',	'13',	'https://wallpapercave.com/wp/wp9990039.jpg',	'https://streamimdb.ru/embed/movie/tt0499549',	'movie',	NULL,	NULL,	'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Avatar-Logo-avatar.svg/960px-Avatar-Logo-avatar.svg.png',	'https://m.media-amazon.com/images/M/MV5BMDEzMmQwZjctZWU2My00MWNlLWE0NjItMDJlYTRlNGJiZjcyXkEyXkFqcGc@._V1_.jpg'),
('1002',	'Cosmos',	'Serie documental que explora el universo y los avances científicos.',	'00:50:00',	'7',	'https://danielmarin.naukas.com/files/2014/03/neil-dg-tyson-cosmos.jpg',	'https://streamimdb.ru/embed/tv/tt2395695',	'documentary',	NULL,	NULL,	'',	'https://pics.filmaffinity.com/cosmos_possible_worlds-589968652-mmed.jpg'),
('1003',	'The Witcher',	'Un cazador de monstruos lucha por encontrar su lugar en un mundo brutal.',	'04:00:00',	'18',	'https://s29288.pcdn.co/wp-content/uploads/2020/01/the-witcher-season-1-poster-750x298-1.jpg',	'https://streamimdb.ru/embed/tv/tt5180504',	'series',	NULL,	NULL,	'https://upload.wikimedia.org/wikipedia/en/0/05/The_Witcher_Logo.png',	'https://m.media-amazon.com/images/I/81UJkXjkmyL.jpg'),
('123',	'The Batman',	'En su segundo año luchando contra el crimen, Batman explora la corrupción existente en la ciudad de Gotham y el vínculo de esta con su propia familia. Además, entrará en conflicto con un asesino en serie conocido como \"el Acertijo\".',	'02:56:00',	'16',	'https://occ-0-8407-2218.1.nflxso.net/dnm/api/v6/6AYY37jfdO6hpXcMjf9Yu5cnmO0/AAAABRZGKb0WLE_o_W8uv5JFk7IO3NXuPlTCuWJs9lpDeq1cctUSf9dvwFJZMS4stKawVIqkfEqMZlWdTkmoOCTrtk2Hxf6SzXz2LhOx.jpg?r=55f',	'https://streamimdb.ru/embed/movie/tt1877830',	'movie',	NULL,	NULL,	'https://upload.wikimedia.org/wikipedia/commons/d/d1/The_Batman_2022_film_logo.png',	'https://es.web.img3.acsta.net/pictures/22/01/27/16/40/2914301.jpg'),
('333',	'Joker',	'La pasión de Arthur Fleck, un hombre ignorado por la sociedad, es hacer reír a la gente. Sin embargo, una serie de trágicos sucesos harán que su visión del mundo se distorsione considerablemente convirtiéndolo en un brillante criminal.',	'02:02:00',	'18',	'https://i0.wp.com/rockandfilms.es/wp-content/uploads/2019/10/1-1.jpg?fit=1280%2C720&ssl=1',	'https://streamimdb.ru/embed/movie/tt7286456',	'movie',	NULL,	NULL,	'https://cdn.mos.cms.futurecdn.net/BSs2g8No7CFR7ACu4rbVxL.jpg',	'https://www.tallengestore.com/cdn/shop/products/Joker_-_Joaquin_Phoenix_-_Hollywood_Action_Movie_Poster_2_80c9c6bd-80ec-4670-ac85-c445e17a579f.jpg?v=1573629351'),
('444',	'Breaking Bad',	'Un profesor de química diagnosticado con cáncer comienza a fabricar metanfetamina.',	'05:00:00',	'18',	'https://static.wikia.nocookie.net/eswikia/images/8/80/Breaking_Bad.png/revision/latest/scale-to-width-down/1600?cb=20160906023713',	'https://streamimdb.ru/embed/tv/tt0903747',	'series',	NULL,	NULL,	'https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Breaking_Bad_logo.svg/500px-Breaking_Bad_logo.svg.png',	'https://www.iamfy.co/cdn/shop/files/m_2Fx1000_2F223dbd30-fb38-4fd1-8724-c1817579e054.jpg?v=1760777206'),
('555',	'Interstellar',	'Un grupo de exploradores viaja a través de un agujero de gusano en el espacio.',	'02:49:00',	'13',	'https://img.englishcinemamadrid.com/nKizXKvqQfZzAMBylGXBi7TuU37mFVp7Mb9phhtftSw/resize:fill:800:450:1:0/gravity:sm/aHR0cHM6Ly9leHBhdGNpbmVtYXByb2QuYmxvYi5jb3JlLndpbmRvd3MubmV0L2ltYWdlcy82MGMzNzFhMy0yNzQyLTQwZWYtYTQwOS1kMzE0NmI0YTNlNDQuanBn.jpg',	'https://streamimdb.ru/embed/movie/tt0816692',	'movie',	NULL,	NULL,	'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Interstellar-logo.jpg/250px-Interstellar-logo.jpg',	'https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg'),
('666',	'Planet Earth',	'Serie documental sobre la naturaleza y los ecosistemas del planeta Tierra.',	'01:00:00',	'7',	'https://hablandoenvidrio.com/wp-content/uploads/2020/03/planet-earth-ii-documental-sobre-el-planeta-1024x576.jpg',	'https://streamimdb.ru/embed/tv/tt0795176',	'documentary',	NULL,	NULL,	NULL,	'https://pics.filmaffinity.com/planet_earth-535384921-large.jpg'),
('777',	'Stranger Things',	'Un grupo de niños descubre fenómenos sobrenaturales en su pequeño pueblo.',	'04:00:00',	'16',	'https://i.ytimg.com/vi/U9W85p8n-mE/maxresdefault.jpg',	'https://streamimdb.ru/embed/tv/tt4574334',	'series',	NULL,	NULL,	'https://upload.wikimedia.org/wikipedia/commons/3/38/Stranger_Things_logo.png',	'https://m.media-amazon.com/images/I/81SG03G+g7L._AC_UF894,1000_QL80_.jpg'),
('888',	'Inception',	'Un ladrón especializado en robar secretos entra en los sueños de sus víctimas.',	'02:28:00',	'13',	'https://image.tmdb.org/t/p/original/rWDkbJlIyqN8KcqXajh9sZMwGzo.jpg',	'https://streamimdb.ru/embed/movie/tt1375666',	'movie',	NULL,	NULL,	'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Inception-wordmark.svg/3840px-Inception-wordmark.svg.png',	'https://www.originalfilmart.com/cdn/shop/files/inception_2010_advance_original_film_art_f4801a23-edb3-4db0-b382-1e2aec1dc927_5000x.jpg?v=1715962948'),
('999',	'The Last Dance',	'Documental sobre Michael Jordan y la histórica temporada de los Chicago Bulls.',	'01:00:00',	'13',	'https://images.justwatch.com/backdrop/177080914/s640/the-last-dance.jpg',	'https://streamimdb.ru/embed/tv/tt8420184',	'documentary',	NULL,	NULL,	'https://upload.wikimedia.org/wikipedia/commons/1/15/Last_Dance_-_logo.png',	'https://i.redd.it/nbwcb0fz5l1d1.jpeg');

DROP TABLE IF EXISTS `CONTENT_GENRE`;
CREATE TABLE `CONTENT_GENRE` (
  `contentId` varchar(255) NOT NULL,
  `genreId` varchar(255) NOT NULL,
  PRIMARY KEY (`contentId`,`genreId`),
  KEY `fk_cg_genre` (`genreId`),
  CONSTRAINT `fk_cg_content` FOREIGN KEY (`contentId`) REFERENCES `CONTENT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cg_genre` FOREIGN KEY (`genreId`) REFERENCES `GENRE` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `EPISODE`;
CREATE TABLE `EPISODE` (
  `id` varchar(255) NOT NULL,
  `contentId` varchar(255) NOT NULL,
  `season` int(11) NOT NULL DEFAULT 1,
  `episode` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `duration` time DEFAULT NULL,
  `videoUrl` varchar(255) NOT NULL,
  `coverUrl` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ep_content` (`contentId`),
  CONSTRAINT `fk_ep_content` FOREIGN KEY (`contentId`) REFERENCES `CONTENT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `EPISODE` (`id`, `contentId`, `season`, `episode`, `title`, `description`, `duration`, `videoUrl`, `coverUrl`) VALUES
('ep-bb-s1e1',	'444',	1,	1,	'Piloto',	'Walter White recibe un diagnóstico que lo cambia todo.',	'00:58:00',	'https://streamimdb.ru/embed/tv/tt0903747?season=1&episode=1',	NULL),
('ep-bb-s1e2',	'444',	1,	2,	'El gato está en la bolsa',	'Walter y Jesse se enfrentan a las consecuencias.',	'00:48:00',	'https://streamimdb.ru/embed/tv/tt0903747?season=1&episode=2',	NULL),
('ep-bb-s2e1',	'444',	2,	1,	'Seven Thirty-Seven',	'Walter y Jesse deben eliminar a dos traficantes.',	'00:47:00',	'https://streamimdb.ru/embed/tv/tt0903747?season=2&episode=1',	NULL),
('ep-got-s1e1',	'1000',	1,	1,	'Winter Is Coming',	'La familia Stark descubre una amenaza más allá del Muro.',	'01:02:00',	'https://streamimdb.ru/embed/tv/tt0944947?season=1&episode=1',	NULL),
('ep-got-s1e2',	'1000',	1,	2,	'The Kingsroad',	'Ned Stark parte hacia Desembarco del Rey.',	'00:56:00',	'https://streamimdb.ru/embed/tv/tt0944947?season=1&episode=2',	NULL),
('ep-got-s2e1',	'1000',	2,	1,	'The North Remembers',	'Joffrey celebra su nombre día con violencia.',	'00:58:00',	'https://streamimdb.ru/embed/tv/tt0944947?season=2&episode=1',	NULL),
('ep-st-s1e1',	'777',	1,	1,	'El mundo al revés',	'Will Byers desaparece misteriosamente.',	'00:49:00',	'https://streamimdb.ru/embed/tv/tt4574334?season=1&episode=1',	NULL),
('ep-st-s1e2',	'777',	1,	2,	'La chica rara',	'Once escapa del laboratorio.',	'00:46:00',	'https://streamimdb.ru/embed/tv/tt4574334?season=1&episode=2',	NULL),
('ep-wit-s1e1',	'1003',	1,	1,	'El principio del fin',	'Geralt llega a Blaviken y se enfrenta a una bruja.',	'01:00:00',	'https://streamimdb.ru/embed/tv/tt5180504?season=1&episode=1',	NULL),
('ep-wit-s1e2',	'1003',	1,	2,	'Cuatro marcos de cobre',	'Geralt acepta un contrato en Posada.',	'00:57:00',	'https://streamimdb.ru/embed/tv/tt5180504?season=1&episode=2',	NULL);

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

INSERT INTO `GENRE` (`id`, `name`) VALUES
('84e78bc3-3848-41eb-9084-e47cd559ec71',	'Comedia'),
('95470410-67d5-4b40-9785-c7374f4c4aff',	'Sci-Fi'),
('96fd07ce-3c69-4f4b-8d6f-7732e34cd4dd',	'Batallas'),
('989ea25f-493b-4490-affe-d3bff40e848a',	'Misterio'),
('abfcd4d1-3454-40fb-8188-87b5ddc5d26b',	'Aventura'),
('ae9d9fa2-490e-4c11-a43a-582863f7b958',	'Anime'),
('cd1a343a-42ea-4d12-9db7-9703a00c198d',	'Acción'),
('e8827449-d3c9-42a7-aca4-54161293a88d',	'Historia');

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
('00d65a19-d49b-4e99-a1a6-f96e14c33904',	'2b2e33cf-0699-47a8-b68a-02d56a758861',	'2026-05-18',	'card',	'completed',	9.99),
('41be5803-bebb-478c-824d-34061e227ce5',	'c6f20b8d-a280-48ad-8e8b-31e1a0e7d35f',	'2026-05-26',	'card',	'completed',	99.99),
('640fce4e-cc4a-422a-a821-0e1a2a1d245d',	'7c1c5efb-21a4-4e6d-aa04-4660b7ee117a',	'2026-06-01',	'card',	'completed',	99.99),
('669af433-35a4-4a91-9896-fec394870b5f',	'00581617-90a5-4ad7-8145-1eb614674a2d',	'2026-06-01',	'card',	'completed',	9.99),
('7ce09b69-ab88-48f7-ab0d-06202ce1e70a',	'c8865232-6e1a-4841-a502-4f7de3905a6f',	'2026-05-22',	'card',	'completed',	99.99),
('a622b9bf-8b70-49e4-adc2-78dde0f54d71',	'c2f4da80-0945-476f-a46b-e6f4a5e9f5e9',	'2026-05-22',	'card',	'completed',	14.59),
('b69f599c-1a2e-44a6-927f-1636ceca6763',	'182fb406-1b7f-4718-b6f9-5ebe56ccbeb6',	'2026-05-26',	'card',	'completed',	140.59),
('bab3913b-aa92-4c24-bacf-225cd250a5e0',	'48737c1e-6234-49da-afd9-4e64c755f349',	'2026-06-02',	'card',	'completed',	9.99),
('d558060f-aed0-430f-81eb-8099c79f41a9',	'c78632e7-525a-4254-964b-84b5a25b9fba',	'2026-05-23',	'card',	'completed',	99.99),
('e340857d-3388-4486-a011-d894751a515e',	'3481e317-eb26-48c4-8049-926823c3c16d',	'2026-05-18',	'card',	'completed',	9.99);

DROP TABLE IF EXISTS `PROFILE`;
CREATE TABLE `PROFILE` (
  `id` varchar(255) NOT NULL,
  `userUsername` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `profileColor` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_profile_user` (`userUsername`),
  CONSTRAINT `PROFILE_ibfk_1` FOREIGN KEY (`userUsername`) REFERENCES `USER` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `PROFILE` (`id`, `userUsername`, `name`, `profileColor`) VALUES
('1',	'Admin',	'Admin',	'#7FA8C9'),
('5dd198ba-f015-4986-b3d4-f0df8e6a1125',	'Tears123',	'Tears',	'#6A6A69'),
('bfbc6cea-7370-4300-9084-aa180dbd91d8',	'Gabrielin',	'Cabra',	'#6A6A69'),
('eef644a5-3d2b-4d14-8b9a-e4a913f30e54',	'gabriell',	'Gerardas',	'#6A6A69');

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
  `type` enum('standard','premium','standard_yearly','premium_yearly','admin_life') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `userId` (`userUsername`),
  CONSTRAINT `SUBSCRIPTION_ibfk_1` FOREIGN KEY (`userUsername`) REFERENCES `USER` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `SUBSCRIPTION` (`id`, `userUsername`, `startDate`, `endDate`, `status`, `type`) VALUES
('00581617-90a5-4ad7-8145-1eb614674a2d',	'Gerardas',	'2026-06-01',	'2026-07-01',	'active',	'standard'),
('1',	'Admin',	'2026-06-02',	'2100-06-02',	'active',	'admin_life'),
('182fb406-1b7f-4718-b6f9-5ebe56ccbeb6',	'Gabrielin',	'2026-05-26',	'2027-05-26',	'active',	'premium_yearly'),
('2b2e33cf-0699-47a8-b68a-02d56a758861',	'gabriell',	'2026-05-18',	'2026-05-22',	'expired',	'standard'),
('3481e317-eb26-48c4-8049-926823c3c16d',	'gabriell',	'2026-05-18',	'2026-05-18',	'expired',	'standard'),
('48737c1e-6234-49da-afd9-4e64c755f349',	'Admin',	'2026-06-02',	'2026-06-02',	'expired',	'standard'),
('7c1c5efb-21a4-4e6d-aa04-4660b7ee117a',	'Tears123',	'2026-06-01',	'2027-06-01',	'active',	'standard_yearly'),
('c2f4da80-0945-476f-a46b-e6f4a5e9f5e9',	'gabriell',	'2026-05-22',	'2026-05-23',	'expired',	'premium'),
('c6f20b8d-a280-48ad-8e8b-31e1a0e7d35f',	'Gabrielin',	'2026-05-26',	'2026-05-26',	'expired',	'standard_yearly'),
('c78632e7-525a-4254-964b-84b5a25b9fba',	'gabriell',	'2026-05-23',	'2027-05-23',	'active',	'standard_yearly'),
('c8865232-6e1a-4841-a502-4f7de3905a6f',	'gabriell',	'2026-05-22',	'2026-05-22',	'expired',	'standard_yearly');

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

INSERT INTO `USER` (`id`, `username`, `password`, `email`, `status`, `rol`, `permissions`) VALUES
('0efeee81-213c-4d01-abce-9f03922ddcdf',	'guerrardas',	'$2b$12$v4SVJpXMP4MxIXpziRHL6.MICw3yLksV7IsdJiE/hkw0j9rqKf0ji',	'guerrardas',	'inactive',	'user',	'none'),
('1bef8c67-c6d2-410a-90ae-f4287d523a41',	'Tears123',	'$2b$12$fPUvl.faj78pT4zQp9DGYui0NXev5gDIcv4tcyiqdn1fuOApD.MOm',	'Tears123',	'inactive',	'user',	'none'),
('8e61948f-d5c1-4144-9ea4-31041c634376',	'gabriell1',	'$2b$12$kwy1tGtX/3Xwf2jSFGqe0u2/GLzen4ozPfr.TJtUCBQaw3ktkPbJS',	'gabriell1',	'active',	'user',	'none'),
('b3ac4467-f827-49c5-99c4-c5c674ed6668',	'Gabrielin',	'$2b$12$KnnQX288zv0zA9w46G6KOOmWe07mlf.tyk7mKp20WcZCVYNgUFNJa',	'Gabrielin',	'active',	'user',	'none'),
('d12df34c-09b9-45b8-ab3e-c8367bb3b849',	'Admin',	'$2b$12$jwc5yRNkpFahlpYFsGxdt.UGjS.Z4bKpINpKJGVUlLztc6O0M3hxu',	'Tears321',	'active',	'superuser',	'total'),
('d5511c93-8afa-41e8-ade2-e7db78571b30',	'gerardas',	'$2b$12$InedEClKb4S2y8LBumYUs.9MalGng0h5WHYlZcO.ZyR5dcJ.3A7e2',	'gerardas',	'active',	'user',	'none'),
('ea24d651-71fd-47f5-b53f-234494d4f9d3',	'gabriell',	'$2b$12$9wPdergYHOA2ZjkR8fDqhuJpKPZUQIMyebNRIU98sCLz253O./hFi',	'gabriell',	'active',	'user',	'none');

-- 2026-06-03 20:21:07 UTC
