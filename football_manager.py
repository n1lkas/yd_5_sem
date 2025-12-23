import mysql.connector
from mysql.connector import Error
from datetime import datetime

class FootballDB:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='krasnodar_football',
                user='root',
                password='vino46060'
            )
            if self.connection.is_connected():
                print("Подключено к базе данных")
                return True
        except Error as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    def execute_query(self, query, params=None, fetch=False):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Error as e:
            print(f"Ошибка запроса: {e}")
            return None
    
    def safe_int(self, value):
        if value is None:
            return 0
        try:
            return int(value)
        except:
            return 0
    
    def safe_float(self, value):
        if value is None:
            return 0.0
        try:
            return float(value)
        except:
            return 0.0
    
    def safe_str(self, value):
        if value is None:
            return "Нет данных"
        return str(value)
    
    def format_date(self, date_value):
        if isinstance(date_value, datetime):
            return date_value.strftime("%d.%m.%Y")
        return self.safe_str(date_value)
    
    def confirm_action(self, message):
        while True:
            response = input(f"{message} (да/нет): ").strip().lower()
            if response in ['да', 'yes', 'y', 'д']:
                return True
            elif response in ['нет', 'no', 'n', 'н']:
                return False
            else:
                print("Пожалуйста, введите 'да' или 'нет'")
    
    def show_menu(self):
        while True:
            print("СИСТЕМА УПРАВЛЕНИЯ КРАСНОДАР-U18")
            print("1. Общая информация о команде")
            print("2. Матчи команды")
            print("3. Игроки и статистика")
            print("4. Билеты")
            print("5. Сведения и отчеты")
            print("6. Администрирование")
            print("7. Выход")
            
            choice = input("\nВыберите пункт (1-7): ").strip()
            
            if choice == '1':
                self.show_team_info()
            elif choice == '2':
                self.show_matches_menu()
            elif choice == '3':
                self.show_players_menu()
            elif choice == '4':
                self.show_tickets()
            elif choice == '5':
                self.show_reports_menu()
            elif choice == '6':
                self.show_admin_menu()
            elif choice == '7':
                print("\n Выход из системы...")
                if self.connection:
                    self.connection.close()
                break
            else:
                print("Неверный выбор")
    
    def show_team_info(self):
        print("ПОЛНАЯ ИНФОРМАЦИЯ О КОМАНДЕ")
        print("\n ОСНОВНАЯ ИНФОРМАЦИЯ")
        
        query = """
        SELECT name, city, coach, last_season_place 
        FROM teams 
        WHERE name = 'Краснодар-U18'
        """
        result = self.execute_query(query, fetch=True)

        if result:
         print(f"Название команды: {self.safe_str(result[0][0])}")
         print(f"Город базирования: {self.safe_str(result[0][1])}")
         print(f"Главный тренер: {self.safe_str(result[0][2])}")
         print(f"Место в прошлом сезоне: {self.safe_int(result[0][3])}")
        
        print("\n СТАТИСТИКА КОМАНДЫ")
        
        stats_query = """
        SELECT 
            COUNT(*) as total_matches,
            SUM(CASE WHEN home_team_id = 1 AND home_score > away_score THEN 1
                     WHEN away_team_id = 1 AND away_score > home_score THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN home_team_id = 1 AND home_score < away_score THEN 1
                     WHEN away_team_id = 1 AND away_score < home_score THEN 1 ELSE 0 END) as losses,
            SUM(CASE WHEN home_score = away_score THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN home_team_id = 1 THEN home_score ELSE away_score END) as goals_for,
            SUM(CASE WHEN home_team_id = 1 THEN away_score ELSE home_score END) as goals_against
        FROM matches
        WHERE home_team_id = 1 OR away_team_id = 1
        """
        
        stats = self.execute_query(stats_query, fetch=True)
        
        if stats and stats[0]:
            s = stats[0]
            matches = self.safe_int(s[0])
            wins = self.safe_int(s[1])
            losses = self.safe_int(s[2])
            draws = self.safe_int(s[3])
            goals_for = self.safe_int(s[4])
            goals_against = self.safe_int(s[5])
            
            diff = goals_for - goals_against
            points = wins * 3 + draws
            
            print(f"Сыграно матчей: {matches}")
            print(f"Побед: {wins}")
            print(f"Поражений: {losses}")
            print(f"Ничьих: {draws}")
            print(f"Забито голов: {goals_for}")
            print(f"Пропущено голов: {goals_against}")
            print(f"Разница мячей: {diff}")
            print(f"Очков: {points}")
        else:
            print("Нет статистики команды")
        
        print("\n ЛУЧШИЕ БОМБАРДИРЫ")
        
        scorers_query = """
        SELECT p.full_name, p.number, SUM(ps.goals) as goals
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.id
        WHERE ps.team_id = 1
        GROUP BY p.id
        HAVING SUM(ps.goals) > 0
        ORDER BY SUM(ps.goals) DESC
        LIMIT 3
        """
        
        scorers = self.execute_query(scorers_query, fetch=True)
        
        if scorers:
            for i, s in enumerate(scorers, 1):
                name = self.safe_str(s[0])
                number = self.safe_int(s[1])
                goals = self.safe_int(s[2])
                print(f"{i}. {name} (№{number}) - {goals} голов")
        
        input("\n Нажмите Enter...")
    
    def show_matches_menu(self):
        print("МАТЧИ КОМАНДЫ")
        
        while True:
            print("\n1. Все матчи")
            print("2. Домашние матчи")
            print("3. Выездные матчи")
            print("4. Назад")
            
            choice = input("\n Выберите (1-4): ").strip()
            
            if choice == '1':
                self.show_all_matches()
            elif choice == '2':
                self.show_home_matches()
            elif choice == '3':
                self.show_away_matches()
            elif choice == '4':
                break
            else:
                print("Неверный выбор")
    
    def show_all_matches(self):
        print("\n ВСЕ МАТЧИ КОМАНДЫ")
        
        query = "SELECT * FROM krasnodar_matches"
        result = self.execute_query(query, fetch=True)
        
        if result:
            print(f"\nВсего матчей: {len(result)}")
            for row in result:
                date_str = self.format_date(row[0])
                status = self.safe_str(row[1])
                opponent = self.safe_str(row[2])
                our_goals = self.safe_int(row[3])
                their_goals = self.safe_int(row[4])
                stadium = self.safe_str(row[5])
                
                print(f"Дата: {date_str}")
                print(f"Статус: {status}")
                print(f"Противник: {opponent}")
                print(f"Счет: {our_goals}:{their_goals}")
                print(f"Стадион: {stadium}")
        else:
            print("Нет данных о матчах")
        
        input("\n Нажмите Enter...")
    
    def show_home_matches(self):
        print("\n ДОМАШНИЕ МАТЧИ")
        
        query = """
        SELECT m.match_date, a.name, m.home_score, m.away_score, s.name
        FROM matches m
        JOIN teams a ON m.away_team_id = a.id
        JOIN stadiums s ON m.stadium_id = s.id
        WHERE m.home_team_id = 1
        ORDER BY m.match_date
        """
        result = self.execute_query(query, fetch=True)
        
        if result:
            print(f"\nДомашних матчей: {len(result)}")
            for row in result:
                date_str = self.format_date(row[0])
                opponent = self.safe_str(row[1])
                our_goals = self.safe_int(row[2])
                their_goals = self.safe_int(row[3])
                stadium = self.safe_str(row[4])
                
                print(f"Дата: {date_str}")
                print(f"Противник: {opponent}")
                print(f"Счет: {our_goals}:{their_goals}")
                print(f"Стадион: {stadium}")
        
        input("\n Нажмите Enter...")
    
    def show_away_matches(self):
        print("\n ВЫЕЗДНЫЕ МАТЧИ")
        
        query = """
        SELECT m.match_date, h.name, m.away_score, m.home_score, s.name
        FROM matches m
        JOIN teams h ON m.home_team_id = h.id
        JOIN stadiums s ON m.stadium_id = s.id
        WHERE m.away_team_id = 1
        ORDER BY m.match_date
        """
        result = self.execute_query(query, fetch=True)
        
        if result:
            print(f"\nВыездных матчей: {len(result)}")
            for row in result:
                date_str = self.format_date(row[0])
                opponent = self.safe_str(row[1])
                our_goals = self.safe_int(row[2])
                their_goals = self.safe_int(row[3])
                stadium = self.safe_str(row[4])
                
                print(f"Дата: {date_str}")
                print(f"Противник: {opponent}")
                print(f"Счет: {our_goals}:{their_goals}")
                print(f"Стадион: {stadium}")
        
        input("\n Нажмите Enter...")
    
    def show_players_menu(self):
        print("ИГРОКИ И СТАТИСТИКА")
        
        while True:
            print("\n1. Все игроки")
            print("2. Поиск игрока")
            print("3. Топ-5 бомбардиров")
            print("4. Назад")
            
            choice = input("\n Выберите (1-4): ").strip()
            
            if choice == '1':
                self.show_all_players()
            elif choice == '2':
                self.search_player()
            elif choice == '3':
                self.show_top_scorers()
            elif choice == '4':
                break
            else:
                print("Неверный выбор")
    
    def show_all_players(self):
        print("\n ВСЕ ИГРОКИ КРАСНОДАР-U18")
        
        query = """
        SELECT p.full_name, p.number, p.position, 
               COUNT(ps.match_id) as matches,
               SUM(ps.goals) as goals,
               ROUND(AVG(ps.minutes_played), 1) as avg_minutes
        FROM players p
        LEFT JOIN player_stats ps ON p.id = ps.player_id AND ps.team_id = 1
        GROUP BY p.id, p.full_name, p.number, p.position
        ORDER BY goals DESC, matches DESC
        """
        
        result = self.execute_query(query, fetch=True)
        
        if result:
            print(f"\n Всего игроков: {len(result)}")
            print(f"{'Игрок':<30} {'№':<4} {'Позиция':<15} {'М':<4} {'Г':<4} {'Мин':<6}")
            
            for row in result:
                player_name = self.safe_str(row[0])
                number = self.safe_int(row[1])
                position = self.safe_str(row[2])
                matches = self.safe_int(row[3])
                goals = self.safe_int(row[4])
                minutes = self.safe_float(row[5])
                
                if len(player_name) > 29:
                    display_name = player_name[:27] + ".."
                else:
                    display_name = player_name
                
                print(f"{display_name:<30} {number:<4} {position:<15} {matches:<4} {goals:<4} {minutes:<6.1f}")
        else:
            print("Нет данных об игроках")
        
        input("\n Нажмите Enter...")
    
    def search_player(self):
        print("\n ПОИСК ИГРОКА")
        name = input("Введите имя или фамилию игрока: ").strip()
        
        if not name:
            print("Введите имя игрока")
            return
        
        query = """
        SELECT p.full_name, p.number, p.position, 
               COUNT(ps.match_id) as matches,
               SUM(ps.goals) as goals,
               ROUND(AVG(ps.minutes_played), 1) as avg_minutes
        FROM players p
        LEFT JOIN player_stats ps ON p.id = ps.player_id AND ps.team_id = 1
        WHERE p.full_name LIKE %s
        GROUP BY p.id, p.full_name, p.number, p.position
        """
        
        result = self.execute_query(query, (f"%{name}%",), fetch=True)
        
        if result:
            print(f"\nНайдено игроков: {len(result)}")
            for row in result:
                print(f"Игрок: {self.safe_str(row[0])}")
                print(f"Номер: {self.safe_int(row[1])}")
                print(f"Позиция: {self.safe_str(row[2])}")
                print(f"Матчей: {self.safe_int(row[3])}")
                print(f"Голов: {self.safe_int(row[4])}")
                print(f"Минут: {self.safe_float(row[5]):.1f}")
        else:
            print("Игрок не найден")
        
        input("\n Нажмите Enter...")
    
    def show_top_scorers(self):
        print("\n ТОП-5 БОМБАРДИРОВ")
        
        query = "SELECT * FROM top_scorers"
        result = self.execute_query(query, fetch=True)
        
        if result:
            print(f"\n ТОП-{len(result)} БОМБАРДИРОВ")
            print(f"{'№':<3} {'Игрок':<25} {'Номер':<6} {'Голов':<8}")
            
            for i, row in enumerate(result, 1):
                player_name = self.safe_str(row[0])
                number = self.safe_int(row[1])
                goals = self.safe_int(row[2])
                print(f"{i:<3} {player_name:<25} {number:<6} {goals:<8}")
        else:
            print("Нет данных о бомбардирах")
        
        input("\n Нажмите Enter...")
    
    def show_tickets(self):
        print("БИЛЕТЫ НА МАТЧИ")
        
        query = "SELECT * FROM home_tickets"
        result = self.execute_query(query, fetch=True)
        
        if result:
            print(f"\n Доступные билеты:")
            
            for row in result:
                date_str = self.format_date(row[0])
                opponent = self.safe_str(row[1])
                stadium = self.safe_str(row[2])
                category = self.safe_str(row[3])
                price = self.safe_float(row[4])
                available = self.safe_int(row[5])
                
                print(f"\n Дата матча: {date_str}")
                print(f"Противник: {opponent}")
                print(f"Стадион: {stadium}")
                print(f"Категория: {category}")
                print(f"Цена: {price:.2f} руб.")
                print(f"Доступно: {available} билетов")
        else:
            print("Нет данных о билетах")
        
        input("\n Нажмите Enter...")
    
    def show_reports_menu(self):
        print("СВЕДЕНИЯ И ОТЧЕТЫ")
        
        while True:
            print("\n1. Сведения о команде")
            print("2. Сведения о стадионах")
            print("3. Отчет по играм на стадионе")
            print("4. Назад")
            
            choice = input("\n Выберите раздел (1-4): ").strip()
            
            if choice == '1':
                self.show_full_team_info()
            elif choice == '2':
                self.show_stadiums_info()
            elif choice == '3':
                self.show_stadium_report()
            elif choice == '4':
                break
            else:
                print("Неверный выбор")
    
    def show_full_team_info(self):
        print("ПОЛНЫЕ СВЕДЕНИЯ О КОМАНДЕ")
        
        query = "SELECT name, city, coach FROM teams WHERE name = 'Краснодар-U18'"
        result = self.execute_query(query, fetch=True)
        
        if result:
            print(f"\n Название команды: {self.safe_str(result[0][0])}")
            print(f"Город: {self.safe_str(result[0][1])}")
            print(f"Тренер: {self.safe_str(result[0][2])}")
        
        query = "SELECT * FROM krasnodar_matches"
        matches = self.execute_query(query, fetch=True)
        
        if matches:
            print(f"\n ВСЕ МАТЧИ КОМАНДЫ:")
            for match in matches:
                date_str = self.format_date(match[0])
                status = self.safe_str(match[1])
                opponent = self.safe_str(match[2])
                our_goals = self.safe_int(match[3])
                their_goals = self.safe_int(match[4])
                stadium = self.safe_str(match[5])
                
                print(f"{date_str}: {status} против {opponent} | Счет: {our_goals}:{their_goals} | Стадион: {stadium}")
        
        input("\n Нажмите Enter...")
    
    def show_stadiums_info(self):
        print("СВЕДЕНИЯ О СТАДИОНАХ")
        
        query = """
        SELECT s.name, s.city, s.capacity, COUNT(m.id) as matches_count
        FROM stadiums s
        LEFT JOIN matches m ON s.id = m.stadium_id
        WHERE m.home_team_id = 1 OR m.away_team_id = 1
        GROUP BY s.id, s.name, s.city, s.capacity
        ORDER BY matches_count DESC
        """
        
        result = self.execute_query(query, fetch=True)
        
        if result:
            print("\n ИНФОРМАЦИЯ О СТАДИОНАХ:")
            print(f"{'Стадион':<25} {'Город':<15} {'Вместимость':<12} {'Матчей':<8}")
            
            for row in result:
                stadium = self.safe_str(row[0])
                city = self.safe_str(row[1])
                capacity = self.safe_int(row[2])
                matches = self.safe_int(row[3])
                
                print(f"{stadium:<25} {city:<15} {capacity:<12} {matches:<8}")
        else:
            print("Нет данных о стадионах")
        
        input("\n Нажмите Enter...")
    
    def show_stadium_report(self):
        print("\n ОТЧЕТ ПО ИГРАМ НА СТАДИОНЕ")
        
        query = "SELECT id, name, city FROM stadiums ORDER BY name"
        stadiums = self.execute_query(query, fetch=True)
        
        if not stadiums:
            print("Нет данных о стадионах")
            input("\n Нажмите Enter...")
            return
        
        print("\n ВЫБЕРИТЕ СТАДИОН:")
        for i, s in enumerate(stadiums, 1):
            print(f"{i}. {s[1]} ({s[2]})")
        
        try:
            choice = int(input("\n Выберите номер стадиона: "))
            if 1 <= choice <= len(stadiums):
                stadium_id = stadiums[choice-1][0]
                stadium_name = stadiums[choice-1][1]

                query = """
                SELECT 
                    COUNT(*) as total_matches,
                    SUM(CASE WHEN home_score > away_score THEN 1 ELSE 0 END) as home_wins,
                    SUM(CASE WHEN away_score > home_score THEN 1 ELSE 0 END) as away_wins,
                    SUM(CASE WHEN home_score = away_score THEN 1 ELSE 0 END) as draws
                FROM matches
                WHERE stadium_id = %s
                """
                
                stats = self.execute_query(query, (stadium_id,), fetch=True)
                
                if stats and stats[0]:
                    print(f"\n СТАТИСТИКА НА СТАДИОНЕ '{stadium_name}':")
                    print(f"   Всего матчей: {self.safe_int(stats[0][0])}")
                    print(f"   Побед хозяев: {self.safe_int(stats[0][1])}")
                    print(f"   Побед гостей: {self.safe_int(stats[0][2])}")
                    print(f"   Ничьих: {self.safe_int(stats[0][3])}")
                
                query = """
                SELECT DISTINCT p.full_name, t.name, SUM(ps.goals) as goals
                FROM player_stats ps
                JOIN players p ON ps.player_id = p.id
                JOIN matches m ON ps.match_id = m.id
                JOIN teams t ON ps.team_id = t.id
                WHERE m.stadium_id = %s AND ps.goals > 0
                GROUP BY p.id, t.id
                ORDER BY t.name, SUM(ps.goals) DESC
                """
                
                scorers = self.execute_query(query, (stadium_id,), fetch=True)
                
                if scorers:
                    print(f"\n ИГРОКИ, ЗАБИВАВШИЕ МЯЧИ:")
                    current_team = ""
                    for scorer in scorers:
                        player_name = self.safe_str(scorer[0])
                        team_name = self.safe_str(scorer[1])
                        goals = self.safe_int(scorer[2])
                        
                        if team_name != current_team:
                            print(f"    {team_name}:")
                            current_team = team_name
                        print(f"      • {player_name} - {goals} голов")
                else:
                    print(f"\n На этом стадионе никто не забивал мячей")
                
            else:
                print("Неверный номер стадиона")
        except ValueError:
            print("Введите число")
        
        input("\n Нажмите Enter...")
    
    def show_admin_menu(self):
        print("АДМИНИСТРИРОВАНИЕ")
        
        while True:
            print("\n1. Сменить тренера")
            print("2. Перевести игрока в другую команду")
            print("3. Отменить встречу")
            print("4. Назад")
            
            choice = input("\n Выберите опцию (1-4): ").strip()
            
            if choice == '1':
                self.change_coach()
            elif choice == '2':
                self.transfer_player()
            elif choice == '3':
                self.cancel_match()
            elif choice == '4':
                break
            else:
                print("Неверный выбор")
    
    def change_coach(self):
        print("\n СМЕНА ТРЕНЕРА")
               
        query = "SELECT coach FROM teams WHERE name = 'Краснодар-U18'"
        result = self.execute_query(query, fetch=True)
        
        if result:
            current_coach = self.safe_str(result[0][0])
            print(f"Текущий тренер: {current_coach}")
        else:
            current_coach = "Неизвестен"
            print("Не удалось получить текущего тренера")

        new_coach = input("\nВведите ФИО нового тренера: ").strip()
        
        if not new_coach:
            print("Введите ФИО тренера")
            input("\n Нажмите Enter...")
            return
        
        if new_coach == current_coach:
            print("Новый тренер совпадает с текущим")
            if not self.confirm_action("Продолжить?"):
                print("Изменение отменено")
                input("\n Нажмите Enter...")
                return
        
        if self.confirm_action(f"Вы уверены, что хотите сменить тренера с '{current_coach}' на '{new_coach}'?"):
            update_query = "UPDATE teams SET coach = %s WHERE name = 'Краснодар-U18'"
            if self.execute_query(update_query, (new_coach,)):
                print(f"Тренер изменен на: {new_coach}")
            else:
                print("Ошибка при изменении тренера")
        else:
            print("Изменение отменено")
        
        input("\n Нажмите Enter...")
    
    def transfer_player(self):
        print("\n ПЕРЕВОД ИГРОКА В ДРУГУЮ КОМАНДУ")

        query = """
        SELECT p.id, p.full_name, p.number, p.position 
        FROM players p
        JOIN player_stats ps ON p.id = ps.player_id
        WHERE ps.team_id = 1
        GROUP BY p.id, p.full_name, p.number, p.position
        ORDER BY p.full_name
        """
        
        players = self.execute_query(query, fetch=True)
        
        if not players:
            print("Нет игроков в команде Краснодар-U18")
            input("\n Нажмите Enter...")
            return
        
        print("\n ИГРОКИ КРАСНОДАР-U18:")
        for i, p in enumerate(players, 1):
            print(f"{i}. {self.safe_str(p[1])} (№{self.safe_int(p[2])}, {self.safe_str(p[3])})")
        
        try:
            player_choice = int(input("\n Выберите номер игрока для перевода: "))
            if 1 <= player_choice <= len(players):
                player_id = players[player_choice-1][0]
                player_name = players[player_choice-1][1]

                query = """
                SELECT id, name, city 
                FROM teams 
                WHERE id != 1
                ORDER BY name
                """
                
                teams = self.execute_query(query, fetch=True)
                
                if not teams:
                    print("Нет других команд для перевода")
                    input("\n Нажмите Enter...")
                    return
                
                print(f"\n КУДА ПЕРЕВЕСТИ ИГРОКА {player_name}?")
                for i, t in enumerate(teams, 1):
                    print(f"{i}. {self.safe_str(t[1])} ({self.safe_str(t[2])})")
                
                team_choice = int(input("\n Выберите номер команды: "))
                
                if 1 <= team_choice <= len(teams):
                    new_team_id = teams[team_choice-1][0]
                    new_team_name = teams[team_choice-1][1]
                    
                    print(f"\n ВНИМАНИЕ: Вы собираетесь перевести игрока:")
                    print(f"   Игрок: {player_name}")
                    print(f"   ИЗ: Краснодар-U18")
                    print(f"   В: {new_team_name}")
                    
                    if self.confirm_action("Вы уверены?"):
                        check_query = "SHOW COLUMNS FROM players LIKE 'team_id'"
                        has_team_id = self.execute_query(check_query, fetch=True)
                        
                        if has_team_id:
                            update_query = "UPDATE players SET team_id = %s WHERE id = %s"
                        else:
                            update_query = None
                        
                        update_stats_query = """
                        UPDATE player_stats 
                        SET team_id = %s 
                        WHERE player_id = %s AND team_id = 1
                        """
                        
                        success = True
                        
                        if update_query:
                            if not self.execute_query(update_query, (new_team_id, player_id)):
                                print("Ошибка при обновлении основной информации игрока")
                                success = False
                        
                        if not self.execute_query(update_stats_query, (new_team_id, player_id)):
                            print("Ошибка при обновлении статистики игрока")
                            success = False
                        
                        if success:
                            print(f"Игрок {player_name} успешно переведен в {new_team_name}")
                        else:
                            print("Ошибка при переводе игрока")
                    else:
                        print("Перевод отменен")
                else:
                    print("Неверный номер команды")
            else:
                print("Неверный номер игрока")
        except ValueError:
            print("Введите число")
        
        input("\n Нажмите Enter...")
    
    def cancel_match(self): 
        print("\n ОТМЕНА ВСТРЕЧИ")
        
        query = """
        SELECT m.id, m.match_date, h.name, a.name, s.name
        FROM matches m
        JOIN teams h ON m.home_team_id = h.id
        JOIN teams a ON m.away_team_id = a.id
        JOIN stadiums s ON m.stadium_id = s.id
        WHERE m.match_date > NOW()
        ORDER BY m.match_date
        """
        
        matches = self.execute_query(query, fetch=True)
        
        if not matches:
            print("Нет запланированных встреч")
            input("\n Нажмите Enter...")
            return
        
        print("\n ВЫБЕРИТЕ ВСТРЕЧУ ДЛЯ ОТМЕНЫ:")
        for i, m in enumerate(matches, 1):
            date_str = self.format_date(m[1])
            home_team = self.safe_str(m[2])
            away_team = self.safe_str(m[3])
            stadium = self.safe_str(m[4])
            print(f"{i}. {date_str}: {home_team} - {away_team} на {stadium}")
        
        try:
            choice = int(input("\n Выберите номер встречи: "))
            if 1 <= choice <= len(matches):
                match_id = matches[choice-1][0]
                match_date = self.format_date(matches[choice-1][1])
                home_team = self.safe_str(matches[choice-1][2])
                away_team = self.safe_str(matches[choice-1][3])
                
                print(f"\n ВНИМАНИЕ: Вы собираетесь отменить встречу:")
                print(f"   Дата: {match_date}")
                print(f"   Матч: {home_team} - {away_team}")
                
                if self.confirm_action("Вы уверены?"):
                    # Удаление
                    queries = [
                        "DELETE FROM tickets WHERE match_id = %s",
                        "DELETE FROM player_stats WHERE match_id = %s",
                        "DELETE FROM matches WHERE id = %s"
                    ]
                    
                    success = True
                    for q in queries:
                        if not self.execute_query(q, (match_id,)):
                            success = False
                            break
                    
                    if success:
                        print("Встреча успешно отменена")
                    else:
                        print("Ошибка при отмене встречи")
                else:
                    print("Отмена встречи отменена")
            else:
                print("Неверный номер")
        except ValueError:
            print("Введите число")
        
        input("\n Нажмите Enter...")

def main():
    print("СИСТЕМА УПРАВЛЕНИЯ ФУТБОЛЬНЫМ КЛУБОМ КРАСНОДАР-U18")
    
    db = FootballDB()
    
    if db.connection and db.connection.is_connected():
        db.show_menu()
    else:
        print("Не удалось подключиться к базе данных")
        print("Проверьте настройки подключения")

if __name__ == "__main__":
    main()