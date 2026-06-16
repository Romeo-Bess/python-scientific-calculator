import customtkinter as ctk
import math

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ScientificCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sci Calculator Pro")
        self.geometry("450x820")
        self.resizable(False, False)
        
        # Color Palette - Evolved Soft UI / Dark Mode
        self.bg_color = "#1C1917"          # Dark Charcoal
        self.display_bg = "#12100E"        # Deep Charcoal display
        self.btn_num_bg = "#2C2A29"        # Number buttons
        self.btn_num_hover = "#3E3C3B"
        self.btn_op_bg = "#EA580C"         # Orange for basic ops
        self.btn_op_hover = "#F97316"
        self.btn_fn_bg = "#44403C"         # Muted brown/gray for scientific fns
        self.btn_fn_hover = "#57534E"
        self.btn_eq_bg = "#2563EB"         # Blue for "="
        self.btn_eq_hover = "#3B82F6"
        self.btn_clear_bg = "#DC2626"      # Red for "C"
        self.btn_clear_hover = "#EF4444"
        
        self.config(bg=self.bg_color)
        self.configure(fg_color=self.bg_color)

        # Header Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="SCIENTIFIC CALCULATOR", 
            font=("Inter", 16, "bold"), 
            text_color="#A8A29E"
        )
        self.title_label.pack(pady=(15, 5))

        # Main display frame
        display_frame = ctk.CTkFrame(self, fg_color=self.display_bg, corner_radius=12)
        display_frame.pack(padx=20, pady=10, fill="x")

        # History display (Scrolling Text Box)
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

        # Active Expression Display
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
        self.entry.bind("<Key>", lambda e: "break")  # Read-only input via keyboard mapping instead

        # Frame for buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(10, 20), fill="both", expand=True)

        # Buttons layout
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['C', '(', ')', '√'],
            ['sin', 'cos', 'tan', 'log'],
            ['exp', 'pi', 'del', 'clear_hist']
        ]

        # Configure columns and rows to be equal weight
        for col in range(4):
            btn_frame.columnconfigure(col, weight=1, pad=8)
        for row in range(len(buttons)):
            btn_frame.rowconfigure(row, weight=1, pad=8)

        # Generate Buttons
        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                btn_text = char
                # Style mappings
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

                # Define commands
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
            # Safety evaluation check / execution
            res = eval(expr, {"__builtins__": None, "math": math})
            
            # Format float output nicely if it is a float
            if isinstance(res, float):
                if res.is_integer():
                    res = int(res)
                else:
                    res = round(res, 8)
            
            self.entry.delete(0, "end")
            self.entry.insert(0, str(res))
            
            # Update history log
            self.history_box.configure(state="normal")
            self.history_box.insert("end", f"{expr} = {res}\n")
            self.history_box.see("end")
            self.history_box.configure(state="disabled")
        except Exception as e:
            self.entry.delete(0, "end")
            self.entry.insert(0, "Error")

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()
