"""
Gera o extenso para um número

## Author: Celso R Vitorino
## Date  : October 01, 2022
"""
from decimal import Decimal

class PorExtenso:

    def get(self) -> str:
        """
        Método que retorna o valor por extenso
        Args:
            não há
        Return:
            extenso: extenso do valor 
        """
        extenso = ''
        usou_conector = False

        for indice, grupo in enumerate(self.__valor_ctl[1:], 1):
            if grupo == '000': continue

            extenso_tmp = self.__extenso_classe(grupo, indice)
            if extenso:
                if not usou_conector:
                    extenso_tmp += f' {PorExtenso._CONECTOR} '
                    usou_conector = True
                else:
                    extenso_tmp += ', '

            extenso = extenso_tmp + extenso

        if self.__valor_ctl[1] == '000' and self.__inteiros: # moeda
            posicao = PorExtenso._PLURAL

            if self.__valor_ctl[2] == '000':
                moeda = f' {PorExtenso._CONECTOR_MOEDA} {PorExtenso._CLASSES[1][posicao]}'
            else:
                moeda = f' {PorExtenso._CLASSES[1][posicao]}'
            extenso += moeda

        if self.__valor_ctl[0] != '000': # centavos
            if extenso:
                extenso += f' {PorExtenso._CONECTOR} '
            extenso += self.__extenso_classe(self.__valor_ctl[0], 0)

        return extenso


    def setValor(self, valor: float | Decimal) -> None:
        """
        Define o valor cujo extenso é desejado
        Args:
            valor: valor como float ou Decimal
        Return:
            não há
        """
        self.__valor_agrupado(valor)


    def setMoeda(self, moeda: tuple[str, str], centavo: tuple[str, str]) -> None:
        """
        Define a moeda para o extenso
        Args:
            moeda: tupla com o nome singular e plural
            centavo: tupla com o nome singular e plural
        Return:
            não há
        """
        self.__moeda = [
            centavo if centavo is not None else ['', ''], 
            moeda if moeda is not None else ['', '']
        ]


# ---------------
# Private Methods
# ---------------

    def __extenso_classe(self, valor: str, indice_classe: int) -> str:
        classe_plural = int(valor) > 1 or (indice_classe == 1 and self.__pluralizar)

        match valor:
            case '000':
                extenso = ''
            case '100':
                extenso = PorExtenso._CEM
            case _:
                extenso = ''

                for indice in range(len(valor)):
                    digito = valor[indice]
                    if digito == '0': continue

                    if extenso: extenso += f' {PorExtenso._CONECTOR} '

                    if indice == 1 and digito == '1': # dezena de 10 a 19
                        posicao = int(valor[indice:]) - 10
                        extenso += PorExtenso._NUMEROS[3][posicao]
                        break

                    posicao = int(digito)
                    extenso += PorExtenso._NUMEROS[indice][posicao]

        if extenso:
            posicao = PorExtenso._PLURAL if classe_plural else PorExtenso._SINGULAR
            if indice_classe >= 2:
                extenso += f' {PorExtenso._CLASSES[indice_classe][posicao]}'
            else:
                if self.__moeda[indice_classe][posicao]:
                    extenso += f' {self.__moeda[indice_classe][posicao]}'

        return extenso


    def __init__(self) -> None:
        self.__pluralizar = None
        self.__decimais = None
        self.__inteiros = None
        self.__valor_ctl = None
        self.__moeda = [PorExtenso._CLASSES[1], PorExtenso._CLASSES[0]]


    def __valor_agrupado(self, valor: (float, Decimal)) -> None:
        if not (valor and isinstance(valor, (int, float, Decimal))):
            raise ValueError('Parâmetro inválido para extenso')

        self.__inteiros = int(valor)
        self.__decimais = f'{valor:031,.2f}'.split('.')[1]
        self.__valor_ctl = list(reversed(f'{self.__inteiros:031,d}'.split(',') + [f'0{self.__decimais}']))
        self.__pluralizar = self.__inteiros > 1


