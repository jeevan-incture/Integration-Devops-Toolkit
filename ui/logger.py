"""
Modern TUI logging and output utilities.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn
from rich.syntax import Syntax
from rich.text import Text
from rich import box
from datetime import datetime
import time


console = Console()


class Logger:
    """Modern TUI logger with rich formatting."""

    @staticmethod
    def header(title: str, subtitle: str = "") -> None:
        """Display header panel."""
        content = title
        if subtitle:
            content += f"\n[dim]{subtitle}[/dim]"
        
        console.print(
            Panel(
                content,
                expand=False,
                border_style="cyan",
                style="bold cyan"
            )
        )

    @staticmethod
    def success(message: str) -> None:
        """Display success message."""
        console.print(f"[bold green]✓[/bold green] {message}")

    @staticmethod
    def error(message: str) -> None:
        """Display error message."""
        console.print(f"[bold red]✗[/bold red] {message}")

    @staticmethod
    def warning(message: str) -> None:
        """Display warning message."""
        console.print(f"[bold yellow]⚠[/bold yellow] {message}")

    @staticmethod
    def info(message: str) -> None:
        """Display info message."""
        console.print(f"[bold blue]ℹ[/bold blue] {message}")

    @staticmethod
    def step(step_num: int, message: str) -> None:
        """Display numbered step."""
        console.print(f"[bold cyan]→[/bold cyan] [bold]{step_num}.[/bold] {message}")

    @staticmethod
    def section(title: str) -> None:
        """Display section divider."""
        console.print(f"\n[bold magenta]━━ {title} ━━[/bold magenta]\n")

    @staticmethod
    def table_iflows(iflows: list[dict]) -> None:
        """Display IFlows in a formatted table."""
        table = Table(title="Integration Flows to Synchronize", box=box.ROUNDED)
        
        table.add_column("Status", style="cyan", width=15)
        table.add_column("IFlow ID", style="green", width=25)
        table.add_column("Name", style="blue", width=30)
        table.add_column("Version", style="yellow", width=10)

        for iflow in iflows:
            status = iflow.get("status", "SYNC")
            status_style = {
                "INITIAL_SYNC": "bold green",
                "NEW_IFLOW": "bold cyan",
                "VERSION_CHANGED": "bold yellow"
            }.get(status, "white")

            table.add_row(
                f"[{status_style}]{status}[/{status_style}]",
                iflow.get("id", "N/A"),
                iflow.get("name", "N/A")[:28],
                iflow.get("version", "N/A")
            )

        console.print(table)

    @staticmethod
    def download_progress(total_files: int):
        """Create progress bar for downloads."""
        return Progress(
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            DownloadColumn(),
            TextColumn("•"),
            TransferSpeedColumn(),
            console=console
        )

    @staticmethod
    def task_progress():
        """Create progress bar for tasks."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        )

    @staticmethod
    def summary(title: str, items: dict) -> None:
        """Display summary panel."""
        summary_text = "\n".join([f"[cyan]{k}:[/cyan] {v}" for k, v in items.items()])
        
        console.print(
            Panel(
                summary_text,
                title=title,
                border_style="green",
                style="bold green"
            )
        )

    @staticmethod
    def error_panel(title: str, error_msg: str) -> None:
        """Display error panel."""
        console.print(
            Panel(
                error_msg,
                title=title,
                border_style="red",
                style="bold red"
            )
        )

    @staticmethod
    def json_output(data: dict) -> None:
        """Display JSON data with syntax highlighting."""
        import json
        json_str = json.dumps(data, indent=2)
        syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
        console.print(syntax)

    @staticmethod
    def table_packages(packages: list[dict]) -> None:
        """Display packages in a formatted table."""
        table = Table(title="Packages to Synchronize", box=box.ROUNDED)
        
        table.add_column("ID", style="cyan", width=20)
        table.add_column("Name", style="green", width=30)
        table.add_column("Description", style="blue", width=40)

        for pkg in packages:
            table.add_row(
                pkg.get("id", "N/A"),
                pkg.get("name", "N/A")[:28],
                pkg.get("description", "")[:38]
            )

        console.print(table)

    @staticmethod
    def success_banner(title: str, message: str = "") -> None:
        """Display success banner with emoji."""
        content = f"[bold green]{title}[/bold green]"
        if message:
            content += f"\n[dim]{message}[/dim]"
        
        console.print(
            Panel(
                content,
                border_style="green",
                style="bold green",
                expand=False,
                padding=(1, 2)
            )
        )

    @staticmethod
    def error_banner(title: str, error_msg: str = "") -> None:
        """Display error banner with emoji."""
        content = f"[bold red]{title}[/bold red]"
        if error_msg:
            content += f"\n[dim red]{error_msg}[/dim red]"
        
        console.print(
            Panel(
                content,
                border_style="red",
                style="bold red",
                expand=False,
                padding=(1, 2)
            )
        )

    @staticmethod
    def workflow_step(step_num: int, title: str, status: str = "pending") -> None:
        """Display workflow step with status indicator."""
        indicators = {
            "pending": "[yellow]⏳[/yellow]",
            "running": "[cyan]🔄[/cyan]",
            "success": "[green]✓[/green]",
            "error": "[red]✗[/red]",
            "skipped": "[dim]⊘[/dim]"
        }
        
        indicator = indicators.get(status, "?")
        console.print(f"{indicator} [{step_num}] {title}")

    @staticmethod
    def progress_section(section_name: str) -> None:
        """Display progress section divider."""
        console.print(f"\n[bold cyan]━━━━ {section_name} ━━━━[/bold cyan]\n")

    @staticmethod
    def stats_box(stats: dict) -> None:
        """Display statistics in a beautiful box."""
        table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
        
        for key, value in stats.items():
            table.add_row(f"[cyan]{key}[/cyan]", f"[bold yellow]{value}[/bold yellow]")
        
        console.print(
            Panel(
                table,
                border_style="cyan",
                padding=(1, 2),
                expand=False
            )
        )

    @staticmethod
    def loading_spinner(message: str) -> None:
        """Display loading message with spinner."""
        from rich.spinner import Spinner
        with console.status(f"[bold cyan]{message}[/bold cyan]", spinner="dots"):
            time.sleep(1)