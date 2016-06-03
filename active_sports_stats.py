import psycopg2

connection = psycopg2.connect("dbname=learning_sql user=dbperson")
cursor = connection.cursor()


def skier_main():
    print("This is a database of skiers from the 1988 Olympic Women's downhill.")
    user_inquiry = input("1: Lookup skier by name? \n"
                         "2: Add a new skier? \n"
                         "3: List oldest skiers? \n"
                         "4: List youngest skiers? \n"
                         "5: Top skiers sorted by age\n"
                         "6: Quit? \n ").lower()
    if user_inquiry == '1':
        skier_inquiry()
    elif user_inquiry == '3':
        skier_old()
    elif user_inquiry == '4':
        skier_young()
    elif user_inquiry == '2':
        add_new_skier()
    elif user_inquiry == '5':
        skier_sort()
    else:
        print("Schussboomers unite! Bye Bye ")


def skier_inquiry():
    hero = input("Enter a skier from the 1988 Olympics (hint: Karen Percy): ")

    cursor.execute("select * from sports_data where athlete = %s;", (hero,))
    results = cursor.fetchone()
    if results is None:
        user_add = input("Sorry, but skier name isn't in database. Want to add? Y/n ").lower()
        if user_add == 'y':
            add_new_skier()
        else:
            skier_main()
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

            cursor.execute("UPDATE sports_data SET team = %s where athlete = %s;", (new_team, results[1]))
            connection.commit()
            print("Thanks for the updated team info.")
        print('_' * 40)
        skier_main()


def skier_old():
    old_skiers = int(input("Enter cutoff age. Results will be that age or older. "))
    cursor.execute("select * from sports_data where age >= %s;", (old_skiers,))
    results = cursor.fetchall()
    print("Not too old to schuss like a pro.")
    for row in results:
        print("Age: {}, Skier: {}".format(row[2], row[1]))
    print('-' * 40)
    skier_main()


def skier_young():
    young_skiers = int(input("Enter cutoff age. Results will be age or younger. "))
    cursor.execute("select * from sports_data where age <= %s;", (young_skiers,))
    results = cursor.fetchall()
    for row in results:
        print("Age: {}, Skier: {}".format(row[2], row[1]))
    print('-' * 40)
    skier_main()


def add_new_skier():
    athlete = input("What cartoon character should've competed in the 1988 Olympics? ")
    rank = int(input("Where would s/he have finished (1-25)? "))
    age = int(input("Age in 1988? "))
    team = input("Perfect to represent what country? ")
    noc = input("3-character country symbol is: ")
    medal = input("Enter gold, silver or bronze: ")
    t_time = input("How many seconds to finish what's usually a 90-second run? ")

    cursor.execute("INSERT INTO sports_data VALUES (%s, %s, %s, %s, %s, %s, %s);",
                   (rank, athlete, age, team, noc, medal, t_time))
    connection.commit()

    print("Thanks for adding to our database of excellent skiers from 1988.")
    print('-' * 40)
    skier_main()


def skier_sort():
    rank = int(input("See the top skiers sorted by age by entering a ranking cutoff 1-30: "))

    cursor.execute("SELECT rank, athlete, age FROM sports_data "
                   "WHERE rank <= %s ORDER BY age DESC, rank ASC;", (rank,))
    results = cursor.fetchall()
    print("Top 10 skiers sorted by age:")
    for row in results:
        print("Age: {}, Rank: {}, Skier: {}".format(row[2], row[0], row[1]))
    print('-' * 40)
    skier_main()


skier_main()
cursor.close()
connection.close()
