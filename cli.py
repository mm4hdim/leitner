import sys
import sqlite3
import csv
import urllib.request
import datetime

import leitner


class CLI:
    def __init__(self, db_path):
        con = sqlite3.connect(db_path)
        self.box = leitner.Box(con)


    def import_csv(self, path_to_csv):
        with open(path_to_csv,'r') as file:
            dr = csv.DictReader(file)
            self.box.import_db(dr)

    def import_gsheet(self, url):
        fname = '/tmp/' + 'leitner_gsheet_csv ' + str(datetime.datetime.now())
        urllib.request.urlretrieve(url,fname)
        self.import_csv(fname)


    def ask_question(self, card):
        print(f'******************************')
        print(f' ({card[0]}) in {card[6]}         {card[5][:10]}')
        print()
        print(f'\tquestion: {card[1]}')
        print(f'\thint:{card[2]}')
        input()
        print(f'\tanswer: {card[3]}')
        print(f'\tnote: {card[4]}\n')

        while (i := input('  true, false, skip, exit: ')) not in ['t','f','s', 'e']:
            pass
        
        print(f'******************************')

        return i
    

    def start(self):
        answer = []

        for card in self.box.get():
            i = self.ask_question(card)


            if i == 't':
                answer.append((card[0], True))
            elif i == 's':
                answer.append((card[0], None))
            elif i == 'e':
                break
            else:
                answer.append((card[0], False))

        else:
            print('this will be run')
            self.box.save(answer)


    def show(self):
        for card in self.box.list_cards():
            print(f'({card[0]})\tin {card[6]}\t{card[1]}: {card[3]}')
            


    def add(self):
        ids = list(map(int, input('enter ids for adding to the loop:').strip().split(' ')))

        self.box.add_to_loop(ids)





if __name__ == '__main__':
    command = sys.argv[1]
    db_path = sys.argv[2]


    cli = CLI(db_path)


    match command:
        case 'create':
            cli.box.prepare_db()

        case 'start':
            cli.start()
            
        case 'import':
            path_to_csv = sys.argv[3]
            cli.import_csv(path_to_csv)

        case 'gsheet':
            url = sys.argv[3]
            cli.import_gsheet(url)

        case 'show':
            cli.show()

        case 'add':
            cli.add()

        case _:
            print('command not found!')
            

