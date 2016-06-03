import psycopg2

connection = psycopg2.connect("dbname=learning_sql user=dbperson")
cursor = connection.cursor()


def skier_main():
    print("This is a database of skiers from the 1988 Olympic Women's downhill.")
    user_inquiry = input("Lookup skier by (n)ame or (a)dd a new skier? or (Q)uit? n/a/q ").lower()
    if user_inquiry == 'n':
        skier_inquiry()
    elif user_inquiry == 'a':
        add_new_skier()
    else:
        print("Schussboomers unite! Bye Bye ")


def skier_inquiry():
    hero = input("Enter skier from the 1988 Olympics (hint: Karen Percy): ")

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
        print('_' * 40)
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
