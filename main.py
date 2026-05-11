import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Параметри підключення з docker-compose.yml
USER = 'my_user'
PASSWORD = 'my_password'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'my_database'

# Строка підключення SQLAlchemy (через mysql-connector-python)
DATABASE_URI = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"


def get_db_engine():
    """Створює підключення до бази з реалізацією retry-логіки."""
    engine = create_engine(DATABASE_URI)
    max_retries = 10

    for attempt in range(1, max_retries + 1):
        try:
            # Спроба підключитись
            with engine.connect() as conn:
                print("Успішно підключено до бази даних MySQL!")
                return engine
        except OperationalError:
            print(f"Спроба {attempt}/{max_retries}: База ще не готова. Повторна спроба через 10 секунд...")
            time.sleep(10)

    raise Exception("Не вдалося підключитися до бази даних після 10 спроб.")


def main():
    try:
        engine = get_db_engine()
        query = "SELECT * FROM titanic"

        # Зчитуємо дані з бази у pandas DataFrame
        df = pd.read_sql(query, engine)

        print("\n--- Результати ---")
        print(f"Завантажено рядків: {df.shape[0]}")
        print(f"Завантажено колонок: {df.shape[1]}")

        print("\nФрагмент даних (перші 5 рядків):")
        print(df.head())

        # Перевірка на NULL (NaN)
        print("\nПеревірка на порожні значення:")
        print(df[['Age', 'Cabin', 'Embarked']].isna().sum())

    except Exception as e:
        print(f"Сталася помилка: {e}")


if __name__ == "__main__":
    main()