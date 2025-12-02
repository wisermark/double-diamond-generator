import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import math

class DoubleDiamondGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Double Diamond SVG Generator")
        self.root.geometry("600x850") # Increased height for more UI elements
        
        # --- Default Configuration ---
        self.config = {
            # Dimensions
            "width": tk.IntVar(value=800),
            "height": tk.IntVar(value=600),
            "margin": tk.IntVar(value=50),
            "gap": tk.IntVar(value=20),
            
            # Header Content
            "title_text": tk.StringVar(value="Double Diamond Design Model"),
            "subtitle_text": tk.StringVar(value="Design Council Framework"),
            
            # Styling
            "stroke_width": tk.IntVar(value=2),
            "stroke_color": tk.StringVar(value="#333333"),
            "text_color": tk.StringVar(value="#000000"),
            "font_size": tk.IntVar(value=20),     # Phase label size
            "title_size": tk.IntVar(value=32),    # Title size
            "subtitle_size": tk.IntVar(value=18), # Subtitle size
            
            # Phase 1: Discover
            "p1_label": tk.StringVar(value="Discover"),
            "p1_color": tk.StringVar(value="#FFD700"), # Gold
            
            # Phase 2: Define
            "p2_label": tk.StringVar(value="Define"),
            "p2_color": tk.StringVar(value="#ADD8E6"), # Light Blue
            
            # Phase 3: Develop
            "p3_label": tk.StringVar(value="Develop"),
            "p3_color": tk.StringVar(value="#90EE90"), # Light Green
            
            # Phase 4: Deliver
            "p4_label": tk.StringVar(value="Deliver"),
            "p4_color": tk.StringVar(value="#FFB6C1"), # Light Pink
        }

        self.create_ui()

    def create_ui(self):
        # Main Canvas
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_lbl = ttk.Label(main_frame, text="Design Council Double Diamond", font=("Helvetica", 16, "bold"))
        title_lbl.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Notebook for Tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
        # --- Tab 1: Dimensions & Layout ---
        tab_dims = ttk.Frame(notebook, padding=10)
        notebook.add(tab_dims, text="Layout & Text")
        
        # Section: Dimensions
        ttk.Label(tab_dims, text="Canvas Dimensions", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.add_entry(tab_dims, "Total Width (px):", self.config["width"], 1)
        self.add_entry(tab_dims, "Total Height (px):", self.config["height"], 2)
        self.add_entry(tab_dims, "Margin (px):", self.config["margin"], 3)
        self.add_entry(tab_dims, "Gap between Diamonds (px):", self.config["gap"], 4)

        # Section: Titles
        ttk.Label(tab_dims, text="Header Content", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 5))
        self.add_entry(tab_dims, "Title Text:", self.config["title_text"], 6)
        self.add_entry(tab_dims, "Subtitle Text:", self.config["subtitle_text"], 7)
        
        # --- Tab 2: Style & Colors ---
        tab_style = ttk.Frame(notebook, padding=10)
        notebook.add(tab_style, text="Style & Colors")

        ttk.Label(tab_style, text="Global Styles", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.add_entry(tab_style, "Title Font Size:", self.config["title_size"], 1)
        self.add_entry(tab_style, "Subtitle Font Size:", self.config["subtitle_size"], 2)
        self.add_entry(tab_style, "Label Font Size:", self.config["font_size"], 3)
        self.add_entry(tab_style, "Stroke Width:", self.config["stroke_width"], 4)
        self.add_color_picker(tab_style, "Stroke Color:", self.config["stroke_color"], 5)
        self.add_color_picker(tab_style, "Text Color:", self.config["text_color"], 6)

        # --- Tab 3: Phases ---
        tab_phases = ttk.Frame(notebook, padding=10)
        notebook.add(tab_phases, text="Phases")

        # Headers
        ttk.Label(tab_phases, text="Phase").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(tab_phases, text="Label Text").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(tab_phases, text="Fill Color").grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Phase Rows
        self.add_phase_row(tab_phases, "1 (Diverge)", self.config["p1_label"], self.config["p1_color"], 1)
        self.add_phase_row(tab_phases, "2 (Converge)", self.config["p2_label"], self.config["p2_color"], 2)
        self.add_phase_row(tab_phases, "3 (Diverge)", self.config["p3_label"], self.config["p3_color"], 3)
        self.add_phase_row(tab_phases, "4 (Converge)", self.config["p4_label"], self.config["p4_color"], 4)

        # --- Action Buttons ---
        btn_frame = ttk.Frame(main_frame, padding=(0, 20, 0, 0))
        btn_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        generate_btn = ttk.Button(btn_frame, text="Generate SVG", command=self.generate_svg)
        generate_btn.pack(side=tk.RIGHT, padx=5)
        
        preview_btn = ttk.Button(btn_frame, text="Preview", command=self.show_preview)
        preview_btn.pack(side=tk.RIGHT, padx=5)

        reset_btn = ttk.Button(btn_frame, text="Reset Defaults", command=self.reset_defaults)
        reset_btn.pack(side=tk.RIGHT, padx=5)

    def add_entry(self, parent, label_text, variable, row):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(parent, textvariable=variable, width=25).grid(row=row, column=1, sticky="w", pady=5, padx=5)

    def add_color_picker(self, parent, label_text, variable, row):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", pady=5)
        
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=1, sticky="w", pady=5, padx=5)
        
        entry = ttk.Entry(frame, textvariable=variable, width=10)
        entry.pack(side=tk.LEFT)
        
        # Color preview/button
        btn = tk.Button(frame, text="Pick", width=4, 
                        command=lambda: self.pick_color(variable))
        btn.pack(side=tk.LEFT, padx=5)

    def add_phase_row(self, parent, phase_name, label_var, color_var, row):
        ttk.Label(parent, text=phase_name).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(parent, textvariable=label_var).grid(row=row, column=1, sticky="ew", pady=5, padx=5)
        
        color_frame = ttk.Frame(parent)
        color_frame.grid(row=row, column=2, sticky="w", pady=5)
        
        entry = ttk.Entry(color_frame, textvariable=color_var, width=8)
        entry.pack(side=tk.LEFT)
        tk.Button(color_frame, text="Pick", width=4, 
                  command=lambda: self.pick_color(color_var)).pack(side=tk.LEFT, padx=5)

    def pick_color(self, variable):
        color = colorchooser.askcolor(initialcolor=variable.get())[1]
        if color:
            variable.set(color)

    def reset_defaults(self):
        msg = "Restart the application to reset to factory defaults."
        messagebox.showinfo("Reset", msg)

    def get_render_data(self):
        """Calculates all coordinates and parameters for rendering (SVG or Canvas)."""
        w = self.config["width"].get()
        h = self.config["height"].get()
        margin = self.config["margin"].get()
        gap = self.config["gap"].get()
        
        stroke_w = self.config["stroke_width"].get()
        stroke_c = self.config["stroke_color"].get()
        text_c = self.config["text_color"].get()
        font_size = self.config["font_size"].get()
        
        title_txt = self.config["title_text"].get()
        title_size = self.config["title_size"].get()
        sub_txt = self.config["subtitle_text"].get()
        sub_size = self.config["subtitle_size"].get()

        # --- Layout Calculation ---
        
        # 1. Header Height Calculation
        # We estimate height based on font size + padding
        header_height = 0
        title_pos = None
        sub_pos = None
        
        current_y = margin
        
        if title_txt:
            # Position text centered horizontally, at current_y
            # For SVG text, y is usually baseline. Let's add size to y.
            title_pos = (w/2, current_y + title_size) 
            header_height += (title_size * 1.5) # 1.5 for line spacing
            current_y += (title_size * 1.5)
            
        if sub_txt:
            sub_pos = (w/2, current_y + sub_size)
            header_height += (sub_size * 1.5)
            current_y += (sub_size * 1.5)
        
        # Add a little extra spacing between subtitle and diamonds
        if header_height > 0:
            header_height += 20 

        # 2. Diamond Drawing Area
        draw_x_start = margin
        draw_x_end = w - margin
        draw_y_start = margin + header_height
        draw_y_end = h - margin
        
        avail_w = draw_x_end - draw_x_start
        avail_h = draw_y_end - draw_y_start
        
        # Center Y for the diamonds
        cy = draw_y_start + (avail_h / 2)
        
        # Diamond Geometry
        # Total available width for diamonds = avail_w
        # This width contains 2 diamonds separated by `gap`.
        # Width of one diamond = (avail_w - gap) / 2
        d_width = (avail_w - gap) / 2
        p_width = d_width / 2 # Phase width

        # X Coordinates relative to the canvas
        x0 = draw_x_start
        x1 = x0 + p_width
        x2 = x0 + d_width
        x3 = x2 + gap
        x4 = x3 + p_width
        x5 = x3 + d_width # which should == draw_x_end

        # Y Coordinates
        y_top = draw_y_start
        y_mid = cy
        y_bot = draw_y_end

        # Define phases
        phases = [
            {
                "label": self.config["p1_label"].get(),
                "color": self.config["p1_color"].get(),
                "points": [(x0, y_mid), (x1, y_top), (x1, y_bot)],
                "text_pos": (x0 + (p_width * 0.5), cy)
            },
            {
                "label": self.config["p2_label"].get(),
                "color": self.config["p2_color"].get(),
                "points": [(x1, y_top), (x2, y_mid), (x1, y_bot)],
                "text_pos": (x1 + (p_width * 0.5), cy)
            },
            {
                "label": self.config["p3_label"].get(),
                "color": self.config["p3_color"].get(),
                "points": [(x3, y_mid), (x4, y_top), (x4, y_bot)],
                "text_pos": (x3 + (p_width * 0.5), cy)
            },
            {
                "label": self.config["p4_label"].get(),
                "color": self.config["p4_color"].get(),
                "points": [(x4, y_top), (x5, y_mid), (x4, y_bot)],
                "text_pos": (x4 + (p_width * 0.5), cy)
            }
        ]

        return {
            "w": w, "h": h,
            "stroke_w": stroke_w, "stroke_c": stroke_c,
            "text_c": text_c, "font_size": font_size,
            "title": {"text": title_txt, "pos": title_pos, "size": title_size},
            "subtitle": {"text": sub_txt, "pos": sub_pos, "size": sub_size},
            "phases": phases
        }

    def show_preview(self):
        try:
            data = self.get_render_data()
            
            # Create popup window
            top = tk.Toplevel(self.root)
            top.title("Preview")
            
            canvas = tk.Canvas(top, width=data["w"], height=data["h"], bg="white")
            canvas.pack()

            # Draw Title
            if data["title"]["text"]:
                canvas.create_text(data["title"]["pos"][0], data["title"]["pos"][1],
                                   text=data["title"]["text"],
                                   fill=data["text_c"],
                                   font=("Arial", -int(data["title"]["size"]), "bold"))

            # Draw Subtitle
            if data["subtitle"]["text"]:
                canvas.create_text(data["subtitle"]["pos"][0], data["subtitle"]["pos"][1],
                                   text=data["subtitle"]["text"],
                                   fill=data["text_c"],
                                   font=("Arial", -int(data["subtitle"]["size"])))

            # Draw Phases
            for phase in data["phases"]:
                points_flat = [coord for point in phase["points"] for coord in point]
                
                canvas.create_polygon(points_flat, 
                                      fill=phase["color"], 
                                      outline=data["stroke_c"], 
                                      width=data["stroke_w"])
                
                canvas.create_text(phase["text_pos"][0], phase["text_pos"][1], 
                                   text=phase["label"], 
                                   fill=data["text_c"],
                                   font=("Arial", -int(data["font_size"])))

        except ValueError:
            messagebox.showerror("Error", "Please ensure all numeric fields contain valid numbers.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_svg(self):
        try:
            data = self.get_render_data()
            w, h = data["w"], data["h"]

            # Start SVG String
            svg_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
    <style>
        .phase-text {{ font-family: Arial, sans-serif; font-size: {data["font_size"]}px; fill: {data["text_c"]}; text-anchor: middle; dominant-baseline: middle; }}
        .title {{ font-family: Arial, sans-serif; font-size: {data["title"]["size"]}px; font-weight: bold; fill: {data["text_c"]}; text-anchor: middle; }}
        .subtitle {{ font-family: Arial, sans-serif; font-size: {data["subtitle"]["size"]}px; fill: {data["text_c"]}; text-anchor: middle; }}
        path {{ stroke: {data["stroke_c"]}; stroke-width: {data["stroke_w"]}; stroke-linejoin: round; }}
    </style>"""

            # Draw Title
            if data["title"]["text"]:
                svg_content += f'\n    <text x="{data["title"]["pos"][0]}" y="{data["title"]["pos"][1]}" class="title">{data["title"]["text"]}</text>'
            
            # Draw Subtitle
            if data["subtitle"]["text"]:
                svg_content += f'\n    <text x="{data["subtitle"]["pos"][0]}" y="{data["subtitle"]["pos"][1]}" class="subtitle">{data["subtitle"]["text"]}</text>'

            # Loop through phases to add paths and text
            for phase in data["phases"]:
                pts = phase["points"]
                path_d = f"M {pts[0][0]},{pts[0][1]} L {pts[1][0]},{pts[1][1]} L {pts[2][0]},{pts[2][1]} Z"
                
                svg_content += f"""
    <!-- Phase: {phase['label']} -->
    <path d="{path_d}" fill="{phase['color']}" />
    <text x="{phase['text_pos'][0]}" y="{phase['text_pos'][1]}" class="phase-text">{phase['label']}</text>"""

            # Close SVG
            svg_content += "\n</svg>"

            # Save File Dialog
            file_path = filedialog.asksaveasfilename(defaultextension=".svg", 
                                                     filetypes=[("SVG files", "*.svg")])
            if file_path:
                with open(file_path, "w") as f:
                    f.write(svg_content)
                messagebox.showinfo("Success", f"SVG successfully saved to:\n{file_path}")

        except ValueError:
            messagebox.showerror("Error", "Please ensure all numeric fields contain valid numbers.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DoubleDiamondGenerator(root)
    root.mainloop()