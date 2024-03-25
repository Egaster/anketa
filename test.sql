CREATE DATABASE IF NOT EXISTS `LOGIN` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `LOGIN`;

CREATE TABLE IF NOT EXISTS `form` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    `phone` varchar(12) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `form` (`id`, `username`, `password`, `phone`) VALUES (2, 'test', '1234', '81111111111');
