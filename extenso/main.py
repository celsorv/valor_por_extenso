from decimal import Decimal
from valor_extenso import ValorPorExtenso

valores = (8_746_102_001.13, 5_000_000.99, 12_105.00, 1_000_000_000.00, 0.01, 0.28, 12_104_100.35)
extenso = ValorPorExtenso()

for valor in valores:
	extenso.setValor(valor)
	print()
	print(f'{valor:17,.2f}: {extenso.get()}')

print()