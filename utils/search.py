def search_records(records, keyword, fields=None):
    result = []
    for rec in records:
        if any(keyword.lower() in str(rec[i]).lower() for i in fields):
            result.append(rec)
    return result