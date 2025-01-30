import datetime
import hashlib
from pathlib import Path

import typer
from julep.types.agent import Agent
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from .app import import_app, console, error_console
from .models import LockedEntity
from .utils import (
    add_entity_to_lock_file,
    get_entity_from_lock_file,
    get_julep_client,
    add_agent_to_julep_yaml,
    update_existing_entity_in_lock_file,
    update_yaml_for_existing_entity,
)


@import_app.command()
def agent(
    id: str = typer.Option(..., "--id", "-i", help="ID of the agent to import"),
    source: Path = typer.Option(
        Path.cwd(),
        "--source",
        "-s",
        help="Path to the source directory. Defaults to current working directory",
    ),
    output: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Path to save the imported agent. Defaults to <project_dir>/src/agents",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """
    Import an agent from the Julep platform.
    """

    output = output or source / "src/agents"

    if not (source / "julep-lock.json").exists():
        error_console.print(Text(
            "Error: 'julep-lock.json' not found in the source directory. Please run 'julep sync' to sync your project and create a lock file.",
            style="bold red"
        ))
        raise typer.Exit(1)

    client = get_julep_client()

    # Importing an existing agent
    if locked_agent := get_entity_from_lock_file(type="agent", id=id, project_dir=source):
        console.print(Text(f"Agent '{id}' already exists in the lock file", style="bold yellow"))
        confirm = typer.confirm(
            f"Do you want to overwrite the existing agent in the lock file and {locked_agent.path}?"
        )

        if not confirm:
            console.print(Text("Operation cancelled", style="bold red"))
            raise typer.Exit(1)

        console.print(Text("Overwriting existing agent...", style="bold yellow"))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console
        ) as progress:
            try:
                fetch_task = progress.add_task("Fetching agent from remote...", start=False)
                progress.start_task(fetch_task)
                remote_agent: Agent = client.agents.get(agent_id=id)
            except Exception as e:
                error_console.print(Text(f"Error fetching agent from remote: {e}", style="bold red"))
                raise typer.Exit(1)
        
        # Create a table to display agent data
        table = Table(title="Agent Data")
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        # Populate the table with agent data
        for key, value in remote_agent.model_dump().items():
            table.add_row(key, str(value))

        console.print(table)

        agent_yaml_path = source / locked_agent.path

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console
        ) as progress:
            try:
                update_task = progress.add_task("Updating agent in '{agent_yaml_path}'...", start=False)
                progress.start_task(update_task)
                update_yaml_for_existing_entity(
                    agent_yaml_path,
                    remote_agent.model_dump(exclude={"id", "created_at", "updated_at"}),
                )
            except Exception as e:
                error_console.print(Text(f"Error updating agent in '{agent_yaml_path}': {e}", style="bold red"))
                raise typer.Exit(1)

        console.print(Text(f"Updated successfully.", style="bold green"))


        console.print(Text(f"Updating agent '{id}' in lock file...", style="bold blue"))
        update_existing_entity_in_lock_file(
            type="agent",
            new_entity=LockedEntity(
                path=str(agent_yaml_path.relative_to(source)),
                id=id,
                last_synced=datetime.datetime.now().isoformat(timespec="milliseconds") + "Z",
                revision_hash=hashlib.sha256(
                    remote_agent.model_dump_json().encode()
                ).hexdigest(),
            ),
            project_dir=source,
        )

        console.print(Text(f"Agent '{id}' imported successfully to '{agent_yaml_path}'", style="bold green"))

        return

    # Importing a new agent (doesn't exist in lock file)
    if not yes:
        confirm = typer.confirm(f"Are you sure you want to import agent '{id}' to '{output}'?")
        if not confirm:
            console.print(Text("Operation cancelled", style="bold red"))
            raise typer.Exit

    try:
        client = get_julep_client()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console
        ) as progress:
            try:
                fetch_task = progress.add_task(
                    "Fetching agent from remote...", start=False)
                progress.start_task(fetch_task)
                remote_agent: Agent = client.agents.get(agent_id=id)
            except Exception as e:
                error_console.print(
                    Text(f"Error fetching agent from remote: {e}", style="bold red"))
                raise typer.Exit(1)
        
        # Create a table to display agent data
        table = Table(title="Agent Data")
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        # Populate the table with agent data
        for key, value in remote_agent.model_dump().items():
            table.add_row(key, str(value))

        console.print(table)


        agent_name = remote_agent.name.lower().replace(" ", "_")

        agent_yaml_path: Path = output / f"{agent_name}.yaml"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console
        ) as progress:
            try:
                update_task = progress.add_task("Updating agent in '{agent_yaml_path}'...", start=False)
                progress.start_task(update_task)
                update_yaml_for_existing_entity(agent_yaml_path, remote_agent.model_dump(
                    exclude={"id", "created_at", "updated_at"}))
                
            except Exception as e:
                error_console.print(Text(f"Error updating agent in '{agent_yaml_path}': {e}", style="bold red"))
                raise typer.Exit(1)
        
        console.print(Text(f"Updated successfully.", style="bold green"))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console
        ) as progress:
            try:
                add_task = progress.add_task("Adding agent to julep.yaml...", start=False)
                progress.start_task(add_task)
                add_agent_to_julep_yaml(source, {
                    "definition": str(agent_yaml_path.relative_to(source)),
                })
            except Exception as e:
                error_console.print(Text(f"Error adding agent to julep.yaml: {e}", style="bold red"))
                raise typer.Exit(1)
        
        console.print(Text(f"Added successfully.", style="bold green"))

        console.print(Text(f"Adding agent to lock file...", style="bold blue"))
        add_entity_to_lock_file(
            type="agent",
            new_entity=LockedEntity(
                path=str(agent_yaml_path.relative_to(source)),
                id=remote_agent.id,
                last_synced=datetime.datetime.now().isoformat(timespec="milliseconds") + "Z",
                revision_hash=hashlib.sha256(
                    remote_agent.model_dump_json().encode()
                ).hexdigest(),
            ),
            project_dir=source,
        )

        console.print(Text(f"Agent '{id}' imported successfully to '{agent_yaml_path}' and added to lock file", style="bold green"))

    except Exception as e:
        error_console.print(Text(f"Error importing agent: {e}", style="bold red"))
        raise typer.Exit(1)