# ValorPorExtenso
## Classe em Python que produz o extenso de um valor monetário
_Python class to write a currency value in full form_

This is a Python script that defines a ValorPorExtenso class that can convert a monetary value (in float or Decimal format) to its corresponding text representation in Brazilian Portuguese.

The class has a setValor method that takes a monetary value as input, and a get method that returns the text representation of the input value. The script defines several private helper methods used to perform the conversion, such as __valor_agrupado, __extenso_classe, etc.

The __valor_agrupado method takes the input value and breaks it down into its integer and decimal parts, and stores them in separate class variables. The integer part is further broken down into groups of three digits, which are stored in a list, with the least significant group at index 0. This list is then used by other methods to generate the text representation of the input value.

The __extenso_classe method takes a three-digit string (representing a group of digits in the input value), and an index indicating the position of the group within the input value. It then converts the three-digit string to its corresponding text representation (using the _NUMEROS class property), and appends the appropriate class name (such as "mil" or "milhões") to the end of the text representation, depending on the position of the group.

The script uses several class properties (such as _NUMEROS, _CONECTOR, _CLASSES, etc.) to store strings used in the conversion process, such as the names of numbers and classes, and connectors between them.

```python

from decimal import Decimal
from valor_extenso import ValorPorExtenso

valores = (8_746_102_001.13, 5_000_000.99, 12_105.00, 1_000_000_000.00, 0.01, 0.28, 12_104_100.35)
extenso = ValorPorExtenso()

for valor in valores:
	extenso.setValor(valor)
	print()
	print(f'{valor:17,.2f}: {extenso.get()}')

print()

"""
Output:

 8,746,102,001.13: Oito Bilhões, Setecentos e Quarenta e Seis Milhões, Cento e Dois Mil e Um Reais e Treze Centavos

     5,000,000.99: Cinco Milhões de Reais e Noventa e Nove Centavos

        12,105.00: Doze Mil e Cento e Cinco Reais

 1,000,000,000.00: Um Bilhão de Reais

             0.01: Um Centavo

             0.28: Vinte e Oito Centavos

    12,104,100.35: Doze Milhões, Cento e Quatro Mil e Cem Reais e Trinta e Cinco Centavos

"""
```
