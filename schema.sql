DROP DATABASE IF EXISTS krasnodar_football;
CREATE DATABASE krasnodar_football;
USE krasnodar_football;

CREATE TABLE stadiums (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE teams (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    coach VARCHAR(100) NOT NULL,
    last_season_place INT NOT NULL
);

CREATE TABLE players (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    number INT,
    position VARCHAR(30) NOT NULL
);

CREATE TABLE matches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    match_date DATETIME NOT NULL,
    status ENUM('запланирован','перенесен','отменен') DEFAULT 'запланирован',
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    stadium_id INT NOT NULL,
    home_score INT,
    away_score INT,
    FOREIGN KEY (home_team_id) REFERENCES teams(id),
    FOREIGN KEY (away_team_id) REFERENCES teams(id),
    FOREIGN KEY (stadium_id) REFERENCES stadiums(id)
) ENGINE=InnoDB;

ALTER TABLE matches
ADD COLUMN match_day DATE
GENERATED ALWAYS AS (DATE(match_date)) STORED;

ALTER TABLE matches
ADD CONSTRAINT one_match_per_day
UNIQUE (match_day, home_team_id);

CREATE TABLE player_stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT NOT NULL,
    match_id INT NOT NULL,
    team_id INT NOT NULL,
    goals INT DEFAULT 0,
    assists INT DEFAULT 0,
    yellow_cards INT DEFAULT 0,
    minutes_played INT,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (match_id) REFERENCES matches(id),
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE TABLE tickets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT NOT NULL,
    category VARCHAR(20) DEFAULT 'обычный',
    price DECIMAL(10,2) NOT NULL,
    available INT DEFAULT 100,
    FOREIGN KEY (match_id) REFERENCES matches(id)
);


INSERT INTO stadiums (name, city, capacity) VALUES
('Стадион Академии', 'Краснодар', 7458),
('Арена Чертаново', 'Москва', 490),
('Урал', 'Екатеринбург', 35000),
('Спартак', 'Москва', 45360),
('Зенит Арена', 'Санкт-Петербург', 64468);

INSERT INTO teams (name, city, coach, last_season_place) VALUES
('Краснодар-U18', 'Краснодар', 'Азим Абдулаевич Фатуллаев', 2),
('СШОР Зенит-U18', 'Санкт-Петербург', 'Иван Петрович Сидоров', 5),
('Чертаново-U18', 'Москва', 'Сергей Владимирович Иванов', 3),
('Урал-U18', 'Екатеринбург', 'Александр Николаевич Петров', 9),
('Зенит-U18', 'Санкт-Петербург', 'Дмитрий Сергеевич Смирнов', 1);

INSERT INTO players (full_name, number, position) VALUES
('Марк Сергеевич Федотов', 1, 'Вратарь'),
('Иван Александрович Федько', 88, 'Вратарь'),
('Дмитрий Викторович Ачкинази', 91, 'Вратарь'),
('Андрей Олегович Карпенко', 99, 'Вратарь'),

('Богдан Иванович Кудзаву', 3, 'Защитник'),
('Степан Дмитриевич Садчиков', 4, 'Защитник'),
('Виктор Петрович Шипуль', 5, 'Защитник'),
('Вадим Андреевич Матвеенко', 6, 'Защитник'),
('Иван Сергеевич Акманов', 14, 'Защитник'),
('Сергей Алексеевич Тройчин', 21, 'Защитник'),
('Никита Владимирович Закарлюка', 50, 'Защитник'),
('Евгений Михайлович Дедяев', 61, 'Защитник'),

('Ярослав Олегович Крючков', 8, 'Полузащитник'),
('Ефим Александрович Буркин', 15, 'Полузащитник'),
('Максим Игоревич Пономаренко', 42, 'Полузащитник'),
('Андрей Викторович Полевой', 64, 'Полузащитник'),
('Артём Дмитриевич Кульбаев', 96, 'Полузащитник'),

('Даниэль Артемович Амбарцумов', 7, 'Нападающий'),
('Кирилл Сергеевич Леконцев', 9, 'Нападающий'),
('Роман Андреевич Сумачёв', 11, 'Нападающий'),
('Андрей Петрович Королёв', 89, 'Нападающий'),
('Артём Владимирович Дряхлов', 90, 'Нападающий'),
('Эльдар Раминович Гусейнов', 97, 'Нападающий');

INSERT INTO matches (match_date, home_team_id, away_team_id, stadium_id, home_score, away_score) VALUES
('2025-08-03 20:00:00', 1, 2, 1, 5, 1),   
('2025-08-10 17:00:00', 3, 1, 2, 2, 1),   
('2025-08-16 20:00:00', 1, 4, 1, 3, 0),   
('2025-08-23 12:00:00', 4, 1, 3, 0, 3),   
('2025-08-30 20:00:00', 1, 5, 1, 1, 1);   


INSERT INTO matches (match_date, home_team_id, away_team_id, stadium_id, home_score, away_score) VALUES
('2026-01-15 19:00:00', 1, 3, 1, NULL, NULL); 

