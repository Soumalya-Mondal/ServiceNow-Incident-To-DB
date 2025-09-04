# define "fetch_ticket_details" function
def fetch_ticket_details(snow_url: str, username: str, password: str, fetch_offset: int):
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        import urllib3
        import requests
        from datetime import datetime, timezone
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S01] - {str(error)}', 'ticket_details' : []}

    # importing "log_writer" function:S02
    try:
        sys.path.append(str(Path.cwd()))
        from support.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S02] - {str(error)}', 'ticket_details' : []}

    # define ServiceNow parameter:S03
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # define empty "batch_ticket_records" list
        batch_ticket_records = []
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
        log_writer(file_name = 'Fetch-Ticket-Details', steps = '03', status = 'SUCCESS', message = 'ServiceNow Parameter Defined')
    except Exception as error:
        log_writer(file_name = 'Fetch-Ticket-Details', steps = '03', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S03] - {str(error)}', 'ticket_details' : []}

    # define "parse_snow_datetime" function:S04
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

    # define "get_display_value" function
    def get_display_value(item, field):
        return item.get(field, {}).get("display_value") or "N/A"

    # define "sanitize_value" function
    def sanitize_value(value):
        if isinstance(value, str):
            return value.replace('\x00', '')  # remove NUL characters
        return value

    # calling ServiceNow API:S05
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
                        sanitize_value(get_display_value(ticket_item, "sys_class_name")),
                        sanitize_value(get_display_value(ticket_item, "company")),
                        sanitize_value(get_display_value(ticket_item, "sys_id")),
                        sanitize_value(get_display_value(ticket_item, "number")),
                        sanitize_value(get_display_value(ticket_item, "sys_created_by")),
                        parse_snow_datetime(ticket_item.get("sys_created_on", {}).get("value")),
                        sanitize_value(get_display_value(ticket_item, "opened_by")),
                        parse_snow_datetime(ticket_item.get("opened_at", {}).get("value")),
                        sanitize_value(get_display_value(ticket_item, "cmdb_ci")),
                        sanitize_value(get_display_value(ticket_item, "u_tenant_category")),
                        sanitize_value(get_display_value(ticket_item, "u_tenant_subcategory")),
                        sanitize_value(get_display_value(ticket_item, "priority")),
                        sanitize_value(get_display_value(ticket_item, "impact")),
                        sanitize_value(get_display_value(ticket_item, "urgency")),
                        sanitize_value(get_display_value(ticket_item, "severity")),
                        sanitize_value(get_display_value(ticket_item, "state")),
                        sanitize_value(get_display_value(ticket_item, "incident_state")),
                        sanitize_value(get_display_value(ticket_item, "assignment_group")),
                        sanitize_value(get_display_value(ticket_item, "assigned_to")),
                        sanitize_value(get_display_value(ticket_item, "parent_incident")),
                        sanitize_value(get_display_value(ticket_item, "u_business_process")),
                        sanitize_value(get_display_value(ticket_item, "u_vendor")),
                        sanitize_value(get_display_value(ticket_item, "u_environment")),
                        sanitize_value(get_display_value(ticket_item, "u_availability_group")),
                        sanitize_value(get_display_value(ticket_item, "short_description")),
                        sanitize_value(get_display_value(ticket_item, "description")),
                        sanitize_value(get_display_value(ticket_item, "resolved_by")),
                        parse_snow_datetime(ticket_item.get("resolved_at", {}).get("value")),
                        sanitize_value(get_display_value(ticket_item, "close_code")),
                        sanitize_value(get_display_value(ticket_item, "close_notes")),
                        sanitize_value(get_display_value(ticket_item, "work_notes")),
                        sanitize_value(get_display_value(ticket_item, "u_tenant_subcategory")),
                        sanitize_value(get_display_value(ticket_item, "upon_reject")),
                        sanitize_value(get_display_value(ticket_item, "origin_table")),
                        sanitize_value(get_display_value(ticket_item, "x_caukp_ebonding_sdc")),
                        sanitize_value(get_display_value(ticket_item, "proposed_by")),
                        sanitize_value(get_display_value(ticket_item, "u_security_type")),
                        sanitize_value(get_display_value(ticket_item, "u_vendor_priority")),
                        sanitize_value(get_display_value(ticket_item, "x_caukp_ebonding_no_return")),
                        sanitize_value(get_display_value(ticket_item, "lessons_learned")),
                        sanitize_value(get_display_value(ticket_item, "knowledge")),
                        sanitize_value(get_display_value(ticket_item, "order")),
                        sanitize_value(get_display_value(ticket_item, "u_security_relevant_reason")),
                        sanitize_value(get_display_value(ticket_item, "x_caukp_ebonding_integration_mode")),
                        sanitize_value(get_display_value(ticket_item, "contract")),
                        sanitize_value(get_display_value(ticket_item, "x_caukp_ebonding_requester_id")),
                        sanitize_value(get_display_value(ticket_item, "business_duration")),
                        sanitize_value(get_display_value(ticket_item, "group_list")),
                        sanitize_value(get_display_value(ticket_item, "u_copied_from")),
                        sanitize_value(get_display_value(ticket_item, "u_template")),
                        parse_snow_datetime(ticket_item.get("u_appointment", {}).get("value")),
                        parse_snow_datetime(ticket_item.get("u_sla_response", {}).get("value")),
                        sanitize_value(get_display_value(ticket_item, "approval_set")),
                        sanitize_value(get_display_value(ticket_item, "u_security_related")),
                        sanitize_value(get_display_value(ticket_item, "major_incident_state")),
                        sanitize_value(get_display_value(ticket_item, "universal_request")),
                        sanitize_value(get_display_value(ticket_item, "correlation_display")),
                        parse_snow_datetime(ticket_item.get("work_start", {}).get("value")),
                        sanitize_value(get_display_value(ticket_item, "u_accelerated")),
                        sanitize_value(get_display_value(ticket_item, "u_complaint")),
                        sanitize_value(get_display_value(ticket_item, "additional_assignee_list")),
                        parse_snow_datetime(ticket_item.get("u_pending_timer", {}).get("value")),
                        sanitize_value(get_display_value(ticket_item, "notify")),
                        sanitize_value(get_display_value(ticket_item, "service_offering")),
                        sanitize_value(get_display_value(ticket_item, "sys_class_name")),
                        parse_snow_datetime(ticket_item.get("follow_up", {}).get("value")),
                        sanitize_value(get_display_value(ticket_item, "reopened_by")),
                        sanitize_value(get_display_value(ticket_item, "u_availability_group")),
                        sanitize_value(get_display_value(ticket_item, "u_approval")),
                        sanitize_value(get_display_value(ticket_item, "u_caukp_ebonding_cmo_id")),
                        sanitize_value(get_display_value(ticket_item, "reassignment_count")),
                        sanitize_value(get_display_value(ticket_item, "u_ola_response_met")),
                        parse_snow_datetime(ticket_item.get("sla_due", {}).get("value")),
                        sanitize_value(get_display_value(ticket_item, "u_event_help_id")),
                        sanitize_value(get_display_value(ticket_item, "comments_and_work_notes"))
                    )
                    # check if "sys_id" and "number" are non-empty
                    if all([ticket_record[2] and ticket_record[2].strip(), ticket_record[3] and ticket_record[3].strip()]):
                        batch_ticket_records.append(ticket_record)
                log_writer(file_name = 'Fetch-Ticket-Details', steps = '05', status = 'SUCCESS', message = f'Total: {len(batch_ticket_records)} Incident Ticket Details Fetched')
                return {'status' : 'SUCCESS', 'message' : 'Ticket Details Fetched', 'ticket_details' : batch_ticket_records}
            else:
                log_writer(file_name = 'Fetch-Ticket-Details', steps = '05', status = 'INFO', message = 'No New Incident Ticket Found In ServiceNow')
                return {'status' : 'INFO', 'message' : 'No More Ticket Details Found In ServiceNow', 'ticket_details' : []}
        else:
            log_writer(file_name = 'Fetch-Ticket-Details', steps = '05', status = 'ERROR', message = str(incident_ticket_data_response.text))
            return {'status' : 'ERROR', 'message' : str(incident_ticket_data_response.text), 'ticket_details' : []}
    except Exception as error:
        log_writer(file_name = 'Fetch-Ticket-Details', steps = '05', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S05] - {str(error)}', 'ticket_details' : []}