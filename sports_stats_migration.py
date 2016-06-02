# this populates the table
import csv
import psycopg2

connection = psycopg2.connect("dbname=learning_sql user=dbperson")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS sports_data;")

table_create_command = """CREATE TABLE sports_data (
  rank NUMERIC (2),
  athlete VARCHAR (50),
  age NUMERIC (2),
  team VARCHAR (40),
  NOC VARCHAR (5),
  medal VARCHAR (12),
  t_time VARCHAR (10)
);"""

cursor.execute(table_create_command)
# connection.commit()

with open("ski_stats") as outfile:
    ski = csv.DictReader(outfile, fieldnames=["rank", "athlete", "age", "team", "NOC", "medal", "t_time"])

    for row in ski:
        print(row)
        cursor.execute("INSERT INTO sports_data VALUES (%s, %s, %s, %s, %s, %s, %s);",
                       (int(row['rank']), row['athlete'],
                        int(row['age']), row['team'], row['NOC'], row['medal'], row['t_time']))

connection.commit()

cursor.close()
connection.close()
