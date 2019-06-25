from pkg_resources import resource_filename


def get_abs_path(path):
    abs_path = resource_filename('snowglobes', path)
    return(abs_path)
