-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-11-2024 a las 03:42:35
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

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `buscar_temporadas` (IN `buscar` VARCHAR(255), IN `limit_val` INT, IN `offset_val` INT)   BEGIN
    SELECT season_specification.season, season_specification.Id_season
    FROM season_specification
    WHERE season_specification.season LIKE buscar
    LIMIT limit_val OFFSET offset_val;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `buscar_usuarios` (IN `buscar` VARCHAR(255), IN `limit_val` INT, IN `offset_val` INT)   BEGIN
    SELECT 
        User, Email, Name, Surname, Lastname, Rol, Id_user
    FROM users
    WHERE 
        User LIKE buscar
        OR Email LIKE buscar
        OR Name LIKE buscar
        OR Surname LIKE buscar
        OR Lastname LIKE buscar
        OR Rol LIKE buscar
        OR Estado LIKE buscar
    LIMIT limit_val OFFSET offset_val;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `contar_clientes` (OUT `total_clientes` INT)   BEGIN
    SELECT COUNT(*) INTO total_clientes
    FROM users
    WHERE users.Rol = 'cliente';
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `contar_productos` (IN `buscar` VARCHAR(255))   BEGIN
    SELECT COUNT(*) 
    FROM products
    WHERE Model LIKE buscar 
       OR Size LIKE buscar 
       OR Name LIKE buscar 
       OR Description LIKE buscar 
       OR Color LIKE buscar;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `contar_temporadas` (IN `buscar` VARCHAR(255))   BEGIN
    SELECT COUNT(*) 
    FROM season_specification
    WHERE season_specification.season LIKE buscar;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `contar_usuarios` (IN `buscar` VARCHAR(255))   BEGIN
    SELECT COUNT(*) 
    FROM users
    WHERE 
        User LIKE buscar
        OR Email LIKE buscar
        OR Name LIKE buscar
        OR Surname LIKE buscar
        OR Lastname LIKE buscar
        OR Rol LIKE buscar
        OR Estado LIKE buscar;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `CountProducts` (IN `buscar` VARCHAR(255))   BEGIN
    SELECT COUNT(*) 
    FROM products
    INNER JOIN season_specification ON products.FK_id_season = season_specification.Id_season
    INNER JOIN users ON products.FK_Id_user = users.Id_user
    WHERE 
        products.Model LIKE buscar OR
        season_specification.season LIKE buscar OR
        products.Size LIKE buscar OR
        products.Name LIKE buscar OR
        products.Description LIKE buscar OR
        products.Price_per_unit LIKE buscar OR
        products.Color LIKE buscar OR
        users.User LIKE buscar;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetProducts` (IN `buscar` VARCHAR(255), IN `limit_param` INT, IN `offset_param` INT)   BEGIN
    SELECT 
        products.Name, 
        products.Model, 
        products.Size, 
        products.Material_composition, 
        products.Price_per_unit, 
        products.Color, 
        products.Id_product
    FROM 
        products
    INNER JOIN season_specification ON products.FK_id_season = season_specification.Id_season
    INNER JOIN users ON products.FK_Id_user = users.Id_user
    WHERE 
        products.Model LIKE buscar OR
        season_specification.season LIKE buscar OR
        products.Size LIKE buscar OR
        products.Name LIKE buscar OR
        products.Description LIKE buscar OR
        products.Price_per_unit LIKE buscar OR
        products.Color LIKE buscar OR
        users.User LIKE buscar
    LIMIT limit_param OFFSET offset_param;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `obtener_comentario_reciente` (OUT `puntuacion` INT, OUT `comentario` TEXT, OUT `producto_nombre` VARCHAR(255), OUT `producto_id` INT)   BEGIN
    SELECT 
        comments.Punctuation, 
        comments.Comment, 
        products.Name, 
        products.Id_product
    INTO 
        puntuacion, 
        comentario, 
        producto_nombre, 
        producto_id
    FROM comments
    INNER JOIN products ON comments.FK_Id_product = products.Id_product
    WHERE comments.Id_coment = (SELECT MAX(Id_coment) FROM comments);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `obtener_conteo_comentarios_por_puntuacion` ()   BEGIN
    SELECT 
        comments.Punctuation, 
        COUNT(*) AS NumComments
    FROM 
        comments
    WHERE 
        comments.Punctuation BETWEEN 1 AND 5  -- Asegura que las puntuaciones sean entre 1 y 5
    GROUP BY 
        comments.Punctuation;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `obtener_productos` (IN `buscar` VARCHAR(255), IN `categoria` VARCHAR(255), IN `limit_val` INT, IN `offset_val` INT)   BEGIN
    CASE 
        WHEN categoria = 'Model' THEN
            SELECT url_imagen, Name, Color, Price_per_unit, Id_product
            FROM products 
            WHERE Model LIKE buscar 
            LIMIT limit_val OFFSET offset_val;
        WHEN categoria = 'Size' THEN
            SELECT url_imagen, Name, Color, Price_per_unit, Id_product
            FROM products 
            WHERE Size LIKE buscar 
            LIMIT limit_val OFFSET offset_val;
        WHEN categoria = 'Name' THEN
            SELECT url_imagen, Name, Color, Price_per_unit, Id_product
            FROM products 
            WHERE Name LIKE buscar 
            LIMIT limit_val OFFSET offset_val;
        WHEN categoria = 'Description' THEN
            SELECT url_imagen, Name, Color, Price_per_unit, Id_product
            FROM products 
            WHERE Description LIKE buscar 
            LIMIT limit_val OFFSET offset_val;
        WHEN categoria = 'Color' THEN
            SELECT url_imagen, Name, Color, Price_per_unit, Id_product
            FROM products 
            WHERE Color LIKE buscar 
            LIMIT limit_val OFFSET offset_val;
        ELSE
            SELECT 'Error: Categoría no válida' AS Error;
    END CASE;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `obtener_producto_reciente` (OUT `producto_nombre` VARCHAR(255))   BEGIN
    SELECT Name 
    INTO producto_nombre
    FROM products 
    WHERE Id_product = (SELECT MAX(Id_product) FROM products);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `obtener_promedio_productos` ()   BEGIN
    SELECT 
        products.Name, 
        products.Id_product, 
        products.url_imagen, 
        IFNULL(AVG(comments.Punctuation), 0) AS AvgPunctuation  -- Reemplazar NULL por 0
    FROM 
        products
    LEFT JOIN 
        comments ON comments.FK_Id_product = products.Id_product
    GROUP BY 
        products.Name, products.Id_product, products.url_imagen
    HAVING 
        AvgPunctuation > 0  -- Opcional: Filtrar productos sin puntuación válida
    ORDER BY 
        AvgPunctuation DESC;
END$$

DELIMITER ;

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
(5, 5, '', 56, 32),
(6, 4, 'Es muy comodo', 56, 33),
(7, 2, '', 54, 34),
(8, 4, '', 54, 61);

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
(32, '', 'Edre-Cobertor Aire Chocolat Regina® Nuvó.', 1, 'Matrimonial', 'Edre-Cobertor Aire Chocolat, Regina® Nuvó.', 'Edre-Cobertor Aire Chocolat, Regina® Nuvó.\r\nNuevo Reverso Jacquard!!\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nNúmero 1 en diseño.\r\n\r\nAltamente térmico.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto', 749, 'rosa', 'Edre-Cobertor Aire Chocolat Regina® Nuvó..png', 54),
(33, '', 'Edre-Cobertor Amo Viajar Regina® Nuvó.', 1, 'Matrimonial', 'Edre-Cobertor Amo Viajar, Regina® Nuvó.', 'Edre-Cobertor Amo Viajar, Regina® Nuvó.\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nNúmero 1 en diseño.\r\n\r\nAltamente térmico.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto tu hogar.\r\n\r\nMatrimonial: 18', 749, 'Negro', 'Edre-Cobertor Amo Viajar Regina® Nuvó..png', 54),
(34, '', 'Edre-Cobertor Carrera Ultra Regina® Nuvó.', 1, 'Matrimonial', 'Edre-Cobertor Carrera Ultra Regina® Nuvó.', 'Edre-Cobertor Carrera Ultra, Regina® Nuvó.\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nNúmero 1 en diseño.\r\n\r\nAltamente térmico.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto tu hogar.\r\n\r\nMatrimonial:', 749, 'azul', 'Edre-Cobertor Carrera Ultra Regina® Nuvó..png', 54),
(35, '', 'Edre-Cobertor Collins Cielo Regina® Nuvó.', 1, 'KingSize', 'Edre-Cobertor Collins Cielo Regina® Nuvó.', 'Edre-Cobertor Collins Cielo, Regina® Nuvó.\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nNúmero 1 en diseño.\r\n\r\nAltamente térmico.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto tu hogar.\r\n\r\nMatrimonial:', 1013, 'Azul', 'Edre-Cobertor Collins Cielo Regina® Nuvó..png', 54),
(36, '', 'Edre-Cobertor Collins Copper Regina® Nuvó.', 1, 'KingSize', 'Edre-Cobertor Collins Copper Regina® Nuvó.', 'Edre-Cobertor Collins Copper, Regina® Nuvó.\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nNúmero 1 en diseño.\r\n\r\nAltamente térmico.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto tu hogar.\r\n\r\nMatrimonial', 1013, 'rojo', 'Edre-Cobertor Collins Copper Regina® Nuvó..png', 54),
(37, '', 'Edre-Cobertor Francis Amanecer Regina® Nuvó.', 1, 'Matrimonial', 'Edre-Cobertor Francis Amanecer Regina® Nuvó.', 'Edre-Cobertor Francis Amanecer, Regina® Nuvó.\r\n Tres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nNúmero 1 en diseño.\r\n\r\nAltamente térmico.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto tu hogar.\r\n\r\nMatrimon', 1013, 'rojo', 'Edre-Cobertor Francis Amanecer Regina® Nuvó..png', 54),
(38, '', 'Edre-Cobertor Glassé Regina® Nuvó.', 1, 'KingSize', 'Edre-Cobertor Glassé Regina® Nuvó.', 'Edre-Cobertor Glassé, Regina® Nuvó.\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nNúmero 1 en diseño.\r\n\r\nAltamente térmico.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.  \r\n\r\n Tres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto tu hogar.\r\n\r\nMatrimonial: 180', 1013, 'rojo', 'Edre-Cobertor Glassé Regina® Nuvó..png', 54),
(39, '', 'Edre-cobertor Global Regina® Nuvó.', 1, 'Matrimonial', 'Edre-cobertor Global Regina® Nuvó.', 'Edre-Cobertor Global, Regina® Nuvó.\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado especial.\r\n\r\n¡Máxima calidad que combina telas ultra-suaves y abrigadoras!\r\n\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto tu hogar.\r\n\r\nMatrimonial: 180 cm x 220 cm.\r\n\r\nKing S', 749, 'azul', 'Edre-cobertor Global Regina® Nuvó..png', 54),
(40, '', 'Edre-Cobertor Hermosa Regina® Nuvó.', 1, 'Matrimonial', 'Edre-Cobertor Hermosa Regina® Nuvó.', 'Edre-Cobertor Hermosa, Regina® Nuvó.\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nNúmero 1 en diseño.\r\n\r\nAltamente térmico.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.  \r\n\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto tu hogar.\r\n\r\nMatrimonial: 180', 749, 'rosa', 'Edre-Cobertor Hermosa Regina® Nuvó..png', 54),
(41, '', 'Edre-Cobertor Zoom Zoom Regina® Nuvó.', 1, 'Matrimonial', 'Edre-Cobertor Zoom Zoom Regina® Nuvó.', 'Edre-Cobertor Zoom Zoom, Regina® Nuvó.\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nNúmero 1 en diseño.\r\n\r\nAltamente térmico.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.   \r\n\r\n \r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto tu hogar.\r\n\r\nMatrimonia', 749, 'azul', 'Edre-Cobertor Zoom Zoom Regina® Nuvó..png', 54),
(42, '', 'Edre-Cobertor Vortex Ginger Regina® Nuvó.', 1, 'Matrimonial', 'Edre-Cobertor Vortex Ginger Regina® Nuvó.', 'Edre-Cobertor Vortex Ginger, Regina® Nuvó.\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nNúmero 1 en diseño.\r\n\r\nAltamente térmico.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nTres capas de fina tela con reverso de borrega o doble vista.\r\n\r\nCapitonado en toda la pieza para asegurar mayor durabilidad.\r\n\r\nMáxima calidad que combina telas ultra-suaves y abrigadoras. Gran variedad de diseños exclusivos que decoran con muy buen gusto tu hogar.\r\n\r\nMatrimonial:', 749, 'rojo', 'Edre-Cobertor Vortex Ginger Regina® Nuvó..png', 54),
(43, '', 'Edredón Luxus Ondina', 1, 'Matrimonial Jumbo', 'Edredón Luxus Ondina', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Años después, seguimos innovando nuestras fibras y procesos para ofrecerte los mejores edredones y cobertores del país. A lo largo del tiempo, Esquimal ha desarrollado diferentes y novedosos estilos para su línea Luxus, reinventándose continuamente para estar a la vanguardia en tendencias de moda, estilo y tecnología.\r\n\r\nNuestro Edredón Odina forma parte de nuestra línea de productos Luxus. Por medi', 1499, 'Beige', 'Edredón Luxus Ondina.png', 54),
(44, '', 'Edredón Luxus Seneca', 1, 'Matrimonial Jumbo', 'Edredón Luxus Seneca', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Años después, seguimos innovando nuestras fibras y procesos para ofrecerte los mejores edredones y cobertores del país. A lo largo del tiempo, Esquimal ha desarrollado diferentes y novedosos estilos para su línea Luxus, reinventándose continuamente para estar a la vanguardia en tendencias de moda, estilo y tecnología.\r\n\r\nNuestro Edredón Seneca forma parte de nuestra línea de productos Luxus. Por med', 1499, 'olivo', 'Edredón Luxus Seneca.png', 54),
(45, '', 'Edredón Luxus Jazz', 1, 'Matrimonial Jumbo', 'Edredón Luxus Jazz', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Años después, seguimos innovando nuestras fibras y procesos para ofrecerte los mejores edredones y cobertores del país. A lo largo del tiempo, Esquimal ha desarrollado diferentes y novedosos estilos para su línea Luxus, reinventándose continuamente para estar a la vanguardia en tendencias de moda, estilo y tecnología.\r\n\r\nNuestro Edredón Jazz forma parte de nuestra línea de productos Luxus. Su intere', 1949, 'azul', 'Edredón Luxus Jazz.png', 54),
(46, '', 'Edredón Luxus Oliver', 1, 'Matrimonial Jumbo', 'Edredón Luxus Oliver', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Años después, seguimos innovando nuestras fibras y procesos para ofrecerte los mejores edredones y cobertores del país. A lo largo del tiempo, Esquimal ha desarrollado diferentes y novedosos estilos para su línea Luxus, reinventándose continuamente para estar a la vanguardia en tendencias de moda, estilo y tecnología.\r\n\r\nNuestro Edredón Oliver forma parte de nuestra línea de productos Luxus. Su inte', 1949, 'Negro', 'Edredón Luxus Oliver.png', 54),
(47, '', 'Edredón Luxus Ampera', 1, 'Matrimonial Jumbo', 'Edredón Luxus Ampera', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Años después, seguimos innovando nuestras fibras y procesos para ofrecerte los mejores edredones y cobertores del país. A lo largo del tiempo, Esquimal ha desarrollado diferentes y novedosos estilos para su línea Luxus, reinventándose continuamente para estar a la vanguardia en tendencias de moda, estilo y tecnología.\r\n\r\nNuestro Edredón Ampera forma parte de nuestra línea de productos Luxus. Abrigat', 1649, 'rosa', 'Edredón Luxus Ampera.png', 54),
(48, '', 'Edredón Luxus Euskadi', 1, 'Matrimonial Jumbo', 'Edredón Luxus Euskadi', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Años después, seguimos innovando nuestras fibras y procesos para ofrecerte los mejores edredones y cobertores del país. A lo largo del tiempo, Esquimal ha desarrollado diferentes y novedosos estilos para su línea Luxus, reinventándose continuamente para estar a la vanguardia en tendencias de moda, estilo y tecnología.\r\n\r\nNuestro Edredón Euskadi forma parte de nuestra línea de productos Luxus. Sorpré', 1799, 'gris', 'Edredón Luxus Euskadi.png', 54),
(49, '', 'Edredón Luxus Merino', 1, 'Matrimonial Jumbo', 'Edredón Luxus Merino', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Años después, seguimos innovando nuestras fibras y procesos para ofrecerte los mejores edredones y cobertores del país. A lo largo del tiempo, Esquimal ha desarrollado diferentes y novedosos estilos para su línea Luxus, reinventándose continuamente para estar a la vanguardia en tendencias de moda, estilo y tecnología.\r\n\r\nNuestro Edredón Merino forma parte de nuestra línea de productos Luxus. Por med', 1799, 'Beige', 'Edredón Luxus Merino.png', 54),
(50, '', 'Edredón Luxus Masaru', 1, 'Matrimonial Jumbo', 'Edredón Luxus Masaru', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Años después, seguimos innovando nuestras fibras y procesos para ofrecerte los mejores edredones y cobertores del país. A lo largo del tiempo, Esquimal ha desarrollado diferentes y novedosos estilos para su línea Luxus, reinventándose continuamente para estar a la vanguardia en tendencias de moda, estilo y tecnología.\r\n\r\nNuestro Edredón Masaru forma parte de nuestra línea de productos Luxus. Sorprén', 2099, 'cafe', 'Edredón Luxus Masaru.png', 54),
(51, '', 'Edredón Luxus Vivian', 1, 'Matrimonial Jumbo', 'Edredón Luxus Vivian', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Años después, seguimos innovando nuestras fibras y procesos para ofrecerte los mejores edredones y cobertores del país. A lo largo del tiempo, Esquimal ha desarrollado diferentes y novedosos estilos para su línea Luxus, reinventándose continuamente para estar a la vanguardia en tendencias de moda, estilo y tecnología.\r\n\r\nNuestro Edredón Vivian forma parte de nuestra línea de productos Luxus. Combina', 1499, 'Morado', 'Edredón Luxus Vivian.png', 54),
(52, '', 'Edredón Luxus Vivian', 1, 'Matrimonial Jumbo', 'Edredón Luxus Vivian', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Años después, seguimos innovando nuestras fibras y procesos para ofrecerte los mejores edredones y cobertores del país. A lo largo del tiempo, Esquimal ha desarrollado diferentes y novedosos estilos para su línea Luxus, reinventándose continuamente para estar a la vanguardia en tendencias de moda, estilo y tecnología.\r\n\r\nNuestro Edredón Vivian forma parte de nuestra línea de productos Luxus. Combina', 1499, 'Morado', 'Edredón Luxus Vivian.png', 54),
(53, '', 'Edredón Premium Kaia', 1, 'Matrimonial Jumbo', 'Edredón Premium Kaia', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Además de ser los primeros, año tras año seguimos mejorando nuestras fibras y procesos para brindarte los mejores edredones y cobertores del país, con los mejores diseños y más avanzadas técnicas de fabricación.\r\n\r\nEl Edredón Premium Kaia es parte de nuestra exitosa línea de calidad PREMIUM. Se desarrolló para ser el edredón más grueso, suave y durable de todos los del país. Es el único en México co', 1199, 'Naranja', 'Edredón Premium Kaia.png', 54),
(54, '', 'Edredón Premium Asper', 1, 'Matrimonial Jumbo', 'Edredón Premium Asper', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Además de ser los primeros, año tras año seguimos mejorando nuestras fibras y procesos para brindarte los mejores edredones y cobertores del país, con los mejores diseños y más avanzadas técnicas de fabricación.\r\n\r\nEl Edredón Premium Asper es parte de nuestra exitosa línea de calidad PREMIUM. Se desarrolló para ser el edredón más grueso, suave y durable de todos los del país. Es el único en México c', 1349, 'negro', 'Edredón Premium Asper.png', 54),
(55, '', 'Edredón Premium Ego', 1, 'Matrimonial Jumbo', 'Edredón Premium Ego', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Además de ser los primeros, año tras año seguimos mejorando nuestras fibras y procesos para brindarte los mejores edredones y cobertores del país, con los mejores diseños y más avanzadas técnicas de fabricación.\r\n\r\nEl Edredón Premium Ego es parte de nuestra exitosa línea de calidad PREMIUM. Se desarrolló para ser el edredón más grueso, suave y durable de todos los del país. Es el único en México con', 1499, 'Negro', 'Edredón Premium Ego.png', 54),
(56, '', 'Edredón Premium Semilla', 1, 'Matrimonial Jumbo', 'Edredón Premium Semilla', '¿Sabías que Esquimal fue la primera marca en ofrecer edredones y cobertores de borrega en México? Además de ser los primeros, año tras año seguimos mejorando nuestras fibras y procesos para brindarte los mejores edredones y cobertores del país, con los mejores diseños y más avanzadas técnicas de fabricación.\r\n\r\nEl Edredón Premium Semilla es parte de nuestra exitosa línea de calidad PREMIUM. Se desarrolló para ser el edredón más grueso, suave y durable de todos los del país. Es el único en México', 1169, 'Verde', 'Edredón Premium Semilla.png', 54),
(57, '', 'Cobertor Borrega Bartolomé', 1, 'Individual', 'Cobertor Borrega Bartolomé', 'Esquimal se caracteriza por siempre ofrecer la mejor calidad y variedad en cobertores invernales. Nuestro Cobertor Borrega Bartolomé está confeccionado con dos capas de tela de borrega estampada con modernos patrones geométricos a dos tonos en su frente y teñida en su reverso. ¡Ninguno se deslava! Su orilla está sobrehilada con hilo grueso de algodón, dándole una apariencia ligera a pesar de su grosor.\r\n\r\n\r\n¿Por qué es extraordinario?\r\n\r\nSúper precio.\r\nTela frontal de borrega estampada.\r\nTecnolo', 929, 'beige', 'Cobertor Borrega Bartolomé.png', 54),
(58, '', 'Cobertor Luxus Felisa', 1, 'Individual', 'Cobertor Luxus Felisa', 'Esquimal se caracteriza por siempre ofrecer la mejor calidad y variedad en cobertores invernales. Nuestro Cobertor Luxus Felisa está confeccionado con tela tipo piel y está texturizado con acabado rasurado. Su diseño es contemporáneo y sobrio, ideal para tus espacios elegantes.\r\n\r\n\r\n¿Por qué es extraordinario?\r\n\r\nSúper precio.\r\nTela frontal con acabado tipo piel y acabado rasurado.\r\nReverso de tela plus de alta calidad rosa.\r\nTecnología Termofabric.\r\nNivel de calidez: Media.', 1199, 'Rosa', 'Cobertor Luxus Felisa.png', 54),
(59, '', 'ALASKA BEIGE', 12, 'Matrimonial', 'ALASKA BEIGE', 'Cobertor ligero Alaska, de increíble diseño para un descanso cálido y suave.\r\n\r\nAtributos:\r\n– Color: beige.\r\n– Muy suave al contacto.\r\n– Cobertor ligero de microfibra.\r\n– Reverso de borrega.\r\n– Hipoalergénico.\r\n– Hecho en México.\r\n– Capitonado.\r\n– Fácil almacenamiento.\r\n– De fácil lavado en casa, a máquina. No usar blanqueador. Tender a la sombra sobre una superficie plana.', 349, 'cafe', 'ALASKA BEIGE.png', 54),
(60, '', 'ALASKA GRIS', 12, 'Matrimonial', 'ALASKA GRIS', 'Cobertor ligero Alaska, de increíble diseño para un descanso cálido y suave.\r\n\r\nAtributos:\r\n– Color: Gris.\r\n– Muy suave al contacto.\r\n– Cobertor ligero de microfibra.\r\n– Reverso de borrega.\r\n– Hipoalergénico.\r\n– Hecho en México.\r\n– Capitonado.\r\n– Fácil almacenamiento.\r\n– De fácil lavado en casa, a máquina. No usar blanqueador. Tender a la sombra sobre una superficie plana.', 349, 'gris', 'ALASKA GRIS.png', 54),
(61, '', 'ALBERTA', 12, 'Matrimonial', 'ALBERTA', 'Bello cobertor ligero Alberta, con diseño de rayas muy bonito para decorar tu recámara y para tener un descanso cálido y suave.\r\n\r\nAtributos:\r\n– Color gris\r\n– Diseño a rayas\r\n– Muy suave al contacto\r\n– Cobertor ligero de microfibra\r\n– Reverso de borrega\r\n– Hipoalergénico\r\n– Hecho en México\r\n– Capitonado\r\n– Fácil almacenamiento\r\n– De fácil lavado en casa, a máquina. No usar blanqueador. Tender a la sombra sobre una superficie plana', 399, 'gris', 'ALBERTA.png', 54);

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
  `Password` varchar(1000) NOT NULL,
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
(54, 'a', 'pbkdf2:sha256:600000$qdR0fJ74gu39ta2u$727ca8e7b8060804bdf8e1d9f93c972c8ae6ca822e0bc92a9b3c8c8885b8315d', 'mario@gmail.com', 'a', 'a', 'a', 'administrador', 'Activo'),
(55, 'b', 'pbkdf2:sha256:600000$LKwiSGE4slUlcYsT$5227b12a6be4603ff47c7230646c259466c7008430a7e70ea8dac5ea3bf8dd8b', 'Manuel@gmail.com', 'b', 'b', 'b', 'administrador', 'Activo'),
(56, 't', 'pbkdf2:sha256:600000$FQSCsQb2o1BYOckG$86d20d403383e98627d166dbd18b5b88c348c0163e56b6922c2d694e8653b345', 'test@gmail.com', 'test', 't', 't', 'cliente', 'Activo');

--
-- Disparadores `users`
--
DELIMITER $$
CREATE TRIGGER `verificar_admin` BEFORE DELETE ON `users` FOR EACH ROW BEGIN
    IF OLD.Rol = 'Administrador' THEN
        IF (SELECT COUNT(*) FROM users WHERE Rol = 'Administrador' AND Id_user != OLD.Id_user) = 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No puedes eliminar este usuario porque debe existir al menos un administrador.';
        END IF;
    END IF;
END
$$
DELIMITER ;

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
  MODIFY `Id_coment` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `contacts`
--
ALTER TABLE `contacts`
  MODIFY `Id_contact` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `content`
--
ALTER TABLE `content`
  MODIFY `Id_contenido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `products`
--
ALTER TABLE `products`
  MODIFY `Id_product` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT de la tabla `season_specification`
--
ALTER TABLE `season_specification`
  MODIFY `Id_season` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `Id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

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
