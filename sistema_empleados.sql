-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-12-2023 a las 21:22:22
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sistema1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sistema_empleados`
--

CREATE TABLE `sistema_empleados` (
  `id` int(10) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `foto` varchar(5000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sistema_empleados`
--

INSERT INTO `sistema_empleados` (`id`, `nombre`, `email`, `foto`) VALUES
(53, 'lee chown', 'leechown@flota.com', '2023171352lee.jpg'),
(54, 'Mark Sullivan', 'Sullivan@mtc.com', '2023170656teniente.jpg'),
(55, 'droid', 'droix@droid.com', '2023170727robot.jpg'),
(56, 'Peter swang', 'peter@loud.com', '2023170832Captura de pantalla 2023-12-09 150033.jpg'),
(57, 'azureneon', 'azure@mimm.com', '2023170919cazador.jpg'),
(58, 'alina korg', 'aline@mtx.com', '2023170950Alina.jpg');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `sistema_empleados`
--
ALTER TABLE `sistema_empleados`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `sistema_empleados`
--
ALTER TABLE `sistema_empleados`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
