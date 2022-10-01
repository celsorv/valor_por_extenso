# ValorPorExtenso
## Classe em Python que produz o extenso de um valor monetário
_Python class to write a currency value in full form_


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
