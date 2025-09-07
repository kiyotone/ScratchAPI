def paginate(records, page, limit):
    start = (page - 1) * limit
    end = start + limit
    return records[start:end]