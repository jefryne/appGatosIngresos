-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 17-02-2024 a las 19:01:44
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `personal_finances`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `category`
--

CREATE TABLE `category` (
  `category_id` smallint(3) NOT NULL,
  `category_name` varchar(50) DEFAULT NULL,
  `category_description` varchar(120) DEFAULT NULL,
  `category_status` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `category`
--

INSERT INTO `category` (`category_id`, `category_name`, `category_description`, `category_status`) VALUES
(1, 'string', 'pepe', 1),
(2, 'plata', 'plata', 1),
(3, 'plata', 'plata', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tokens`
--

CREATE TABLE `tokens` (
  `token` char(180) NOT NULL,
  `user_id` char(30) DEFAULT NULL,
  `token_status` tinyint(1) DEFAULT 1,
  `token_created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `transactions`
--

CREATE TABLE `transactions` (
  `transactions_id` int(10) UNSIGNED NOT NULL,
  `user_id` char(30) DEFAULT NULL,
  `category_id` smallint(3) DEFAULT NULL,
  `amount` float(10,2) DEFAULT NULL,
  `t_description` varchar(120) DEFAULT NULL,
  `t_type` enum('revenue','expenses') DEFAULT NULL,
  `t_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `user_id` char(30) NOT NULL,
  `full_name` varchar(80) DEFAULT NULL,
  `mail` varchar(100) DEFAULT NULL,
  `passhash` varchar(140) DEFAULT NULL,
  `user_role` enum('admin','user') DEFAULT NULL,
  `user_status` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `update_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`user_id`, `full_name`, `mail`, `passhash`, `user_role`, `user_status`, `created_at`, `update_at`) VALUES
('3SRkTy0OxyZuBtRjgLioGAiIc8WfOw', 'carlos', 'carlos@example.com', '$2b$12$03SeTlin1FpAGgRvnQqc2ecJ20.c3KXK2Tpn9COX5NkQLa8tFjRGy', 'admin', 1, '2024-02-17 20:23:12', '2024-02-17 15:23:12'),
('hyotqwnH82jJbZevZansQhOdgjT7qA', 'jeffry', 'jeffry@gmail.com', '$2b$12$Iai1UBZA6ekTTFdgVCajz.YEa3QP3bxJJx9wW2L9wVKgrA890uqby', 'admin', 1, '2024-02-17 19:30:49', '2024-02-17 17:26:11'),
('nfaVdV6PNRTrlS3dTq2KayA3lpBYPd', 'pepa', 'pepa@gmail.com', '$2b$12$o8IyG5qS.TSR4BMpmPWZge8XEgOMe..xFK9GpqP6WX7Ms5x79ySjq', 'user', 1, '2024-02-17 19:31:21', '2024-02-17 17:27:15'),
('SUBeIbBCV1S6AFULl2lsP1Q47nMPI9', 'string', 'user@example.com', '$2b$12$jMVjxk7afAG9JZXPNnzsLeNR7lkSnuJl/bKXvjynXQdhT/w25/cDu', 'user', 1, '2024-02-17 20:22:16', '2024-02-17 15:22:16');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`category_id`);

--
-- Indices de la tabla `tokens`
--
ALTER TABLE `tokens`
  ADD PRIMARY KEY (`token`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`transactions_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `mail` (`mail`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `category`
--
ALTER TABLE `category`
  MODIFY `category_id` smallint(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `transactions`
--
ALTER TABLE `transactions`
  MODIFY `transactions_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tokens`
--
ALTER TABLE `tokens`
  ADD CONSTRAINT `tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Filtros para la tabla `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
