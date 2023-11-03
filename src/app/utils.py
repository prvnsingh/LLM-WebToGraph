import yaml


def read_yaml_file(file_path):
    """
    Load a YAML file and return its contents as a Python dictionary.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: A dictionary containing the YAML configuration.
    """
    try:
        with open(file_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
        return config
    except FileNotFoundError:
        print(f"Error: Config file not found at {file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error: Failed to load YAML from {file_path}. {e}")
        return {}



