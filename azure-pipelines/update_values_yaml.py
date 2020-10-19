"""
A script used for updating HELM value files with the new container image name pushed to container registry.
"""
import yaml
from argparse import ArgumentParser


def __read_yaml_file(filename: str) -> dict:
    """
    Reads a yaml files returns it as dict
    :param filename: The filename of a YAML file
    :return: The Yaml file parsed as a dict
    """
    with open(filename, 'r') as file:
        return yaml.safe_load(file)


def __replace_or_add_value(yaml_dict: dict, key: str, new_value: str):
    """
    Updates a specific key value set, or adds if it doesn't already exist
    :param yaml_dict: A dict representation of a Yaml file
    :param key: the key to add or replace
    :param new_value: the updated or new value
    :return: the updated ditct
    """
    print(yaml_dict.keys())
    if key not in yaml_dict.keys():
        print(f"Adding new {key}: {new_value}")
    else:
        print(f"Updating ({key}: {yaml_dict[key]}) -> ({key}: {new_value})")
    yaml_dict[key] = new_value
    print(yaml_dict)


def __write_file(yaml_dict: dict, filename: str):
    """
    Dumps a Yaml dict to file
    :param yaml_dict: The yaml dict to write to file
    :param filename: The filename of the file
    """
    with open(filename, 'w') as file:
        data = yaml.dump(yaml_dict, file)
        print(data)


def __setup_argparser() -> ArgumentParser:
    """
    Sets up an arg parser for this app
    :return: an ArgumentParser
    """
    parser = ArgumentParser(description="Updates a helm values.yaml file")
    parser.add_argument("--file", type=str, help="File to replace value in", required=True)
    parser.add_argument("--key", type=str, help="Key to get new value", required=True)
    parser.add_argument("--value", type=str, help="The new value to the key", required=True)
    return parser


if __name__ == '__main__':
    parser = __setup_argparser()
    args = parser.parse_args()
    yaml_dict = __read_yaml_file(args.file)
    __replace_or_add_value(yaml_dict, args.key, args.value)
    __write_file(yaml_dict, args.file)
