"""
--------------------------------------
Class : ValorPorExtenso v1.0
Date  : October 01, 2022
Author: Celso Roberto Vitorino
--------------------------------------
"""

from decimal import Decimal

class ValorPorExtenso:

    def get(self):
        extenso = ''
        usou_conector = False

        for indice, grupo in enumerate(self.valor_ctl[1:], 1):
            if grupo == '000': continue

            posicao = ValorPorExtenso._PLURAL if int(grupo) > 1 else ValorPorExtenso._SINGULAR
            extenso_tmp = self.__extenso_grupo(grupo, indice)
            if extenso:
                if not usou_conector:
                    extenso_tmp += f' {ValorPorExtenso._CONECTOR} '
                    usou_conector = True
                else:
                    extenso_tmp += ', '

            extenso = extenso_tmp + extenso

        if self.valor_ctl[1] == '000' and self.inteiros: # moeda
            posicao = ValorPorExtenso._PLURAL

            if self.valor_ctl[2] == '000':
                moeda = f' {ValorPorExtenso._CONECTOR_MOEDA} {ValorPorExtenso._CLASSES[1][posicao]}'
            else:
                moeda = f' {ValorPorExtenso._CLASSES[1][posicao]}'
            extenso += moeda

        if self.valor_ctl[0] != '000': # centavos
            if extenso:
                extenso += f' {ValorPorExtenso._CONECTOR} '
            extenso += self.__extenso_grupo(self.valor_ctl[0], 0)

        return extenso


    def __extenso_grupo(self, valor, indice_grupo):
        if valor == '000': return ''

        if valor == '100':
            extenso = ValorPorExtenso._CEM
            extenso += f' {ValorPorExtenso._CLASSES[indice_grupo][ValorPorExtenso._PLURAL]}'
            return extenso

        grupo_plural = int(valor) > 1 or (indice_grupo == 1 and self.pluralizar)
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
            posicao = ValorPorExtenso._PLURAL if grupo_plural else ValorPorExtenso._SINGULAR
            extenso += f' {ValorPorExtenso._CLASSES[indice_grupo][posicao]}'

        return extenso


    def setValor(self, valor):
        self.__valor_agrupado(valor)


    def __init__(self):
        self.pluralizar = None
        self.decimais = None
        self.inteiros = None
        self.valor = None
        self.valor_ctl = None


    def __valor_agrupado(self, valor):
        if not (valor and isinstance(valor, (int, float, Decimal))):
            raise ValueError('Parâmetro inválido para extenso')
        elif valor > 990_999_999_999_999_999_999_999:
            raise ValueError('Valor excede o limite de 990.999.999.999.999.999.999')

        self.valor = valor
        self.inteiros = int(valor)
        self.decimais = f'{valor:031,.2f}'.split('.')[1]
        self.valor_ctl = list(reversed(f'{self.inteiros:031,d}'.split(',') + [f'0{self.decimais}']))
        self.pluralizar = self.inteiros > 1


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
    )

    _CEM = 'Cem'

    _CONECTOR = 'e'
    _CONECTOR_MOEDA = 'de'
