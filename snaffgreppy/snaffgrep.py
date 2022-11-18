import typer
import re

from pathlib import Path


app = typer.Typer()

SNAFF_RE = re.compile(r"^\[(?P<execution_system>).*\] (?P<found_timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}Z) \[(?P<found_type>.*)\] \{(?P<found_rating>.*)\}\<(?P<found_details>.*)\>\((?P<found_path>.*)\) (?P<found_content>.*)")
FILENAME_RE = re.compile(r"^([a-zA-Z0-9\s_\\.\-\(\):])+.\w*$")
PASS_RE = re.compile(r"[Pp][aA][sS][sS]([wW][oO][rR][dD])*|[Pp][wW][dD]")
URL_RE = re.compile(r"https?:\/\/(www\\*\.)?[-a-zA-Z0-9@:%\\._\+~#=$]{1,256}\\*\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+\\.~#?&//=]*)")
FILENAMEONLY_RE = re.compile(r"^(\w)*\.\w+$")


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
    )
):
    with open(snaffler_file, "r") as snaffile:
        snaffresults = snaffile.readlines()
    for line in snaffresults:
        linematch = SNAFF_RE.search(line)
        if linematch:
            content = linematch.group("found_content")
            if content.endswith("\\"):
                content = content[:-1]
            content = content.replace("\\r\\n", "\r\n")
            content = content.replace("\\n", "\r\n")
            content = content.replace("\\ ", " ")
            content = content.replace("\\.", ".")
            content = content.replace("\\#", "#")
            content = content.replace("\\*", "*")
            content = content.replace("\\[", "[")
            content = content.replace("\\\\", "\\")
            # disable print of filenames and filenendings (only) without content
            filenameonly = FILENAMEONLY_RE.match(content)
            # filter out "HasPassword,LookNearbyFor.txtFiles"
            if not content == "HasPassword,LookNearbyFor.txtFiles" and \
                    not filenameonly and \
                    linematch.group("found_type") == "File":
                typer.secho(typer.style(linematch.group("found_path"), fg=typer.colors.GREEN))
                print(content)
                print()


if __name__ == "__main__":
    app()