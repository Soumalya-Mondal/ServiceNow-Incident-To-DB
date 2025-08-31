# define "fetch_ticket_details" function
def fetch_ticket_details(snow_url: str, username: str, password: str, fetch_offset: int):
    # importing python module:S01
    try:
        import urllib3
        import requests
        from datetime import datetime, timezone
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S01] - {str(error)}', 'ticket_details' : []}

    # define ServiceNow parameter:S02
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        snow_credential = (username, password)
        snow_headers = {
            'Accept': 'Application/json',
            'Content-Type': 'Application/json'
        }
        snow_params = {
            'sysparm_display_value': 'all',
            'sysparm_query': 'ORDERBYsys_created_on',
            'sysparm_exclude_reference_link' : 'true',
            'sysparm_fields': 'assigned_to,assignment_group,close_code,close_notes,cmdb_ci,company,description,impact,incident_state,number,opened_at,opened_by,parent_incident,priority,resolved_at,resolved_by,severity,short_description,state,sys_class_name,sys_created_by,sys_created_on,sys_id,u_availability_group,u_business_process,u_environment,u_tenant_category,u_tenant_subcategory,u_vendor,urgency,work_notes',
            'sysparm_limit' : '10000',
            'sysparm_offset' : str(fetch_offset)
        }
        snow_api_url = f'{snow_url}/api/now/table/incident'
        batch_ticket_records = []
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S02] - {str(error)}', 'ticket_details' : []}
    
    # define "parse_snow_datetime" function:S03
    def parse_snow_datetime(value):
        EPOCH_UTC = datetime(1970, 1, 1, tzinfo = timezone.utc)
        s = (value or '').strip()
        if (not s):
            return EPOCH_UTC
        # try common ServiceNow Date-Time formats
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f'):
            try:
                return datetime.strptime(s, fmt).replace(tzinfo = timezone.utc)
            except ValueError:
                pass
        # try ISO-8601
        try:
            return datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(timezone.utc)
        except ValueError:
            return EPOCH_UTC

    # calling ServiceNow API:S03
    try:
        incident_ticket_data_response = requests.get(snow_api_url, auth = snow_credential, headers = snow_headers, params = snow_params, verify = False)
        # check the response status code
        if (int(incident_ticket_data_response.status_code) == 200):
            incident_ticket_result = incident_ticket_data_response.json().get('result', [])
            # if there is no result
            if (incident_ticket_result):
                # loop through all the ticket details
                for ticket_item in incident_ticket_result:
                    ticket_record = (
                        ticket_item.get('sys_class_name', {}).get('display_value'), #ticket_type
                        ticket_item.get('company', {}).get('display_value'), #company
                        ticket_item.get('sys_id', {}).get('display_value'), #sys_id
                        ticket_item.get('number', {}).get('display_value'), #number
                        ticket_item.get('sys_created_by', {}).get('display_value'), #created_by
                        parse_snow_datetime(str(ticket_item.get('sys_created_on', {}).get('value'))), #created_on
                        ticket_item.get('opened_by', {}).get('display_value'), #opend_by
                        parse_snow_datetime(str(ticket_item.get('opened_at', {}).get('value'))), #opened_at
                        ticket_item.get('cmdb_ci', {}).get('display_value'), #configuration_item
                        ticket_item.get('u_tenant_category', {}).get('display_value'), #category
                        ticket_item.get('u_tenant_subcategory', {}).get('display_value'), #subcategory
                        ticket_item.get('priority', {}).get('display_value'), #priority
                        ticket_item.get('impact', {}).get('display_value'), #impact
                        ticket_item.get('urgency', {}).get('display_value'), #urgency
                        ticket_item.get('severity', {}).get('display_value'), #severity
                        ticket_item.get('state', {}).get('display_value'), #state
                        ticket_item.get('incident_state', {}).get('display_value'), #incident_state
                        ticket_item.get('assignment_group', {}).get('display_value'), #assignment_group
                        ticket_item.get('assigned_to', {}).get('display_value'), #assigned_to
                        ticket_item.get('parent_incident', {}).get('display_value'), #parent_incident
                        ticket_item.get('u_business_process', {}).get('display_value'), #business_process
                        ticket_item.get('u_vendor', {}).get('display_value'), #vendor
                        ticket_item.get('u_environment', {}).get('display_value'), #environment
                        ticket_item.get('u_availability_group', {}).get('display_value'), #availability_group
                        ticket_item.get('short_description', {}).get('display_value'), #short_description
                        ticket_item.get('description', {}).get('display_value'), #description
                        ticket_item.get('resolved_by', {}).get('display_value'), #resolved_by
                        parse_snow_datetime(str(ticket_item.get('resolved_at', {}).get('value'))), #resolved_at
                        ticket_item.get('close_code', {}).get('display_value'), #close_code
                        ticket_item.get('close_notes', {}).get('display_value'), #close_notes
                        ticket_item.get('work_notes', {}).get('display_value') #work_notes
                    )
                    # append ticket into batch
                    batch_ticket_records.append(ticket_record)
                return {'status' : 'SUCCESS', 'message' : 'Ticket Details Fetched', 'ticket_details' : batch_ticket_records}
            else:
                return {'status' : 'INFO', 'message' : 'No More Ticket Details Found In ServiceNow', 'ticket_details' : []}
        else:
            return {'status' : 'ERROR', 'message' : str(incident_ticket_data_response.text), 'ticket_details' : []}
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S03] - {str(error)}', 'ticket_details' : []}