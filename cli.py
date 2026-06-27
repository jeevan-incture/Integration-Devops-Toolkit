"""
Entry point for the SAP Integration DevOps Toolkit.
"""

import argparse
import sys
from commands.sync import run as sync_run
from ui.logger import Logger, console
from ui.help import (
    MAIN_HELP, MAIN_EPILOG, 
    SYNC_HELP, SYNC_DESCRIPTION, SYNC_EPILOG,
    CONFIG_HELP, PACKAGE_HELP
)
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich import box


def display_banner() -> None:
    """Display enhanced application banner with ASCII art."""
    
    banner_art = """
[bold cyan]
  ███████╗ █████╗ ██████╗     ██╗███╗   ██╗████████╗    ██████╗ ███████╗██╗   ██╗ ██████╗ ██████╗ ███████╗
  ██╔════╝██╔══██╗██╔══██╗    ██║████╗  ██║╚══██╔══╝    ██╔══██╗██╔════╝██║   ██║██╔═══██╗██╔══██╗██╔════╝
  ███████╗███████║██████╔╝    ██║██╔██╗ ██║   ██║       ██║  ██║█████╗  ██║   ██║██║   ██║██████╔╝███████╗
  ╚════██║██╔══██║██╔═══╝     ██║██║╚██╗██║   ██║       ██║  ██║██╔══╝  ╚██╗ ██╔╝██║   ██║██╔═══╝ ╚════██║
  ███████║██║  ██║██║         ██║██║ ╚████║   ██║       ██████╔╝███████╗ ╚████╔╝ ╚██████╔╝██║     ███████║
  ╚══════╝╚═╝  ╚═╝╚═╝         ╚═╝╚═╝  ╚═══╝   ╚═╝       ╚═════╝ ╚══════╝  ╚═══╝   ╚═════╝ ╚═╝     ╚══════╝
[/bold cyan]
    """
    
    console.print(banner_art)
    
    subtitle = Text("Seamless synchronization of SAP Integration Flows to GitHub", justify="center")
    subtitle.stylize("dim cyan")
    console.print(subtitle)
    console.print()


def display_system_info() -> None:
    """Display system information panel."""
    
    info_table = Table(title="System Information", box=box.SIMPLE, show_header=False)
    info_table.add_column("", style="dim", width=20)
    info_table.add_column("", style="cyan")
    
    info_table.add_row("[cyan]Version[/cyan]", "1.0.0")
    info_table.add_row("[cyan]Status[/cyan]", "[green]✓ Ready[/green]")
    info_table.add_row("[cyan]Environment[/cyan]", "[yellow]Production[/yellow]")
    
    console.print(
        Panel(
            info_table,
            border_style="magenta",
            padding=(0, 1)
        )
    )
    console.print()


def display_config_menu() -> str:
    """Display configuration format selection menu."""
    
    config_table = Table(title="Select Configuration Format", box=box.ROUNDED, show_header=True)
    config_table.add_column("Option", style="cyan", width=10)
    config_table.add_column("Format", style="green", width=15)
    config_table.add_column("Description", style="yellow", width=50)
    
    config_table.add_row("[bold]1[/bold]", "JSON", "Structured data format - Recommended")
    config_table.add_row("[bold]2[/bold]", "CSV", "Spreadsheet format - Easy to edit")
    
    console.print(config_table)
    console.print()
    
    choice = Prompt.ask(
        "[cyan bold]Choose configuration format[/cyan bold]",
        choices=["1", "2"],
        default="1"
    )
    
    format_map = {"1": "json", "2": "csv"}
    return format_map[choice]


def display_sync_menu() -> dict:
    """Display sync options menu."""
    
    sync_table = Table(title="Select Sync Mode", box=box.ROUNDED, show_header=True)
    sync_table.add_column("Option", style="cyan", width=10)
    sync_table.add_column("Mode", style="green", width=15)
    sync_table.add_column("Description", style="yellow", width=50)
    
    sync_table.add_row("[bold]1[/bold]", "All Packages", "Sync all packages from config")
    sync_table.add_row("[bold]2[/bold]", "Single Package", "Sync a specific package")
    
    console.print(sync_table)
    console.print()
    
    choice = Prompt.ask(
        "[cyan bold]Choose sync mode[/cyan bold]",
        choices=["1", "2"],
        default="1"
    )
    
    result = {"mode": "all", "package_id": None}
    
    if choice == "2":
        result["mode"] = "single"
        package_id = Prompt.ask("[cyan bold]Enter Package ID[/cyan bold]")
        result["package_id"] = package_id.strip()
    
    return result


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    
    parser = argparse.ArgumentParser(
        prog="integration-devops",
        description=MAIN_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=MAIN_EPILOG,
        add_help=True
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sync command
    sync_parser = subparsers.add_parser(
        "sync",
        help=SYNC_HELP,
        description=SYNC_DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=SYNC_EPILOG
    )
    
    sync_parser.add_argument(
        "--config",
        choices=["json", "csv"],
        help=CONFIG_HELP,
        required=False,
        metavar="FORMAT"
    )
    
    sync_parser.add_argument(
        "--package",
        type=str,
        help=PACKAGE_HELP,
        required=False,
        metavar="PACKAGE_ID",
        dest="package"
    )

    return parser


def main() -> None:
    # Display enhanced banner
    console.clear()
    display_banner()
    display_system_info()
    
    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.command == "sync":
            console.print()
            
            # Get config format
            config_format = args.config
            if not config_format:
                config_format = display_config_menu()
            
            # Get sync mode
            sync_options = args.package
            if not sync_options:
                sync_options = display_sync_menu()
                package_id = sync_options.get("package_id")
            else:
                package_id = sync_options
            
            console.print()
            sync_run(config_format=config_format, package_id=package_id)
        
    except KeyboardInterrupt:
        Logger.warning("\n\n⏹ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        console.print()
        Logger.error_panel("❌ Fatal Error", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()