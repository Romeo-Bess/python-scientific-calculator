import customtkinter as ctk
import math
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# App configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AdvancedCalculatorSuite(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Scientific & Graphing Calculator Suite")
        self.geometry("550x850")
        self.resizable(False, False)

        # Color System
        self.bg_color = "#1C1917"          # Dark Charcoal
        self.display_bg = "#12100E"        # Deep Charcoal
        self.btn_num_bg = "#2C2A29"        # Number buttons
        self.btn_num_hover = "#3E3C3B"
        self.btn_op_bg = "#EA580C"         # Orange operators
        self.btn_op_hover = "#F97316"
        self.btn_fn_bg = "#44403C"         # Muted scientific buttons
        self.btn_fn_hover = "#57534E"
        self.btn_eq_bg = "#2563EB"         # Blue equals
        self.btn_eq_hover = "#3B82F6"
        self.btn_clear_bg = "#DC2626"      # Red clear
        self.btn_clear_hover = "#EF4444"

        self.configure(fg_color=self.bg_color)

        # Header Title
        self.header_label = ctk.CTkLabel(
            self,
            text="CALCULATOR SUITE PRO",
            font=("Inter", 18, "bold"),
            text_color="#A8A29E"
        )
        self.header_label.pack(pady=(15, 5))

        # Main Tab Container
        self.tabview = ctk.CTkTabview(self, segmented_button_fg_color="#2C2A29", segmented_button_selected_color="#EA580C")
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(5, 10))

        # Add tabs
        self.tab_calc = self.tabview.add("Calculator")
        self.tab_graph = self.tabview.add("Grapher")
        self.tab_convert = self.tabview.add("Converter")
        self.tab_solver = self.tabview.add("Solver")

        self.setup_calculator_tab()
        self.setup_grapher_tab()
        self.setup_converter_tab()
        self.setup_solver_tab()
        self.setup_footer()

        # Keyboard Event Binding
        self.bind("<Key>", self.handle_keyboard_input)
        self.focus_set()

    def setup_footer(self):
        # Bottom controls for theme toggling
        footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        footer_frame.pack(fill="x", side="bottom", padx=20, pady=(0, 10))

        self.theme_label = ctk.CTkLabel(footer_frame, text="Dark Theme", font=("Inter", 11, "bold"), text_color="#78716C")
        self.theme_label.pack(side="left", padx=(5, 10))

        self.theme_switch = ctk.CTkSwitch(
            footer_frame, 
            text="", 
            command=self.toggle_theme, 
            progress_color="#EA580C"
        )
        self.theme_switch.pack(side="left")
        self.theme_switch.select() # Start in dark mode

        self.shortcut_info = ctk.CTkLabel(
            footer_frame, 
            text="Keyboard binds active", 
            font=("Inter", 11, "italic"), 
            text_color="#57534E"
        )
        self.shortcut_info.pack(side="right", padx=5)

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.theme_label.configure(text="Dark Theme")
        else:
            ctk.set_appearance_mode("Light")
            self.theme_label.configure(text="Light Theme")

    # ================= CALCULATOR TAB =================
    def setup_calculator_tab(self):
        # Display Area
        display_frame = ctk.CTkFrame(self.tab_calc, fg_color=self.display_bg, corner_radius=12)
        display_frame.pack(padx=5, pady=10, fill="x")

        self.history_box = ctk.CTkTextbox(
            display_frame, 
            height=120, 
            font=("Inter", 12), 
            fg_color="transparent", 
            text_color="#78716C",
            wrap="word"
        )
        self.history_box.pack(padx=10, pady=(10, 5), fill="both", expand=True)
        self.history_box.insert("1.0", "History:\n")
        self.history_box.configure(state="disabled")

        self.entry = ctk.CTkEntry(
            display_frame, 
            placeholder_text="0",
            font=("Inter", 32, "bold"), 
            fg_color="transparent", 
            border_width=0, 
            text_color="#FFFFFF",
            justify="right"
        )
        self.entry.pack(padx=10, pady=(5, 15), fill="x")

        # Buttons Grid Frame
        btn_frame = ctk.CTkFrame(self.tab_calc, fg_color="transparent")
        btn_frame.pack(padx=5, pady=10, fill="both", expand=True)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['C', '(', ')', '√'],
            ['sin', 'cos', 'tan', 'log'],
            ['exp', 'pi', 'del', 'clear_hist']
        ]

        for col in range(4):
            btn_frame.columnconfigure(col, weight=1, pad=8)
        for row in range(len(buttons)):
            btn_frame.rowconfigure(row, weight=1, pad=8)

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                btn_text = char
                if char in '0123456789.':
                    bg = self.btn_num_bg
                    hover = self.btn_num_hover
                    fg = "#FFFFFF"
                elif char in ['/', '*', '-', '+']:
                    bg = self.btn_op_bg
                    hover = self.btn_op_hover
                    fg = "#FFFFFF"
                elif char == '=':
                    bg = self.btn_eq_bg
                    hover = self.btn_eq_hover
                    fg = "#FFFFFF"
                elif char in ['C', 'del']:
                    bg = self.btn_clear_bg
                    hover = self.btn_clear_hover
                    fg = "#FFFFFF"
                elif char == 'clear_hist':
                    bg = "#451A03"
                    hover = "#78350F"
                    fg = "#FDBA74"
                    btn_text = "cls hist"
                else:
                    bg = self.btn_fn_bg
                    hover = self.btn_fn_hover
                    fg = "#E7E5E4"
                    if char == 'pi':
                        btn_text = "π"

                # Command Routing
                if char == '=':
                    cmd = self.calculate
                elif char == 'C':
                    cmd = self.clear_entry
                elif char == 'del':
                    cmd = self.delete_char
                elif char == 'clear_hist':
                    cmd = self.clear_history
                elif char == '√':
                    cmd = lambda: self.insert_text("math.sqrt(")
                elif char == 'sin':
                    cmd = lambda: self.insert_text("math.sin(math.radians(")
                elif char == 'cos':
                    cmd = lambda: self.insert_text("math.cos(math.radians(")
                elif char == 'tan':
                    cmd = lambda: self.insert_text("math.tan(math.radians(")
                elif char == 'log':
                    cmd = lambda: self.insert_text("math.log10(")
                elif char == 'exp':
                    cmd = lambda: self.insert_text("math.exp(")
                elif char == 'pi':
                    cmd = lambda: self.insert_text(str(math.pi))
                else:
                    cmd = lambda txt=char: self.insert_text(txt)

                btn = ctk.CTkButton(
                    btn_frame, 
                    text=btn_text, 
                    font=("Inter", 16, "bold"),
                    fg_color=bg, 
                    hover_color=hover, 
                    text_color=fg, 
                    height=52,
                    corner_radius=8,
                    command=cmd
                )
                btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

    def insert_text(self, txt):
        current = self.entry.get()
        self.entry.delete(0, "end")
        self.entry.insert(0, current + txt)

    def clear_entry(self):
        self.entry.delete(0, "end")

    def delete_char(self):
        current = self.entry.get()
        if current:
            self.entry.delete(0, "end")
            self.entry.insert(0, current[:-1])

    def clear_history(self):
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        self.history_box.insert("1.0", "History:\n")
        self.history_box.configure(state="disabled")

    def calculate(self):
        try:
            expr = self.entry.get()
            if not expr.strip():
                return
            res = eval(expr, {"__builtins__": None, "math": math})
            
            if isinstance(res, float):
                if res.is_integer():
                    res = int(res)
                else:
                    res = round(res, 8)
            
            self.entry.delete(0, "end")
            self.entry.insert(0, str(res))
            
            self.history_box.configure(state="normal")
            self.history_box.insert("end", f"{expr} = {res}\n")
            self.history_box.see("end")
            self.history_box.configure(state="disabled")
        except Exception:
            self.entry.delete(0, "end")
            self.entry.insert(0, "Error")

    def handle_keyboard_input(self, event):
        # Prevent input if active focus is inside other tab entry fields
        focused_widget = self.focus_get()
        if isinstance(focused_widget, ctk.CTkEntry) and focused_widget != self.entry:
            return

        char = event.char
        keysym = event.keysym

        if char in '0123456789.+-*/()':
            self.insert_text(char)
        elif keysym == "Return" or char == '=':
            self.calculate()
        elif keysym == "BackSpace":
            self.delete_char()
        elif keysym == "Escape":
            self.clear_entry()

    # ================= GRAPHER TAB =================
    def setup_grapher_tab(self):
        # Config options
        control_frame = ctk.CTkFrame(self.tab_graph, fg_color="transparent")
        control_frame.pack(fill="x", padx=10, pady=10)

        # Label & Entry for function f(x)
        fn_label = ctk.CTkLabel(control_frame, text="f(x) =", font=("Inter", 16, "bold"), text_color="#A8A29E")
        fn_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.graph_fn_entry = ctk.CTkEntry(
            control_frame, 
            placeholder_text="x**2 - 4*x + 3", 
            font=("Inter", 14), 
            width=220
        )
        self.graph_fn_entry.grid(row=0, column=1, padx=5, pady=5)
        self.graph_fn_entry.insert(0, "math.sin(x)")

        # X min/max ranges
        range_label = ctk.CTkLabel(control_frame, text="X range:", font=("Inter", 12), text_color="#78716C")
        range_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.xmin_entry = ctk.CTkEntry(control_frame, placeholder_text="-10", font=("Inter", 12), width=70)
        self.xmin_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.xmin_entry.insert(0, "-10")

        self.xmax_entry = ctk.CTkEntry(control_frame, placeholder_text="10", font=("Inter", 12), width=70)
        self.xmax_entry.grid(row=1, column=1, padx=(90, 5), pady=5, sticky="w")
        self.xmax_entry.insert(0, "10")

        plot_btn = ctk.CTkButton(
            control_frame, 
            text="Plot Graph", 
            font=("Inter", 14, "bold"),
            fg_color=self.btn_op_bg, 
            hover_color=self.btn_op_hover, 
            command=self.plot_graph,
            width=120
        )
        plot_btn.grid(row=0, column=2, rowspan=2, padx=10, pady=5)

        # Plot output Canvas Frame
        self.plot_frame = ctk.CTkFrame(self.tab_graph, fg_color=self.display_bg, corner_radius=12)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Empty initial plot setup
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor=self.display_bg)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.display_bg)
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.grid(True, color='#2C2A29')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def plot_graph(self):
        try:
            fn_str = self.graph_fn_entry.get()
            xmin = float(self.xmin_entry.get())
            xmax = float(self.xmax_entry.get())

            if xmin >= xmax:
                return

            # Generate datapoints
            steps = 500
            x_vals = []
            y_vals = []
            dx = (xmax - xmin) / steps

            for i in range(steps + 1):
                x = xmin + i * dx
                try:
                    # Safely calculate expression y for given x
                    context = {"x": x, "math": math, "sin": math.sin, "cos": math.cos, "tan": math.tan, "pi": math.pi, "e": math.e}
                    y = eval(fn_str, {"__builtins__": None}, context)
                    x_vals.append(x)
                    y_vals.append(y)
                except Exception:
                    continue

            self.ax.clear()
            self.ax.set_facecolor(self.display_bg)
            self.ax.plot(x_vals, y_vals, color="#EA580C", linewidth=2.5)
            self.ax.tick_params(colors='white')
            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['left'].set_color('white')
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.grid(True, color='#2C2A29')
            self.canvas.draw()

        except Exception as e:
            # Revert to error label or state
            pass

    # ================= CONVERTER TAB =================
    def setup_converter_tab(self):
        # Convert type selection
        sel_frame = ctk.CTkFrame(self.tab_convert, fg_color="transparent")
        sel_frame.pack(fill="x", padx=20, pady=15)

        type_label = ctk.CTkLabel(sel_frame, text="Category:", font=("Inter", 14, "bold"), text_color="#A8A29E")
        type_label.pack(side="left", padx=5)

        self.conv_category = ctk.CTkComboBox(
            sel_frame, 
            values=["Length", "Weight", "Temperature"], 
            command=self.update_converter_units,
            button_color="#EA580C",
            button_hover_color="#F97316"
        )
        self.conv_category.pack(side="left", padx=10)

        # Input & Output frame
        conv_grid = ctk.CTkFrame(self.tab_convert, fg_color=self.display_bg, corner_radius=12)
        conv_grid.pack(fill="both", expand=True, padx=20, pady=10)

        # From Frame
        from_frame = ctk.CTkFrame(conv_grid, fg_color="transparent")
        from_frame.pack(fill="x", padx=20, pady=20)

        self.from_val_entry = ctk.CTkEntry(from_frame, placeholder_text="0.0", font=("Inter", 18), width=180)
        self.from_val_entry.pack(side="left", padx=5)
        self.from_val_entry.insert(0, "1")
        self.from_val_entry.bind("<KeyRelease>", lambda e: self.do_conversion())

        self.from_unit_combo = ctk.CTkComboBox(from_frame, values=["Meters", "Feet", "Inches", "Miles"], width=120)
        self.from_unit_combo.pack(side="right", padx=5)

        # Arrow indicator
        arrow_label = ctk.CTkLabel(conv_grid, text="↓", font=("Inter", 28), text_color="#EA580C")
        arrow_label.pack(pady=5)

        # To Frame
        to_frame = ctk.CTkFrame(conv_grid, fg_color="transparent")
        to_frame.pack(fill="x", padx=20, pady=20)

        self.to_val_label = ctk.CTkLabel(to_frame, text="0.0", font=("Inter", 24, "bold"), text_color="#FFFFFF")
        self.to_val_label.pack(side="left", padx=5)

        self.to_unit_combo = ctk.CTkComboBox(to_frame, values=["Meters", "Feet", "Inches", "Miles"], width=120)
        self.to_unit_combo.pack(side="right", padx=5)

        # Trigger initial conversion setup
        self.update_converter_units("Length")

    def update_converter_units(self, category):
        if category == "Length":
            units = ["Meters", "Feet", "Inches", "Miles"]
        elif category == "Weight":
            units = ["Kilograms", "Pounds", "Ounces", "Grams"]
        else: # Temperature
            units = ["Celsius", "Fahrenheit", "Kelvin"]

        self.from_unit_combo.configure(values=units)
        self.to_unit_combo.configure(values=units)
        self.from_unit_combo.set(units[0])
        self.to_unit_combo.set(units[1])
        self.do_conversion()

    def do_conversion(self):
        try:
            category = self.conv_category.get()
            val = float(self.from_val_entry.get())
            unit_from = self.from_unit_combo.get()
            unit_to = self.to_unit_combo.get()

            res = 0.0

            if category == "Length":
                # Convert to base (Meters)
                to_meters = {"Meters": 1.0, "Feet": 0.3048, "Inches": 0.0254, "Miles": 1609.34}
                base = val * to_meters.get(unit_from, 1.0)
                # Convert from base to target
                from_meters = {"Meters": 1.0, "Feet": 3.28084, "Inches": 39.3701, "Miles": 0.000621371}
                res = base * from_meters.get(unit_to, 1.0)
            elif category == "Weight":
                # Convert to base (Grams)
                to_grams = {"Grams": 1.0, "Kilograms": 1000.0, "Pounds": 453.592, "Ounces": 28.3495}
                base = val * to_grams.get(unit_from, 1.0)
                from_grams = {"Grams": 1.0, "Kilograms": 0.001, "Pounds": 0.00220462, "Ounces": 0.035274}
                res = base * from_grams.get(unit_to, 1.0)
            else: # Temperature
                # Convert to Celsius
                if unit_from == "Celsius":
                    c = val
                elif unit_from == "Fahrenheit":
                    c = (val - 32) * 5/9
                else: # Kelvin
                    c = val - 273.15

                # Convert Celsius to Target
                if unit_to == "Celsius":
                    res = c
                elif unit_to == "Fahrenheit":
                    res = c * 9/5 + 32
                else: # Kelvin
                    res = c + 273.15

            self.to_val_label.configure(text=f"{round(res, 6)}")
        except ValueError:
            self.to_val_label.configure(text="Invalid Input")

    # ================= SOLVER TAB =================
    def setup_solver_tab(self):
        # Choose Solver Type
        sel_frame = ctk.CTkFrame(self.tab_solver, fg_color="transparent")
        sel_frame.pack(fill="x", padx=20, pady=15)

        self.solver_mode = ctk.CTkComboBox(
            sel_frame, 
            values=["Quadratic Equation", "Linear System (2x2)"], 
            command=self.toggle_solver_view,
            button_color="#EA580C",
            button_hover_color="#F97316"
        )
        self.solver_mode.pack(fill="x", padx=10)

        # Solver inputs frame
        self.solver_grid = ctk.CTkFrame(self.tab_solver, fg_color=self.display_bg, corner_radius=12)
        self.solver_grid.pack(fill="both", expand=True, padx=20, pady=10)

        # Placeholder label for solving output
        self.solve_res_label = ctk.CTkLabel(
            self.tab_solver, 
            text="Enter coefficients and click Solve", 
            font=("Inter", 14, "bold"),
            text_color="#A8A29E"
        )
        self.solve_res_label.pack(pady=15)

        # Trigger Initial Layout
        self.toggle_solver_view("Quadratic Equation")

    def toggle_solver_view(self, mode):
        # Clear solver grid
        for child in self.solver_grid.winfo_children():
            child.destroy()

        if mode == "Quadratic Equation":
            # ax^2 + bx + c = 0
            title = ctk.CTkLabel(self.solver_grid, text="ax² + bx + c = 0", font=("Inter", 16, "bold"), text_color="#EA580C")
            title.pack(pady=10)

            inp_frame = ctk.CTkFrame(self.solver_grid, fg_color="transparent")
            inp_frame.pack(pady=10)

            ctk.CTkLabel(inp_frame, text="a =", font=("Inter", 14)).grid(row=0, column=0, padx=5, pady=5)
            self.entry_qa = ctk.CTkEntry(inp_frame, width=80)
            self.entry_qa.grid(row=0, column=1, padx=5, pady=5)
            self.entry_qa.insert(0, "1")

            ctk.CTkLabel(inp_frame, text="b =", font=("Inter", 14)).grid(row=1, column=0, padx=5, pady=5)
            self.entry_qb = ctk.CTkEntry(inp_frame, width=80)
            self.entry_qb.grid(row=1, column=1, padx=5, pady=5)
            self.entry_qb.insert(0, "-5")

            ctk.CTkLabel(inp_frame, text="c =", font=("Inter", 14)).grid(row=2, column=0, padx=5, pady=5)
            self.entry_qc = ctk.CTkEntry(inp_frame, width=80)
            self.entry_qc.grid(row=2, column=1, padx=5, pady=5)
            self.entry_qc.insert(0, "6")

            solve_btn = ctk.CTkButton(self.solver_grid, text="Solve", fg_color="#EA580C", hover_color="#F97316", command=self.solve_quadratic)
            solve_btn.pack(pady=15)

        else:
            # 2x2 System:
            # a1x + b1y = c1
            # a2x + b2y = c2
            title = ctk.CTkLabel(self.solver_grid, text="System: ax + by = c", font=("Inter", 16, "bold"), text_color="#EA580C")
            title.pack(pady=10)

            inp_frame = ctk.CTkFrame(self.solver_grid, fg_color="transparent")
            inp_frame.pack(pady=10)

            # Eq 1
            ctk.CTkLabel(inp_frame, text="Eq 1:").grid(row=0, column=0, padx=5, pady=5)
            self.entry_a1 = ctk.CTkEntry(inp_frame, width=50, placeholder_text="a1")
            self.entry_a1.grid(row=0, column=1, padx=2, pady=5)
            self.entry_a1.insert(0, "2")
            ctk.CTkLabel(inp_frame, text="x +").grid(row=0, column=2, padx=2, pady=5)
            self.entry_b1 = ctk.CTkEntry(inp_frame, width=50, placeholder_text="b1")
            self.entry_b1.grid(row=0, column=3, padx=2, pady=5)
            self.entry_b1.insert(0, "1")
            ctk.CTkLabel(inp_frame, text="y =").grid(row=0, column=4, padx=2, pady=5)
            self.entry_c1 = ctk.CTkEntry(inp_frame, width=50, placeholder_text="c1")
            self.entry_c1.grid(row=0, column=5, padx=2, pady=5)
            self.entry_c1.insert(0, "8")

            # Eq 2
            ctk.CTkLabel(inp_frame, text="Eq 2:").grid(row=1, column=0, padx=5, pady=5)
            self.entry_a2 = ctk.CTkEntry(inp_frame, width=50, placeholder_text="a2")
            self.entry_a2.grid(row=1, column=1, padx=2, pady=5)
            self.entry_a2.insert(0, "1")
            ctk.CTkLabel(inp_frame, text="x -").grid(row=1, column=2, padx=2, pady=5)
            self.entry_b2 = ctk.CTkEntry(inp_frame, width=50, placeholder_text="b2")
            self.entry_b2.grid(row=1, column=3, padx=2, pady=5)
            self.entry_b2.insert(0, "1")  # represents -1y implicitly, let's keep inputs absolute coefficients
            self.entry_b2.insert(0, "-1")
            ctk.CTkLabel(inp_frame, text="y =").grid(row=1, column=4, padx=2, pady=5)
            self.entry_c2 = ctk.CTkEntry(inp_frame, width=50, placeholder_text="c2")
            self.entry_c2.grid(row=1, column=5, padx=2, pady=5)
            self.entry_c2.insert(0, "1")

            solve_btn = ctk.CTkButton(self.solver_grid, text="Solve System", fg_color="#EA580C", hover_color="#F97316", command=self.solve_system)
            solve_btn.pack(pady=15)

    def solve_quadratic(self):
        try:
            a = float(self.entry_qa.get())
            b = float(self.entry_qb.get())
            c = float(self.entry_qc.get())

            if a == 0:
                self.solve_res_label.configure(text="Coefficient 'a' cannot be zero.")
                return

            disc = b**2 - 4*a*c
            if disc > 0:
                x1 = (-b + math.sqrt(disc)) / (2*a)
                x2 = (-b - math.sqrt(disc)) / (2*a)
                self.solve_res_label.configure(text=f"Two real roots:\nx1 = {round(x1, 5)},  x2 = {round(x2, 5)}")
            elif disc == 0:
                x = -b / (2*a)
                self.solve_res_label.configure(text=f"One real root:\nx = {round(x, 5)}")
            else:
                real = -b / (2*a)
                imag = math.sqrt(-disc) / (2*a)
                self.solve_res_label.configure(text=f"Complex roots:\nx1 = {round(real, 5)} + {round(imag, 5)}i\nx2 = {round(real, 5)} - {round(imag, 5)}i")
        except ValueError:
            self.solve_res_label.configure(text="Invalid input coefficients.")

    def solve_system(self):
        try:
            a1 = float(self.entry_a1.get())
            b1 = float(self.entry_b1.get())
            c1 = float(self.entry_c1.get())

            a2 = float(self.entry_a2.get())
            # Clean up default duplicate prepended value if present
            b2_str = self.entry_b2.get()
            b2 = float(b2_str)
            c2 = float(self.entry_c2.get())

            # Cramer's Rule
            D = a1 * b2 - b1 * a2
            if D == 0:
                self.solve_res_label.configure(text="No unique solution (Determinant = 0)")
                return

            Dx = c1 * b2 - b1 * c2
            Dy = a1 * c2 - c1 * a2

            x = Dx / D
            y = Dy / D

            self.solve_res_label.configure(text=f"Solution:\nx = {round(x, 5)}\ny = {round(y, 5)}")
        except ValueError:
            self.solve_res_label.configure(text="Invalid input coefficients.")

if __name__ == "__main__":
    app = AdvancedCalculatorSuite()
    app.mainloop()