INSERT INTO player_stats (player_id, match_id, team_id, goals, assists, minutes_played) VALUES
(2, 1, 1, 0, 0, 90),   
(6, 1, 1, 1, 0, 90),   
(16, 1, 1, 1, 0, 77),  
(19, 1, 1, 1, 0, 74),  
(21, 1, 1, 2, 0, 90),  
(15, 1, 1, 0, 0, 62),  
(22, 1, 1, 0, 0, 67),  
(20, 1, 1, 0, 0, 88),  
(5, 1, 1, 0, 0, 8),    
(13, 1, 1, 0, 0, 8),   
(10, 1, 1, 0, 0, 13), 
(9, 1, 1, 0, 0, 16),   
(18, 1, 1, 0, 0, 28),  
(17, 1, 1, 0, 0, 23),  


(2, 2, 1, 0, 0, 90),  
(12, 2, 1, 0, 0, 90),  
(13, 2, 1, 0, 0, 83),  
(4, 2, 1, 1, 0, 90),   
(16, 2, 1, 0, 0, 76),  
(15, 2, 1, 0, 0, 64),  
(21, 2, 1, 0, 0, 90),  
(22, 2, 1, 0, 0, 90),  
(20, 2, 1, 0, 0, 90),  
(5, 2, 1, 0, 0, 7),    
(10, 2, 1, 0, 0, 14),  
(7, 2, 1, 0, 0, 26),   
(9, 2, 1, 0, 0, 22),  
(18, 2, 1, 0, 0, 26),  


(3, 3, 1, 0, 0, 90),   
(5, 3, 1, 0, 0, 87),   
(12, 3, 1, 0, 0, 90),  
(13, 3, 1, 0, 0, 90),  
(9, 3, 1, 0, 0, 90),  
(16, 3, 1, 1, 0, 90),
(15, 3, 1, 0, 0, 67),  
(21, 3, 1, 1, 0, 80), 
(22, 3, 1, 0, 0, 90),  
(20, 3, 1, 0, 0, 85),  
(10, 3, 1, 0, 0, 23), 
(7, 3, 1, 0, 0, 5),    
(4, 3, 1, 0, 0, 3),    
(18, 3, 1, 0, 0, 10);  

INSERT INTO tickets (match_id, category, price, available) VALUES
(1, 'обычный', 500.00, 3000),
(1, 'VIP', 1500.00, 100),
(3, 'обычный', 500.00, 3000),
(3, 'VIP', 1500.00, 100),
(5, 'обычный', 600.00, 3000),
(5, 'VIP', 1800.00, 100);

INSERT INTO tickets (match_id, category, price, available) VALUES
(6, 'обычный', 700.00, 2500),
(6, 'VIP', 2000.00, 80);


CREATE VIEW krasnodar_matches AS
SELECT 
    m.match_date as дата,
    CASE 
        WHEN m.home_team_id = 1 THEN 'Дома'
        ELSE 'В гостях'
    END as статус,
    CASE 
        WHEN m.home_team_id = 1 THEN a.name
        ELSE h.name
    END as противник,
    CASE 
        WHEN m.home_team_id = 1 THEN m.home_score
        ELSE m.away_score
    END as голы_краснодара,
    CASE 
        WHEN m.home_team_id = 1 THEN m.away_score
        ELSE m.home_score
    END as голы_противника,
    s.name as стадион
FROM matches m
JOIN teams h ON m.home_team_id = h.id
JOIN teams a ON m.away_team_id = a.id
JOIN stadiums s ON m.stadium_id = s.id
WHERE m.home_team_id = 1 OR m.away_team_id = 1
ORDER BY m.match_date;

CREATE VIEW player_stats_view AS
SELECT 
    p.full_name as игрок,
    p.number as номер,
    p.position as позиция,
    COUNT(ps.match_id) as матчей,
    SUM(ps.goals) as голов,
    SUM(ps.assists) as передач,
    SUM(ps.yellow_cards) as жк,
    ROUND(AVG(ps.minutes_played), 1) as средние_минуты
FROM players p
LEFT JOIN player_stats ps ON p.id = ps.player_id AND ps.team_id = 1
GROUP BY p.id, p.full_name, p.number, p.position
ORDER BY голов DESC, матчей DESC;

CREATE VIEW top_scorers AS
SELECT 
    p.full_name as игрок,
    p.number as номер,
    SUM(ps.goals) as голов
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
WHERE ps.team_id = 1
GROUP BY p.id, p.full_name, p.number
HAVING SUM(ps.goals) > 0
ORDER BY голов DESC;

CREATE OR REPLACE VIEW home_tickets AS
SELECT 
    m.match_date AS дата_матча,
    a.name AS противник,
    s.name AS стадион,
    tkt.category AS категория,
    CASE
        WHEN tm.last_season_place <= 3 AND s.capacity > 30000 THEN 1800
        WHEN tm.last_season_place <= 3 THEN 1500
        WHEN tm.last_season_place >= 15 THEN 500
        ELSE 800
    END AS цена,
    tkt.available AS доступно
FROM matches m
JOIN teams tm ON m.home_team_id = tm.id
JOIN teams a ON m.away_team_id = a.id
JOIN stadiums s ON m.stadium_id = s.id
JOIN tickets tkt ON m.id = tkt.match_id
WHERE m.match_date > NOW()
  AND m.status = 'запланирован'
ORDER BY m.match_date;
