from BD_Cred import init_db

def help():
    print(70*"-" + '''
exit (або e) << завершити виконання скрипту
a << список всіх авторів
q << список всіх цитат        
name:Steve Martin (або n:st) << список усіх цитат автора Steve Martin 
tags:life,love (або t:li,lo) << список цитат з тегами life або love
''' + 70*"-")
    

def main():
    db = init_db()
    if db is None:
        print(f"?? Немає з'єднання з базою даних.")
        exit()

    my_authors = db["authors"]
    my_qoutes = db["qoutes"]

    while True:
        try:
            consol = input("\nВведіть команду (h - допомога;  exit - вихід):\n>>>").strip()
            if consol[0] == 'e':    # exit (або e) << завершити виконання скрипту
                break
            elif consol[0] == 'h':
                help()
            elif consol[0] == 'a':  # a << список всіх авторів
                result = my_authors.find()
                if result:    
                    print("\n>> Список усіх авторів:")
                    for doc in result:
                        fullname = doc['fullname']
                        born_date = doc['born_date']
                        born_location = doc['born_location']
                        print(f"> fullname: {fullname}; born_date: {born_date};\nborn_location: {born_location}")

            elif consol[0] == 'q':  # q << список всіх цитат  
                result = my_qoutes.find()
                if result:   
                    print("\n>> Список усіх цитат:") 
                    for doc in result:
                        tags = doc['tags']
                        author = my_authors.find_one({'_id': doc['author']})["fullname"]
                        qoute = doc['quote']
                        print(f"author: {author}; tags: {tags};\nqoute: {qoute}")

            elif consol[0] == 'n':    # name:Steve Martin (або n:st) << список всіх цитат автора
                l = consol.split(':')
                author = None
                for a in my_authors.find():
                    if l[1][:2].lower() == a["fullname"][:2].lower():
                        author = a
                        break
                if author is None:
                    print(f"?? Такий автор {l[1]!r} мені не відомий")
                    continue

                name = author["fullname"]
                result = my_qoutes.find({"author": author['_id']})
                if result:   
                    print(f"\n>> Список усіх цитат {name!r}:") 
                    for doc in result:
                        print("> tags: ", doc['tags'])
                        print(f"  qoute: {doc['quote']}")
                else:
                    print(f"?? Жодної цитати з автором {name!r} не знайдено.")

            elif consol[0] == 't':  # tags:life,love (або t:li,lo) << список цитат, де є теги
                l = consol.split(':')
                l = set(l[1].split(','))
                for t in l:         # loop for every tag in l 
                    result = []
                    for q in my_qoutes.find():
                        tags = q["tags"]
                        for g in tags:
                            if t[:2].lower() == g[:2].lower():
                                result.append(q)
                                break
                    if result:
                        print(f"\n>> Список усіх цитат з тегом {t!r}:")
                        for doc in result:
                            name = my_authors.find_one({'_id': doc['author']})["fullname"]
                            print(f"> author: {name}  tags: {doc['tags']}")
                            print(f"  qoute: {doc['quote']}")
                    else:
                        print(f"?? Цитати з тегом {t!r} не знайдено.")                    

            else:
                print(f'?? така команда {consol!r} мені не відома')

        except ValueError as ve:
            print(ve)


if __name__ == '__main__':
    main()
