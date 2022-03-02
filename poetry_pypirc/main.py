from configparser import ConfigParser
from pathlib import Path
import sh
import toml

PYPIRC_FILE = Path.home() / ".pypirc"


def main():
    parser = ConfigParser()
    parser.read(PYPIRC_FILE)
    pypirc = parser._sections

    index_servers = (pypirc.get("distutils") or {}).get('index-servers')
    if not index_servers:
        return
    
    config = pypirc.get(index_servers) or {}
    if config.get("repository"):
        sh.poetry.config(f"repositories.{index_servers}", config["repository"])
    
    if config.get("username") and config.get("password"):
        sh.poetry.config(f"http-basic.{index_servers}", config.get("username"), config.get("password"))

if __name__ == '__main__':
    main()