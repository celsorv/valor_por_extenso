# ValorPorExtenso
## Classe em Python que produz o extenso de um valor monetário
_Python class to write a currency value in full form_


```python

extenso = ValorPorExtenso()

valores = (8_746_102_015.13, 5_000_000.99, 12_105.00, 1_000_000_000.00, 0.01, 0.28, 1_001_001.01)
estilo  = [None] * len(valores)

estilo[1] = ExtensoEstilo.UPPERCASE
estilo[3] = ExtensoEstilo.DEFAULT
estilo[5] = ExtensoEstilo.LOWERCASE
estilo[-1] = ExtensoEstilo.UPPERCASE

for idx, valor in enumerate(valores):
  extenso.setEstilo(estilo[idx])
  print(f'{valor:18,.2f} ->', extenso.get(valor))

"""
Output:

8,746,102,015.13 - Oito Bilhões, Setecentos e Quarenta e Seis Milhões, Cento e Dois Mil, Quinze Reais e Treze Centavos
    5,000,000.99 - CINCO MILHÕES DE REAIS E NOVENTA E NOVE CENTAVOS
       12,105.00 - Doze Mil, Cento e Cinco Reais
1,000,000,000.00 - Um Bilhão de Reais
            0.01 - Um Centavo
            0.28 - vinte e oito centavos
    1,001,001.01 - UM MILHÃO, UM MIL, UM REAL E UM CENTAVO
"""
```
