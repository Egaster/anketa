CREATE DATABASE IF NOT EXISTS `LOGIN` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `LOGIN`;

CREATE TABLE IF NOT EXISTS `form` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    `phone` varchar(12) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

select * from `form`;

CREATE TABLE IF NOT EXISTS `result` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `session` int(11) not null,
    `uid` varchar(50) NOT NULL,
    `qid` varchar(50) NOT NULL,
    `answer` varchar(25),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `questions` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `qid` varchar(50) not null,
    `question` varchar(250) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

 insert into `questions` (`qid`, `question`) values
 (1,  "Проходили ли Вы процедуру банкротства?"),
 (2, "Прошло уже более 5 лет с момента прохождения процедуры банкротства?"),
 (3, "Ваша общая сумма долговых обязательств менее 500 тысяч рублей?"),
 (4, "Ваша общая сумма долговых обязательств менее 25 тысяч рублей?"),
 (5, "Ваша общая сумма долговых обязательств более 1 миллиона рублей?"),
 (6, "Действует ли в отношении Вас неоконченное исполнительное производство по взысканию денежных средств?"),
 (7, "Исполнительный документ был выдан Вам 7 или менее лет назад?"),
 (8, "Действовало ли ранее в отношении Вас исполнительное производство по взысканию денежных средств?"),
 (9, "Действует ли в отношении Вас неоконченное исполнительное производство по взысканию денежных средств?"),
 (10, "Ваш основной доход это заработная плата или доходы с ИП или Вы безработный?"),
 (11, "Получаете ли Вы пенсию или социальные выплаты?"),
 (12, "Предъявлялся ли Вам не позднее 1 года назад исполнительный документ по имущественным требованиям, который не был исполнен или был исполнен частично?"),
 (13, "Есть ли у Вас имущество, на которое можно обратить взыскание?"),
 (14, "Срок просрочки Ваших обязательств уже наступил?"),
 (15, "Срок просрочки Ваших обязательств более 3 месяцев?"),
 (16, "Срок с момента выявления у Вас неплатежеспособности и (или) недостаточности денежных средств более 30 дней?"),
 (17, "Являетесь ли Вы неплатежеспособным?"),
 (18, "Достаточно ли у Вас имущества для исполнения обязательств?"),
 (19, "Есть ли у Вас документальное подтверждение неплатежеспособности?"),
 (20, "Есть ли у Вас непогашенная судимость за экономические преступления?");
 
 create table if not exists `answers` (
	`aid` varchar(50) not null primary key,
    `text` varchar(250) not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

 insert into `answers` (`aid`, `text`) values 
 ('yes', 'Да'),
 ('no', 'Нет'),
 ('end', 'Производство окончено в связи с отсутствием имущества'),
 ('again','	Производство окончено, но после этого возбуждено новое');
-- select * from `answers`;
-- drop table `result`;
-- select * from `questions`;

CREATE TABLE IF NOT EXISTS `sessions` (
    `uid` varchar(50) NOT NULL primary key,
    `session` int(11)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- drop table `sessions`;
-- select  * from `sessions`;
