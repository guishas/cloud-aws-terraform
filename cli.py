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

    while selected_index != 6:
        options = ["[1] Criar", "[2] Listar", "[3] Deletar", "[4] Terraform CLI", "[5] Mudar região", "[6] Recredenciar", "[7] Sair"]
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

            if selected_index_create == 3:
                sg_name = console.input("Digite o nome do Grupo de Segurança: ")
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                data["security_groups"].append({"name": sg_name})
                with open('terraform/variables.json', 'w') as f:
                    json.dump(data, f, indent=4)
                console.print("\n")

            if selected_index_create == 4:
                user_name = console.input("Digite o nome do Usuário: ")
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                data["users"].append({"name": user_name})
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

            if selected_index_list == 4:
                console.print("Listando Usuários", style="bold cyan")
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                for index, user in enumerate(data["users"]):
                    console.print(f"[bold purple][{index+1}][/bold purple] [bold purple]Nome:[/bold purple] {user['name']}")
                console.print("\n")

        if selected_index == 2:
            options = ["[1] VPC", "[2] Subnet", "[3] Instância", "[4] Grupo de Segurança", "[5] Usuário", "[6] Voltar"]
            terminal_menu = TerminalMenu(options, title="O que deseja deletar?")
            selected_index_delete = terminal_menu.show()

            if selected_index_delete == 0:
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                options = [vpc["name"] for vpc in data["vpcs"]]
                terminal_menu = TerminalMenu(options, title="Qual VPC deseja deletar?")
                selected_index_vpc = terminal_menu.show()
                vpc_name = options[selected_index_vpc]
                data["vpcs"].pop(selected_index_vpc)
                with open('terraform/variables.json', 'w') as f:
                    json.dump(data, f, indent=4)
                console.print("\n")

            if selected_index_delete == 1:
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                options = [subnet["name"] for subnet in data["subnets"]]
                terminal_menu = TerminalMenu(options, title="Qual Subnet deseja deletar?")
                selected_index_subnet = terminal_menu.show()
                subnet_name = options[selected_index_subnet]
                data["subnets"].pop(selected_index_subnet)
                with open('terraform/variables.json', 'w') as f:
                    json.dump(data, f, indent=4)
                console.print("\n")

            if selected_index_delete == 2:
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                options = [instance["name"] for instance in data["instances"]]
                terminal_menu = TerminalMenu(options, title="Qual Instância deseja deletar?")
                selected_index_instance = terminal_menu.show()
                instance_name = options[selected_index_instance]
                data["instances"].pop(selected_index_instance)
                with open('terraform/variables.json', 'w') as f:
                    json.dump(data, f, indent=4)
                console.print("\n")

            if selected_index_delete == 3:
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                options = [sg["name"] for sg in data["security_groups"]]
                terminal_menu = TerminalMenu(options, title="Qual Grupo de Segurança deseja deletar?")
                selected_index_sg = terminal_menu.show()
                sg_name = options[selected_index_sg]
                data["security_groups"].pop(selected_index_sg)
                with open('terraform/variables.json', 'w') as f:
                    json.dump(data, f, indent=4)
                console.print("\n")

            if selected_index_delete == 4:
                f = open('terraform/variables.json')
                data = json.load(f)
                f.close()
                options = [user["name"] for user in data["users"]]
                terminal_menu = TerminalMenu(options, title="Qual Usuário deseja deletar?")
                selected_index_user = terminal_menu.show()
                user_name = options[selected_index_user]
                data["users"].pop(selected_index_user)
                with open('terraform/variables.json', 'w') as f:
                    json.dump(data, f, indent=4)
                console.print("\n")

        if selected_index == 3:
            options = ["[1] Init", "[2] Plan", "[3] Apply", "[4] Destroy", "[5] Voltar"]
            terminal_menu = TerminalMenu(options, title="O que deseja fazer?")
            selected_index_terraform = terminal_menu.show()

            if selected_index_terraform == 0:
                console.print("Iniciando Terraform...", style="bold cyan")
                run_terraform_command("init")

            if selected_index_terraform == 1:
                console.print("Gerando Plan...", style="bold cyan")
                run_terraform_command("plan")

            if selected_index_terraform == 2:
                console.print("Aplicando...", style="bold cyan")
                run_terraform_command("apply")
                console.print("[AVISO] Caso tenho criado um ou mais usuários, lembre-se de copiar a senha gerada para poder fazer login na AWS!", style="bold yellow")
                console.print("[AVISO] Ao fazer o login usando o nome do usuário e a sua senha, você será obrigado a escolher uma nova senha!\n", style="bold yellow")

            if selected_index_terraform == 3:
                console.print("Destruindo...", style="bold cyan")
                run_terraform_command("destroy")

        if selected_index == 4:
            # show actual region
            # get actual region from json file variables.json
            f = open('terraform/variables.json')
            data = json.load(f)
            f.close()
            region = data["region"]["name"]
            console.print(f"Região atual: [bold cyan]{region}[/bold cyan]", style="bold purple")
            regs = {
                "Leste dos EUA (Norte da Virgínia)": "us-east-1",
                "Leste dos EUA (Ohio)": "us-east-2",
                "Oeste dos EUA (Norte da Califórnia)": "us-west-1",
                "Oeste dos EUA (Oregon)": "us-west-2",
            }
            options = ["Leste dos EUA (Norte da Virgínia)", "Leste dos EUA (Ohio)", "Oeste dos EUA (Norte da California)", "Oeste dos EUA (Oregon)"]
            terminal_menu = TerminalMenu(options, title="Qual região deseja utilizar?")
            selected_index_region = terminal_menu.show()

            data["region"]["name"] = options[selected_index_region]
            data["region"]["code"] = regs[options[selected_index_region]]
            with open('terraform/variables.json', 'w') as f:
                json.dump(data, f, indent=4)
            console.print("Região atualizada com sucesso!", style="bold green")
            console.print(f"Nova região: [bold cyan]{options[selected_index_region]}[/bold cyan]", style="bold purple")
            console.print("\n")

        if selected_index == 5:
            reset_credentials()


if __name__ == '__main__':
    main()