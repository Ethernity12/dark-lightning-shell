from pathlib import Path
from typing import List
import argparse
import logging
import subprocess, shutil, os, tempfile, colorama


def install_script(pkg_list: List[str]) -> None:
    for pkg in pkg_list:
        logger.info(colorama.Fore.CYAN + 'Checking ' + colorama.Style.BRIGHT + f'{pkg}' + colorama.Style.RESET_ALL + colorama.Fore.CYAN + ' package...')
        if not is_pkg_exits(pkg):
            logger.info(colorama.Fore.YELLOW + 'Installing package: ' + colorama.Style.BRIGHT + f'{pkg}')
            install_pkg(pkg)
            logger.info(colorama.Fore.GREEN + 'Successfully installed: ' + colorama.Style.BRIGHT + f'{pkg}')
        else:
            logger.info(colorama.Fore.GREEN +  colorama.Style.BRIGHT + f'{pkg}' + colorama.Style.RESET_ALL + colorama.Fore.GREEN + ' package is already installed, skipping...')


def install_pkg(pkg_name: str) -> None:
    subprocess.run(['sudo', 'paru', '-S', '--noconfirm', f'{pkg_name}'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)

def is_pkg_exits(pkg_name: str) -> bool:
    return shutil.which(pkg_name)

def test_installer():
    install_script(['git', 'wget', 'nano'])


if not shutil.which('paru'):
    subprocess.run(
        ['sudo', 'pacman', '-S', '--needed', 'base-devel']
    )
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "paru"

        subprocess.run(
            ["git", "clone", "https://aur.archlinux.org/paru.git", str(repo)],
        )

        subprocess.run(
            ["makepkg", "-si", "--noconfirm"],
            cwd=repo,
        )


if __name__ == '__main__':
    # ---- Initial script settings ----
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()


    # ---- Logger setup ----
    logger = logging.getLogger('installer')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()

    if args.quiet:
        handler.setLevel(logging.ERROR)
    elif args.verbose:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(handler)

    test_installer()