-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         5.7.33 - MySQL Community Server (GPL)
-- SO del servidor:              Win64
-- HeidiSQL Versión:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando estructura para tabla pythonflaskcontactos.blog
CREATE TABLE IF NOT EXISTS `blog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author_id` int(11) NOT NULL DEFAULT '0',
  `title` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contenido` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `img` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `FK_blog_users` (`author_id`),
  CONSTRAINT `FK_blog_users` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;

-- Volcando datos para la tabla pythonflaskcontactos.blog: ~30 rows (aproximadamente)
/*!40000 ALTER TABLE `blog` DISABLE KEYS */;
INSERT INTO `blog` (`id`, `author_id`, `title`, `contenido`, `img`, `created_at`, `updated_at`) VALUES
	(69, 211, 'El congreso ultrasónico', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In rhoncus odio ut molestie luctus. Duis vel metus lorem. Aliquam eleifend lorem et erat faucibus tristique. In sit amet est arcu. Duis aliquet felis nisi, venenatis luctus ligula venenatis in. Donec a dui vulputate, cursus nunc a, varius lacus. Mauris vestibulum placerat quam, eget egestas ligula porta sit amet. Curabitur venenatis lacus sit amet aliquam dapibus. Pellentesque nec nisl eu felis tincidunt porttitor. Aenean ut turpis egestas turpis ornare ultricies. Ut non magna quis augue interdum sollicitudin. Vestibulum laoreet, metus vel pretium euismod, lorem risus aliquet risus, sit amet mollis est leo ac erat. In sit amet leo et sapien porttitor interdum quis ut elit. Nunc posuere nibh in enim hendrerit, vel vestibulum nibh vestibulum.', '20211204175906_comenzamos.jpg', '2020-01-01 23:59:59', '2021-11-28 12:43:43'),
	(76, 407, 'Isabella post12', 'Aliquam eleifend lorem et erat faucibus tristique.', '20211204180414_asombro.png', '2021-10-17 19:23:39', '2021-12-05 14:11:25'),
	(77, 2, 'Lorem Luctus Ut Foundation', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', '', '2021-10-17 19:23:39', NULL),
	(82, 3, 'Adipiscing Lacus Ut Associates', 'Donec a dui vulputate, cursus nunc a, varius lacus.', '', '2021-10-17 19:23:39', NULL),
	(84, 2, 'Purus Ac Institute', 'Pellentesque nec nisl eu felis tincidunt porttitor.', '', '2021-10-17 19:23:39', NULL),
	(86, 2, 'Adipiscing Fringilla Porttitor Inc.', 'Vestibulum laoreet, metus vel pretium euismod, lorem risus aliquet risus, sit amet mollis est leo ac erat.', '', '2021-10-17 19:23:39', NULL),
	(88, 3, 'Risus Quis LLC', 'Aenean scelerisque, elit vitae placerat dictum, nunc leo laoreet tellus, ut suscipit neque diam lobortis elit.', '', '2021-10-17 19:23:39', NULL),
	(90, 2, 'Enim Etiam Imperdiet Foundation', 'In finibus sagittis scelerisque.', '', '2021-10-17 19:23:39', NULL),
	(91, 3, 'Fringilla Cursus Corporation', 'Aenean at vestibulum orci.', '', '2021-10-17 19:23:39', NULL),
	(92, 2, 'Quisque Ornare Tortor PC', 'Interdum et malesuada fames ac ante ipsum primis in faucibus.', '', '2021-10-17 19:23:39', NULL),
	(93, 2, 'Purus Mauris Ltd', 'Aenean ac vestibulum massa.\r\nUt id sem risus.\r\nDuis quis erat faucibus tellus consequat luctus.\r\n', '', '2021-10-17 19:23:39', NULL),
	(94, 2, 'Nunc Industries', 'Nam ut tellus mi.\r\nDonec posuere tellus non dapibus pulvinar.\r\nDuis sit amet turpis a elit varius gravida quis vitae tortor.\r\n', '', '2021-10-17 19:23:39', NULL),
	(95, 2, 'Natoque Corporation', 'Vivamus at urna elementum, imperdiet mauris vitae, facilisis sem.\r\nNunc augue ipsum, porta at tellus ac, dictum feugiat velit.', '', '2021-10-17 19:23:39', NULL),
	(96, 3, 'Mus PC', 'Vestibulum id sem vel enim consectetur hendrerit tincidunt in augue.\r\nInteger nec placerat mi.\r\nFusce et faucibus ante, nec lacinia urna.', '', '2021-10-17 19:23:39', NULL),
	(97, 2, 'Blandit Nam Incorporated', 'Curabitur lobortis, quam in dignissim laoreet, dolor diam pellentesque dui, id consectetur velit dui rhoncus velit.\r\nAliquam mauris mi, aliquam sit amet lacinia vel, luctus ut massa.\r\nCurabitur ullamcorper elementum tortor sit amet sodales.', '', '2021-10-17 19:23:39', NULL),
	(98, 2, 'Enim Limited', 'Donec ac nibh libero.\r\nAliquam vel convallis metus.\r\nNullam tempor bibendum velit.', '', '2021-10-17 19:23:39', NULL),
	(99, 3, 'Ipsum Inc.', 'Phasellus pretium finibus consequat.\r\nPhasellus aliquet commodo tellus eu bibendum.\r\nEtiam ac sagittis tellus, id facilisis mauris.\r\nUt sagittis egestas lectus non mollis.', '', '2021-10-17 19:23:39', NULL),
	(100, 1, 'Scelerisque Dui Inc.', 'Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.\r\n\r\nEtiam id leo eu orci pharetra efficitur aliquet eu nunc.\r\nVivamus vitae lacinia nibh.', '', '2021-10-17 19:23:39', NULL),
	(101, 461, 'Lucian Staniak', 'Dijo: "No existe ninguna felicidad sin lágrimas"', '', '2021-11-28 14:03:35', '2021-11-28 14:05:37'),
	(102, 1, 'Blogspot #a1', 'Donec neque mi, malesuada tincidunt lacus in, hendrerit varius metus.\r\nEtiam ultrices imperdiet dolor, eu consectetur dui vestibulum sit amet.\r\nDonec nec massa sollicitudin, mollis diam in, fermentum elit.', '', '2021-12-04 17:35:41', '2021-12-04 17:35:41'),
	(103, 1, 'Blogspot #a12', 'Suspendisse sagittis iaculis turpis a vehicula.\r\nProin mattis turpis nunc, nec suscipit est sagittis eu.\r\nEtiam consequat non nisi in pellentesque.', '', '2021-12-04 17:55:56', '2021-12-04 17:55:56'),
	(104, 1, 'Blogspot #a3', 'Quisque sodales varius orci, nec porta augue blandit nec.\r\nDonec porttitor odio at consectetur consequat.', '', '2021-12-04 17:57:39', '2021-12-04 17:57:39'),
	(105, 1, 'Blogspot #a14', 'Vivamus vitae lacinia nibh.\r\nDonec neque mi, malesuada tincidunt lacus in, hendrerit varius metus.\r\nEtiam ultrices imperdiet dolor, eu consectetur dui vestibulum sit amet.\r\nDonec nec massa sollicitudin, mollis diam in, fermentum elit.\r\nSuspendisse sagittis iaculis turpis a vehicula.\r\nProin mattis turpis nunc, nec suscipit est sagittis eu.', '', '2021-12-04 17:59:04', '2021-12-04 17:59:04'),
	(106, 1, 'Blogspot #a15', 'Etiam ac sagittis tellus, id facilisis mauris.\r\nUt sagittis egestas lectus non mollis.\r\nClass aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.\r\n\r\nEtiam id leo eu orci pharetra efficitur aliquet eu nunc.', '20211204182656_composer.jpg', '2021-12-04 18:03:28', '2021-12-04 18:03:28'),
	(107, 1, 'Blogspot #a16', 'Donec neque mi, malesuada tincidunt lacus in, hendrerit varius metus.\r\nEtiam ultrices imperdiet dolor, eu consectetur dui vestibulum sit amet.\r\nDonec nec massa sollicitudin, mollis diam in, fermentum elit.\r\nSuspendisse sagittis iaculis turpis a vehicula.', '20211204183118_comenzamos2.jpg', '2021-12-04 18:03:28', '2021-12-04 18:03:28'),
	(108, 1, 'Blogspot #a17', 'Proin mattis turpis nunc, nec suscipit est sagittis eu.\r\nEtiam consequat non nisi in pellentesque.\r\nQuisque sodales varius orci, nec porta augue blandit nec.\r\nDonec porttitor odio at consectetur consequat.', NULL, '2021-12-04 18:14:45', '2021-12-04 18:14:45'),
	(109, 1, 'Blogspot #a18', 'Curabitur ullamcorper elementum tortor sit amet sodales.\r\nDonec ac nibh libero.\r\nAliquam vel convallis metus.\r\nNullam tempor bibendum velit.\r\nPhasellus pretium finibus consequat.\r\nPhasellus aliquet commodo tellus eu bibendum.', NULL, '2021-12-04 18:25:51', '2021-12-04 18:25:51'),
	(110, 1, 'Blogspot #a19', 'Fusce et faucibus ante, nec lacinia urna.\r\nCurabitur lobortis, quam in dignissim laoreet, dolor diam pellentesque dui, id consectetur velit dui rhoncus velit.\r\nAliquam mauris mi, aliquam sit amet lacinia vel, luctus ut massa.', NULL, '2021-12-04 18:31:03', '2021-12-04 18:31:03'),
	(111, 1, 'Blogspot 1', 'Duis sit amet turpis a elit varius gravida quis vitae tortor.\r\nVivamus at urna elementum, imperdiet mauris vitae, facilisis sem.\r\nNunc augue ipsum, porta at tellus ac, dictum feugiat velit.\r\n\r\nVestibulum id sem vel enim consectetur hendrerit tincidunt in augue.', NULL, '2021-12-05 13:40:45', '2021-12-05 13:40:45'),
	(112, 401, 'Blogspot 222', 'Curabitur tempor lectus vel auctor scelerisque.\r\nAliquam euismod tempus purus sit amet dapibus.\r\n\r\nAenean ac vestibulum massa.\r\nUt id sem risus.\r\nDuis quis erat faucibus tellus consequat luctus.\r\nNam ut tellus mi.', NULL, '2021-12-05 13:43:34', '2021-12-05 13:57:54'),
	(113, 1, 'Gamma Ray', 'El contenido de este post está relacionado con el grupo musical llamado Gamma Ray, cuya expresión musical se enmarca en el género Power Metal. La revista.', '20211204180908_a.jpg', '2021-12-19 19:13:35', '2021-12-19 19:13:35'),
	(114, 1, 'abc', 'abc', '20211204180908_a.jpg', '2022-01-07 19:36:05', '2021-12-19 19:36:05'),
	(115, 1, '2022', 'El abecedario comienza con las primeras dos letras del alfabeto.', '20211219194017_bienhecho.jpg', '2022-01-08 18:47:00', '2022-01-08 18:47:00'),
	(116, 1, 'Romansky', 'El post romansky', '20220122195841_composer.jpg', '2022-01-22 19:57:38', '2022-01-22 19:57:38'),
	(117, 1, 'Título turco', 'Este post fue creado ya usando current_user de Flask-Login', NULL, '2022-02-13 14:38:27', '2022-02-13 14:38:27');
/*!40000 ALTER TABLE `blog` ENABLE KEYS */;

-- Volcando estructura para tabla pythonflaskcontactos.contactos
CREATE TABLE IF NOT EXISTS `contactos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla pythonflaskcontactos.contactos: ~5 rows (aproximadamente)
/*!40000 ALTER TABLE `contactos` DISABLE KEYS */;
INSERT INTO `contactos` (`id`, `nombre`, `telefono`, `email`, `created_at`, `updated_at`) VALUES
	(1, 'José David', '77777772', 'roberto@gmail.com', '2021-09-16 13:19:44', '2021-09-16 13:19:44'),
	(3, 'abcd', '+1123456789', '1@gmail.com', '2021-09-16 18:31:36', '2021-09-16 18:31:36'),
	(4, 'df', '+112345678', 'test@eydosdev.com', '2021-09-16 18:31:36', '2021-09-16 18:31:36'),
	(5, 'Jonás Mortero', '+525556581113', 'joe@gmail.com.mx', '2021-09-16 19:20:28', '2021-09-16 19:35:06'),
	(6, 'Sandra Gómez', '+12344656789', 'sandara@gmail.com', '2021-09-19 19:40:50', '2021-09-19 19:40:50');
