import json
import sqlite3
import random

def main():
    conn = sqlite3.connect('cars_dealers.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dealers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            City TEXT,
            Address TEXT,
            Area TEXT,
            Rating REAL
        )
    ''')

    with open('dilers .json', 'r', encoding='utf-8') as f:
        dealers_data = json.load(f)
        dealers = dealers_data if isinstance(dealers_data, list) else dealers_data.get('dealers', [])

    for dealer in dealers:
        cursor.execute('''
            INSERT INTO dealers (Name, City, Address, Area, Rating)
            VALUES (?, ?, ?, ?, ?)
        ''', (dealer['Name'], dealer['City'], dealer['Address'], dealer['Area'], dealer['Rating']))

    cursor.execute('SELECT id FROM dealers')
    dealer_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firm TEXT,
            model TEXT,
            year INTEGER,
            power INTEGER,
            color TEXT,
            price INTEGER,
            dealer_id INTEGER REFERENCES dealers(id) ON DELETE CASCADE
        )
    ''')

    with open('cars .json', 'r', encoding='utf-8') as f:
        cars_data = json.load(f)
        cars = cars_data.get('cars', [])

    for car in cars:
        random_dealer_id = random.choice(dealer_ids)
        cursor.execute('''
            INSERT INTO cars (firm, model, year, power, color, price, dealer_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (car['firm'], car['model'], car['year'], car['power'], car['color'], car['price'], random_dealer_id))

    conn.commit()
    conn.close()
    print("База данных создана успешно")

if __name__ == "__main__":
    main()
