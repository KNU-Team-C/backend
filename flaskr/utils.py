from sqlalchemy import text


def string_arg_to_ids_list(arg):
    result = []
    for arg_id in arg.split(','):
        if arg_id:
            result.append(int(arg_id))
    return result


flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]


def filter_by_text(text_str, query):
    if len(text_str) > 0:
        return query.filter(text("LOWER(name) LIKE LOWER(:query)").params(query=text_str + '%'))
    return query
