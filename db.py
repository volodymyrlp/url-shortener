import pymysql


def get_connection():
    connection = pymysql.connect(
        host='mysql',
        port=3306,
        user="root",
        password="secret123",
        database="urlshortener"
    )
    return connection


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS links (
            id INT AUTO_INCREMENT PRIMARY KEY,
            short_code VARCHAR(10) NOT NULL,
            original_url TEXT NOT NULL,
            clicks INT DEFAULT 0
        )
        """)
    conn.commit()
    conn.close()
    print("Everything is ready!")


if __name__ == '__main__':
    init_db()
