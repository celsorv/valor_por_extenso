"""

Class : ValorPorExtenso v1.0
Date  : September 23, 2022
Author: Celso Roberto Vitorino

"""

class ValorPorExtenso:

  NOMENCLATURA = (
    ('', 'cem', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 
     'seiscentos', 'setecentos', 'oitocentos', 'novecentos'),
    ('', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa'),
    ('', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove'),
  )

  DEZ_DEZENOVE =  ('dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze', 'dezesseis', 'dezessete', 
     'dezoito', 'dezenove')

  
  CONECTOR = 'e'
  CONECTOR_MOEDA = 'de'
  CENTO = ('cem', 'cento')
  EXCLUDENTE_CONECTOR_MOEDA = 'mil'

  AGRUPA_S = ('bilhão', 'milhão', 'mil', 'real', 'centavo')
  AGRUPA_P = ('bilhões', 'milhões', 'mil', 'reais', 'centavos')
  INDEX_MOEDA = 3


  def __init__(self, valor = None):
    if valor:
      self.setValor(valor)
    else:
      self.valor = None
      self.valor_otm = None


  def __separa_valor(self):
    
    parte_inteira = int(self.valor)
    parte_decimal = f'{self.valor:018,.2f}'.split('.')[1]

    self.valor_otm = f'{parte_inteira:015,d}'.split(',') + [f'0{parte_decimal}']


  def setValor(self, valor):

    if valor > 990_999_999_999.99:
      raise ValueError('Valor limitado a 990.999.999.999,99')

    self.valor = valor
    self.__separa_valor()

    
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



  def get(self):

    extenso = []

    for idx, grupo in enumerate(self.valor_otm):
      is_grupo_moeda = (idx == ValorPorExtenso.INDEX_MOEDA)

      extenso_tmp = self.__extenso_grupo(grupo)


      if extenso_tmp:

        if int(grupo) > 1:
          extenso_tmp.append(ValorPorExtenso.AGRUPA_P[idx])
        else:
          extenso_tmp.append(ValorPorExtenso.AGRUPA_S[idx])

        if extenso:
          extenso.append([ValorPorExtenso.CONECTOR])

        extenso.append(extenso_tmp)

      elif is_grupo_moeda and extenso:
        if extenso[-1][-1] != ValorPorExtenso.EXCLUDENTE_CONECTOR_MOEDA:
          extenso_tmp.append(ValorPorExtenso.CONECTOR_MOEDA)
        extenso_tmp.append(ValorPorExtenso.AGRUPA_P[idx])
        extenso.append(extenso_tmp)

    extenso = ' '.join(map(str, [e for v in extenso for e in v]))

    return extenso


  def __str__(self):
    return self.get()


# --- main

valor = 8_743_102_015.13

extenso = ValorPorExtenso()
extenso.setValor(valor)
print(extenso)
