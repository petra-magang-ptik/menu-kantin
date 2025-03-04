-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 03, 2025 at 04:47 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kantin`
--

-- --------------------------------------------------------

--
-- Table structure for table `kantin`
--

CREATE TABLE `kantin` (
  `id` int(11) NOT NULL,
  `Gedung` varchar(255) DEFAULT NULL,
  `Nama_Stall` varchar(255) DEFAULT NULL,
  `Nama_Produk` varchar(255) DEFAULT NULL,
  `Harga` decimal(10,2) DEFAULT NULL,
  `Keterangan_Tambahan` text DEFAULT NULL,
  `Gambar` varchar(255) DEFAULT NULL,
  `Kategori` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kantin`
--

INSERT INTO `kantin` (`id`, `Gedung`, `Nama_Stall`, `Nama_Produk`, `Harga`, `Keterangan_Tambahan`, `Gambar`, `Kategori`) VALUES
(1, 'Gedung P', 'Soto Ayam Jago', 'Soto ayam biasa', 16000.00, '', './images/test.jpg', 'makanan'),
(2, 'Gedung P', 'Soto Ayam Jago', 'Soto ayam Special', 18000.00, 'lauk ayam lebih banyak dari biasa', './images/page.jpg', 'makanan'),
(3, 'Gedung P', 'Soto Ayam Jago', 'Soto ayam goreng', 22000.00, '', './images/Resep-Soto-Ayam-Goreng-Madura.jpg', 'makanan'),
(4, 'Gedung P', 'Soto Ayam Jago', 'Soto telor biasa/asin', 13000.00, 'bisa pilih telur rebus biasa atau telur rebus asin', './images/soto telor biasa.jpg', 'makanan'),
(5, 'Gedung P', 'Soto Ayam Jago', 'Soto telor muda uritan', 16000.00, '', './images/soto uritan.jpg', 'makanan'),
(6, 'Gedung P', 'Soto Ayam Jago', 'Soto tempe + tahu crispy', 13000.00, '', './images/soto tempetahu.jpeg', 'makanan'),
(7, 'Gedung P', 'Soto Ayam Jago', 'Soto daging sapi', 18000.00, '', './images/soto daging.jpeg', 'makanan'),
(8, 'Gedung P', 'Soto Ayam Jago', 'Soto daging sapi spesial', 20000.00, 'lauk daging sapi lebih banyak dari biasa', './images/soto daging sapi spesial.jpg', 'makanan'),
(9, 'Gedung P', 'Soto Ayam Jago', 'Nasi uduk ayam goreng/crispy', 22000.00, '', './images/nasi uduk ayam goreng krispi.jpg', 'makanan'),
(10, 'Gedung P', 'Soto Ayam Jago', 'Nasi uduk telor dadar', 12000.00, '', './images/nasi uduk telor dadar.jpeg', 'makanan'),
(11, 'Gedung P', 'Soto Ayam Jago', 'Nasi uduk tahu tempe', 12000.00, '', './images/nasi uduk tahu tempe.jpeg', 'makanan'),
(12, 'Gedung P', 'Soto Ayam Jago', 'Nasi uduk 3T ( tahu tempe telor)', 16000.00, '', './images/pesan.jpg', 'makanan'),
(13, 'Gedung P', 'Soto Ayam Jago', 'Nasi uduk empal', 22000.00, '', './images/nasi uduk empal.jpg', 'makanan'),
(14, 'Gedung P', 'Soto Ayam Jago', 'Nasi uduk babat paru', 22000.00, '', './images/nasi uduk paru babat.jpeg', 'makanan'),
(15, 'Gedung P', 'Soto Ayam Jago', 'Nasi goreng jawa/mawut', 16000.00, 'bisa pilih nasi goreng jawa atau nasi goreng mawut', './images/nasigorengmawut.jpg', 'makanan'),
(16, 'Gedung P', 'Soto Ayam Jago', 'Nasi goreng babat', 22000.00, '', './images/nasi goreng babat.jpg', 'makanan'),
(17, 'Gedung P', 'Soto Ayam Jago', 'Nasi mie sayur', 16000.00, '', './images/nasi mie sayur.jpg', 'makanan'),
(18, 'Gedung P', 'Soto Ayam Jago', 'Nasi aneka sayur', NULL, 'harga bervariasi tergantung sayuran yang dipilih', './images/nasi sayur.jpg', 'makanan'),
(19, 'Gedung P', 'NDOKEE! EXPRESS', 'Cap cay', 30000.00, 'dengan nasi putih', './images/capcay.jpg', 'makanan'),
(20, 'Gedung P', 'NDOKEE! EXPRESS', 'Ayam telur asin', 25000.00, 'dengan nasi putih', './images/ayamtelurasin.jpg', 'makanan'),
(21, 'Gedung P', 'NDOKEE! EXPRESS', 'Ayam koloke', 25000.00, 'dengan nasi putih', './images/ayam koloke.jpg', 'makanan'),
(22, 'Gedung P', 'NDOKEE! EXPRESS', 'Ayam lada hitam', 25000.00, 'dengan nasi putih', './images/ayam_lada_hitam.jpg', 'makanan'),
(23, 'Gedung P', 'NDOKEE! EXPRESS', 'Ayam saos inggris', 25000.00, 'dengan nasi putih', './images/ayam saus inggris.jpeg', 'makanan'),
(24, 'Gedung P', 'NDOKEE! EXPRESS', 'Fuyunghai', 25000.00, 'dengan nasi putih', './images/fuyunghai.jpg', 'makanan'),
(25, 'Gedung P', 'NDOKEE! EXPRESS', 'Cap cay', 30000.00, 'dengan bakmie/kwetiau/bihun (pilih 1)', './images/capcay.jpg', 'makanan'),
(26, 'Gedung P', 'NDOKEE! EXPRESS', 'Mie ayam lada hitam', 25000.00, '', './images/mie ayam lada hitam.jpg', 'makanan'),
(27, 'Gedung P', 'NDOKEE! EXPRESS', 'Lomie', 20000.00, '', './images/lomie.jpg', 'makanan'),
(28, 'Gedung P', 'NDOKEE! EXPRESS', 'Tamie cap cay', 35000.00, '', './images/tamie capcay.jpg', 'makanan'),
(29, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi putih', 5000.00, '', './images/nasi putih.jpg', 'makanan'),
(30, 'Gedung P', 'NDOKEE! EXPRESS', 'Telor', 5000.00, 'bisa pilih dadar/ceplok/orak arik', './images/telur.jpg', 'makanan'),
(31, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng ayam', 20000.00, '', './images/nasi goreng ayam.jpeg', 'makanan'),
(32, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng spesial', 25000.00, 'pilih lauk telor/lap jiang/ham/kornet/sosis', './images/nasi goreng spesial.jpg', 'makanan'),
(33, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng mawut', 25000.00, '', './images/nasi goreng mawut.jpg', 'makanan'),
(34, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng hong kong', 25000.00, '', './images/nasi goreng hongkong.jpg', 'makanan'),
(35, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng ikan asin', 25000.00, '', './images/nasi goreng ikan asin.jpg', 'makanan'),
(36, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng telor', 30000.00, 'pilih telor lap jiong/ham/kornet/sosis', './images/nasi goreng telor.jpeg', 'makanan'),
(37, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng UP', 35000.00, '', './images/Nasi goreng UP.jpg', 'makanan'),
(38, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng telor asin', 35000.00, '', './images/nasi goreng telor asin.jpg', 'makanan'),
(39, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng ayam koloke', 35000.00, '', './images/nasi goreng ayam koloke.jpg', 'makanan'),
(40, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng ayam lada hitam', 35000.00, '', './images/nasi goreng ayam lada hitam.jpg', 'makanan'),
(41, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng saos inggris', 35000.00, '', './images/nasi goreng saus inggris.jpg', 'makanan'),
(42, 'Gedung P', 'NDOKEE! EXPRESS', 'Nasi goreng fuyunghai', 35000.00, '', './images/nasi goreng fuyunghai.jpeg', 'makanan'),
(43, 'Gedung P', 'Depot KITA', 'Nasi ayam goreng kremes', 25000.00, '', './images/nasi ayam goreng kremes.jpg', 'makanan'),
(44, 'Gedung P', 'Depot KITA', 'Nasi ayam goreng kalasan', 25000.00, '', './images/ayam-goreng-kalasan-foto-resep-utama.jpg', 'makanan'),
(45, 'Gedung P', 'Depot KITA', 'Nasi empal suwir', 25000.00, '', './images/nasi empal suwir.jpg', 'makanan'),
(46, 'Gedung P', 'Depot KITA', 'Nasi ayam hongkong', 20000.00, 'bisa jumbo + 8000 (porsi lebih besar)', './images/nasi ayam hongkong.jpg', 'makanan'),
(47, 'Gedung P', 'Depot KITA', 'Nasi koloke', 20000.00, 'bisa jumbo + 8000 (porsi lebih besar)', './images/nasi goreng ayam koloke.jpg', 'makanan'),
(48, 'Gedung P', 'Depot KITA', 'Nasi ayam geprek', 20000.00, 'bisa jumbo + 8000 (porsi lebih besar)', './images/nasi ayam geprek.jpg', 'makanan'),
(49, 'Gedung P', 'Depot KITA', 'Nasi ayam kungpao', 20000.00, 'bisa jumbo + 8000 (porsi lebih besar)', './images/nasi kungpao.jpeg', 'makanan'),
(50, 'Gedung P', 'Depot KITA', 'Nasi ham', 25000.00, '', './images/nasi ham.jpeg', 'makanan'),
(51, 'Gedung P', 'Depot KITA', 'Nasi fuyunghai', 20000.00, '', './images/nasi fuyunghai.jpg', 'makanan'),
(52, 'Gedung P', 'Depot KITA', 'Nasi bbq', 20000.00, 'bisa jumbo + 8000 (porsi lebih besar)', './images/nasi bbq.jpeg', 'makanan'),
(53, 'Gedung P', 'Depot KITA', 'Sosis bakar', 6000.00, 'untuk 1 sosis (tanpa nasi)', './images/sosis bakar.jpg', 'snack'),
(54, 'Gedung P', 'Depot KITA', 'Nasi mayo', 25000.00, 'ayam mayo', './images/nasi mayo.jpeg', 'makanan'),
(55, 'Gedung P', 'Carnival', 'French fries (kentang)', 17000.00, 'dengan pilihan bumbu: barbeque, ayam bakar, balado, jagung manis, cheese, super pedas dan pilihan saus: saus mayonnaise, chili sauce, tomato sauce (bisa lebih dari 1 bumbu/saus', './images/french fries.jpeg', 'snack'),
(56, 'Gedung P', 'Carnival', 'Mushroom crispy (jamur)', 15000.00, 'dengan pilihan bumbu: barbeque, ayam bakar, balado, jagung manis, cheese, super pedas dan pilihan saus: saus mayonnaise, chili sauce, tomato sauce (bisa lebih dari 1 bumbu/saus', './images/mushroom crispy.jpeg', 'snack'),
(57, 'Gedung P', 'Carnival', 'Tahu crispy', 13000.00, 'dengan pilihan bumbu: barbeque, ayam bakar, balado, jagung manis, cheese, super pedas dan pilihan saus: saus mayonnaise, chili sauce, tomato sauce (bisa lebih dari 1 bumbu/saus', './images/tahu crispy.jpg', 'snack'),
(58, 'Gedung P', 'Carnival', 'Kulit ayam crispy', 15000.00, 'dengan pilihan bumbu: barbeque, ayam bakar, balado, jagung manis, cheese, super pedas dan pilihan saus: saus mayonnaise, chili sauce, tomato sauce (bisa lebih dari 1 bumbu/saus', './images/kulit ayam crispy.jpg', 'snack'),
(59, 'Gedung P', 'Carnival', 'Fishball', 17000.00, '(bola ikan, isi 10) dengan pilihan bumbu: barbeque, ayam bakar, balado, jagung manis, cheese, super pedas dan pilihan saus: saus mayonnaise, chili sauce, tomato sauce (bisa lebih dari 1 bumbu/saus', './images/fish ball.jpg', 'snack'),
(60, 'Gedung P', 'Carnival', 'Shrimp ball', 17000.00, '(bola udang, isi 8) dengan pilihan bumbu: barbeque, ayam bakar, balado, jagung manis, cheese, super pedas dan pilihan saus: saus mayonnaise, chili sauce, tomato sauce (bisa lebih dari 1 bumbu/saus', './images/shrimp ball.jpeg', 'snack'),
(61, 'Gedung P', 'Carnival', 'Curly fries', 18000.00, 'dengan pilihan bumbu: barbeque, ayam bakar, balado, jagung manis, cheese, super pedas dan pilihan saus: saus mayonnaise, chili sauce, tomato sauce (bisa lebih dari 1 bumbu/saus', './images/curly fries.jpeg', 'snack'),
(62, 'Gedung P', 'Carnival', 'Combo seafood tofu', 20000.00, '(french fries + seafood tofu) dengan pilihan bumbu: barbeque, ayam bakar, balado, jagung manis, cheese, super pedas dan pilihan saus: saus mayonnaise, chili sauce, tomato sauce (bisa lebih dari 1 bumbu/saus', './images/seafood tofu.jpeg', 'snack'),
(63, 'Gedung P', 'Carnival', 'Combo nugget', 20000.00, '(french fries + nugget) dengan pilihan bumbu: barbeque, ayam bakar, balado, jagung manis, cheese, super pedas dan pilihan saus: saus mayonnaise, chili sauce, tomato sauce (bisa lebih dari 1 bumbu/saus', './images/combo nugget.jpg', 'snack'),
(64, 'Gedung P', 'Carnival', 'Combo sosis', 20000.00, '(french fries + sosis) dengan pilihan bumbu: barbeque, ayam bakar, balado, jagung manis, cheese, super pedas dan pilihan saus: saus mayonnaise, chili sauce, tomato sauce (bisa lebih dari 1 bumbu/saus', './images/sosis bakar.jpg', 'snack'),
(65, 'Gedung P', 'Japanese Food', 'Yakimeshi original', 20000.00, '', './images/yakimeshi original.jpg', 'makanan'),
(66, 'Gedung P', 'Japanese Food', 'Yakimeshi babi', 25000.00, '', './images/yakimeshi babi.jpg', 'makanan'),
(67, 'Gedung P', 'Japanese Food', 'Yakimeshi hongkong', 25000.00, '', './images/yakimeshi hongkong.jpeg', 'makanan'),
(68, 'Gedung P', 'Japanese Food', 'Yakimeshi ikan asin', 25000.00, '', './images/yakimeshi ikan asin.jpg', 'makanan'),
(69, 'Gedung P', 'Japanese Food', 'Yakimeshi ham telur', 25000.00, '', './images/yakimeshi ham telr.jpg', 'makanan'),
(70, 'Gedung P', 'Japanese Food', 'Yakimeshi smoked beef', 25000.00, '', './images/yakimeshi smoked beef.jpeg', 'makanan'),
(71, 'Gedung P', 'Japanese Food', 'Yakisoba', 20000.00, '', './images/yakisoba.jpg', 'makanan'),
(72, 'Gedung P', 'Japanese Food', 'Ramen', 20000.00, 'pilih tingkat pedas level 0 sampai 10', './images/ramen.jpg', 'makanan'),
(73, 'Gedung P', 'Japanese Food', 'Curry ramen', 25000.00, '', './images/curry ramen.jpeg', 'makanan'),
(74, 'Gedung P', 'Japanese Food', 'Chickin raisu teriyaki', 25000.00, '', './images/chicken raisu teriyaki.jpg', 'makanan'),
(75, 'Gedung P', 'Japanese Food', 'Chickin raisu Yakiniku', 25000.00, '', './images/chickin raisu yakiniku.jpeg', 'makanan'),
(76, 'Gedung P', 'Japanese Food', 'Chickin raisu blackpepper', 25000.00, '', './images/chickin raisu blackpepper.jpg', 'makanan'),
(77, 'Gedung P', 'Japanese Food', 'Chickin raisu karage', 25000.00, '', './images/chickin raisu karage.jpg', 'makanan'),
(78, 'Gedung P', 'Japanese Food', 'Chickin raisu katsu', 25000.00, '', './images/chickin raisu katsu.jpg', 'makanan'),
(79, 'Gedung P', 'Japanese Food', 'Chickin raisu singapore butter milk', 25000.00, '', './images/Chickin raisu singapore butter milk.jpg', 'makanan'),
(80, 'Gedung P', 'Japanese Food', 'Omurice', 25000.00, '', './images/Omurice.jpg', 'makanan'),
(81, 'Gedung P', 'Japanese Food', 'Okonomiyaki', 25000.00, '', './images/Okonomiyaki.jpg', 'makanan'),
(82, 'Gedung P', 'Japanese Food', 'Sushi katsu', 20000.00, '', './images/Sushi katsu.jpg', 'makanan'),
(83, 'Gedung P', 'Japanese Food', 'Sushi tuna', 20000.00, '', './images/Sushi tuna.jpeg', 'makanan'),
(84, 'Gedung P', 'Japanese Food', 'Sushi crabstick', 20000.00, '', './images/Sushi crabstick.jpeg', 'makanan'),
(85, 'Gedung P', 'Japanese Food', 'Paket hemat bento mix', 20000.00, '', './images/Paket hemat bento mix.jpg', 'makanan'),
(86, 'Gedung P', 'Japanese Food', 'Paket hemat Yakimeshi + koloke', 30000.00, '', './images/nasi goreng ayam koloke.jpg', 'makanan'),
(87, 'Gedung P', 'Japanese Food', 'Paket hemat Yakimeshi + lada hitam', 30000.00, '', './images/nasi goreng ayam lada hitam.jpg', 'makanan'),
(88, 'Gedung P', 'Japanese Food', 'Paket hemat Yakimeshi + ayam mentega', 30000.00, '', './images/Paket hemat Yakimeshi + ayam mentega.jpg', 'makanan'),
(89, 'Gedung P', 'Japanese Food', 'Paket hemat Yakimeshi +  karage', 30000.00, '', './images/yakimeshi karage.jpeg', 'makanan'),
(90, 'Gedung P', 'Japanese Food', 'Paket hemat Yakimeshi + ayam saos inggris', 30000.00, '', './images/nasi goreng saus inggris.jpg', 'makanan'),
(91, 'Gedung P', 'Japanese Food', 'Paket hemat Yakimeshi + ayam cabe garam', 30000.00, '', './images/Paket hemat Yakimeshi + ayam cabe garam.jpg', 'makanan'),
(92, 'Gedung P', 'Japanese Food', 'Paket hemat Yakimeshi + katsu', 30000.00, '', './images/yakimeshi katsu.jpeg', 'makanan'),
(93, 'Gedung P', 'Japanese Food', 'Telor', 5000.00, 'bisa dadar/ceploki/orak arik', './images/telur.jpg', 'makanan'),
(94, 'Gedung P', 'Japanese Food', 'Nasi putih', 5000.00, '', './images/nasi putih.jpg', 'makanan'),
(95, 'Gedung P', 'OPA OYS', 'Kopi americano', 15000.00, '', './images/americano.jpg', 'minuman'),
(96, 'Gedung P', 'OPA OYS', 'Kopi aren latte', 15000.00, '', './images/Kopi aren latte.jpeg', 'minuman'),
(97, 'Gedung P', 'OPA OYS', 'Kopi caramel latte', 15000.00, '', './images/Kopi caramel latte.jpeg', 'minuman'),
(98, 'Gedung P', 'OPA OYS', 'Kopi hazelnut latte', 15000.00, '', './images/Kopi hazelnut latte.jpeg', 'minuman'),
(99, 'Gedung P', 'OPA OYS', 'Kopi Tubruk', 15000.00, '', './images/Kopi-Tubruk.jpg', 'minuman'),
(100, 'Gedung P', 'OPA OYS', 'Kopi cinnamon latte', 15000.00, '', './images/Kopi cinnamon latte.jpg', 'minuman'),
(101, 'Gedung P', 'OPA OYS', 'Kopi V60', 15000.00, '', './images/Kopi V60.jpg', 'minuman'),
(102, 'Gedung P', 'OPA OYS', 'Taro oreo', 15000.00, '', './images/Taro oreo.jpeg', 'minuman'),
(103, 'Gedung P', 'OPA OYS', 'Thai tea', 15000.00, '', './images/Thai tea.jpeg', 'minuman'),
(104, 'Gedung P', 'OPA OYS', 'Teh tarik', 15000.00, '', './images/Teh tarik.jpg', 'minuman'),
(105, 'Gedung P', 'OPA OYS', 'Yakult leci', 17000.00, '', './images/Yakult leci.jpg', 'minuman'),
(106, 'Gedung P', 'OPA OYS', 'Matcha', 18000.00, '', './images/matcha.jpg', 'minuman'),
(107, 'Gedung P', 'OPA OYS', 'Jus jambu', 10000.00, '', './images/Jus jambu.jpg', 'minuman'),
(108, 'Gedung P', 'OPA OYS', 'Jus semangka', 10000.00, '', './images/Jus semangka.jpg', 'minuman'),
(109, 'Gedung P', 'OPA OYS', 'Jus melon', 10000.00, '', './images/Jus melon.jpg', 'minuman'),
(110, 'Gedung P', 'OPA OYS', 'Jus sirsak', 10000.00, '', './images/Jus sirsak.jpg', 'minuman'),
(111, 'Gedung P', 'OPA OYS', 'Jus stroberi', 10000.00, '', './images/jus stroberi.png', 'minuman'),
(112, 'Gedung P', 'OPA OYS', 'Jus jeruk', 10000.00, '', './images/Jus jeruk.jpg', 'minuman'),
(113, 'Gedung P', 'OPA OYS', 'Jus pisang', 10000.00, '', './images/Jus pisang.jpeg', 'minuman'),
(114, 'Gedung P', 'OPA OYS', 'Jus buah naga', 10000.00, '', './images/Jus buah naga.jpg', 'minuman'),
(115, 'Gedung P', 'OPA OYS', 'Jus mangga', 10000.00, '', './images/Jus mangga.jpg', 'minuman'),
(116, 'Gedung P', 'OPA OYS', 'Jus alpukat', 12000.00, '', './images/Jus alpukat.jpg', 'minuman'),
(117, 'Gedung P', 'OPA OYS', 'Jus wortel', 10000.00, '', './images/Jus wortel.jpg', 'minuman'),
(118, 'Gedung P', 'OPA OYS', 'Jus timun', 10000.00, '', './images/Jus timun.jpg', 'minuman'),
(119, 'Gedung P', 'OPA OYS', 'Jus apel', 10000.00, '', './images/Jus apel (1).jpeg', 'minuman'),
(120, 'Gedung P', 'OPA OYS', 'Milkshake fosco', 15000.00, '', './images/Milkshake fosco.jpeg', 'minuman'),
(121, 'Gedung P', 'OPA OYS', 'Milkshake black forest', 15000.00, '', './images/Milkshake black forest.jpeg', 'minuman'),
(122, 'Gedung P', 'OPA OYS', 'Milkshake choco cream', 15000.00, '', './images/Milkshake choco cream.jpg', 'minuman'),
(123, 'Gedung P', 'OPA OYS', 'Milkshake rum raisin', 15000.00, '', './images/Milkshake rum raisin.jpeg', 'minuman'),
(124, 'Gedung P', 'OPA OYS', 'Milkshake vanilla ria', 15000.00, '', './images/Milkshake vanilla ria.jpeg', 'minuman'),
(125, 'Gedung P', 'OPA OYS', 'Milkshake tiramisu', 15000.00, '', './images/Milkshake tiramisu.jpeg', 'minuman'),
(126, 'Gedung P', 'OPA OYS', 'Milkshake milk cream', 15000.00, '', './images/Milkshake milk cream.jpg', 'minuman'),
(127, 'Gedung P', 'OPA OYS', 'Milkshake cappucino', 15000.00, '', './images/Milkshake cappucino.jpeg', 'minuman'),
(128, 'Gedung P', 'OPA OYS', 'Sirup melon', 5000.00, '', './images/Sirup melon.jpeg', 'minuman'),
(129, 'Gedung P', 'OPA OYS', 'Sirup anggur', 5000.00, '', './images/Sirup anggur.jpeg', 'minuman'),
(130, 'Gedung P', 'OPA OYS', 'Jeruk peras', 7000.00, '', './images/Jus jeruk.jpg', 'minuman'),
(131, 'Gedung P', 'OPA OYS', 'Es cao / cao susu', 7000.00, '', './images/es cao.jpg', 'minuman'),
(132, 'Gedung P', 'OPA OYS', 'Nutrisari', 7000.00, 'pilih rasa nutrisari', './images/nutrisari.jpeg', 'minuman'),
(133, 'Gedung P', 'Dapur Mapan', 'Nasi merah', 10000.00, 'dari beras merah (nasi aja, tanpa lauk)', './images/nasi merah.jpg', 'makanan'),
(134, 'Gedung P', 'Dapur Mapan', 'Nasi pecel ori', 12000.00, 'nasi + bumbu pecel, tanpa lauk', './images/Nasi pecel ori\'.jpg', 'makanan'),
(135, 'Gedung P', 'Dapur Mapan', 'Nasi rawon', 25000.00, '', './images/Nasi rawon.jpg', 'makanan'),
(136, 'Gedung P', 'Dapur Mapan', 'Nasi krengsengan', 25000.00, '', './images/Nasi krengsengan.jpeg', 'makanan'),
(137, 'Gedung P', 'Dapur Mapan', 'Nasi empal kremes', 25000.00, '', './images/Nasi empal kremes.jpg', 'makanan'),
(138, 'Gedung P', 'Dapur Mapan', 'Nasi paru pedas', 25000.00, '', './images/Nasi paru pedas.jpeg', 'makanan'),
(139, 'Gedung P', 'Dapur Mapan', 'Nasi cumi', 25000.00, '', './images/Nasi cumi.jpg', 'makanan'),
(140, 'Gedung P', 'Dapur Mapan', 'Nasi dori telur asin', 23000.00, '', './images/Nasi dori telur asin.jpeg', 'makanan'),
(141, 'Gedung P', 'Dapur Mapan', 'Nasi ayam bakar', 23000.00, '', './images/Nasi ayam bakar.jpg', 'makanan'),
(142, 'Gedung P', 'Dapur Mapan', 'Nasi ayam matah', 22000.00, '', './images/Nasi ayam matah.jpg', 'makanan'),
(143, 'Gedung P', 'Dapur Mapan', 'Nasi ayam kremes', 22000.00, '', './images/nasi ayam goreng kremes.jpg', 'makanan'),
(144, 'Gedung P', 'Dapur Mapan', 'Nasi ayam penyet', 22000.00, '', './images/Nasi ayam penyet.jpeg', 'makanan'),
(145, 'Gedung P', 'Dapur Mapan', 'Nasi ayam rendang', 22000.00, '', './images/Nasi ayam rendang.jpg', 'makanan'),
(146, 'Gedung P', 'Dapur Mapan', 'Nasi ayam mayo', 22000.00, '', './images/Nasi ayam mayo.jpeg', 'makanan'),
(147, 'Gedung P', 'Dapur Mapan', 'Nasi ayam kungpao', 22000.00, '', './images/Nasi ayam kungpao.jpg', 'makanan');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kantin`
--
ALTER TABLE `kantin`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `kantin`
--
ALTER TABLE `kantin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=148;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
