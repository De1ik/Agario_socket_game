def get_field_cond(data: str) -> str:
    open_m = None
    for i in range(len(data)):
        if data[i] == '<':
            open_m = i
        elif data[i] == '>' and open_m is not None:
            res = data[open_m+1:i]
            return res
    return ''