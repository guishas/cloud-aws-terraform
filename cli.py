from functions import *
import time
import json

console = Console()

def main():
    selected_index = -1

    console.print("Bem-vindo à PyTerraform AWS CLI", style="bold purple")
    console.print("Buscando credenciais AWS...", style="bold yellow")
    time.sleep(1)
    check_if_credentials_are_set()

    while selected_index != 5:
        options = ["[1] Criar", "[2] Listar", "[3] Deletar", "[4] Terraform CLI", "[5] Recredenciar", "[6] Sair"]
        terminal_menu = TerminalMenu(options, title="Escolha uma opção:")
        selected_index = terminal_menu.show()

        if selected_index == 0:
            options = ["[1] VPC", "[2] Subnet", "[3] Instância", "[4] Grupo de Segurança", "[5] Usuário", "[6] Voltar"]
            terminal_menu = TerminalMenu(options, title="O que deseja criar?")
            selected_index_create = terminal_menu.show()

            if selected_index_create == 0:
                vpc_name = console.input("Digite o nome da VPC: ")
                vpc_cidr = console.input("[bold red]CUIDADO! Use o formato x.x.x.x/x[/bold red] Digite o CIDR da VPC: ")
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                data["vpcs"].append({"name": vpc_name, "cidr": vpc_cidr})
                with open('terraform/variables.json', 'w') as f:
                    json.dump(data, f, indent=4)
                console.print("\n")

            if selected_index_create == 1:
                subnet_name = console.input("Digite o nome da Subnet: ")
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                options = [vpc["name"] for vpc in data["vpcs"]]
                terminal_menu = TerminalMenu(options, title="Em qual VPC deseja criar a Subnet?")
                selected_index_vpc = terminal_menu.show()
                vpc_name = options[selected_index_vpc]
                subnet_cidr = console.input("[bold red]CUIDADO! Use o formato x.x.x.x/x[/bold red] Digite o CIDR da Subnet: ")
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                data["subnets"].append({"name": subnet_name, "vpc_name": vpc_name, "cidr": subnet_cidr})
                with open('terraform/variables.json', 'w') as f:
                    json.dump(data, f, indent=4)
                console.print("\n")

            if selected_index_create == 2:
                instance_name = console.input("Digite o nome da Instância: ")
                options = ["t1.micro", "t2.nano", "t2.micro", "t2.small", "t2.medium", "t2.large"]
                terminal_menu = TerminalMenu(options, title="Escolha o tipo da Instância:")
                selected_index_instance_type = terminal_menu.show()
                instance_type = options[selected_index_instance_type]
                imgs = {
                    "Ubuntu Server 22.04 LTS": "ami-08c40ec9ead489470",
                    "Ubuntu Server 20.04 LTS": "ami-0149b2da6ceec4bb0",
                }
                options = ["Ubuntu Server 22.04 LTS", "Ubuntu Server 20.04 LTS"]
                terminal_menu = TerminalMenu(options, title="Escolha a imagem da Instância:")
                selected_index_instance_image = terminal_menu.show()
                instance_image = imgs[options[selected_index_instance_image]]
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                data["instances"].append({"name": instance_name, "instance_type": instance_type, "ami": instance_image, "image": options[selected_index_instance_image]})
                with open('terraform/variables.json', 'w') as f:
                    json.dump(data, f, indent=4)
                console.print("\n")

        if selected_index == 1:
            options = ["[1] VPCs", "[2] Subnets", "[3] Instâncias", "[4] Grupos de Segurança", "[5] Usuários", "[6] Voltar"]
            terminal_menu = TerminalMenu(options, title="O que deseja listar?")
            selected_index_list = terminal_menu.show()

            if selected_index_list == 0:
                console.print("Listando VPCs", style="bold cyan")
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                for index, vpc in enumerate(data["vpcs"]):
                    console.print(f"[bold purple][{index+1}][/bold purple] [bold purple]Nome:[/bold purple] {vpc['name']}, [bold purple]CIDR:[/bold purple] {vpc['cidr']}")
                console.print("\n")

            if selected_index_list == 1:
                console.print("Listando Subnets", style="bold cyan")
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                for index, subnet in enumerate(data["subnets"]):
                    console.print(f"[bold purple][{index+1}][/bold purple] [bold purple]Nome:[/bold purple] {subnet['name']}, [bold purple]VPC:[/bold purple] {subnet['vpc_name']}, [bold purple]CIDR:[/bold purple] {subnet['cidr']}")
                console.print("\n")

            if selected_index_list == 2:
                console.print("Listando Instâncias", style="bold cyan")
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                for index, instance in enumerate(data["instances"]):
                    console.print(f"[bold purple][{index+1}][/bold purple] [bold purple]Nome:[/bold purple] {instance['name']}, [bold purple]Tipo:[/bold purple] {instance['instance_type']}, [bold purple]Imagem:[/bold purple] {instance['image']}")
                console.print("\n")

            if selected_index_list == 3:
                console.print("Listando Grupos de Segurança", style="bold cyan")
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                for index, sg in enumerate(data["security_groups"]):
                    console.print(f"[bold purple][{index+1}][/bold purple] [bold purple]Nome:[/bold purple] {sg['name']}, [bold purple]VPC:[/bold purple] {sg['vpc_name']}, [bold purple]Regras:[/bold purple] {sg['rules']}")
                console.print("\n")

        if selected_index == 2:
            options = ["[1] VPC", "[2] Subnet", "[3] Instância", "[4] Grupo de Segurança", "[5] Usuário", "[6] Voltar"]
            terminal_menu = TerminalMenu(options, title="O que deseja deletar?")
            selected_index_delete = terminal_menu.show()

        if selected_index == 3:
            options = ["[1] Init", "[2] Plan", "[3] Apply", "[4] Destroy", "[5] Voltar"]
            terminal_menu = TerminalMenu(options, title="O que deseja fazer?")
            selected_index_terraform = terminal_menu.show()

            if selected_index_terraform == 0:
                run_terraform_command("init")

            if selected_index_terraform == 1:
                run_terraform_command("plan")

            if selected_index_terraform == 2:
                run_terraform_command("apply")

            if selected_index_terraform == 3:
                run_terraform_command("destroy")

        if selected_index == 4:
            reset_credentials()


if __name__ == '__main__':
    main()