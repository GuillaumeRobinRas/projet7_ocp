def map_client_update(request):
    update_mapping = {
        'loan_amount': 'AMT_CREDIT',
        'age': 'DAYS_BIRTH',
        'income': 'AMT_INCOME_TOTAL',
        'loan_duration_months': 'AMT_ANNUITY',
        'gender': 'CODE_GENDER'
    }

    client_update = {}
    for param, column in update_mapping.items():
        value = request.args.get(param)
        if value is not None:
            client_update[column] = float(value)
    return client_update
