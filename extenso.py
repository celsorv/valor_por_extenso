"""
--------------------------------------
Class : ValorPorExtenso v1.0
Date  : September 23, 2022
Author: Celso Roberto Vitorino
--------------------------------------
"""

from enum import Enum

class ExtensoEstilo(Enum):
  DEFAULT = 1
  CAPITALIZE = 2
  UPPERCASE = 3
  LOWERCASE = 4

class ValorPorExtenso:

  NOMENCLATURA = (
    ('', 'Cem', 'Duzentos', 'Trezentos', 'Quatrocentos', 'Quinhentos', 'Seiscentos', 'Setecentos', 'Oitocentos', 'Novecentos'),
    ('', '', 'Vinte', 'Trinta', 'Quarenta', 'Cinquenta', 'Sessenta', 'Setenta', 'Oitenta', 'Noventa'),
    ('', 'Um', 'Dois', 'Três', 'Quatro', 'Cinco', 'Seis', 'Sete', 'Oito', 'Nove'),
  )

  DEZ_DEZENOVE =  ('Dez', 'Onze', 'Doze', 'Treze', 'Quatorze', 'Quinze', 'Dezesseis', 'Dezessete', 'Dezoito', 'Dezenove')
  
  CONECTOR = 'e'
  CONECTOR_MOEDA = 'de'
  CENTO = ('Cem', 'Cento')
  EXCLUDENTE_CONECTOR_MOEDA = 'Mil'

  CLASSE_S = ('Bilhão', 'Milhão', 'Mil', 'Real', 'Centavo')
  CLASSE_P = ('Bilhões', 'Milhões', 'Mil', 'Reais', 'Centavos')
  INDEX_MOEDA = 3


  def __init__(self, estilo = None):
      self.setEstilo(estilo)
    

  def setEstilo(self, estilo):
    if estilo == ExtensoEstilo.UPPERCASE:
      self.setUppercase(True)
    elif estilo == ExtensoEstilo.CAPITALIZE:
      self.setCapitalize(True)
    elif estilo == ExtensoEstilo.LOWERCASE:
      self.setLowercase(False)
    else:
      self.setCapitalize(True)


  def setCapitalize(self, capitalize):
    self.capitalize = capitalize
    self.uppercase = False


  def setUppercase(self, uppercase):
    self.uppercase = uppercase
    self.capitalize = False

  def setLowercase(self, lowercase):
    self.capitalize = False
    self.uppercase = False


  def get(self, valor):
    valor_str = ValorPorExtenso.__valor_str(valor)

    extenso = []

    for idx, grupo in enumerate(valor_str):
      is_grupo_moeda = (idx == ValorPorExtenso.INDEX_MOEDA)

      extenso_tmp = self.__extenso_grupo(grupo)

      if extenso_tmp:
        if int(grupo) > 1:
          extenso_tmp.append(ValorPorExtenso.CLASSE_P[idx])
        else:
          extenso_tmp.append(ValorPorExtenso.CLASSE_S[idx])

        if extenso:
          extenso.append([ValorPorExtenso.CONECTOR])
        extenso.append(extenso_tmp)

      elif is_grupo_moeda and extenso:
        if extenso[-1][-1] != ValorPorExtenso.EXCLUDENTE_CONECTOR_MOEDA:
          extenso_tmp.append(ValorPorExtenso.CONECTOR_MOEDA)

        extenso_tmp.append(ValorPorExtenso.CLASSE_P[idx])
        extenso.append(extenso_tmp)

    if self.uppercase:
      return ' '.join(map(str.upper, [e for v in extenso for e in v]))

    elif not self.capitalize:
      return ' '.join(map(str.lower, [e for v in extenso for e in v]))

    return ' '.join(map(str, [e for v in extenso for e in v]))
    
    
  def __extenso_grupo(self, numero_str):
    extenso = []

    for idx, algarismo in enumerate(numero_str):
      if algarismo == '0': continue

      numerico = int(algarismo)
      is_dez_a_dezenove = (idx == 1 and numerico == 1)

      if idx and extenso:
        if extenso[-1] == ValorPorExtenso.CENTO[0]:
          extenso[-1] = ValorPorExtenso.CENTO[1]
        extenso.append(ValorPorExtenso.CONECTOR)

      if is_dez_a_dezenove:
        n = int(numero_str[-1])
        extenso.append(ValorPorExtenso.DEZ_DEZENOVE[n])
        break

      extenso.append(ValorPorExtenso.NOMENCLATURA[idx][numerico])

    return extenso


  def __valor_str(valor):
    if not (valor and isinstance(valor, (int, float))):
      raise ValueError('Parâmetro inválido para extenso')
    elif valor > 990_999_999_999.99:
      raise ValueError('Valor excede o limite de 990.999.999.999,99')

    parte_inteira = int(valor)
    parte_decimal = f'{valor:018,.2f}'.split('.')[1]

    return f'{parte_inteira:015,d}'.split(',') + [f'0{parte_decimal}']



# --- utilizando a classe

extenso = ValorPorExtenso()

valores = (8_746_102_015.13, 5_000_000.99, 12_105.00, 1_000_000_000.00, 0.01, 0.28, 12_104_100.35)
estilo  = [None] * len(valores)

estilo[1] = ExtensoEstilo.UPPERCASE
estilo[3] = ExtensoEstilo.DEFAULT
estilo[5] = ExtensoEstilo.LOWERCASE
estilo[-1] = ExtensoEstilo.UPPERCASE

for idx, valor in enumerate(valores):
  extenso.setEstilo(estilo[idx])
  print(f'{valor:18,.2f} ->', extenso.get(valor))
