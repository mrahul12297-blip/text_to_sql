import os
import sqlite3
import pandas as pd


DATABASE = "ecommerce.db"
DATA_FOLDER = "data"


connection = sqlite3.connect(DATABASE)

for file in os.listdir(DATA_FOLDER):

    if file.endswith(".csv"):

        file_path = os.path.join(DATA_FOLDER, file)

        table_name = file.replace(".csv", "")

        df = pd.read_csv(file_path)

        df.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )

        print(f"Loaded {file} → {table_name}")


connection.close()

print("\nDatabase created successfully!")