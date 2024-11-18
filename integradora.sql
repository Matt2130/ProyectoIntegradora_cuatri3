-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-11-2024 a las 01:56:20
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `integradora`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comments`
--

CREATE TABLE `comments` (
  `Id_coment` int(11) NOT NULL,
  `Punctuation` double NOT NULL,
  `Comment` mediumtext NOT NULL,
  `FK_Id_customer` int(11) NOT NULL,
  `FK_Id_product` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comments`
--

INSERT INTO `comments` (`Id_coment`, `Punctuation`, `Comment`, `FK_Id_customer`, `FK_Id_product`) VALUES
(1, 1, '1', 39, 21),
(2, 1, '1', 39, 21),
(3, 1, '1', 39, 21),
(4, 5, 'Ta guapo', 21, 21);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contacts`
--

CREATE TABLE `contacts` (
  `Id_contact` int(11) NOT NULL,
  `Facebook` varchar(2100) NOT NULL,
  `Instagram` varchar(2100) NOT NULL,
  `Tik_tok` varchar(2100) NOT NULL,
  `Email` varchar(320) NOT NULL,
  `Twitter` varchar(2100) NOT NULL,
  `Whatsapp` varchar(30) NOT NULL,
  `Phone` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `contacts`
--

INSERT INTO `contacts` (`Id_contact`, `Facebook`, `Instagram`, `Tik_tok`, `Email`, `Twitter`, `Whatsapp`, `Phone`) VALUES
(1, 'https://www.facebook.com/blancosyconfeccionesdedurango', 'https://www.instagram.com/blancos_y_confecciones/', '', 'bcd_xcatalogo@yahoo.com.mx', '', '6181686644', '6188181814');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `content`
--

CREATE TABLE `content` (
  `Id_contenido` int(11) NOT NULL,
  `Title` varchar(50) NOT NULL,
  `Describe` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `content`
--

INSERT INTO `content` (`Id_contenido`, `Title`, `Describe`) VALUES
(1, 'Misión', 'Mantener al alcance de todos los mejores artículos de blancos, renovando los inventarios en cada temporada para ofrecer lo más novedoso y garantizar la satisfacción de nuestros clientes.'),
(2, 'Visión', 'Ser reconocidos como el líder nacional en productos de blancos que proporcionen confort, calidez y durabilidad, destacándonos por nuestra calidad e innovación.'),
(3, 'Acerca de nosotros', 'Blancos y Confecciones de Durango se distingue por ofrecer a sus clientes una amplia variedad de productos de reconocidas marcas como Íntima, Vianney, Elefantito, Esquimal, Regina, Selene, Chiquimundo, y Dormi Real.\r\n\r\nLa sucursal de venta por catálogo, que es el foco de este proyecto, está orientada a la venta al mayoreo, actuando como proveedor para revendedores de productos de blancos. La empresa busca mantenerse como un socio confiable para aquellos que desean comercializar estos productos, brindando un programa de afiliación especial para mayoristas con beneficios exclusivos.'),
(5, 'Historia', 'Blancos y Confecciones de Durango fue fundada en 1979 por el señor José De Jesús Malacara Alonso. Su visión era ofrecer productos de blancos de alta calidad a un público amplio, lo que llevó a la empresa a expandirse en su momento a los estados de Coahuila y Chihuahua.\r\n\r\nEn el año 2005, la empresa dio un giro significativo al abrir su sucursal de venta por catálogo, dirigida por Jeanette Malacara Ibarra. Esta sucursal comenzó en un pequeño local con la representación de apenas tres marcas y un inventario limitado. Con el paso del tiempo, la sucursal fue ampliando tanto su catálogo de productos como sus acuerdos con los proveedores, logrando en la actualidad trabajar con más de diez marcas reconocidas en el mercado.'),
(6, 'Valores', 'Honestidad\r\nRespeto\r\nServicio\r\nAmabilidad'),
(7, 'Objetivos', 'Blancos y Confecciones de Durango S.A. de C.V. tiene el objetivo de tener a la disposición de nuestros clientes la mejor variedad de blancos para el hogar y de la mejor calidad. Ofreciendo los mejores precios y mayores beneficios para toda nuestra comunidad.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `products`
--

CREATE TABLE `products` (
  `Id_product` int(11) NOT NULL,
  `Material_composition` varchar(50) NOT NULL,
  `Model` varchar(100) NOT NULL,
  `FK_id_season` int(11) NOT NULL,
  `Size` varchar(50) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Description` varchar(500) NOT NULL,
  `Price_per_unit` double NOT NULL,
  `Color` varchar(50) NOT NULL,
  `url_imagen` tinytext NOT NULL,
  `FK_Id_user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`Id_product`, `Material_composition`, `Model`, `FK_id_season`, `Size`, `Name`, `Description`, `Price_per_unit`, `Color`, `url_imagen`, `FK_Id_user`) VALUES
(19, '1', 'gojo', 1, '1', '1', '1', 1, '1', 'gojo.png', 39),
(20, '2', '4', 12, '5', '61', '71', 8, '9', 'tablet.png', 21),
(21, 'Energia', 'Satoru', 1, '25', 'Test', 'Prueba de registro con imagenes, y con datos un poco más realistas', 25, 'Azul azulado', 'Satoru.png', 39),
(25, 'bits', 'hola', 1, '25', 'Mario', 'xcvbcfgb', 50, 'red', 'hola.png', 39),
(26, '5', '5', 1, '5', '5', '5', 5, '5', '5.png', 39),
(27, '0', '10', 10, '1', '01', '0', 10, '1', '10.png', 39),
(28, '10', '10', 10, '10', '10', '10', 10, '10', '10.png', 39),
(29, '0', 'asd', 10, '10', '10', '10', 10, '1', 'asd.png', 39);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `season_specification`
--

CREATE TABLE `season_specification` (
  `Id_season` int(11) NOT NULL,
  `season` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `season_specification`
--

INSERT INTO `season_specification` (`Id_season`, `season`) VALUES
(1, 'invierno'),
(10, 'primavera'),
(11, 'verano'),
(12, 'otoño');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `Id_user` int(11) NOT NULL,
  `User` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Email` varchar(150) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Surname` varchar(25) NOT NULL,
  `Lastname` varchar(25) NOT NULL,
  `Rol` varchar(25) NOT NULL,
  `Estado` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`Id_user`, `User`, `Password`, `Email`, `Name`, `Surname`, `Lastname`, `Rol`, `Estado`) VALUES
(21, 'testuser', 'cliente', 'cliente@hotmail.com', 'Test', 'User', 'Example', 'cliente', 'Inactivo'),
(39, 'admin', 'admin', 'admin@hotmail.com', 'Mario', 'a', 'z', 'administrador', 'Activo'),
(40, 'testuser', 'testpassword', 'testuser@example.com', 'Test', 'User', 'Example', 'cliente', 'Inactivo');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`Id_coment`);

--
-- Indices de la tabla `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`Id_contact`);

