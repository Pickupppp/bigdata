import dao


def get_thread_wordcount():
    words = dao.get_thread_wordcount()
    res = []
    for item in words:
        if item[1] <= 3:
            break
        res.append({'name': item[0], 'value': item[1]})
    return res


def get_post_wordcount():
    words = dao.get_post_wordcount()
    res = []
    for item in words:
        if item[1] <= 3:
            break
        res.append({'name': item[0], 'value': item[1]})
    return res


def get_comment_wordcount():
    words = dao.get_comment_wordcount()
    res = []
    for item in words:
        if item[1] <= 3:
            break
        res.append({'name': item[0], 'value': item[1]})
    return res


def get_yesterday_post():
    return dao.get_yesterday_post()


def get_yesterday_comment():
    return dao.get_yesterday_comment()


def get_post_ip():
    ip = dao.get_post_ip()
    res = []
    for item in ip:
        if item[0] in ['中国香港', '中国澳门']:
            res.append({'name': item[0][-2:], 'value': item[1]})
        else:
            res.append({'name': item[0], 'value': item[1]})
    return res
