#!/usr/bin/python3
from os import system
from sys import argv
from subprocess import check_output

areas = ['coloque',
         'seus',
         'clusters'
         'aqui',
        ]


def main(opcao, area_namespace=''):
    if opcao == 'pods':
        system("kubectl get pods -owide")
    elif opcao == 'top':
        system("kubectl top pods")
    elif opcao == 'hpa':
        system("kubectl get hpa")
    elif opcao == 'default':
        system("kubectl config get-contexts | grep '^*' |"
               "tr -s ' ' | cut -d ' ' -f2,5")
    elif opcao == 'cluster':
        if area_namespace in areas:
            comando = f"kubectl config use-context {area_namespace}"
            system(comando)
        else:
            print("Cluster inexistente.")
            print_clusters()
    elif opcao == 'namespace':
        if not area_namespace:
            print("Informe o namespace")
        else:
            comando = "kubectl get namespaces | cut -d ' ' -f1"
            namespaces = check_output(comando,
                                      encoding='UTF-8',
                                      shell=True,
                                      executable='/bin/bash').splitlines()
            if area_namespace in namespaces:
                for cluster in areas:
                    comando = f"kubectl config set-context {cluster} \
                              --namespace={area_namespace}"
                    system(comando)
            else:
                print(f"{area_namespace} não encontrada!")
    else:
        print(f"\nOpção inválida: {opcao}\n")
        help()


def print_clusters():
    print("Clusteres disponíveis")
    for cluster in areas:
        print(f"\t- {cluster}")


def help():
    mensagem = ("Parâmentros obrigatórios/disponíveis:\n"
                "\t- pods: Exibe as pods do namespace.\n"
                "\t- top: Exibe o uso de memória e CPU das pods.\n"
                "\t- hpa: Exibe o status do hpa.\n"
                "\t- default: Exibe o cluster e namespace padrão.\n"
                "\t- cluster: Altera o cluster padrão.\n"
                "\t- namespace: Altera o namespace padrão de todos"
                " os clusters.\n")
    print(mensagem)


if __name__ == '__main__':
    if len(argv) == 2:
            main(argv[1])
    elif len(argv) == 3:
            main(argv[1], argv[2])
    else:
        print("Algo deu errado.")
        help()
        print_clusters()
