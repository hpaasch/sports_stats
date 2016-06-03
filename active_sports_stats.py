import psycopg2

connection = psycopg2.connect("dbname=learning_sql user=dbperson")
cursor = connection.cursor()


def skier_main():
    print("This is a database of skiers from the 1988 Olympic Women's downhill.")
    user_inquiry = input("N: Lookup skier by name? \n"
                         "A: Add a new skier? \n"
                         "O: List oldest skiers? \n"
                         "Y: List youngest skiers? \n"
                         "Q: Quit? \nn/a/o/y/q ").lower()
    if user_inquiry == 'n':
        skier_inquiry()
    elif user_inquiry == 'o':
        skier_old()
    elif user_inquiry == 'y':
        skier_young()
    elif user_inquiry == 'a':
        add_new_skier()
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
    old_skiers = int(input("Enter cutoff age. Results will be >= age. "))
    cursor.execute("select * from sports_data where age >= %s;", (old_skiers,))
    results = cursor.fetchall()
    print("Not too old to schuss like a pro.")
    for row in results:
        print("Age: {}, Skier: {}".format(row[2], row[1]))
    print('-' * 40)
    skier_main()


def skier_young():
    young_skiers = int(input("Enter cutoff age. Results will be <= age. "))
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

skier_main()
cursor.close()
connection.close()
