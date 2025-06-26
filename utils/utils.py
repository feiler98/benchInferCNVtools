"""
------------------------------------------------------------------------------------------------------------------------
UTILS
-----

used for basic standard functionalities
just meant as a small library of compact and universal functions

------------------------------------------------------------------------------------------------------------------------
"""


# imports
# ______________________________________________________________________________________________________________________
from pathlib import Path
from configparser import ConfigParser
import json
# ______________________________________________________________________________________________________________________


# configuration file [.ini] handling as class
# -------------------------------------------
class GetConfig:
    def __init__(self, cfg_obj=None, path_cfg: str = None):
        self.cfg_obj = cfg_obj
        self.path_cfg = path_cfg

    @classmethod
    def get_config(cls, config_name: str):
        """
        :param config_name: name of config-file [.ini]
        :return: returns config obj
        """

        path_main = get_project_dir(Path.cwd(), "main")
        config_path = path_main / "config" / config_name
        if not config_path.exists():
            raise FileExistsError("Config File could not be found!")
        cfg_obj = ConfigParser()
        cfg_obj.read(str(config_path))
        return cls(cfg_obj=cfg_obj, path_cfg=str(config_path))

    def __check_loaded(self):
        for keys, values in self.__dict__.items():
            if values is None:
                raise ValueError("""
#####################################################
No config-file has been loaded.
Initialize the class by using '.get_config(config_name)'
#####################################################
                                 """)

    def return_section(self, section: str) -> dict:
        """
        :param section: name of the target-section
        :return:
        """

        # check if initialized
        # --------------------
        GetConfig.__check_loaded(self)

        return dict(self.cfg_obj.items(section))

    def return_all(self) -> dict:
        """
        :return: dict of dict sections
        """

        # check if initialized
        # --------------------
        GetConfig.__check_loaded(self)

        return self.cfg_obj.items()

    def get_cfg_sections(self):

        # check if initialized
        # --------------------
        GetConfig.__check_loaded(self)

        return list(self.cfg_obj.keys())

    def get_repair_config_section(self, section: str, dict_params: dict) -> dict:
        """
        :param section: name of the target-section
        :param dict_params: dictionary of hard-coded keys/values that need to be available
        :return: returns section as dictionary
        """

        # check if initialized
        # --------------------
        GetConfig.__check_loaded(self)

        # update config if section is missing
        list_sections_available = GetConfig.get_cfg_sections(self)
        if section not in list_sections_available:
            self.cfg_obj.add_section(section)
            with open(self.path_cfg, 'w') as update_ini:
                self.cfg_obj.write(update_ini)

        section_dict = GetConfig.return_section(self, section)

        # update config if in the section params are missing
        return_section = {}
        for keys, values in dict_params.items():
            if keys not in list(section_dict.keys()):
                self.cfg_obj.set(section, keys, values)
                return_section[keys] = values
                with open(self.path_cfg, 'w') as update_ini:
                    self.cfg_obj.write(update_ini)
            else:
                return_section[keys] = section_dict[keys]
        return return_section


def get_project_dir(cwd: Path, parent_path_str: str) -> Path:
    """
    -> recursive path search until getting main
    :param cwd: pathlib.Path obj
    :param parent_path_str: string that is contained within the path
    :return: Path parent with target string as dir
    """

    if cwd.name != parent_path_str:
        parent_path = cwd.parent
        # always return the recursion, otherwise output is None
        return get_project_dir(cwd=parent_path, parent_path_str=parent_path_str)
    else:
        return cwd


# JSON file handling
# ------------------
def get_json_dict(json_file_path: str) -> dict:
    """
    :param json_file_path: string path of JSON file
    :return: python dictionary of JSON file
    """

    if not Path(json_file_path).exists():
        raise FileExistsError("JSON File could not be found!")
    with open(json_file_path, 'r') as in_file:
        return json.load(in_file)


def save_as_json_dict(dict_saving: dict, json_file_path: str, name_file: str) -> None:
    """
    :param dict_saving: dictionary that should be written to JSON file
    :param json_file_path: target directory
    :param name_file: name of file without the '.json'
    :return:
    """

    if Path(json_file_path).exists() and isinstance(dict_saving, dict):  # w is overwrite, a is append
        target_file = Path(json_file_path) / f"{name_file}.json"
        if not target_file.exists():  # check if file exists, otherwise touch
            target_file.touch()
            print(f"File {target_file} has been created...")
        with open(target_file, "w") as out_file:
            json.dump(dict_saving, out_file)
    else:
        raise ValueError("Inputted path or dictionary are incorrect!")


# debugging
if __name__ == "__main__":
    pass
