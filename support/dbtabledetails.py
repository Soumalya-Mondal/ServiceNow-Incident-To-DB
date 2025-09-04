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
            work_notes TEXT,
            u_tenant_subcategory TEXT,
            upon_reject TEXT,
            origin_table TEXT,
            x_caukp_ebonding_sdc TEXT,
            proposed_by TEXT,
            u_security_type TEXT,
            u_vendor_priority TEXT,
            x_caukp_ebonding_no_return TEXT,
            lessons_learned TEXT,
            knowledge TEXT,
            "order" TEXT,
            u_security_relevant_reason TEXT,
            x_caukp_ebonding_integration_mode TEXT,
            contract TEXT,
            x_caukp_ebonding_requester_id TEXT,
            business_duration TEXT,
            group_list TEXT,
            u_copied_from TEXT,
            u_template TEXT,
            u_appointment TIMESTAMPTZ,
            u_sla_response TIMESTAMPTZ,
            approval_set TEXT,
            u_security_related TEXT,
            major_incident_state TEXT,
            universal_request TEXT,
            correlation_display TEXT,
            work_start TIMESTAMPTZ,
            u_accelerated TEXT,
            u_complaint TEXT,
            additional_assignee_list TEXT,
            u_pending_timer TIMESTAMPTZ,
            notify TEXT,
            service_offering TEXT,
            sys_class_name TEXT,
            follow_up TIMESTAMPTZ,
            reopened_by TEXT,
            u_availability_group TEXT,
            u_approval TEXT,
            u_caukp_ebonding_cmo_id TEXT,
            reassignment_count TEXT,
            u_ola_response_met TEXT,
            sla_due TIMESTAMPTZ,
            u_event_help_id TEXT,
            comments_and_work_notes TEXT,
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