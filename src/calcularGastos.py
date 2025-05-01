import pandas as pd

def generar_csv_consumo(path_csv: str = 'data/consumo_cochabamba.csv'):
    data = {
        'Categoría': [
            'Alimentación', 'Transporte', 'Vivienda', 'Vestimenta',
            'Entretenimiento', 'Salud', 'Educación','Comunicacion', 
            'deuda', 'Otros'
        ],
        'Gasto Mín (Bs.)': [550, 150, 750, 100, 100, 100, 50, 50, 0, 50],
        'Gasto Máx (Bs.)': [900, 300, 1250, 200, 300, 400, 200, 100, 0, 150]
    }
    df = pd.DataFrame(data)
    # Añadir fila de ingreso fijo
    ingreso = 2061
    df.loc[len(df)] = ['Ingreso', ingreso, ingreso]
    df.to_csv(path_csv, index=False)
    print(f"CSV guardado en: {path_csv}")

def calcular_gastos_y_ahorro(path_csv: str = 'data/consumo_cochabamba.csv'):
    df = pd.read_csv(path_csv)
    # Mostrar la tabla
    print("\nPlanilla de Consumo Mensual:")
    print(df.to_string(index=False))
    # Cálculo de totales
    gastos = df[df['Categoría'] != 'Ingreso']
    gasto_min = gastos['Gasto Mín (Bs.)'].sum()
    gasto_max = gastos['Gasto Máx (Bs.)'].sum()
    ingreso = df.loc[df['Categoría'] == 'Ingreso', 'Gasto Mín (Bs.)'].iloc[0]
    # Ahorros
    ahorro_escenario_min_gasto = ingreso - gasto_max   # escenario gasto máximo
    ahorro_escenario_max_gasto = ingreso - gasto_min   # escenario gasto mínimo

    print(f"\nTotal gasto mínimo: Bs. {gasto_min}")
    print(f"Total gasto máximo: Bs. {gasto_max}")
    print(f"Ahorro en escenario de gasto MÁXIMO: Bs. {ahorro_escenario_min_gasto}")
    print(f"Ahorro en escenario de gasto MÍNIMO: Bs. {ahorro_escenario_max_gasto}")

if __name__ == "__main__":
    generar_csv_consumo()
    calcular_gastos_y_ahorro()