/*!40000 ALTER TABLE `contactos` ENABLE KEYS */;

-- Volcando estructura para tabla pythonflaskcontactos.roles
CREATE TABLE IF NOT EXISTS `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla pythonflaskcontactos.roles: ~2 rows (aproximadamente)
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` (`id`, `Nombre`, `slug`) VALUES
	(1, 'Administrador', 'administrador'),
	(2, 'Editor', 'editor'),
	(3, 'Visor', 'visor');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;

-- Volcando estructura para tabla pythonflaskcontactos.submissions
CREATE TABLE IF NOT EXISTS `submissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `forma` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `datos` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla pythonflaskcontactos.submissions: ~23 rows (aproximadamente)
/*!40000 ALTER TABLE `submissions` DISABLE KEYS */;
INSERT INTO `submissions` (`id`, `forma`, `datos`, `created_at`) VALUES
	(1, 'contacto', '{"nombre": "Jonás", "email": "jonas@gmail.com", "mensaje": "Mensaje de Jonás", "documento": null}', '2022-01-23 17:54:11'),
	(2, 'contacto', '{"nombre": "Sandra Gómez", "email": "sandra.gomez@gmail.com", "mensaje": "Mensaje de Sandra Gómez", "documento": "20220123175833_a.jpg"}', '2022-01-23 17:58:32'),
	(3, 'contacto', '{"nombre": "Ron", "email": "ron@gmail.com", "mensaje": "Mensaje de Ron Ron", "documento": null}', '2022-01-23 17:58:32'),
	(4, 'contacto', '{"nombre": "Mariana", "email": "mariana@gmail.com", "mensaje": "Este es el mensaje de Mariana, enviado a las 5:59", "documento": "20220123175959_abcdefghijklmnnopqrstuvwxyz123456789_ABCDEFGHIJKLMNNOPQRSTUVWXYZ.jpg"}', '2022-01-23 17:58:32'),
	(5, 'contacto', '{"nombre": "Joe", "email": "joe@gmail.com", "mensaje": "Mensaje provisional de Joe", "documento": null}', '2022-01-23 17:58:32'),
	(6, 'contacto', '{"nombre": "Robert", "email": "robert@gmail.com", "mensaje": "Mensaje de robert", "documento": null}', '2022-01-23 18:07:28'),
	(7, 'contacto', '{"nombre": "Alfa", "email": "alfa@gmail.com", "mensaje": "Mensaje alfañero", "documento": null}', '2022-01-23 18:07:49'),
	(8, 'contacto', '{"nombre": "Beta", "email": "betaa@gmail.com", "mensaje": "Mensaje betancio", "documento": "20220123181142_asombro.png"}', '2022-01-23 18:11:42'),
	(9, 'contacto', '{"nombre": "David", "email": "david@gmail.com", "mensaje": "Esto es una prueba de envío de formulario, veamos qué tal funciona.", "documento": "20220123182346_bienhecho.jpg"}', '2022-01-23 18:23:46'),
	(10, 'contacto', '{"nombre": "David", "email": "david@gmail.com", "mensaje": "Esto es una prueba de envío de formulario, veamos qué tal funciona.", "documento": "20220123182540_bienhecho.jpg"}', '2022-01-23 18:25:40'),
	(11, 'contacto', '{"nombre": "David", "email": "david@gmail.com", "mensaje": "Esto es una prueba de envío de formulario, veamos qué tal funciona.", "documento": "20220123182836_bienhecho.jpg"}', '2022-01-23 18:28:36'),
	(12, 'contacto', '{"nombre": "Rigoberto", "email": "rigoberto@gmail.com", "mensaje": "Hola, presento una denuncia administrativa contra el encargado del website, que supongo es un webmaster, porque no sabe hacer nada, es un inútil.", "documento": "20220123204414_comenzamos.jpg"}', '2022-01-23 20:44:14'),
	(13, 'contacto', '{"nombre": "Rigoberto", "email": "rigoberto@gmail.com", "mensaje": "Hola, presento una denuncia administrativa contra el encargado del website, que supongo es un webmaster, porque no sabe hacer nada, es un inútil.", "documento": "20220123204610_comenzamos.jpg"}', '2022-01-23 20:46:10'),
	(14, 'contacto', '{"nombre": "Alfa", "email": "official.dduran@gmail.com", "mensaje": "Mensaje alfa", "documento": null}', '2022-01-29 18:25:45'),
	(15, 'contacto', '{"nombre": "Alfa", "email": "official.dduran@gmail.com", "mensaje": "Mensaje alfa", "documento": null}', '2022-01-29 18:41:54'),
	(16, 'contacto', '{"nombre": "Rigoberto González", "email": "official.dduran@gmail.com", "mensaje": "Envío adjunto en JPG", "documento": "20220129185411_composer.jpg"}', '2022-01-29 18:54:11'),
	(17, 'contacto', '{"nombre": "Rongo", "email": "rongo@gmail.com", "mensaje": "Mensaje de Rongo. Viene adjunto una imagen JPG", "documento": "20220129190002_composer.jpg"}', '2022-01-29 19:00:02'),
	(18, 'contacto', '{"nombre": "Ronquero", "email": "ronquero@gmail.com", "mensaje": "Mensaje ronquero. Viene adjunto un archivo composer de las 7:05 pm.", "documento": "20220129190502_composer.jpg"}', '2022-01-29 19:05:02'),
	(19, 'contacto', '{"nombre": "Sandra Gómez", "email": "sandra@gmail.com", "mensaje": "Snadra envía un archivo en JPEG", "documento": "20220129193708_archivo.jpeg"}', '2022-01-29 19:37:08'),
	(20, 'contacto', '{"nombre": "Sandra Gómez", "email": "sandra@gmail.com", "mensaje": "Snadra envía un archivo en JPEG", "documento": "20220129194028_archivo.jpeg"}', '2022-01-29 19:40:28'),
	(21, 'contacto', '{"nombre": "Sandra Gómez", "email": "sandra@gmail.com", "mensaje": "Snadra envía un archivo en JPEG", "documento": "20220129194121_archivo.jpeg"}', '2022-01-29 19:41:21'),
	(22, 'contacto', '{"nombre": "Pensativo", "email": "pensativo@gmail.com", "mensaje": "Este mensaje lo envío desde mi iPhone. Adjunto un archivo en formato PNG, que es más pesado que un JPG.", "documento": "20220129195757_asombro.png"}', '2022-01-29 19:57:57'),
	(23, 'contacto', '{"nombre": "Ron", "email": "official.dduran@gmail.com", "mensaje": "Roño dice hola", "documento": "20220129204238_a.jpg"}', '2022-01-29 20:42:38'),
	(24, 'contacto', '{"nombre": "Saramiento", "email": "sarmiento@gmail.com", "mensaje": "Envío documento adjunto. En teoría debería deshabilitarse el botón submit después que validó el formulario.", "documento": "20220129204625_a.jpg"}', '2022-01-29 20:46:25');
/*!40000 ALTER TABLE `submissions` ENABLE KEYS */;

-- Volcando estructura para tabla pythonflaskcontactos.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contrasena` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rol` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla pythonflaskcontactos.users: ~18 rows (aproximadamente)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `nombre`, `email`, `contrasena`, `rol`, `created_at`, `updated_at`) VALUES
	(1, 'David', 'official.dduran@gmail.com', 'sha256$TAZT5tgw3YVYBtXF$a767459d6f9ff8cd4194307564ba80399d57a0ce712b64ca6f2e2bb87e666d00', 'viewer', '2021-09-12 17:07:00', '2022-02-07 14:28:16'),
	(2, 'Durán', 'official.dduran@yahoo.com', 'sha256$TAZT5tgw3YVYBtXF$a767459d6f9ff8cd4194307564ba80399d57a0ce712b64ca6f2e2bb87e666d00', 'admin', '2021-10-24 15:03:25', '2022-02-07 15:19:03'),
	(3, 'Ramírez', 'official-dduran@outlook.com', 'sha256$TAZT5tgw3YVYBtXF$a767459d6f9ff8cd4194307564ba80399d57a0ce712b64ca6f2e2bb87e666d00', 'autor', '2021-10-24 15:03:44', '2022-02-07 14:28:16'),
	(211, 'Ibero', 'webmaster02.dit@ibero.mx', 'sha256$TAZT5tgw3YVYBtXF$a767459d6f9ff8cd4194307564ba80399d57a0ce712b64ca6f2e2bb87e666d00', 'viewer', '2021-10-31 00:00:00', '2022-02-07 14:28:16'),
	(212, 'Georginas', 'e@gmail.com', '629151', 'autor', '2021-10-31 00:00:00', '2022-02-07 14:28:16'),
	(401, 'Georginas', 'f@gmail.com', '49B 5T4', 'autor', '2021-10-31 00:00:00', '2022-02-07 14:28:16'),
	(407, 'Georginas', 'g@gmail.com', '22706', 'autor', '2021-10-31 00:00:00', '2022-02-07 14:28:16'),
	(408, 'Georginas', 'h@gmail.com', '22244', 'autor', '2021-10-31 00:00:00', '2022-02-07 14:28:16'),
	(461, 'Georginas', 'i@gmail.com', '20413', 'autor', '2021-10-31 00:00:00', '2022-02-07 14:28:16'),
	(462, 'Georginas', 'j@gmail.com', '85401-42973', 'autor', '2021-10-31 00:00:00', '2022-02-07 14:28:16'),
	(504, 'Georginas', 'j@gmail.com', 'mefis-tofeles', 'autor', '2021-10-31 17:34:58', '2022-02-07 14:28:16'),
	(505, 'Georginas', 'k@gmail.com', '$2b$12$yCH/E0d9Ptyg8KcqHblTzOanN5MmbvHyT00x5Ak.gqfpW/Yo9ATdS', 'autor', '2021-11-07 19:37:29', '2022-02-07 14:28:16'),
	(506, 'Georginas', 'l@gmail.com', '$2b$12$gVs80Sfrt12YixCx/CV9auvkS.iJMc4P8kggIIEAnEYJKJyWmRMye', 'autor', '2021-11-07 19:45:44', '2022-02-07 14:28:16'),
	(507, 'Georginas', 'm@gmail.com', '$2b$12$r1wMaapiZ4z1alCP/0GPw.945u0AAxAfwjWBAugnyIBLjHjlnFi/S', 'autor', '2022-02-06 18:29:35', '2022-02-07 14:28:16'),
	(508, 'Georginas', 'o@gmail.com', 'sha256$Bdme80ashm6OYmrK$fced339a9fe7580b05375f234024ff334bf9b802483431deb96bbfe60514aca3', 'autor', '2022-02-07 11:49:19', '2022-02-07 14:28:16'),
	(509, 'Georginas', 'p@gmail.com', 'sha256$K2NqyDOMy8hGgnYX$c4ed6458e347261f61e11c5d24c74513c9aa7312a9f1c35e602382d05f61a2ae', 'autor', '2022-02-07 11:55:48', '2022-02-07 14:28:16'),
	(510, 'Ramiro', 'ramiro@gmail.com', 'sha256$5982e805a3fc3d62b08c9abd247e82cc2e3914a81e751f97423a7453e33f01ff', 'admin', '2022-02-07 14:51:46', '2022-02-07 14:58:51'),
	(511, 'Lastimonio', 'last@gmail.com', 'sha256$Ncoacv7B6PXEqUNT$abf2f61526c05cff374b46a11b2fa14c1a78a97f511bb7a6bb03b83bc4b79ebd', 'admin', '2022-02-07 16:14:36', '2022-02-07 16:16:46');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
