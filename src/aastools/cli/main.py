import typer
import requests

from pathlib import Path
from aastools import __version__, services, crud
from aastools.settings import settings
from aastools.upload import upload_aas, upload_aas_folder

app = typer.Typer(name="aas", help="Asset Administration Shell Tools CLI")
shell_app = typer.Typer(help="Manage Asset Administration Shells")
submodel_app = typer.Typer(help="Manage Submodels")

app.add_typer(shell_app, name="shell")
app.add_typer(submodel_app, name="submodel")


@app.callback()
def print_header():
    typer.echo("===============================================")
    typer.echo(f"Asset Administration Shell Tools v{__version__}")
    typer.echo(f"Host: {settings.host} ({services.health()})")
    typer.echo("===============================================\n")


# ───────────────────────────── info ─────────────────────────────

@app.command()
def info():
    """Display all AAS shells and their submodels."""
    typer.echo("ℹ️ Showing all shells")
    shells = crud.get_shells()

    for shell in shells:
        typer.echo(f"{shell['idShort']}: {shell['id']}")
        submodels = services.get_shell_submodels(shell["id"])
        for i, sub in enumerate(submodels):
            is_last = i == len(submodels) - 1
            prefix = "└──" if is_last else "├──"
            typer.echo(f"{prefix} {sub['idShort']}: {sub['id']}")

    submodel_ids = services.find_unreferenced_submodels()
    if submodel_ids:
        typer.echo("\n⚠️ Unreferenced Submodels:")
        for sub_id in submodel_ids:
            sub = crud.get_submodel(sub_id)
            typer.echo(f"- {sub['idShort']} ({sub_id})")


# ───────────────────────────── upload ─────────────────────────────

@app.command()
def upload(path: Path):
    """Upload an AAS file or folder."""
    if path.is_file():
        typer.echo(f"ℹ️ Uploading file: {path}")
        upload_aas(path)
    elif path.is_dir():
        typer.echo(f"ℹ️ Uploading all AAS files in folder: {path}")
        upload_aas_folder(path)
    else:
        typer.secho(f"❌ Path '{path}' does not exist or is invalid.", fg=typer.colors.RED)


# ───────────────────────────── nuke ─────────────────────────────

@app.command()
def nuke():
    """Delete all shells and submodels."""
    typer.echo("☣️ Deleting all Shells and Submodels!")
    services.delete_all_shells()
    services.delete_all_submodels()


# ───────────────────────────── shell ─────────────────────────────

@shell_app.command("delete")
def delete_shell(shell_id: str, cascade: bool = typer.Option(False, "--cascade", "-c", help="Also delete referenced submodels")):
    """Delete a shell by ID."""
    typer.echo(f"🗑️ Deleting Shell: {shell_id}")
    if cascade:
        services.delete_shell_cascading(shell_id)
        typer.echo(f"✅ Shell '{shell_id}' and its submodels deleted.")
    else:
        crud.delete_shell(shell_id)
        typer.echo(f"✅ Shell '{shell_id}' deleted.")


# ───────────────────────────── submodel ─────────────────────────────

@submodel_app.command("delete")
def delete_submodel(submodel_id: str, unlink: bool = typer.Option(False, "--unlink", "-u", help="Remove references from shells")):
    """Delete a submodel by ID."""
    typer.echo(f"🗑️ Deleting Submodel: {submodel_id}")
    try:
        crud.delete_submodel(submodel_id)
        typer.echo(f"✅ Submodel '{submodel_id}' deleted.")
    except requests.exceptions.HTTPError:
        typer.secho(f"❌ Submodel '{submodel_id}' doesn't exist.", fg=typer.colors.RED)

    if unlink:
        services.remove_submodel_references(submodel_id)
        typer.echo(f"✅ Removed Shell references to Submodel '{submodel_id}'.")


if __name__ == "__main__":
    app()
