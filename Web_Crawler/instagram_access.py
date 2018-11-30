
def ig_creds(kw_number):
    if kw_number == 1:
        username = 'USERNAME1'
        pwd = 'PASSWORD1'
    elif kw_number == 2:
        username = 'USERNAME2'
        pwd = 'PASSWORD2'
    elif kw_number == 3:
        username = 'USERNAME3'
        pwd = 'PASSWORD3'
    return dict(username=username, pwd=pwd)
