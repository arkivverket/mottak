import os

hooks_folder = 'hooks'
tusd_hooks_valid_names = ['pre-create', 'post-create', 'pre-finish', 'post-finish', 'post-terminate', 'post-receive']


def test_hooks_executable():
    files = os.listdir(hooks_folder)
    for filename in files:
        if is_hook_name(filename):
            hook_path = hooks_folder + os.path.sep + filename
            assert os.access(hook_path, os.X_OK), f"{hook_path} needs to be executable. Use chmod +x <filename>"


def is_hook_name(filename: str) -> bool:
    return filename in tusd_hooks_valid_names