# ----------------
# Class properties
# ----------------

    _SINGULAR = 0
    _PLURAL = 1

    _NUMEROS = (
        ('', 'Cento', 'Duzentos', 'Trezentos', 'Quatrocentos', 'Quinhentos', 'Seiscentos', 'Setecentos', 'Oitocentos', 'Novecentos'),
        ('', '', 'Vinte', 'Trinta', 'Quarenta', 'Cinquenta', 'Sessenta', 'Setenta', 'Oitenta', 'Noventa'),
        ('', 'Um', 'Dois', 'Três', 'Quatro', 'Cinco', 'Seis', 'Sete', 'Oito', 'Nove'),
        ('Dez', 'Onze', 'Doze', 'Treze', 'Quatorze', 'Quinze', 'Dezesseis', 'Dezessete', 'Dezoito', 'Dezenove')
    )

    _CLASSES = (
        ('Real', 'Reais', False),
        ('Centavo', 'Centavos', False),
        ('Mil', 'Mil', False),
        ('Milhão', 'Milhões', True),
        ('Bilhão', 'Bilhões', True),
        ('Trilhão', 'Trilhões', True),
        ('Quatrilhão', 'Quatrilhões', True),
        ('Quintilhão', 'Quintilhões', True),
        ('Sextilhão', 'Sextilhões', True),
        ('Septilhão', 'Septilhões', True),
        ('Octilhão', 'Octilhões', True),
        ('Nonilhão', 'Nonilhões', True),
        ('Decilhão', 'Decilhões', True),
        ('Undecilhão', 'Undecilhões', True),
        ('Duodecilhão', 'Duodecilhões', True),
    )

    _CEM = 'Cem'

    _CONECTOR = 'e'
    _CONECTOR_MOEDA = 'de'


if __name__ == '__main__':

    vp = PorExtenso()

    valor = Decimal('983_121_613_112_832_531_086_112_215_155_136_123_456_789.12')
    valor_formatado = f'\nR$ {valor:,.2f}\n'.replace(',', 'X').replace('.', ',').replace('X', '.')
    vp.setValor(valor)
    extenso = vp.get()
    print(valor_formatado)
    print(extenso, "\n")

    # R$ 983.121.613.112.832.531.086.112.215.155.136.123.456.789,12
    #
    # Novecentos e Oitenta e Três Duodecilhões, Cento e Vinte e Um Undecilhões, 
    # Seiscentos e Treze Decilhões, Cento e Doze Nonilhões, Oitocentos e Trinta e 
    # Dois Octilhões, Quinhentos e Trinta e Um Septilhões, Oitenta e Seis Sextilhões, 
    # Cento e Doze Quintilhões, Duzentos e Quinze Quatrilhões, Cento e Cinquenta e 
    # Cinco Trilhões, Cento e Trinta e Seis Bilhões, Cento e Vinte e Três Milhões, 
    # Quatrocentos e Cinquenta e Seis Mil e Setecentos e Oitenta e Nove Reais e 
    # Doze Centavos 

    valor = 125.83
    valor_formatado = f'\nUS$ {valor:.2f}\n'
    vp.setValor(valor)
    vp.setMoeda(['Dólar', 'Dólares'], ['Cent', 'Cents'])
    extenso = vp.get()
    print(valor_formatado)
    print(extenso, "\n")

    # US$ 125.83
    # Cento e Vinte e Cinco Dólares e Oitenta e Três Cents 

    # ------------------------------------
    # Puzzle Bitcoin key 66
    # ------------------------------------
    min_private_key = 0x20000000000000000
    max_private_key = 0x3ffffffffffffffff

    # 36.893.488.147.419.103.232
    # ---
    # Trinta e Seis Quintilhões, Oitocentos e Noventa e Três Quatrilhões, 
    # Quatrocentos e Oitenta e Oito Trilhões, Cento e Quarenta e Sete Bilhões, 
    # Quatrocentos e Dezenove Milhões, Cento e Três Mil e Duzentos e Trinta e Dois 

    # ------------------------------------
    # Puzzle Bitcoin key 130
    # ------------------------------------
    min_private_key = 0x200000000000000000000000000000000
    max_private_key = 0x3ffffffffffffffffffffffffffffffff

    # 680.564.733.841.876.926.926.749.214.863.536.422.912
    # ---
    # Seiscentos e Oitenta Undecilhões, Quinhentos e Sessenta e Quatro Decilhões, 
    # Setecentos e Trinta e Três Nonilhões, Oitocentos e Quarenta e Um Octilhões, 
    # Oitocentos e Setenta e Seis Septilhões, Novecentos e Vinte e Seis Sextilhões, 
    # Novecentos e Vinte e Seis Quintilhões, Setecentos e Quarenta e Nove Quatrilhões, 
    # Duzentos e Quatorze Trilhões, Oitocentos e Sessenta e Três Bilhões, Quinhentos e 
    # Trinta e Seis Milhões, Quatrocentos e Vinte e Dois Mil e Novecentos e Doze 

    valor = max_private_key - min_private_key + 1
    valor_formatado = f'\n{valor:,.0f}\n'.replace(',', 'X').replace('.', ',').replace('X', '.')
    vp.setValor(valor)
    vp.setMoeda(None, None)
    extenso = vp.get()
    print(valor_formatado)
    print(extenso, "\n")
