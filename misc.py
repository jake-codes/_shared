import os

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_env_vars(env_vars):

    output = []

    for var in env_vars:
        name = var[0]
        default = var[1]
        val = os.getenv(name) or default
        if not val or not len(val):
            print_warning('{} not set'.format(name))
            val = input("{}:".format(name))
            os.environ[name] = val
            os.system('export {}={}'.format(name,val))
        output.append(val)

    return output


    # email = os.getenv('NR_EMAIL') or 'jneal@newrelic.com'
    # username = os.getenv('NR_USERNAME') or 'jneal'
    # password = os.getenv('NR_PASSWORD')

    # if not email:
    #     print_warning('NR_EMAIL not set')
    #     email = input("email: ")
    #     os.environ['NR_EMAIL'] = email
    #     os.system("export NR_EMAIL={}".format(email))

    # if not username:
    #     print_warning('NR_USERNAME not set')
    #     username = input("username: ")
    #     os.environ['NR_USERNAME'] = username
    #     os.system("export NR_USERNAME={}".format(username))

    # if not password:
    #     print_warning('NR_PASSWORD not set')
    #     password = getpass.getpass('Password:')
    #     os.environ['NR_PASSWORD'] = password
    #     os.system("export NR_PASSWORD={}".format(password))

    # return (email, username, password)