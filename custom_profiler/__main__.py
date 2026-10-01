import argparse
from rich import print
from . import __version__
from .functions import interactive_mode, generate_mutations, save_dictionary

def banner():
    print("[bold cyan]=============================================[/bold cyan]")
    print("[bold green]       ADVANCED CUSTOM PROFILER      [/bold green]")
    print("[bold cyan]=============================================[/bold cyan]")
    print(f"               [italic]Version {__version__}[/italic]\n")

def main():
    banner()
    info = interactive_mode()
    
    if any(info.values()):
        print("\n[bold yellow][*] Generating dictionary based on profile...[/bold yellow]")
        dictionary = generate_mutations(info)
        save_dictionary(dictionary, info['firstname'])
    else:
        print("[bold red][-] No information provided. Exiting.[/bold red]")

if __name__ == "__main__":
    main()