## Calculadora de Ahorro Financiero con GUI (CustomTkinter)

Esta aplicación permite comparar dos modelos de ahorro:

1. **Anualidad Discreta (Valor Futuro)**
2. **Modelo Continuo (EDO)**

Ofrece interfaz gráfica para introducir parámetros, calcular cada modelo y generar una comparativa de resultados con gráfica.

---

## Requisitos Previos

* **Python** 3.8 o superior
* **pip** (gestor de paquetes de Python)
* Un entorno virtual de Python (`venv`)

---

## Instalación

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/rolando2012/Calculadora-de-Ahorro-Financiero-con-GUI.git
   cd Calculadora-de-Ahorro-Financiero-con-GUI

   ```

2. **Crear y activar un entorno virtual**

   ```bash
   python3 -m venv env
   source env/bin/activate    # En macOS/Linux
   .\\env\\Scripts\\activate # En Windows
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

   > **requirements.txt**:
   >
   > ```text
   > customtkinter
   > numpy
   > matplotlib
   > otros
   > ```

---

## Uso

1. **Lanzar la aplicación**

   ```bash
   python interfaz.py
   ```

2. **Navegar por las pestañas**

   * **Anualidad Discreta (Valor Futuro)**: introduce el aporte mensual, tasa anual (%) y plazo (meses). Presiona **Calcular**.
   * **Modelo Continuo (EDO)**: define el capital inicial, tasa continua (%), paso Δt y presiona **Simular**.
   * **Comparativa**: una vez realizados ambos cálculos, haz clic en **Generar Comparativa** para ver la gráfica superpuesta y los resúmenes actualizados.

3. **Interpretar Resultados**

   * Los valores finales se mostrarán en la interfaz, junto con detalles de los parámetros utilizados.
   * La gráfica comparativa muestra la evolución temporal de ambos modelos.

---

## Estructura de Archivos

```
├──data
   ├──consumo_cochabamba.csv
├──src 
   |──interfaz.py        # Código principal de la GUI
├── requirements.txt   # Dependencias necesarias
└── README.md          # Documentación del proyecto
```

---

