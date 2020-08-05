import os
import platform


def mkdir(root_path, path):
    current_system = platform.system()
    if current_system == 'Windows':
        path = root_path + '\\' + path
    elif current_system == 'Linux':
        path = root_path + '/' + path
    is_existes = os.path.exists(path)
    if not is_existes:
        os.makedirs(path)
