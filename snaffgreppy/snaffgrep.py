import typer

from pathlib import Path

from constants import (
    SNAFF_RE, URL_RE, FILENAMEONLY_RE, PASS_RE, FILENAME_RE, NETUSE_RE
)
from dirtree import DirectoryTree


app = typer.Typer()


@app.command()
def main(
    snaffler_file: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    exclusion_content: str = typer.Option(
        None
    )
):
    with open(snaffler_file, "r") as snaffile:
        snaffresults = snaffile.readlines()
    content_library: list = []
    credentials: dict = {}
    for line in snaffresults:
        linematch = SNAFF_RE.search(line)
        if linematch:
            content = linematch.group("found_content")
            if content.endswith("\\"):
                content = content[:-1]
            content = content.replace("\\r\\n", "\r\n")
            content = content.replace("\\n", "\r\n")
            content = content.replace("\\t", "\t")
            content = content.replace("\\(", "(")
            content = content.replace("\\)", ")")
            content = content.replace("\\ ", " ")
            content = content.replace("\\.", ".")
            content = content.replace("\\$", "$")
            content = content.replace("\\#", "#")
            content = content.replace("\\*", "*")
            content = content.replace("\\[", "[")
            content = content.replace("\\\\", "\\")
            # disable print of filenames and filenendings (only) without content
            filenameonly = FILENAMEONLY_RE.match(content)
            # filter out "HasPassword,LookNearbyFor.txtFiles"
            if not content == "HasPassword,LookNearbyFor.txtFiles" and \
                    content not in content_library and \
                    not filenameonly and \
                    linematch.group("found_type") == "File":
                if exclusion_content:
                    # TODO: loop
                    # TODO: only print if exclusion not in content
                    pass
                typer.secho(typer.style(linematch.group("found_path"), fg=typer.colors.GREEN))
                password = PASS_RE.search(content)
                if password:
                    content = content[:password.start()] + typer.style(content[password.start():password.end()], fg=typer.colors.RED) + content[password.end():]
                typer.secho(content)
                print()
                credz = NETUSE_RE.search(content)
                if credz:
                    user = ""
                    if credz.group("domain"):
                        user += credz.group("domain")  + "\\"
                    user += credz.group("username")
                    credentials[user] = credz.group("password")
                content_library.append(content)
    typer.secho(typer.style("CREDENTIALS:"), bg=typer.colors.GREEN)
    for user in credentials:
        print("\t", user, credentials[user])


@app.command()
def paths(
    snaffler_file: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )
):
    paths = [
        r"\\HOST1.PRAHA.CZCOMPANY.CZ\MONT$\PC02\boot.PC02.wim",
        r"\\HOST1.PRAHA.CZCOMPANY.CZ\MONT$\PC02\boot.PC05.wim",
        r"\\HOST1.PRAHA.CZCOMPANY.CZ\Dev$\Apps\NEW set\Unattend.xml",
        r"\\HOST1.PRAHA.CZCOMPANY.CZ\Dev$\Isos\boot\WinPE.wim"
    ]
    tree: DirectoryTree = DirectoryTree()
    for path in paths:
        tree.add_unc(path)
    print(tree.drives)


if __name__ == "__main__":
    app()
