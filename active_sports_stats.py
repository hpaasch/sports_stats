import psycopg2

conn = psycopg2.connect("dbname=learning_sql user=dbperson")
cur = conn.cursor()


def skier_main(cursor, connection):
    print("This is a database of skiers from the 1988 Olympic Women's downhill.")
    user_inquiry = input("1: Lookup skier by name? \n"
                         "2: Add a new skier? \n"
                         "3: List oldest skiers? \n"
                         "4: List youngest skiers? \n"
                         "5: Top skiers sorted by age\n"
                         "6: Quit? \n ").lower()
    if user_inquiry == '1':
        skier_inquiry(cursor, connection)
    elif user_inquiry == '3':
        skier_old(cursor, connection)
    elif user_inquiry == '4':
        skier_young(cursor, connection)
    elif user_inquiry == '2':
        add_new_skier(cursor, connection)
    elif user_inquiry == '5':
        skier_sort(cursor, connection)
    else:
        print("Schussboomers unite! Bye Bye ")


def skier_inquiry(cursor, connection):
    hero = input("Enter a skier from the 1988 Olympics (hint: Karen Percy): ")

    cursor.execute("SELECT * FROM sports_data WHERE athlete = %s;", (hero,))
    results = cursor.fetchone()
    if results is None:
        user_add = input("Sorry, but skier name isn't in database. Want to add? Y/n ").lower()
        print('-' * 40)
        if user_add == 'y':
            add_new_skier(cursor, connection)
        else:
            skier_main(cursor, connection)
    else:
        print("Great memory! Excellent skier!")
        print("Skier: {}\n"
              "Medal: {}\n"
              "Rank: {}\n"
              "Team: {}\n"
              "Time: {}\n"
              "Age: {}".format(results[1], results[5], results[0], results[3], results[6], results[2]))
        make_change = input("Need to update team? Y/n ")
        if make_change == 'y':
            new_team = (input("Input new team country name "))

            cursor.execute("UPDATE sports_data SET team = %s WHERE athlete = %s;", (new_team, results[1]))
            connection.commit()
            print("Thanks for the updated team info.")
        print('_' * 40)
        skier_main(cursor, connection)


def skier_old(cursor, connection):
    old_skiers = int(input("Enter cutoff age. Results will be that age or older. "))
    cursor.execute("SELECT * FROM sports_data WHERE age >= %s ORDER BY age DESC;", (old_skiers,))
    results = cursor.fetchall()
    print("Not too old to schuss like a pro.")
    for row in results:
        print("Age: {}, Skier: {}".format(row[2], row[1]))
    print('-' * 40)
    skier_main(cursor, connection)


def skier_young(cursor, connection):
    young_skiers = int(input("Enter cutoff age. Results will be that age or younger. "))
    cursor.execute("SELECT * FROM sports_data WHERE age <= %s ORDER BY age ASC;", (young_skiers,))
    results = cursor.fetchall()
    for row in results:
        print("Age: {}, Skier: {}".format(row[2], row[1]))
    print('-' * 40)
    skier_main(cursor, connection)


def add_new_skier(cursor, connection):
    athlete = input("What cartoon character should've competed in the 1988 Olympics? ")
    while True:
        try:
            rank = int(input("Where would s/he have finished (1-25)? "))
            break
        except ValueError:
            print("Oopsies. Requires a 2-digit number only. Try again.")
    while True:
        try:
            age = int(input("Age in 1988? "))
            break
        except ValueError:
            print("Oopsies. Requires a 2-digit number only. Try again.")
    team = input("Perfect to represent what country? ")
    noc = input("3-character country symbol is: ")
    medal = input("Enter gold, silver or bronze: ")
    t_time = input("How many seconds to finish what's usually a 90-second run? ")

    cursor.execute("INSERT INTO sports_data VALUES (%s, %s, %s, %s, %s, %s, %s);",
                   (rank, athlete, age, team, noc, medal, t_time))

    connection.commit()

    print("Thanks for adding to our database of excellent skiers from 1988.")
    print('-' * 40)
    skier_main(cursor, connection)


def skier_sort(cursor, connection):
    rank = int(input("See the top skiers sorted by age by entering a ranking cutoff 1-30: "))

    cursor.execute("SELECT rank, athlete, age FROM sports_data "
                   "WHERE rank <= %s ORDER BY age DESC, rank ASC;", (rank,))
    results = cursor.fetchall()
    print("Skiers ranked at or above {}, sorted by age and then rank:".format(rank))
    for row in results:
        print("Age: {}, Rank: {}, Skier: {}".format(row[2], row[0], row[1]))
    print('-' * 40)
    skier_main(cursor, connection)


skier_main(cur, conn)
cur.close()
conn.close()
