import yaml
import argparse


def read_file(filename: str) -> dict:
    with open(filename, 'r') as file:
        return yaml.safe_load(file)


def replace_or_add_value(yaml_dict: dict, key: str, new_value: str):
    print(yaml_dict.keys())
    if key not in yaml_dict.keys():
        print(f"Adding new {key}: {new_value}")
    else:
        print(f"Updating ({key}: {yaml_dict[key]}) -> ({key}: {new_value})")
    yaml_dict[key] = new_value
    print(yaml_dict)


def write_file(yaml_dict: dict, filename: str):
    with open(filename, 'w') as file:
        data = yaml.dump(yaml_dict, file)
        print(data)


def setup_argparser():
    parser = argparse.ArgumentParser(description="Updates a helm values.yaml file")
    parser.add_argument("--file", type=str, help="File to replace value in", required=True)
    parser.add_argument("--key", type=str, help="Key to get new value", required=True)
    parser.add_argument("--value", type=str, help="The new value to the key", required=True)
    return parser


if __name__ == '__main__':
    parser = setup_argparser()
    args = parser.parse_args()
    yaml_dict =read_file(args.file)
    replace_or_add_value(yaml_dict, args.key, args.value)
    write_file(yaml_dict, args.file)
