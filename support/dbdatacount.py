# define "db_data_count" function
def db_data_count(db_name: str, username: str, password: str, db_host: str, db_port: str):
    # importing python module:S01
    try:
        import psycopg2
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Count:S01] - {str(error)}', 'row_count' : 0}

    # define db connection parameter:S02
    try:
        db_connection_parameter = {
            "dbname" : str(db_name),
            "user" : str(username),
            "password" : str(password),
            "host" : str(db_host),
            "port" : str(db_port)
        }
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Count:S02] - {str(error)}', 'row_count' : 0}
    
    # check if "incident_data" table present and fetch row count:S03
    try:
        with psycopg2.connect(**db_connection_parameter) as database_connection:  # type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute('''
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'incident_data'
                );''')
                table_exists = database_cursor.fetchone()[0]
                # check if "incident_data" table present
                if table_exists:
                    # fetch row count from "incident_data" table
                    database_cursor.execute('SELECT COUNT(*) FROM incident_data;')
                    records_count = database_cursor.fetchone()[0]
                    return {'status' : 'SUCCESS', 'message' : 'Total Rows Count Fetched For "incident_data" Table', 'row_count' : int(records_count)}
                else:
                    return {'status' : 'ERROR', 'message' : '"incident_data" Table Not Present Inside Database', 'row_count' : 0}
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Count:S03] - {str(error)}', 'row_count' : 0}