import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Set appearance mode and default color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FinancialSimulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Simulador Financiero")
        self.geometry("1200x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # App title
        self.app_title = ctk.CTkLabel(self.sidebar_frame, text="Simulador Financiero", 
                                      font=ctk.CTkFont(size=20, weight="bold"))
        self.app_title.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Sidebar buttons
        self.vf_button = ctk.CTkButton(self.sidebar_frame, text="Valor Futuro", 
                                       command=self.show_vf_frame)
        self.vf_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.edo_button = ctk.CTkButton(self.sidebar_frame, text="Modelo EDO", 
                                        command=self.show_edo_frame)
        self.edo_button.grid(row=2, column=0, padx=20, pady=10)
        
        self.expenses_button = ctk.CTkButton(self.sidebar_frame, text="Gestionar Gastos", 
                                           command=self.show_expenses_frame)
        self.expenses_button.grid(row=3, column=0, padx=20, pady=10)
        
        self.results_button = ctk.CTkButton(self.sidebar_frame, text="Resultados", 
                                          command=self.show_results_frame)
        self.results_button.grid(row=4, column=0, padx=20, pady=10)
        
        # Appearance mode
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Apariencia:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                       command=self.change_appearance_mode)
        self.appearance_mode_option.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_option.set("Dark")
        
        # UI Scaling
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="Escala UI:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                               command=self.change_scaling)
        self.scaling_option.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.scaling_option.set("100%")
        
        # Initialize frames
        self.vf_frame = None
        self.edo_frame = None
        self.expenses_frame = None
        self.results_frame = None
        
        # Initialize data storage
        self.income = 0
        self.expenses_data = {
            'Categoría': [
                'Ingreso', 'Alimentación', 'Transporte', 'Vivienda', 'Vestimenta',
                'Entretenimiento', 'Salud', 'Educación', 'Comunicación', 
                'Deuda', 'Otros'
            ],
            'Gasto Mín (Bs.)': [0, 550, 150, 750, 100, 100, 100, 50, 50, 0, 50],
            'Gasto Máx (Bs.)': [0, 900, 300, 1250, 200, 300, 400, 200, 100, 0, 150]
        }
        self.df_expenses = pd.DataFrame(self.expenses_data)
        
        # VF parameters
        self.vf_params = {
            'P': 161,          # Aporte mensual (Bs.)
            'r_annual': 0.03,  # Tasa anual (3%)
            'n_months': 120    # Número de meses (10 años)
        }
        
        # EDO parameters
        self.edo_params = {
            'I0': 2061,   # Ingreso inicial
            'g': 0.05,    # Tasa de crecimiento de ingreso (anual)
            'c0': 50,     # Consumo autónomo
            'c1': 0.9,    # Propensión marginal al consumo
            'c2': 0.1,    # Efecto ahorro en consumo
            'r': 0.03,    # Tasa de rendimiento (anual)
            'A0': 161,    # Ahorro inicial
            'T': 10       # Tiempo total (años)
        }
        
        # Show VF frame by default
        self.show_vf_frame()

    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling(self, new_scaling):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_vf_frame(self):
        self.clear_main_frame()
        
        # Create scrollable frame
        self.vf_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.vf_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(self.vf_frame, text="Cálculo de Valor Futuro (VF)", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Input parameters frame
        params_frame = ctk.CTkFrame(self.vf_frame)
        params_frame.pack(fill="x", padx=10, pady=10)
        
        # Income input
        income_frame = ctk.CTkFrame(params_frame)
        income_frame.pack(fill="x", padx=10, pady=10)
        
        income_label = ctk.CTkLabel(income_frame, text="Ingreso mensual (Bs.):", width=200)
        income_label.pack(side="left", padx=(10, 10))
        
        self.income_entry = ctk.CTkEntry(income_frame, width=150)
        self.income_entry.pack(side="left", padx=(0, 10))
        self.income_entry.insert(0, str(self.vf_params['P']))
        
        # Parameters frame with grid layout
        grid_frame = ctk.CTkFrame(params_frame)
        grid_frame.pack(fill="x", padx=10, pady=10)
        
        # Monthly contribution
        ctk.CTkLabel(grid_frame, text="Aporte mensual (Bs.):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.monthly_contrib_entry = ctk.CTkEntry(grid_frame, width=150)
        self.monthly_contrib_entry.grid(row=0, column=1, padx=10, pady=10)
        self.monthly_contrib_entry.insert(0, str(self.vf_params['P']))
        
        # Annual interest rate
        ctk.CTkLabel(grid_frame, text="Tasa anual (%):").grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.annual_rate_entry = ctk.CTkEntry(grid_frame, width=150)
        self.annual_rate_entry.grid(row=0, column=3, padx=10, pady=10)
        self.annual_rate_entry.insert(0, str(self.vf_params['r_annual']*100))
        
        # Investment period
        ctk.CTkLabel(grid_frame, text="Plazo (meses):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.months_entry = ctk.CTkEntry(grid_frame, width=150)
        self.months_entry.grid(row=1, column=1, padx=10, pady=10)
        self.months_entry.insert(0, str(self.vf_params['n_months']))
        
        # Years equivalent
        ctk.CTkLabel(grid_frame, text="Equivalente en años:").grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.years_label = ctk.CTkLabel(grid_frame, text=f"{self.vf_params['n_months']/12:.1f}")
        self.years_label.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        
        # Update years when months change
        def update_years(event):
            try:
                months = int(self.months_entry.get())
                self.years_label.configure(text=f"{months/12:.1f}")
            except ValueError:
                self.years_label.configure(text="Error")
        
        self.months_entry.bind("<KeyRelease>", update_years)
        
        # Calculate button
        calculate_button = ctk.CTkButton(params_frame, text="Calcular Valor Futuro", 
                                       command=self.calculate_vf)
        calculate_button.pack(pady=20)
        
        # Results section
        results_frame = ctk.CTkFrame(self.vf_frame)
        results_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        results_title = ctk.CTkLabel(results_frame, text="Resultados", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        results_title.pack(pady=10)
        
        self.vf_result_label = ctk.CTkLabel(results_frame, text="")
        self.vf_result_label.pack(pady=5)
        
        self.monthly_contrib_result_label = ctk.CTkLabel(results_frame, text="")
        self.monthly_contrib_result_label.pack(pady=5)
        
        self.total_contrib_result_label = ctk.CTkLabel(results_frame, text="")
        self.total_contrib_result_label.pack(pady=5)
        
        self.interest_earned_label = ctk.CTkLabel(results_frame, text="")
        self.interest_earned_label.pack(pady=5)
        
        # Update income entry with current value
        if self.df_expenses['Gasto Mín (Bs.)'][0] > 0:
            self.income_entry.delete(0, "end")
            self.income_entry.insert(0, str(self.df_expenses['Gasto Mín (Bs.)'][0]))
    
    def show_edo_frame(self):
        self.clear_main_frame()
        
        # Create scrollable frame
        self.edo_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.edo_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(self.edo_frame, text="Simulación de Modelo EDO", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Parameters section
        params_frame = ctk.CTkFrame(self.edo_frame)
        params_frame.pack(fill="x", padx=10, pady=10)
        
        params_title = ctk.CTkLabel(params_frame, text="Parámetros del Modelo", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        params_title.pack(pady=10)
        
        # Parameters grid
        params_grid = ctk.CTkFrame(params_frame)
        params_grid.pack(fill="x", padx=20, pady=10)
        
        # First row
        ctk.CTkLabel(params_grid, text="Ingreso inicial (I0):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.i0_entry = ctk.CTkEntry(params_grid, width=100)
        self.i0_entry.grid(row=0, column=1, padx=10, pady=10)
        self.i0_entry.insert(0, str(self.edo_params['I0']))
        
        ctk.CTkLabel(params_grid, text="Tasa crecimiento ingreso (g):").grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.g_entry = ctk.CTkEntry(params_grid, width=100)
        self.g_entry.grid(row=0, column=3, padx=10, pady=10)
        self.g_entry.insert(0, str(self.edo_params['g']))
        
        # Second row
        ctk.CTkLabel(params_grid, text="Consumo autónomo (c0):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.c0_entry = ctk.CTkEntry(params_grid, width=100)
        self.c0_entry.grid(row=1, column=1, padx=10, pady=10)
        self.c0_entry.insert(0, str(self.edo_params['c0']))
        
        ctk.CTkLabel(params_grid, text="Propensión marginal al consumo (c1):").grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.c1_entry = ctk.CTkEntry(params_grid, width=100)
        self.c1_entry.grid(row=1, column=3, padx=10, pady=10)
        self.c1_entry.insert(0, str(self.edo_params['c1']))
        
        # Third row
        ctk.CTkLabel(params_grid, text="Efecto ahorro en consumo (c2):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.c2_entry = ctk.CTkEntry(params_grid, width=100)
        self.c2_entry.grid(row=2, column=1, padx=10, pady=10)
        self.c2_entry.insert(0, str(self.edo_params['c2']))
        
        ctk.CTkLabel(params_grid, text="Tasa de rendimiento (r):").grid(row=2, column=2, padx=10, pady=10, sticky="w")
        self.r_entry = ctk.CTkEntry(params_grid, width=100)
        self.r_entry.grid(row=2, column=3, padx=10, pady=10)
        self.r_entry.insert(0, str(self.edo_params['r']))
        
        # Fourth row
        ctk.CTkLabel(params_grid, text="Ahorro inicial (A0):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.a0_entry = ctk.CTkEntry(params_grid, width=100)
        self.a0_entry.grid(row=3, column=1, padx=10, pady=10)
        self.a0_entry.insert(0, str(self.edo_params['A0']))
        
        ctk.CTkLabel(params_grid, text="Tiempo total (años):").grid(row=3, column=2, padx=10, pady=10, sticky="w")
        self.t_entry = ctk.CTkEntry(params_grid, width=100)
        self.t_entry.grid(row=3, column=3, padx=10, pady=10)
        self.t_entry.insert(0, str(self.edo_params['T']))
        
        # Simulate button
        simulate_button = ctk.CTkButton(params_frame, text="Simular Modelo EDO", 
                                      command=self.simulate_edo)
        simulate_button.pack(pady=20)
        
        # Results frame for simulation
        self.edo_results_frame = ctk.CTkFrame(self.edo_frame)
        self.edo_results_frame.pack(fill="x", padx=10, pady=(20, 10), expand=True)
        
        results_title = ctk.CTkLabel(self.edo_results_frame, text="Resultados de la Simulación", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        results_title.pack(pady=10)
        
        self.edo_result_label = ctk.CTkLabel(self.edo_results_frame, text="")
        self.edo_result_label.pack(pady=5)
        
        # Frame for the graph
        self.graph_frame = ctk.CTkFrame(self.edo_frame)
        self.graph_frame.pack(fill="both", padx=10, pady=10, expand=True)
    
    def show_expenses_frame(self):
        self.clear_main_frame()
        
        # Create scrollable frame
        self.expenses_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.expenses_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(self.expenses_frame, text="Gestión de Gastos", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.expenses_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Income input
        income_frame = ctk.CTkFrame(buttons_frame)
        income_frame.pack(fill="x", padx=10, pady=10)
        
        income_label = ctk.CTkLabel(income_frame, text="Ingreso mensual (Bs.):", width=200)
        income_label.pack(side="left", padx=(10, 10))
        
        self.expenses_income_entry = ctk.CTkEntry(income_frame, width=150)
        self.expenses_income_entry.pack(side="left", padx=(0, 10))
        self.expenses_income_entry.insert(0, str(self.df_expenses['Gasto Mín (Bs.)'][0]))
        
        # Load and save buttons
        load_csv_button = ctk.CTkButton(buttons_frame, text="Cargar CSV", 
                                      command=self.load_expenses_csv)
        load_csv_button.pack(side="left", padx=10, pady=10)
        
        save_csv_button = ctk.CTkButton(buttons_frame, text="Guardar CSV", 
                                      command=self.save_expenses_csv)
        save_csv_button.pack(side="left", padx=10, pady=10)
        
        calculate_button = ctk.CTkButton(buttons_frame, text="Calcular Ahorros", 
                                       command=self.calculate_savings)
        calculate_button.pack(side="right", padx=10, pady=10)
        
        # Table frame
        table_frame = ctk.CTkFrame(self.expenses_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create Treeview for expenses
        columns = ("Categoría", "Gasto Mín (Bs.)", "Gasto Máx (Bs.)")
        self.expenses_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Define headings
        for col in columns:
            self.expenses_tree.heading(col, text=col)
            self.expenses_tree.column(col, width=150, anchor="center")
        
        # Set style for dark mode compatibility
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#2a2d2e", 
                        foreground="white", 
                        fieldbackground="#2a2d2e")
        style.map('Treeview', background=[('selected', '#22559b')])
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.expenses_tree.yview)
        self.expenses_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.expenses_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Populate treeview with data
        self.update_expenses_table()
        
        # Add right-click menu for editing
        self.context_menu = tk.Menu(self.expenses_tree, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.edit_expense)
        
        self.expenses_tree.bind("<Button-3>", self.show_context_menu)
        self.expenses_tree.bind("<Double-1>", self.edit_expense)
        
        # Results frame
        self.savings_results_frame = ctk.CTkFrame(self.expenses_frame)
        self.savings_results_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        results_title = ctk.CTkLabel(self.savings_results_frame, text="Resultados de Ahorro", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        results_title.pack(pady=10)
        
        self.min_expenses_label = ctk.CTkLabel(self.savings_results_frame, text="")
        self.min_expenses_label.pack(pady=5)
        
        self.max_expenses_label = ctk.CTkLabel(self.savings_results_frame, text="")
        self.max_expenses_label.pack(pady=5)
        
        self.min_savings_label = ctk.CTkLabel(self.savings_results_frame, text="")
        self.min_savings_label.pack(pady=5)
        
        self.max_savings_label = ctk.CTkLabel(self.savings_results_frame, text="")
        self.max_savings_label.pack(pady=5)
    
    def show_results_frame(self):
        self.clear_main_frame()
        
        # Create scrollable frame
        self.results_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(self.results_frame, text="Resultados y Comparativas", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Summary frame
        summary_frame = ctk.CTkFrame(self.results_frame)
        summary_frame.pack(fill="x", padx=10, pady=10)
        
        summary_title = ctk.CTkLabel(summary_frame, text="Resumen de Simulaciones", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        summary_title.pack(pady=10)
        
        # Results table
        columns_frame = ctk.CTkFrame(summary_frame)
        columns_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(columns_frame, text="Modelo", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(columns_frame, text="Valor Final (Bs.)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(columns_frame, text="Detalles", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(columns_frame, text="Valor Futuro (Anualidad Discreta)").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.vf_summary_label = ctk.CTkLabel(columns_frame, text="-")
        self.vf_summary_label.grid(row=1, column=1, padx=10, pady=5)
        self.vf_details_label = ctk.CTkLabel(columns_frame, text="-")
        self.vf_details_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(columns_frame, text="Modelo Continuo (EDO)").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.edo_summary_label = ctk.CTkLabel(columns_frame, text="-")
        self.edo_summary_label.grid(row=2, column=1, padx=10, pady=5)
        self.edo_details_label = ctk.CTkLabel(columns_frame, text="-")
        self.edo_details_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        
        # Graph comparison section
        graph_frame = ctk.CTkFrame(self.results_frame)
        graph_frame.pack(fill="both", expand=True, padx=10, pady=(20, 10))
        
        graph_title = ctk.CTkLabel(graph_frame, text="Comparativa Gráfica", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        graph_title.pack(pady=10)
        
        # Frame for matplotlib graph
        self.plot_frame = ctk.CTkFrame(graph_frame)
        self.plot_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Generate comparison graph button
        compare_button = ctk.CTkButton(graph_frame, text="Generar Comparativa", 
                                     command=self.generate_comparison)
        compare_button.pack(pady=10)
        
    def show_context_menu(self, event):
        # Show context menu on right-click
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def edit_expense(self, event=None):
        # Get selected item
        selected_item = self.expenses_tree.focus()
        if not selected_item:
            return
        
        # Get values
        values = self.expenses_tree.item(selected_item, "values")
        category = values[0]
        min_expense = values[1]
        max_expense = values[2]
        
        # Create dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Editar {category}")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make it modal
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Form
        ctk.CTkLabel(dialog, text="Categoría:").grid(row=0, column=0, padx=20, pady=20, sticky="w")
        category_label = ctk.CTkLabel(dialog, text=category)
        category_label.grid(row=0, column=1, padx=20, pady=20, sticky="w")
        
        ctk.CTkLabel(dialog, text="Gasto Mínimo (Bs.):").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        min_entry = ctk.CTkEntry(dialog)
        min_entry.grid(row=1, column=1, padx=20, pady=10)
        min_entry.insert(0, min_expense)
        
        ctk.CTkLabel(dialog, text="Gasto Máximo (Bs.):").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        max_entry = ctk.CTkEntry(dialog)
        max_entry.grid(row=2, column=1, padx=20, pady=10)
        max_entry.insert(0, max_expense)
        
        # Save button
        def save_changes():
            # Update dataframe
            category_idx = self.df_expenses[self.df_expenses['Categoría'] == category].index[0]
            
            try:
                new_min = float(min_entry.get())
                new_max = float(max_entry.get())
                
                # Validate inputs
                if new_min > new_max:
                    messagebox.showwarning("Advertencia", "El gasto mínimo no puede ser mayor que el máximo.")
                    return
                
                self.df_expenses.at[category_idx, 'Gasto Mín (Bs.)'] = new_min
                self.df_expenses.at[category_idx, 'Gasto Máx (Bs.)'] = new_max
                
                # Update tree
                self.update_expenses_table()
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        
        save_button = ctk.CTkButton(dialog, text="Guardar", command=save_changes)
        save_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)
    
    def update_expenses_table(self):
        # Clear existing items
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        # Insert rows from dataframe
        for index, row in self.df_expenses.iterrows():
            self.expenses_tree.insert("", "end", values=(
                row['Categoría'], 
                row['Gasto Mín (Bs.)'], 
                row['Gasto Máx (Bs.)']
            ))
    
    def load_expenses_csv(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                df = pd.read_csv(file_path)
                
                # Validate columns
                required_columns = ['Categoría', 'Gasto Mín (Bs.)', 'Gasto Máx (Bs.)']
                if not all(col in df.columns for col in required_columns):
                    messagebox.showerror("Error", 
                                       "El archivo CSV debe contener las columnas: 'Categoría', 'Gasto Mín (Bs.)', 'Gasto Máx (Bs.)'")
                    return
                
                # Ensure 'Ingreso' category exists
                if 'Ingreso' not in df['Categoría'].values:
                    # Add Ingreso with 0 values
                    income_row = pd.DataFrame({
                        'Categoría': ['Ingreso'],
                        'Gasto Mín (Bs.)': [0],
                        'Gasto Máx (Bs.)': [0]
                    })
                    df = pd.concat([income_row, df]).reset_index(drop=True)
                
                self.df_expenses = df
                self.update_expenses_table()
                
                # Update income entry
                income_value = self.df_expenses.loc[
                    self.df_expenses['Categoría'] == 'Ingreso', 'Gasto Mín (Bs.)'].iloc[0]
                self.expenses_income_entry.delete(0, "end")
                self.expenses_income_entry.insert(0, str(income_value))
                
                messagebox.showinfo("Éxito", "Archivo CSV cargado correctamente.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
    
    def save_expenses_csv(self):
        file_path = filedialog.asksaveasfilename(
            title="Guardar como CSV",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                # Update income value before saving
                income_idx = self.df_expenses[self.df_expenses['Categoría'] == 'Ingreso'].index[0]
                self.df_expenses.at[income_idx, 'Gasto Mín (Bs.)'] = float(self.expenses_income_entry.get())
                self.df_expenses.at[income_idx, 'Gasto Máx (Bs.)'] = float(self.expenses_income_entry.get())
                
                # Save to CSV
                self.df_expenses.to_csv(file_path, index=False)
                messagebox.showinfo("Éxito", "Archivo CSV guardado correctamente.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el archivo: {str(e)}")
    
    def calculate_savings(self):
        try:
            # Update income from entry
            income_value = float(self.expenses_income_entry.get())
            income_idx = self.df_expenses[self.df_expenses['Categoría'] == 'Ingreso'].index[0]
            self.df_expenses.at[income_idx, 'Gasto Mín (Bs.)'] = income_value
            self.df_expenses.at[income_idx, 'Gasto Máx (Bs.)'] = income_value
            
            # Calculate total expenses (excluding income)
            expenses_df = self.df_expenses[self.df_expenses['Categoría'] != 'Ingreso']
            total_min_expense = expenses_df['Gasto Mín (Bs.)'].sum()
            total_max_expense = expenses_df['Gasto Máx (Bs.)'].sum()
            
            # Calculate savings
            min_savings = income_value - total_max_expense  # Scenario with maximum expenses
            max_savings = income_value - total_min_expense  # Scenario with minimum expenses
            
            # Update labels
            self.min_expenses_label.configure(text=f"Total gastos mínimos: Bs. {total_min_expense:,.2f}")
            self.max_expenses_label.configure(text=f"Total gastos máximos: Bs. {total_max_expense:,.2f}")
            self.min_savings_label.configure(text=f"Ahorro en escenario de gasto MÁXIMO: Bs. {min_savings:,.2f}")
            self.max_savings_label.configure(text=f"Ahorro en escenario de gasto MÍNIMO: Bs. {max_savings:,.2f}")
            
            # Update monthly contribution in VF calculation
            self.vf_params['P'] = min_savings  # Use minimum savings as default monthly contribution
            
            # If VF frame is active, update entry
            if hasattr(self, 'monthly_contrib_entry') and self.monthly_contrib_entry.winfo_exists():
                self.monthly_contrib_entry.delete(0, "end")
                self.monthly_contrib_entry.insert(0, str(min_savings))
            
            return min_savings, max_savings
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular ahorros: {str(e)}")
            return 0, 0
    
    def calculate_vf(self):
        try:
            # Get parameters from entries
            P = float(self.monthly_contrib_entry.get())
            r_annual = float(self.annual_rate_entry.get()) / 100  # Convert percentage to decimal
            n_months = int(self.months_entry.get())
            
            # Update parameters
            self.vf_params['P'] = P
            self.vf_params['r_annual'] = r_annual
            self.vf_params['n_months'] = n_months
            
            # Calculate monthly rate
            r_monthly = r_annual / 12
            
            # Calculate future value
            if r_monthly != 0:
                FV = P * ((1 + r_monthly)**n_months - 1) / r_monthly
            else:
                FV = P * n_months
            
            # Total contributions
            total_contributions = P * n_months
            
            # Interest earned
            interest_earned = FV - total_contributions
            
            # Update result labels
            self.vf_result_label.configure(text=f"Valor Futuro: Bs. {FV:,.2f}")
            self.monthly_contrib_result_label.configure(text=f"Aporte mensual: Bs. {P:,.2f}")
            self.total_contrib_result_label.configure(text=f"Total aportado: Bs. {total_contributions:,.2f}")
            self.interest_earned_label.configure(text=f"Interés generado: Bs. {interest_earned:,.2f}")
            
            # Update summary in results frame
            if hasattr(self, 'vf_summary_label') and self.vf_summary_label.winfo_exists():
                self.vf_summary_label.configure(text=f"Bs. {FV:,.2f}")
                self.vf_details_label.configure(
                    text=f"Aporte: Bs. {P:,.2f}/mes, Tasa: {r_annual*100:.2f}%, Plazo: {n_months} meses"
                )
            
            return FV
            
        except ValueError as e:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
            return 0
    
    def dAdt(self, t, A, I0, g, c0, c1, c2, r):
        # EDO function: dA/dt = I - C + rA
        I = I0 * np.exp(g * t)  # Income grows exponentially
        C = c0 + c1 * I - c2 * A  # Consumption function
        return I - C + r * A
    
    def simulate_edo(self):
        try:
            # Get parameters from entries
            I0 = float(self.i0_entry.get())
            g = float(self.g_entry.get())
            c0 = float(self.c0_entry.get())
            c1 = float(self.c1_entry.get())
            c2 = float(self.c2_entry.get())
            r = float(self.r_entry.get())
            A0 = float(self.a0_entry.get())
            T = float(self.t_entry.get())
            
            # Update parameters
            self.edo_params['I0'] = I0
            self.edo_params['g'] = g
            self.edo_params['c0'] = c0
            self.edo_params['c1'] = c1
            self.edo_params['c2'] = c2
            self.edo_params['r'] = r
            self.edo_params['A0'] = A0
            self.edo_params['T'] = T
            
            # Simulation parameters
            t0 = 0
            dt = 0.1
            n_steps = int((T - t0) / dt)
            
            # Arrays for storing results
            times = np.linspace(t0, T, n_steps+1)
            A_values = np.zeros(n_steps+1)
            I_values = np.zeros(n_steps+1)
            C_values = np.zeros(n_steps+1)
            
            # Initial conditions
            A_values[0] = A0
            I_values[0] = I0
            C_values[0] = c0 + c1 * I0 - c2 * A0
            
            # RK4 Integration
            A = A0
            t = t0
            
            for i in range(1, n_steps+1):
                k1 = self.dAdt(t, A, I0, g, c0, c1, c2, r)
                k2 = self.dAdt(t + dt/2, A + k1 * dt/2, I0, g, c0, c1, c2, r)
                k3 = self.dAdt(t + dt/2, A + k2 * dt/2, I0, g, c0, c1, c2, r)
                k4 = self.dAdt(t + dt, A + k3 * dt, I0, g, c0, c1, c2, r)
                A = A + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)
                t += dt
                
                A_values[i] = A
                I_values[i] = I0 * np.exp(g * t)
                C_values[i] = c0 + c1 * I_values[i] - c2 * A_values[i]
            
            # Final result
            final_A = A_values[-1]
            
            # Update result label
            self.edo_result_label.configure(text=f"Valor acumulado final: Bs. {final_A:,.2f}")
            
            # Update summary in results frame
            if hasattr(self, 'edo_summary_label') and self.edo_summary_label.winfo_exists():
                self.edo_summary_label.configure(text=f"Bs. {final_A:,.2f}")
                self.edo_details_label.configure(
                    text=f"I0: Bs. {I0:,.2f}, g: {g:.2f}, r: {r:.2f}, T: {T} años"
                )
            
            # Clear existing graph
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            # Create plot
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(times, A_values, 'b-', label='Ahorro (A)')
            ax.plot(times, I_values, 'g--', label='Ingreso (I)')
            ax.plot(times, C_values, 'r-.', label='Consumo (C)')
            
            ax.set_xlabel('Tiempo (años)')
            ax.set_ylabel('Valor (Bs.)')
            ax.set_title('Simulación de Modelo Continuo (EDO)')
            ax.legend()
            ax.grid(True)
            
            # Embed plot
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            return final_A, times, A_values, I_values, C_values
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para todos los parámetros.")
            return 0, [], [], [], []
        
    def generate_comparison(self):
        # Calculate VF
        vf_result = self.calculate_vf()
        
        # Simulate EDO
        edo_result, times, A_values, _, _ = self.simulate_edo()
        
        # Generate comparison plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Create plot
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Plot EDO results
        ax.plot(times, A_values, 'b-', label='Modelo Continuo (EDO)')
        
        # Plot VF results (assuming uniform growth)
        n_years = self.vf_params['n_months'] / 12
        vf_times = np.linspace(0, n_years, 100)
        r = self.vf_params['r_annual']
        P = self.vf_params['P']
        
        if r != 0:
            vf_values = [P * 12 * ((1 + r)**(t) - 1) / r for t in vf_times]
        else:
            vf_values = [P * 12 * t for t in vf_times]
        
        ax.plot(vf_times, vf_values, 'r--', label='Anualidad Discreta (VF)')
        
        ax.set_xlabel('Tiempo (años)')
        ax.set_ylabel('Valor Acumulado (Bs.)')
        ax.set_title('Comparación de Modelos de Ahorro')
        ax.legend()
        ax.grid(True)
        
        # Show final values
        ax.text(0.02, 0.95, f'VF final: Bs. {vf_result:,.2f}', transform=ax.transAxes)
        ax.text(0.02, 0.90, f'EDO final: Bs. {edo_result:,.2f}', transform=ax.transAxes)
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = FinancialSimulatorApp()
    app.mainloop()