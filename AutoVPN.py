from Meraki import Mx
from Audit import Audit


def main():
    log.write("Conectando na API Dashboard Meraki, Organization: , MX: ")
    mx64Bh = Mx('', '', '')

    log.write('Conectando na API Dashboard Meraki, Organization: , MX: ')
    mx64Arcos = Mx('', '', '')
    log.write("A Conexão foi um sucesso! Verificando status da VPN Site-To-Site")

    if mx64Bh.vpnStatus() == "unreachable":
        log.write("Problema na VPN identificado")
        log.write("Identificando o status do Dashboard do MX64 de T1...")

        if mx64Arcos.status():
            log.write("O MX64T1 está online, iniciando processo de reinicialização do MX64T2...")

            mx64Bh.rebootDevice()
            log.write("MX reiniciado com sucesso!")
        else:
            log.write("Mx64T1 está offline, nenhuma ação será realizada...\n")
    else:
        log.write("Nenhum problema na VPN Site-To-Site foi Identificado...\n")


if __name__ == "__main__":
    log = Audit("AutoVPN.log")

    try:
        log.write("Iniciando Script de Troubleshooting AutoVPN-Meraki...\n")
        main()
    except Exception as e:
        log.write(str(e) + "\n")

    log.write("Script Encerrado...")
    log.save()
