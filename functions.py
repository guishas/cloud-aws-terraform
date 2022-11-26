import os
from simple_term_menu import TerminalMenu
from rich.console import Console
import time
import json
from textwrap import dedent

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
        console.print("[ATENÇÃO] Você pode colocar suas credenciais nas variáveis de ambiente do seu sistema, facilitando o uso da aplicação!", style="bold yellow")
        console.print("Para fazer isso, basta criar as variáveis de ambiente AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY com suas credenciais!", style="bold yellow")
        console.print("Caso não saiba como fazer isso, é simples: no terminal digite export AWS_ACCESS_KEY_ID=<sua_access_key_id> e depois export AWS_SECRET_ACCESS_KEY=<sua_secret_access_key>", style="bold yellow")
        console.print("Por agora, vamos te credenciar para que você possa usar a aplicação!\n", style="bold yellow")
        set_credentials()
    else:
        console.print("Credenciais encontradas! Agora é só usufruir da aplicação\n", style="bold green")

def run_terraform_command(command):
    write_instances_and_sgs_to_file()
    cwd = os.getcwd()
    os.chdir(cwd + "/terraform")
    os.system(f"terraform {command}")
    os.chdir(cwd)
    console.print("\n")

def write_instances_and_sgs_to_file():
    f = open("terraform/variables.json")
    data = json.load(f)
    f.close()

    with open("terraform/basefile.txt", "r") as f:
        with open("terraform/resources.tf", "w") as ff:
            for line in f.readlines():
                ff.write(line)

    with open("terraform/resources.tf", "a") as f:
        for instance in data["instances"]:
            tf = dedent("""
            resource "aws_instance" "{}" {{
                instance_type   = "{}"
                ami             = "{}"
                
                vpc_security_group_ids = [
                    tobool("{}") ? aws_security_group.{}.id : aws_security_group.default.id
                ]

                depends_on = [
                    aws_security_group.{}, aws_security_group.default
                ]
                
                tags = {{
                    Name = "{}"
                }}
            }}
            """.format(instance["name"], instance["instance_type"], instance["ami"], str(instance["has_sg"]).lower(), instance["sg"], instance["sg"], instance["name"]))

            f.write(tf)

        for sg in data["security_groups"]:
            tf = dedent("""
            resource "aws_security_group" "{}" {{
                name        = "{}"
                vpc_id      = "vpc-5d9e5327"

                ingress {{
                    from_port        = 22
                    to_port          = 22
                    protocol         = "tcp"
                    cidr_blocks      = ["0.0.0.0/0"]
                }}

                egress {{
                    from_port        = 0
                    to_port          = 0
                    protocol         = "-1"
                    cidr_blocks      = ["0.0.0.0/0"]
                }}

                tags = {{
                    Name = "{}"
                }}
            }}
            """.format(sg["name"], sg["name"], sg["name"]))

            f.write(tf)

        for sn in data["subnets"]:
            tf = dedent("""
            resource "aws_subnet" "{}" {{
                vpc_id                  = aws_vpc.{}.id
                cidr_block              = "{}"

                depends_on = [
                    aws_vpc.{}
                ]

                tags = {{
                    Name = "{}"
                }}
            }}
            """.format(sn["name"], sn["vpc_name"], sn["cidr"], sn["vpc_name"], sn["name"]))

            f.write(tf)

        for vpc in data["vpcs"]:
            tf = dedent("""
            resource "aws_vpc" "{}" {{
                cidr_block = "{}"

                tags = {{
                    Name = "{}"
                }}
            }}
            """.format(vpc["name"], vpc["cidr"], vpc["name"]))

            f.write(tf)