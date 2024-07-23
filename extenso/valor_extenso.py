"""
Gera o extenso para um valor monetário

## Author: Celso R Vitorino
## Date  : October 01, 2022
"""
from decimal import Decimal

class ValorPorExtenso:

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

            posicao = ValorPorExtenso._PLURAL if int(grupo) > 1 else ValorPorExtenso._SINGULAR
            extenso_tmp = self.__extenso_classe(grupo, indice)
            if extenso:
                if not usou_conector:
                    extenso_tmp += f' {ValorPorExtenso._CONECTOR} '
                    usou_conector = True
                else:
                    extenso_tmp += ', '

            extenso = extenso_tmp + extenso

        if self.__valor_ctl[1] == '000' and self.__inteiros: # moeda
            posicao = ValorPorExtenso._PLURAL

            if self.__valor_ctl[2] == '000':
                moeda = f' {ValorPorExtenso._CONECTOR_MOEDA} {ValorPorExtenso._CLASSES[1][posicao]}'
            else:
                moeda = f' {ValorPorExtenso._CLASSES[1][posicao]}'
            extenso += moeda

        if self.__valor_ctl[0] != '000': # centavos
            if extenso:
                extenso += f' {ValorPorExtenso._CONECTOR} '
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


# ---------------
# Private Methods
# ---------------

    def __extenso_classe(self, valor: str, indice_classe: int) -> str:
        classe_plural = int(valor) > 1 or (indice_classe == 1 and self.__pluralizar)

        match valor:
            case '000':
                extenso = ''
            case '100':
                extenso = ValorPorExtenso._CEM
            case _:
                extenso = ''

                for indice in range(len(valor)):
                    digito = valor[indice]
                    if digito == '0': continue

                    if extenso: extenso += f' {ValorPorExtenso._CONECTOR} '

                    if indice == 1 and digito == '1': # dezena de 10 a 19
                        posicao = int(valor[indice:]) - 10
                        extenso += ValorPorExtenso._NUMEROS[3][posicao]
                        break

                    posicao = int(digito)
                    extenso += ValorPorExtenso._NUMEROS[indice][posicao]

        if extenso:
            posicao = ValorPorExtenso._PLURAL if classe_plural else ValorPorExtenso._SINGULAR
            extenso += f' {ValorPorExtenso._CLASSES[indice_classe][posicao]}'

        return extenso


    def __init__(self) -> None:
        self.__pluralizar = None
        self.__decimais = None
        self.__inteiros = None
        self.__valor = None
        self.__valor_ctl = None


    def __valor_agrupado(self, valor: (float, Decimal)) -> None:
        if not (valor and isinstance(valor, (int, float, Decimal))):
            raise ValueError('Parâmetro inválido para extenso')
        # elif valor > 990_999_999_999_999_999_999_999:
        #     raise ValueError('Valor excede o limite de 990.999.999.999.999.999.999')

        self.__valor = valor
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
        ('Centavo', 'Centavos', False),
        ('Real', 'Reais', False),
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

# ----------------
# Exemplo de uso
# ----------------

if __name__ == "__main__":

    valor = Decimal('983_121_613_112_832_531_086_112_215_155_136_123_456_789.12')
   
    vp = ValorPorExtenso()
    vp.setValor(valor)

    extenso = vp.get()
    valor_formatado = f'\nR$ {valor:,.2f}\n'.replace(',', 'X').replace('.', ',').replace('X', '.')
    
    print(valor_formatado)
    print(extenso, "\n")

    # R$ 983.121.613.112.832.531.086.112.215.155.136.123.456.789,12
    #
    # Novecentos e Oitenta e Três Duodecilhões, Cento e Vinte e Um Undecilhões, Seiscentos e 
    # Treze Decilhões, Cento e Doze Nonilhões, Oitocentos e Trinta e Dois Octilhões, Quinhentos e 
    # Trinta e Um Septilhões, Oitenta e Seis Sextilhões, Cento e Doze Quintilhões, Duzentos e 
    # Quinze Quatrilhões, Cento e Cinquenta e Cinco Trilhões, Cento e Trinta e Seis Bilhões, 
    # Cento e Vinte e Três Milhões, Quatrocentos e Cinquenta e Seis Mil e Setecentos e Oitenta e
    # Nove Reais e Doze Centavos
    #

