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
    
def get_transactions(type = None, category_id = None, start_date = None, end_date = None, search_text = None, order_by = None, order_dir = "ASC"):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    if type is not None:
        query += " AND type = ?"
        params.append(type)
    
    if category_id is not None:
        query += " AND category_id = ?"
        params.append(category_id)
    
    if start_date is not None:
        query += " AND date >= ?"
        params.append(start_date)
        
    if end_date is not None:
        query += " AND date <= ?"
        params.append(end_date)
    
    if search_text is not None:
        query += " AND description LIKE ?"
        params.append(f"%{search_text}%")
        
    if order_by is not None:
        allowed_columns = ["date", "amount", "type", "category_id", "description"]
        if order_by in allowed_columns:
            if order_dir.upper() in ["ASC", "DESC"]:
                query += f" ORDER BY {order_by} {order_dir.upper()}"
            else:
                query += f" ORDER BY {order_by} ASC"
        
    
    
        
    cursor.execute(query, params)    
    results = cursor.fetchall()
    conn.close()
    return results
   
if __name__ == '__main__':
    initialize_db()
    