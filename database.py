import sqlite3

DB_NAME = "finanzen.db"
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES categories(id)
            )
        """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            category_id INTEGER,
            description TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
            )
    """)
        
    
    
    conn.commit()
    conn.close()

def add_category(name, parent_id = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO categories (name, parent_id)
        VALUES (?, ?)
        """, (name, parent_id))
    conn.commit()
    conn.close()
    
def get_categories(parent_id = None):
    conn = get_connection()
    cursor = conn.cursor()
    if parent_id is None:
        cursor.execute("SELECT * FROM categories WHERE parent_id is NULL",)
    else:
        cursor.execute("SELECT * FROM categories WHERE parent_id = ?",(parent_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def update_category(category_id, new_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE categories SET name = ? WHERE id = ?
        """, (new_name, category_id))
    conn.commit()
    conn.close()
    
def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM categories WHERE id = ?
        """, (category_id,))
    conn.commit()
    conn.close()

def add_transaction(date, amount, type, category_id, description = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (date, amount, type, category_id, description)
        VALUES (?, ?, ?, ?, ?)
    """, (date, amount, type, category_id, description))
    conn.commit()
    conn.close()
   
if __name__ == '__main__':
    initialize_db()
    print("Database initialized")
    add_category("Reinigung")
    add_category("Holz")
    add_category("Putzmittel", parent_id=1)
    print(get_categories())

    update_category(1, "Haushalt")
    print(get_categories())

    delete_category(2)
    print(get_categories())