--
-- Indices de la tabla `content`
--
ALTER TABLE `content`
  ADD PRIMARY KEY (`Id_contenido`);

--
-- Indices de la tabla `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`Id_product`),
  ADD KEY `FK_id_season` (`FK_id_season`),
  ADD KEY `FK_Id_user` (`FK_Id_user`);

--
-- Indices de la tabla `season_specification`
--
ALTER TABLE `season_specification`
  ADD PRIMARY KEY (`Id_season`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`Id_user`),
  ADD KEY `FK_id_rol` (`Rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `comments`
--
ALTER TABLE `comments`
  MODIFY `Id_coment` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `contacts`
--
ALTER TABLE `contacts`
  MODIFY `Id_contact` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `content`
--
ALTER TABLE `content`
  MODIFY `Id_contenido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `products`
--
ALTER TABLE `products`
  MODIFY `Id_product` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `season_specification`
--
ALTER TABLE `season_specification`
  MODIFY `Id_season` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `Id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `Products_ibfk_1` FOREIGN KEY (`FK_id_season`) REFERENCES `season_specification` (`Id_season`) ON DELETE CASCADE,
  ADD CONSTRAINT `Products_ibfk_2` FOREIGN KEY (`FK_Id_user`) REFERENCES `users` (`Id_user`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
