import os
from simple_term_menu import TerminalMenu
from rich.console import Console
import time

console = Console()

def create_aws_credentials_environment_variables(aws_access_key, aws_secret_key):
    os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key

def set_credentials():
    aws_access_key = console.input("Digite sua AWS Access Key ID: ")
    aws_secret_key = console.input("Digite sua AWS Secret Access Key: ")
    create_aws_credentials_environment_variables(aws_access_key, aws_secret_key)
    console.print("Credenciais criadas com sucesso!\n", style="bold green")

def reset_credentials():
    console.print("Vamos te recredenciar, espere um momento...", style="bold yellow")
    time.sleep(1)
    aws_access_key = console.input("Digite sua AWS Access Key ID: ")
    aws_secret_key = console.input("Digite sua AWS Secret Access Key: ")
    create_aws_credentials_environment_variables(aws_access_key, aws_secret_key)
    console.print("Credenciais recriadas com sucesso!\n", style="bold green")

def check_if_credentials_are_set():
    if os.environ.get('AWS_ACCESS_KEY_ID') is None or os.environ.get('AWS_SECRET_ACCESS_KEY') is None:
        console.print("Credenciais não encontradas!", style="bold red")
        console.print("Para começar, vamos te credenciar para o funcionamento correto da aplicação!")
        set_credentials()

def run_terraform_command(command):
    cwd = os.getcwd()
    os.chdir(cwd + "/terraform")
    os.system(f"terraform {command}")
    os.chdir(cwd)
    console.print("\n")