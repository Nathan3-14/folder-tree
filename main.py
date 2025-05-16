from math import exp
import os
import tomllib
from rich.console import Console

console = Console()
try:
    config = tomllib.load(open("config.toml", "rb"))
except FileNotFoundError:
    console.print("[#FFAF00 bold]\[WARN] No config file found, loading default[/#FFAF00 bold]") #type:ignore
    config = {
        "colours": ["#827717", "#827717", "#cddc39", "#dce775", "#f0f4c3"],
        "icons": {}
    }

config_icons = config["icons"]
config_colours = config["colours"]

def print_tree(path: str, max_recursion: int=5):
    for dirpath, _, filenames in os.walk(path):
        dir_name = dirpath.split("\\")[-1]
        # console.print(f"Dirpath: {dirpath}\nDir_name: {dir_name}\nFilenames: {filenames}\n")
        levels = len(dirpath.split("\\"))
        
        level_colour = config_colours[levels]
        console.print(f"{"   "*levels}[{level_colour} bold]┗━━━▶ {chr(config_icons["folder"])} {dir_name}[/{level_colour} bold]")
        if levels >= max_recursion:
            continue
        for file_name in filenames:
            console.print(f"{"   "*(levels+1)}   [{level_colour} bold]┗━━━▶ {chr(config_icons["file"])} {file_name}[/{level_colour} bold]")

if __name__ == "__main__":
    print_tree("test")