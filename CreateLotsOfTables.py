import oracledb

from faker import Faker

fake = Faker()
Faker.seed(0)

tables = []
username = 'APP_USER'



with open("/Users/dgiles/Downloads/create_tables.sql", "w+") as ctsql, open("/Users/dgiles/Downloads/grant_access.sql", "w+") as gsql, open("/Users/dgiles/Downloads/drop_tables.sql", "w+") as tsql:
    for i in range(1,1000):
        table_name = fake.company().replace(' ','_').replace(',','').replace('-','_')
        ctsql.write(f"CREATE TABLE IF NOT EXISTS {table_name} (column1 number, column2 number, column3 number);\n" )
        gsql.write(f"GRANT SELECT, UPDATE, INSERT ON {table_name} TO {username};\n")
        tsql.write(f"DROP TABLE IF EXISTS {table_name};\n")


