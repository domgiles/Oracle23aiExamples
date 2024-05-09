import argparse

import oracledb


def install_schema(args):
    dba_username = args.dba_user
    dba_password = args.dba_password
    user_name = args.user
    password = args.password
    hostname = args.hostname
    database = args.database
    connect_string = args.connectionstring

    if connect_string is None:
        connect_string = f"//{hostname}/{database}"

    try:
        with oracledb.connect(user=dba_username, password=dba_password, dsn=connect_string, mode=oracledb.AUTH_MODE_SYSDBA) as dba_connection:
            with dba_connection.cursor() as cursor:
                cursor.execute(f'DROP USER IF EXISTS {user_name} CASCADE ')
                cursor.execute(f'CREATE USER {user_name} IDENTIFIED BY {password} ')
                cursor.execute(f"ALTER USER {user_name} DEFAULT TABLESPACE USERS QUOTA UNLIMITED ON USERS")
                cursor.execute(f"ALTER USER {user_name} TEMPORARY TABLESPACE TEMP")
                cursor.execute(f"GRANT CONNECT, RESOURCE, DB_DEVELOPER_ROLE, CREATE MLE to {user_name}")
                cursor.execute(f"GRANT EXECUTE ON JAVASCRIPT to {user_name}")
    except Exception as ex:
        print(f"Failed to create schema {user_name} : {ex}")
        exit(-1)

    try:
        with oracledb.connect(user=user_name, password=password, dsn=connect_string) as user_connection:
            with user_connection.cursor() as cursor:
                cursor.execute("select * from all_objects where object_name = 'ORDS'")
                result_set = cursor.fetchmany()
                if len(result_set) > 0:
                    cursor.execute(f'''
                        begin
                            ORDS.enable_schema(
                                p_enabled             => TRUE,
                                p_schema              => '{user_name}',
                                p_url_mapping_type    => 'BASE_PATH',
                                p_url_mapping_pattern => '{user_name}',
                                p_auto_rest_auth      => TRUE
                              );
                        end;''')
                    cursor.execute(f'''
                        BEGIN
                            ORDS.ENABLE_OBJECT(
                                    p_object => 'CUSTOMERS_DV',
                                    p_object_type => 'VIEW'
                                );
                        END;''')
                    user_connection.commit()
                else:
                    print("ORDS hasn't been installed in the database")
                    exit(-1)
    except:
        print(f"Failed to enable the schema {user_name} for ORDS")
        exit(-1)
    print(f"Created schema {user_name}")
    exit(0)


def drop_schema(args):
    dba_username = args.dba_user
    dba_password = args.dba_password
    user_name = args.user
    hostname = args.hostname
    database = args.database
    connect_string = args.connectionstring

    if connect_string is None:
        connect_string = f"//{hostname}/{database}"

    try:
        with oracledb.connect(user=dba_username, password=dba_password, dsn=connect_string, mode=oracledb.AUTH_MODE_SYSDBA) as dba_connection:
            with dba_connection.cursor() as cursor:
                cursor.execute(f'DROP USER IF EXISTS {user_name} CASCADE ')
    except Exception as ex:
        print(f"Failed to drop user {user_name}")
        exit(-1)
    print(f"Dropped user {user_name}")
    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Installer', description='Install/Deinstall Oracle 23c Examples')
    group = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument('-du', '--dba_user', help='sys username', required=True)
    parser.add_argument('-dp', '--dba_password', help='sys password', required=True)
    parser.add_argument('-u', '--user', help='example schema name', required=True)
    parser.add_argument('-p', '--password', help='example schema password', required=True)
    parser.add_argument('-ho', '--hostname', help='hostmname of target database', required=False)
    parser.add_argument('-d', '--database', help='name of the database/service to run transactions against', required=False)
    parser.add_argument('-cs', '--connectionstring', help='a full connection string rather than using hostname and database', required=False)
    group.add_argument('-i', '--install', help='Install schema and configure ords for 23c Examples', action='store_true')
    group.add_argument('-di', '--deinstall', help='Drop schema for 23c Examples', action='store_true', required=False)

    args = parser.parse_args()

    if args.install:
        install_schema(args)
    elif args.deinstall:
        drop_schema(args)