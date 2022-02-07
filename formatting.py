class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_error(str):
    print(BColors.FAIL + str + BColors.ENDC)

def print_warning(str, verbose=True):
    if verbose:
        print(BColors.WARNING + str + BColors.ENDC)

def print_success(str, verbose=True):
    if verbose:
        print(BColors.OKBLUE + str + BColors.ENDC)

def print_(str, verbose=True):
    if verbose:
        print(str)