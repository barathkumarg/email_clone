-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 16, 2022 at 01:42 PM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `YJhCmVseWc`
--

-- --------------------------------------------------------

--
-- Table structure for table `receive_mail`
--

CREATE TABLE `receive_mail` (
  `id` int(100) NOT NULL,
  `receiver_mail` varchar(50) NOT NULL,
  `sender_mail` varchar(50) NOT NULL,
  `sender_name` varchar(100) NOT NULL,
  `subject` varchar(250) NOT NULL,
  `message` varchar(1000) NOT NULL,
  `attachment_link` varchar(300) DEFAULT NULL,
  `attachment_name` varchar(300) DEFAULT NULL,
  `date_time` varchar(100) NOT NULL,
  `starred` int(2) NOT NULL DEFAULT 0,
  `read_status` int(2) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sent_mail`
--

CREATE TABLE `sent_mail` (
  `id` int(100) NOT NULL,
  `sender_mail` varchar(50) NOT NULL,
  `receiver_mail` varchar(50) NOT NULL,
  `receiver_name` varchar(100) NOT NULL,
  `subject` varchar(250) NOT NULL,
  `message` varchar(1000) NOT NULL,
  `attachment_link` varchar(500) DEFAULT NULL,
  `attachment_name` varchar(300) DEFAULT NULL,
  `date_time` varchar(100) NOT NULL,
  `starred` int(2) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user_data`
--

CREATE TABLE `user_data` (
  `mail_id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `phone_no` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `receive_mail`
--
ALTER TABLE `receive_mail`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sent_mail`
--
ALTER TABLE `sent_mail`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `receive_mail`
--
ALTER TABLE `receive_mail`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sent_mail`
--
ALTER TABLE `sent_mail`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
