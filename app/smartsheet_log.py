from app import config

def smartsheet_log_signup(customer_id, signup_time, message):
    """
    Create row in smartsheet based on environment variables
    """

    if (not config.SMARTSHEET_TOKEN) or (not config.SMARTSHEET_SIGNUP_SHEET):
        return None

    import smartsheet

    smartsheet_api = smartsheet.Smartsheet(config.SMARTSHEET_TOKEN)
    action = smartsheet_api.Sheets.list_sheets(include_all=True)
    sheets = action.data
    for sheetInfo in sheets:
        if sheetInfo.name == config.SMARTSHEET_SIGNUP_SHEET:
            sheet = smartsheet_api.Sheets.get_sheet(sheetInfo.id)
            break

    else:
        print("Failed logging signup from %s. A smartsheet named %s wasn't found under token %s"
                % (customer_id, config.SMARTSHEET_SIGNUP_SHEET, config.SMARTSHEET_TOKEN))

    cols = smartsheet_api.Sheets.get_columns(sheetInfo.id)
    row = smartsheet_api.models.Row()
    row.to_top = True
    row.cells.append({
            'column_id': cols[config.SMARTSHEET_COL_SIGNUP_TIME],
            'value': signup_time,
            'strict': False
        },
        {
            'column_id': cols[config.SMARTSHEET_COL_CUSTOMER_ID],
            'value': customer_id,
            'strict': False
        },
        {
            'column_id': cols[config.SMARTSHEET_COL_MESSAGE],
            'value': message,
            'strict': False
        },
    )

    return smartsheet_api.Sheets.add_rows(sheetInfo.id, [row])

