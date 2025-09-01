# define "db_table_details" function
def db_table_details(db_name: str, username: str, password: str, db_host: str, db_port: str) -> dict[str, str]:
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        import psycopg2
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Details:S01] - {str(error)}'}

    # importing "log_writer" function:S02
    try:
        sys.path.append(str(Path.cwd()))
        from support.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Details:S02] - {str(error)}'}

    # define db connection parameter:S03
    try:
        db_connection_parameter = {
            "dbname" : str(db_name),
            "user" : str(username),
            "password" : str(password),
            "host" : str(db_host),
            "port" : str(db_port)
        }
        log_writer(file_name = 'DB-Table-Details', steps = '03', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(file_name = 'DB-Table-Details', steps = '03', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Details:S03] - {str(error)}'}

    # check if "incident_data" table present and fetch row count:S04
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
                    log_writer(file_name = 'DB-Table-Details', steps = '04', status = 'SUCCESS', message = 'Table "incident_data" Already Present')
                    # fetch row count from "incident_data" table
                    database_cursor.execute('SELECT COUNT(*) FROM incident_data;')
                    records_count = database_cursor.fetchone()[0]
                    # check "records_count"
                    if (int(records_count) == 0):
                        log_writer(file_name = 'DB-Table-Details', steps = '04', status = 'SUCCESS', message = 'Table "incident_data" Has No Data, Droping Table')
                        # drop table
                        database_cursor.execute('DROP TABLE incident_data')
                    else:
                        log_writer(file_name = 'DB-Table-Details', steps = '04', status = 'SUCCESS', message = 'Table "incident_data" Already Present')
                        return {'status' : 'SUCCESS', 'message' : '"incident_data" Table Already Present'}
    except Exception as error:
        log_writer(file_name = 'DB-Table-Details', steps = '04', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Details:S04] - {str(error)}'}

    # define "incident_data" table create SQL:S05
    try:
        incident_data_table_create_sql = '''
        CREATE TABLE incident_data (
            id SERIAL PRIMARY KEY,
            ticket_type VARCHAR(50),
            company VARCHAR(50),
            sys_id VARCHAR(50) UNIQUE NOT NULL,
            number VARCHAR(50) NOT NULL,
            created_by VARCHAR(50),
            created_on TIMESTAMPTZ,
            opened_by VARCHAR(50),
            opened_at TIMESTAMPTZ,
            configuration_item VARCHAR(100),
            category VARCHAR(50),
            subcategory VARCHAR(50),
            priority VARCHAR(20),
            impact VARCHAR(20),
            urgency VARCHAR(20),
            severity VARCHAR(20),
            state VARCHAR(20),
            incident_state VARCHAR(20),
            assignment_group VARCHAR(50),
            assigned_to VARCHAR(50),
            parent_incident VARCHAR(50),
            business_process VARCHAR(100),
            vendor VARCHAR(100),
            environment VARCHAR(100),
            availability_group VARCHAR(100),
            short_description VARCHAR(100),
            description VARCHAR(1000),
            resolved_by VARCHAR(50),
            resolved_at TIMESTAMPTZ,
            close_code VARCHAR(50),
            close_notes VARCHAR(500),
            work_notes TEXT,
            CONSTRAINT sys_id_not_blank CHECK (btrim(sys_id) <> ''),
            CONSTRAINT number_not_blank CHECK (btrim(number) <> '')
        );
        ALTER TABLE incident_data OWNER TO soumalya;'''
        log_writer(file_name = 'DB-Table-Details', steps = '05', status = 'SUCCESS', message = 'Table Create SQL Define For "incident_data"')
    except Exception as error:
        log_writer(file_name = 'DB-Table-Details', steps = '05', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Details:S05] - {str(error)}'}

    # create "incident_data" table:S06
    try:
        with psycopg2.connect(**db_connection_parameter) as database_connection: # type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(incident_data_table_create_sql)
    except Exception as error:
        log_writer(file_name = 'DB-Table-Details', steps = '06', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Details:S06] - {str(error)}'}

    # check if "incident_data" table create:S07
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
                    log_writer(file_name = 'DB-Table-Details', steps = '07', status = 'SUCCESS', message = 'Table "incident_data" Created')
                    return {'status' : 'SUCCESS', 'message' : '"incident_data" Table Created'}
                else:
                    log_writer(file_name = 'DB-Table-Details', steps = '07', status = 'ERROR', message = 'Table "incident_data" Not Created')
                    return {'status' : 'ERROR', 'message' : '"incident_data" Table Not Created'}
    except Exception as error:
        log_writer(file_name = 'DB-Table-Details', steps = '07', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Table-Details:S07] - {str(error)}'}