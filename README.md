# ValorPorExtenso
## Classe em Python que produz o extenso de um valor monetário
_Python class to write a currency value in full form_

This is a Python script that defines a PorExtenso class that can convert a monetary value (in float or Decimal format) to its corresponding text representation in Brazilian Portuguese.

The class has a setValor method that takes a monetary value as input, and a get method that returns the text representation of the input value. The script defines several private helper methods used to perform the conversion, such as __valor_agrupado, __extenso_classe, etc.

The __valor_agrupado method takes the input value and breaks it down into its integer and decimal parts, and stores them in separate class variables. The integer part is further broken down into groups of three digits, which are stored in a list, with the least significant group at index 0. This list is then used by other methods to generate the text representation of the input value.

The __extenso_classe method takes a three-digit string (representing a group of digits in the input value), and an index indicating the position of the group within the input value. It then converts the three-digit string to its corresponding text representation (using the _NUMEROS class property), and appends the appropriate class name (such as "mil" or "milhões") to the end of the text representation, depending on the position of the group.

The script uses several class properties (such as _NUMEROS, _CONECTOR, _CLASSES, etc.) to store strings used in the conversion process, such as the names of numbers and classes, and connectors between them.

```python

from decimal import Decimal
from valor_extenso import PorExtenso

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

```

### Updates
#### 2024, August
- New method allows you to configure the currency name
