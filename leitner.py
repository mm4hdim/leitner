import datetime


class Box:

    def __init__(self, db_connection):
        self.connection = db_connection
        self.cursor = self.connection.cursor()



    def prepare_db(self):
        sql = '''CREATE TABLE cards (
                id INTEGER PRIMARY KEY,
                question TEXT,
                hint TEXT,
                answer TEXT,
                note TEXT,
                datetime timestamp,
                position INTEGER
             )'''

        self.cursor.execute(sql)
        # search when we neet to commit
        # self.connection.commit()



    def import_db(self, words):
        for word in words:
            self.cursor.execute('''INSERT INTO cards (question, hint, answer, note, datetime, position) VALUES ( ?, ?, ?, ?, ?, ?)''',
                (word['question'], word['hint'], word['answer'], word['note'], datetime.datetime.now(), 0))

        self.connection.commit()


    def export_db(self):
        pass



    def add_card(self, word):
        pass


    def edit_card(self, id):
        pass


    def list_cards(self):
        self.cursor.execute('SELECT * FROM cards')
        cards = self.cursor.fetchall()
        return cards
    

    def add_to_loop(self, ids):
        for id in ids:
            self.cursor.execute('UPDATE cards SET position = 1 WHERE position = 0 AND id = ?',(id,))

        self.connection.commit()


    def get(self):
        self.cursor.execute('SELECT * FROM cards WHERE position IN (30, 15, 7, 3, 1) ORDER BY position DESC')
        cards = self.cursor.fetchall()
        return cards


    # id -> status
    def save(self, cards_status):
        self.cursor.execute('SELECT id, position  FROM cards WHERE position IN (30, 15, 7, 3, 1) ORDER BY position DESC')
        cards = self.cursor.fetchall()

        # check the list
        db_ids, _ = zip(*cards)
        st_ids, _ = zip(*cards_status)

        # print(db_ids)
        # print(st_ids)

        if db_ids != st_ids:
            return False
        
        self.cursor.execute('UPDATE cards SET position = position + 1 WHERE position BETWEEN 1 AND 30')

        for id, status in cards_status:

            if status == True:
                pass
            elif status == None:
                self.cursor.execute('UPDATE cards SET position = position - 1 WHERE id = ?',(id,))
            else: # status equal to False or other
                self.cursor.execute('UPDATE cards SET position = 1 WHERE id = ?',(id,))
        
        self.connection.commit()

        return True
