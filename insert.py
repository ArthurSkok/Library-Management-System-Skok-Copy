import sqlite3
import csv

def main():

    with open('books1.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            id = reader.line_num - 1
            title = row[1]
            subtitle = row[2]
            authors = row[3]
            genre = row[4]

            if subtitle != '':
                title = title + ': ' + subtitle
            
            try:
                sqlite_connect = sqlite3.connect('library.db')
                cursor = sqlite_connect.cursor()
                sqlite_insert = """INSERT INTO "books"
                                  (id, title, authors, genre, availability) 
                                  VALUES (?, ?, ?, ?, ?);"""

                data = (id, title, authors, genre, 'In Stock')
                cursor.execute(sqlite_insert, data)
                sqlite_connect.commit()
                print("Successfully inserted book #", id, "into the Books table")

                cursor.close()

            except sqlite3.Error as err:
                print("Failed to insert book #", id, "into the Books table because of ", err)

            finally:
                if sqlite_connect:
                    sqlite_connect.close()

if __name__=="__main__":
    main()