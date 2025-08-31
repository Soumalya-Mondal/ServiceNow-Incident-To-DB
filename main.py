# define main function
if __name__ == '__main__':
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import time
    except Exception as error:
        print(f'ERROR - [S01] - {str(error)}')

    # define folder and file path:S02
    try:
        sys.path.append(str(Path.cwd()))
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
    except Exception as error:
        print(f'ERROR - [S02] - {str(error)}')

    # importing user-define module:S03
    try:
        from support.totalticketcount import total_ticket_count
        from support.dbtabledetails import db_table_details
        from support.fetchticketdetails import fetch_ticket_details
        from support.dbdatainsert import db_data_insert
    except Exception as error:
        print(f'ERROR - [S03] - {str(error)}')

    # check if ".env" file is present and valid:S04
    try:
        if (env_file_path.exists() and env_file_path.is_file()):
            environment_values = dotenv_values(env_file_path)
            snow_endpoint = str(environment_values.get('SNOW_ENDPOINT', 'NONE'))
            snow_username = str(environment_values.get('SNOW_USERNAME', 'NONE'))
            snow_password = str(environment_values.get('SNOW_PASSWORD', 'NONE'))
            pg_host = str(environment_values.get('PG_HOST', 'LOCALHOST'))
            pg_port = str(environment_values.get('PG_PORT', '5432'))
            pg_database = str(environment_values.get('PG_DB_NAME', 'NONE'))
            pg_username = str(environment_values.get('PG_USERNAME', 'NONE'))
            pg_password = str(environment_values.get('PG_PASSWORD', 'NONE'))
        else:
            print(f'ERROR - ".env" File Is Not Present')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [S04] - {str(error)}')

    # fetching total incident ticket count:S06
    try:
        ticket_count_backend_response = total_ticket_count(snow_url = str(snow_endpoint), username = str(snow_username), password = str(snow_password), ticket_type = 'incident')
        # check the result
        if ((str(ticket_count_backend_response['status']).lower()) == 'success'):
            incident_ticket_count = ticket_count_backend_response['ticket_count']
            print(f'INFO - Total: "{incident_ticket_count}" Ticket Present In ServiceNow')
        elif ((str(ticket_count_backend_response['status']).lower()) == 'error'):
            print(f"ERROR - {ticket_count_backend_response['message']}")
            sys.exit(1)
        else:
            print('ERROR - Total Ticket Count Not Fetched')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [S06] - {str(error)}')

    # checking "incident_data" table details:S07
    try:
        db_table_details_backend_response = db_table_details(db_name = str(pg_database), username = str(pg_username), password = str(pg_password), db_host = str(pg_host), db_port = str(pg_port))
        # check the result
        if ((str(db_table_details_backend_response['status']).lower()) == 'success'):
            print(f"SUCCESS - {db_table_details_backend_response['message']}")
        elif ((str(db_table_details_backend_response['status']).lower()) == 'info'):
            print(f"INFO - {db_table_details_backend_response['message']}")
        elif ((str(db_table_details_backend_response['status']).lower()) == 'error'):
            print(f"ERROR - {db_table_details_backend_response['message']}")
        else:
            print('ERROR - Database Details Not Fetched')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [S07] - {str(error)}')

    # loop till ServiceNow stop sending data
    batch_ticket_offset = 0
    while True:
        execution_start_time = time.time()
        # fetching ticket details:S08
        try:
            fetch_ticket_details_backend_response = fetch_ticket_details(snow_url = str(snow_endpoint), username = str(snow_username), password = str(snow_password), fetch_offset = int(batch_ticket_offset))
            # check the result
            if (((str(fetch_ticket_details_backend_response['status'])).lower()) == 'info'):
                print(f"INFO - {fetch_ticket_details_backend_response['message']}")
                sys.exit(1)
            elif (((str(fetch_ticket_details_backend_response['status'])).lower()) == 'error'):
                print(f"ERROR - {fetch_ticket_details_backend_response['message']}")
                sys.exit(1)
        except Exception as error:
            print(f'ERROR - [S08] - {str(error)}')

        # insert data into database:S09
        try:
            if ((str(fetch_ticket_details_backend_response['status']).lower()) == 'success'):
                db_data_insert_backend_response = db_data_insert(db_name = str(pg_database), username = str(pg_username), password = str(pg_password), db_host = str(pg_host), db_port = str(pg_port), batch_ticket_data = fetch_ticket_details_backend_response['ticket_details'])
                # check the result
                if ((str(db_data_insert_backend_response['status']).lower()) == 'success'):
                    print(f"SUCCESS - Total: {db_data_insert_backend_response['row_count']} Data Inserted Into Database")
                elif ((str(db_data_insert_backend_response['status']).lower()) == 'error'):
                    print(f"ERROR - {db_data_insert_backend_response['message']}")
                    sys.exit(1)
        except Exception as error:
            print(f'ERROR - [S09] - {str(error)}')

        # appending ticket offset value
        batch_ticket_offset += 10000
        # print execution time
        print(f'Total Execution Time: {(time.time() - execution_start_time):.2f}')