import os
from sys import argv
import tomllib
from typing import Any, Dict, List, Union
from rich.console import Console

def get_key_from_values(value: Any, _dict: Dict[Any, List[Any]]) -> Any:
    pass

console = Console()
args = argv[1:]


#* Load runtime config *#
# theme: Dict[str, Union[List, Dict[str, int], Dict[str, List[str]]]] = {
#     "colours": ["#827717", "#827717", "#cddc39", "#dce775", "#f0f4c3", "#FFFFFF"],
#     "icons": {"folder": 0xea83, "folder_open": 0xea83, "file": 0xea7b},
#     "icon_extensions": {}
# }
theme = {
    "colours": ["#827717", "#827717", "#cddc39", "#dce775", "#f0f4c3", "#FFFFFF"],
    "icons": {"folder": 0xea83, "folder_open": 0xea83, "file": 0xea7b},
    "icon_extensions": {}
}

recursion_limit = 4
if "-t" in args:
    tag_index = args.index("-t")
    try:
        file_path = args[tag_index+1]
    except IndexError:
        console.print(f"[#FF0000][bold][ERROR][/bold] No file path given after -t tag[/#FF0000]")
        quit()
    try:
        theme = tomllib.load(open(file_path, "rb"))
    except FileNotFoundError:
        console.print(f"[#FF0000][bold][ERROR][/bold] No file named {file_path}[/#FF0000]")
        quit()
if "-r" in args:
    tag_index = args.index("-r")
    try:
        recursion_limit = int(args[tag_index+1])
    except IndexError:
        console.print("[#FF0000][bold][ERROR][/bold] No value given after -r tag[/#FF0000]")
        quit()
    except ValueError:
        console.print("[#FF0000][bold][ERROR][/bold] Invalid value given for -r tag[/#FF0000]")
        quit()



theme_icons: Dict[str, int] = theme["icons"] #type:ignore
theme_colours: List[str] = theme["colours"] #type:ignore
theme_icon_extensions: Dict[str, List[str]] = theme["icon_extensions"] #type:ignore

def print_tree(path: str, max_recursion: int=4):
    for dirpath, _, filenames in os.walk(path):
        dir_name = dirpath.split("\\")[-1]
        # console.print(f"Dirpath: {dirpath}\nDir_name: {dir_name}\nFilenames: {filenames}\n")
        levels = len(dirpath.split("\\"))
        
        current_level_colour = theme_colours[levels]
        child_level_colour = theme_colours[levels+1]
        console.print(f"{"     "*(levels)}[{current_level_colour} bold]┗━━▶ {chr(theme_icons["folder" if levels >= max_recursion else "folder_open"])} {dir_name}[/{current_level_colour} bold]")
        if levels >= max_recursion:
            continue
        for file_name in filenames:
            file_name_extension = file_name.split(".")[-1]
            if file_name_extension in list(theme_icon_extensions.keys()):
                icon_id = file_name_extension
            else:
                icon_id = "file"
            console.print(f"{"     "*(levels+1)}[{child_level_colour} bold]┗━━▶ {chr(theme_icons[icon_id])} {file_name}[/{child_level_colour} bold]")

if __name__ == "__main__":
    print_tree("test", max_recursion=recursion_limit)
    # console.print(tomllib.load(open("theme.toml", "rb")))