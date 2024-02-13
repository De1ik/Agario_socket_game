def get_correct_type(data):
    op_m = None
    for index in range(len(data)):
        if data[index] == '<':
            op_m = index
        elif data[index] == '>' and op_m is not None:
            res = data[op_m + 1:index]
            res = list(map(int, res.split(',')))
            return res