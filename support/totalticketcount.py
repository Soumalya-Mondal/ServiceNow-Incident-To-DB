# define "total_ticket_count" function
def total_ticket_count(snow_url: str, username: str, password: str, ticket_type: str) -> dict[str, str]:
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        import urllib3
        import requests
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[Total-Ticket-Count:S01] - {str(error)}', 'ticket_count' : '0'}

    # importing user-define function:S02
    try:
        sys.path.append(str(Path.cwd()))
        from support.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[Total-Ticket-Count:S02] - {str(error)}', 'ticket_count' : '0'}

    # define ServiceNow parameter:S02
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        snow_credential = (username, password)
        snow_headers = {
            'Accept': 'Application/json',
            'Content-Type': 'Application/json'
        }
        snow_parm = {
            'sysparm_count' : 'true'
        }
        snow_api_url = f'{snow_url}/api/now/stats/{ticket_type.lower()}'
        log_writer(file_name = 'Total-Ticket-Count', steps = '02', status = 'SUCCESS', message = 'All ServiceNow Parameter Defined')
    except Exception as error:
        log_writer(file_name = 'Total-Ticket-Count', steps = '02', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[Total-Ticket-Count:S02] - {str(error)}', 'ticket_count' : '0'}

    # calling ServiceNow API:S03
    try:
        ticket_count_response = requests.get(snow_api_url, auth = snow_credential, headers = snow_headers, params = snow_parm, verify = False)
        # check the response status code
        if (int(ticket_count_response.status_code) == 200):
            total_incident_ticket_count = int(ticket_count_response.json().get('result', {}).get('stats', {}).get('count'))
            log_writer(file_name = 'Total-Ticket-Count', steps = '03', status = 'SUCCESS', message = f'Total: "{total_incident_ticket_count}" Incident Tickets Are Present Inside ServiceNow')
            return {'status' : 'SUCCESS', 'message' : 'Total Incident Ticket Count Fetched', 'ticket_count' : str(total_incident_ticket_count)}
        else:
            log_writer(file_name = 'Total-Ticket-Count', steps = '03', status = 'SUCCESS', message = str(ticket_count_response.text))
            return {'status' : 'ERROR', 'message' : str(ticket_count_response.text), 'ticket_count' : '0'}
    except Exception as error:
        log_writer(file_name = 'Total-Ticket-Count', steps = '03', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[Total-Ticket-Count:S03] - {str(error)}'}