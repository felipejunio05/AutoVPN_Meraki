from datetime import datetime
from os import path

__all__ = ["Audit"]


class Audit:

    def __init__(self, file: str) -> None:

        """
            Cria um objeto que permite salvar observações em um arquivo de texto.

            :param file: Determina o nome do arquivo.
            :type file: str
        """

        self.__validation(file=file)

        self.__logFile: str = file
        self.__content: str = ""

        if path.exists(file) and path.isfile(file):
            with open(self.__logFile, "r") as file:
                for line in file.readlines():
                    self.__content += line

            self.__content += "\n"

    def write(self, txt: str) -> bool:

        """
            Este método escreve uma linha no arquivo

            :param txt: O valor passado para este parâmetro será escrito no arquivo.
            :type txt: str
        """

        self.__validation(txt=txt)

        try:
            self.__content += f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}: {txt}\n'

            opOk = True
        except Exception as Error:
            print(Error)
            opOk = False

        return opOk

    def save(self) -> None:

        """
            Salva as alterações no Arquivo.
        """

        with open(self.__logFile, "w") as file:
            file.writelines(self.__content)

    @staticmethod
    def __validation(**kwargs: any) -> None:

        """
            Valida parâmetros do construtor da classe.

            :param kwargs: Deve ser informando os parâmetros do construtor da classe.
            :type kwargs: any
        """

        if not isinstance(*kwargs.values(), str):
            raise ValueError("O parâmetro '{}' é do tipo string, e o valor "
                             "informado é do tipo {}".format(*kwargs.keys(), str(type(*kwargs.values()))[8:-2]))
