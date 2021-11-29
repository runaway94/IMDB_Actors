from IMDB_Actors.data import create_databases, save_to_database

if __name__ == '__main__':
    # create_databases.create_databases("localhost", "anna", "1234")
    # test = "INSERT INTO actors VALUES ({1}, {2});"
    # #test.format(1, "Anna")
    # print(test)
    # txt1 = "INSERT INTO actors VALUES ({id}, {name}, {age}, {gender}, {nationality}, {bio}, {pos});".format(id=1, name="\'Anna\'", age=27, gender="\'w\'", nationality="\'german\'", bio="\'coole socke\'", pos=1)
    # print(txt1)
    # sqlText="\"\"" + txt1 + "\"\"";
    # print(sqlText)
    save_to_database.save_actor()