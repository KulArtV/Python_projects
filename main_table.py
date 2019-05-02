import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("deadline_main_database.db",
                                     check_same_thread=False)
        self.main_cursor = self.conn.cursor()
        self.main_cursor.execute("""CREATE TABLE 
                                    IF NOT EXISTS deadline_main_database
                                   (chat_id integer, deadline_id integer)""")

        self.main_cursor.execute("""CREATE TABLE IF NOT EXISTS deadline_type_one
                                   (deadline_id integer, type text, 
                                   subject text, name text, 
                                   estimate_time integer, dead_time text,
                                   status integer)""")

        self.main_cursor.execute("""CREATE TABLE IF NOT EXISTS deadline_type_two
                                   (deadline_id integer, type text, 
                                   subject text, name text, 
                                   estimate_time integer, dead_time text,
                                   status integer)""")
        query = "SELECT max(deadline_id) FROM deadline_main_database"
        amount_query = "SELECT count(deadline_id) FROM deadline_main_database"
        self.main_cursor.execute(query)
        query_result_tuple = self.main_cursor.fetchone()
        self.main_cursor.execute(amount_query)
        amount_query_result_tuple = self.main_cursor.fetchone()

        if amount_query_result_tuple[0] > 0:
            self.last_deadline_id = query_result_tuple[0] + 1
        else:
            self.last_deadline_id = 0

    def insert_in_type_one(self, new_deadline):
        self.main_cursor.execute("INSERT INTO deadline_type_one "
                                 "VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 (self.last_deadline_id, new_deadline.type,
                                  new_deadline.subject, new_deadline.name,
                                  new_deadline.estimate_time,
                                  new_deadline.dead_time,
                                  new_deadline.status))
        self.conn.commit()

    def insert_in_type_two(self, new_deadline):
        self.main_cursor.execute("INSERT INTO deadline_type_two "
                                 "VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 (self.last_deadline_id, new_deadline.type,
                                  new_deadline.subject, new_deadline.name,
                                  new_deadline.estimate_time,
                                  new_deadline.dead_time,
                                  new_deadline.status))
        self.conn.commit()

    def insert_deadline(self, chat_id_to_insert, new_deadline):
        self.main_cursor.execute(
            "INSERT INTO deadline_main_database VALUES (?,?)",
            (chat_id_to_insert, self.last_deadline_id))
        self.conn.commit()
        if new_deadline.type == 'home':
            self.insert_in_type_one(new_deadline)
        elif new_deadline.type == 'study':
            self.insert_in_type_two(new_deadline)
        self.last_deadline_id += 1

    def get_all_deadlines(self, chat_id):
        sql = '''
              SELECT deadline_type_one.name, deadline_type_one.subject,
                     deadline_type_one.estimate_time, deadline_type_one.dead_time
              FROM deadline_main_database
              INNER JOIN deadline_type_one 
              ON deadline_type_one.deadline_id = 
                 deadline_main_database.deadline_id
              WHERE deadline_main_database.chat_id == chat_id
              UNION
              SELECT deadline_type_two.name, deadline_type_two.subject,
                     deadline_type_two.estimate_time, deadline_type_two.dead_time
              FROM deadline_main_database
              INNER JOIN deadline_type_two 
              ON deadline_type_two.deadline_id = 
                 deadline_main_database.deadline_id
              WHERE deadline_main_database.chat_id == chat_id
        '''
        self.main_cursor.execute(sql)
        return self.main_cursor.fetchall()
