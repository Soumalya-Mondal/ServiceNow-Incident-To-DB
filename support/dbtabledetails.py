# define "db_table_details" function
def db_table_details(db_name: str, username: str, password: str, db_host: str, db_port: str) -> dict[str, str]:
    # importing python module:S01
    try:
        import psycopg2
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Create:S01] - {str(error)}'}

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
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Create:S02] - {str(error)}'}

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
                    # check "records_count"
                    if (int(records_count) == 0):
                        # drop table
                        database_cursor.execute('DROP TABLE incident_data')
                    else:
                        return {'status' : 'INFO', 'message' : f'"incident_data" Table Already Present; {records_count} Rows Present'}
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Create:S03] - {str(error)}'}

    # define "incident_data" table create SQL:S04
    try:
        incident_data_table_create_sql = '''
        CREATE TABLE incident_data (
            id SERIAL PRIMARY KEY,
            ticket_type TEXT,
            company TEXT,
            sys_id VARCHAR(50) UNIQUE NOT NULL,
            number VARCHAR(50) NOT NULL,
            created_by TEXT,
            created_on TIMESTAMPTZ,
            opened_by TEXT,
            opened_at TIMESTAMPTZ,
            configuration_item TEXT,
            category TEXT,
            subcategory TEXT,
            priority TEXT,
            impact TEXT,
            urgency TEXT,
            severity TEXT,
            state TEXT,
            incident_state TEXT,
            assignment_group TEXT,
            assigned_to TEXT,
            parent_incident TEXT,
            business_process TEXT,
            vendor TEXT,
            environment TEXT,
            availability_group TEXT,
            short_description TEXT,
            description TEXT,
            resolved_by TEXT,
            resolved_at TIMESTAMPTZ,
            close_code TEXT,
            close_notes TEXT,
            work_notes TEXT
        );
        ALTER TABLE incident_data OWNER TO soumalya;'''
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Create:S04] - {str(error)}'}

    # create "incident_data" table:S05
    try:
        with psycopg2.connect(**db_connection_parameter) as database_connection: # type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(incident_data_table_create_sql)
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Create:S05] - {str(error)}'}

    # check if "incident_data" table create:S06
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
                    return {'status' : 'SUCCESS', 'message' : '"incident_data" Table Created'}
                else:
                    return {'status' : 'ERROR', 'message' : '"incident_data" Table Not Created'}
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Create:S06] - {str(error)}'}