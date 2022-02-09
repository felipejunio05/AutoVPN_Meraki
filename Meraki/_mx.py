import json
import requests

__all__ = ['Mx']


class Mx:
    def __init__(self, apiKey: str, organizationId: str, serial: str) -> None:

        """
            Cria um objeto que permite consultar ou executar ações em um MX por meio de API.

            :param apiKey: Chave de API Dashboard Meraki.
            :type apiKey: str
            :param organizationId: Número de identificação da organização.
            :type organizationId: str
            :param serial: Número de serial do equipamento MX.
            :type serial: str
        """

        self.__validation(apiKey, organizationId, serial)

        self.__baseUrl: str = "https://dashboard.meraki.com/api/v1/"
        self.__headers: dict = {'X-Cisco-Meraki-API-Key': apiKey, 'Content-Type': 'application/json'}

        self.__devicesStatus: str = "organizations/{}/devices/statuses".format(organizationId)
        self.__vpnStatusApi: str = 'organizations/{}/appliance/vpn/statuses'.format(organizationId)
        self.__rebootApi: str = 'devices/{}/reboot'.format(serial)

        request = requests.get(self.__baseUrl + self.__devicesStatus, headers=self.__headers, )

        if request.status_code == 200:
            organizationDevices = request.json()
            self.__deviceInfo: dict = [reg for reg in organizationDevices if reg['serial'] == serial][0]
        else:
            raise ValueError("Houve um erro em realizar o request, "
                             "código do erro: {}".format(request.status_code))

    def vpnStatus(self) -> str:

        """
            Método retorna o status da AutoVPN L2L.
        """

        vpnStatus: str = 'Unknown'
        request = requests.get(self.__baseUrl + self.__vpnStatusApi, headers=self.__headers, )

        if request.status_code == 200:
            response = request.json()
        else:
            raise ValueError("Houve um erro em realizar o request, código do erro: {}".format(request.status_code))

        for reg in response:
            if reg['deviceSerial'] == self.__deviceInfo['serial']:
                vpnStatus = reg['merakiVpnPeers'][0]['reachability']

                break

        return vpnStatus

    def rebootDevice(self) -> bool:

        """
            Reinicia o MX.
        """

        request = requests.post(self.__baseUrl + self.__rebootApi, headers=self.__headers, )

        if request.status_code == 202:
            response = request.json()
        else:
            raise ValueError("Houve um erro em realizar o request, código do erro: {}".format(request.status_code))

        return response["success"]

    def status(self) -> str:

        """
            Retorna o Status do MX.
        """

        return self.__deviceInfo['status'] == "online"

    @staticmethod
    def __validation(*args: any) -> None:
        """
            Valida parâmetros do construtor da classe.

            :param args: Deve ser informando os parâmetros do construtor da classe.
            :type args: any
        """

        params = ["apiKey", "organizationId", "serial"]

        for i in range(len(params)):
            if not isinstance(args[i], str):
                raise ValueError("O parâmetro '{}' é do tipo string, e o valor "
                                 "informado é do tipo {}".format(params[i], str(type(args[i]))[8:-2]))
