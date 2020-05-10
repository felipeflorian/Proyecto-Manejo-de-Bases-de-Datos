import xlsxwriter

libro = xlsxwriter.Workbook('Presupuesto1.xlsx')
hoja = libro.add_worksheet()

# El presupuesto que pintaremos en la hoja de cálculo
presupuesto = (
    ['Equipos',     4000],
    ['Cable',        100],
    ['Armario',      200],
    ['Switch',        99],
    ['AP',            50],
    ['Router',       150],
    ['Mano de Obra', 350],
)

# Nos posicionamos en la primera columna de la primera fila
row = 0
col = 0

# Iteramos los datos para ir pintando fila a fila
for concepto, precio in (presupuesto):
    hoja.write(row, col,     concepto)
    hoja.write(row, col + 1, precio)
    row += 1

#Pintamos la fila de totales
hoja.write(row, 0, 'Total:')
hoja.write(row, 1, '=SUM(B1:B7)')

#Cerramos el libro
libro.close()
