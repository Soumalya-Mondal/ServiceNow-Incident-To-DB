# define main function
if __name__ == '__main__':
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import urllib3
        import requests
        from datetime import datetime, timezone
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
    except Exception as error:
        print(f'ERROR - [S03] - {str(error)}')

    # check if ".env" file is present and valid:S04
    try:
        if (env_file_path.exists() and env_file_path.is_file()):
            environment_values = dotenv_values(env_file_path)
            snow_api_url_for_stats = str(environment_values.get('SNOW_URL_STATS', 'NONE'))
            snow_api_url_for_data = str(environment_values.get('SNOW_URL_DATA', 'NONE'))
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

    # define db connection parameter:S05
    try:
        database_connection_parameter = {
            "dbname" : str(pg_database),
            "user" : str(pg_username),
            "password" : str(pg_password),
            "host" : str(pg_host),
            "port" : str(pg_port)
        }
    except Exception as error:
        print(f'ERROR - [S05] - {str(error)}')

    # fetching total incident ticket count:S06
    try:
        ticket_count_backend_response = total_ticket_count(snow_url = str(snow_api_url_for_stats), username = str(snow_username), password = str(snow_password), ticket_type = 'incident')
        # check the result
        if ((str(ticket_count_backend_response['status']).lower()) == 'success'):
            incident_ticket_count = ticket_count_backend_response['ticket_count']
            print(incident_ticket_count)
        elif ((str(ticket_count_backend_response['status']).lower()) == 'error'):
            print(f"ERROR - {ticket_count_backend_response['message']}")
            sys.exit(1)
        else:
            print('ERROR - Total Ticket Count Not Fetched')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [S06] - {str(error)}')