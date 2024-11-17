-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 17, 2024 at 02:55 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `integradora`
--

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `Id_coment` int(11) NOT NULL,
  `Punctuation` int(5) NOT NULL,
  `Comment` mediumtext NOT NULL,
  `FK_Id_customer` int(11) NOT NULL,
  `FK_Id_product` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`Id_coment`, `Punctuation`, `Comment`, `FK_Id_customer`, `FK_Id_product`) VALUES
(1, 5, 'Ta good', 39, 21),
(2, 5, 'Ta good', 39, 21),
(3, 1, 'a', 21, 20),
(4, 2, '2', 39, 21),
(5, 5, '5', 39, 21),
(6, 5, '5', 39, 21);

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
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
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`Id_contact`, `Facebook`, `Instagram`, `Tik_tok`, `Email`, `Twitter`, `Whatsapp`, `Phone`) VALUES
(1, 'https://www.facebook.com/blancosyconfeccionesdedurango', 'https://www.instagram.com/blancos_y_confecciones/', '', 'bcd_xcatalogo@yahoo.com.mx', '', '6181686644', '6188181814');

-- --------------------------------------------------------

--
-- Table structure for table `content`
--

CREATE TABLE `content` (
  `Id_contenido` int(11) NOT NULL,
  `Title` varchar(50) NOT NULL,
  `Describe` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `content`
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
-- Table structure for table `products`
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
-- Dumping data for table `products`
--

INSERT INTO `products` (`Id_product`, `Material_composition`, `Model`, `FK_id_season`, `Size`, `Name`, `Description`, `Price_per_unit`, `Color`, `url_imagen`, `FK_Id_user`) VALUES
(19, '1', 'gojo', 1, '1', '1', '1', 1, '1', 'gojo.png', 39),
(20, '1', 'tablet', 1, '1', '1', '1', 1, '1', 'tablet.png', 39),
(21, 'Energia', 'Satoru', 1, '25', 'Test', 'Prueba de registro con imagenes, y con datos un poco más realistas', 25, 'Azul azulado', 'Satoru.png', 39);

-- --------------------------------------------------------

--
-- Table structure for table `season_specification`
--

CREATE TABLE `season_specification` (
  `Id_season` int(11) NOT NULL,
  `season` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `season_specification`
--

INSERT INTO `season_specification` (`Id_season`, `season`) VALUES
(1, 'invierno'),
(10, 'primavera'),
(11, 'verano'),
(12, 'otoño');

-- --------------------------------------------------------

--
-- Table structure for table `users`
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
-- Dumping data for table `users`
--

INSERT INTO `users` (`Id_user`, `User`, `Password`, `Email`, `Name`, `Surname`, `Lastname`, `Rol`, `Estado`) VALUES
(21, 'testuser', 'cliente', 'cliente.hotmail.com', 'Test', 'User', 'Example', 'administrador', 'Inactivo'),
(39, 'admin', 'admin', 'admin@hotmail.com', 'Mario', 'a', 'z', 'administrador', 'Activo'),
(40, 'testuser', 'testpassword', 'testuser@example.com', 'Test', 'User', 'Example', 'cliente', 'Inactivo'),
(41, 'a', 'a', 'a@a', 'a', 'a', 'a', 'cliente', 'Activo');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`Id_coment`),
  ADD KEY `comments_ibfk_1` (`FK_Id_customer`),
  ADD KEY `FK_Id_product` (`FK_Id_product`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`Id_product`),
  ADD KEY `FK_id_season` (`FK_id_season`),
  ADD KEY `FK_Id_user` (`FK_Id_user`);

--
-- Indexes for table `season_specification`
--
ALTER TABLE `season_specification`
  ADD PRIMARY KEY (`Id_season`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`Id_user`),
  ADD KEY `FK_id_rol` (`Rol`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `Id_coment` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `Id_product` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `season_specification`
--
ALTER TABLE `season_specification`
  MODIFY `Id_season` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `Id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`FK_Id_customer`) REFERENCES `users` (`Id_user`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`FK_Id_product`) REFERENCES `products` (`Id_product`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `Products_ibfk_1` FOREIGN KEY (`FK_id_season`) REFERENCES `season_specification` (`Id_season`) ON DELETE CASCADE,
  ADD CONSTRAINT `Products_ibfk_2` FOREIGN KEY (`FK_Id_user`) REFERENCES `users` (`Id_user`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
