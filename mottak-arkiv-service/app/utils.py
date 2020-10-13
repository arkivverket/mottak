from pathlib import Path


def get_project_root() -> Path:
    """
    This method is used when building absolute Paths.
    Relative Paths isn't functioning when using pytest from root.
    :return:
    """
    return Path(__file__).parent.parent
