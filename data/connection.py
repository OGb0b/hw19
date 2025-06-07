import psycopg2

try:
    conn = psycopg2.connect(
        user = 'postgres',
        password='0000',
        host='127.0.0.1',
        port='5432',
        database='postgres'
    )
except Exception as e:
    print('Ошибка подключения к базе данных')

cur = conn.cursor()


def add_user(input_id, username):
    try:
        cur.execute(
            """
            SELECT id from users
            """
        )
        users_id = cur.fetchall()
        for user_id in users_id:
            if user_id[0] == input_id:
                return True
        cur.execute(
            """
            INSERT INTO users (id, username)
            VALUES (%s, %s)
            """,
            (input_id, username,)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return False


def add_note(note_text, user_id):
    try:
        cur.execute(
            """
            INSERT INTO notes (note_text, user_id)
            VALUES (%s, %s)
            """,
            (note_text, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False


def show_user_notes(user_id):
    try:
        cur.execute(
            """
            SELECT id, note_text from notes where user_id = %s ORDER BY id
            """,
            (user_id,)
        )
        notes = cur.fetchall()
        if not notes:
            return "📭 У вас пока нет заметок."
        notes_list = [f"{i+1}. {note[1]}" for i, note in enumerate(notes)]
        return "📋 Ваши заметки:\n\n" + "\n".join(
            f"{note}" for i, note in enumerate(notes_list)
        )
    except Exception as e:
        conn.rollback()
        return f"Произошла ошибка при получении заметок:{e}"


def show_notes_to_delete(user_id):
    try:
        cur.execute(
            """
            SELECT id, note_text from notes where user_id = %s ORDER BY id
            """,
            (user_id,)
        )
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        return f"Произошла ошибка при получении заметок:{e}"

def delete_note(note_id, user_id):
    try:
        cur.execute(
            """
            DELETE FROM notes where id = %s AND user_id = %s""",
            (note_id, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return f"Произошла ошибка при удалении: {e}"