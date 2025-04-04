import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Processor")
        self.root.geometry("1000x600")
        
        # Variables
        self.original_image = None
        self.processed_image = None
        self.display_image = None
        self.current_filename = None
        
        # Create the GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for controls
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Load and save buttons
        ttk.Button(control_frame, text="Load Image", command=self.load_image).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="Save Processed Image", command=self.save_image).pack(fill=tk.X, pady=5)
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Image filtering
        filtering_frame = ttk.LabelFrame(control_frame, text="Image Filtering", padding="5")
        filtering_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(filtering_frame, text="Blur", 
                  command=self.apply_blur).pack(fill=tk.X, pady=2)
        
        ttk.Button(filtering_frame, text="Sharpen", 
                  command=self.apply_sharpen).pack(fill=tk.X, pady=2)
        
        ttk.Button(filtering_frame, text="Find Edges", 
                  command=self.apply_edge_detection).pack(fill=tk.X, pady=2)
        
        ttk.Button(filtering_frame, text="Emboss", 
                  command=self.apply_emboss).pack(fill=tk.X, pady=2)
        
        # Color manipulation
        color_frame = ttk.LabelFrame(control_frame, text="Color Manipulation", padding="5")
        color_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(color_frame, text="Enhance Brightness", 
                  command=self.enhance_brightness).pack(fill=tk.X, pady=2)
        
        self.brightness_factor = tk.DoubleVar(value=1.5)
        ttk.Label(color_frame, text="Brightness Factor:").pack(anchor=tk.W)
        brightness_scale = ttk.Scale(color_frame, from_=0.1, to=3.0, variable=self.brightness_factor, orient=tk.HORIZONTAL)
        brightness_scale.pack(fill=tk.X, pady=2)
        
        ttk.Button(color_frame, text="Enhance Contrast", 
                  command=self.enhance_contrast).pack(fill=tk.X, pady=2)
        
        self.contrast_factor = tk.DoubleVar(value=1.5)
        ttk.Label(color_frame, text="Contrast Factor:").pack(anchor=tk.W)
        contrast_scale = ttk.Scale(color_frame, from_=0.1, to=3.0, variable=self.contrast_factor, orient=tk.HORIZONTAL)
        contrast_scale.pack(fill=tk.X, pady=2)
        
        ttk.Button(color_frame, text="Grayscale", 
                  command=self.convert_to_grayscale).pack(fill=tk.X, pady=2)
        
        # Transformations
        transform_frame = ttk.LabelFrame(control_frame, text="Transformations", padding="5")
        transform_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(transform_frame, text="Rotate 90°", 
                  command=self.rotate_90).pack(fill=tk.X, pady=2)
        
        ttk.Button(transform_frame, text="Rotate 180°", 
                  command=self.rotate_180).pack(fill=tk.X, pady=2)
        
        ttk.Button(transform_frame, text="Rotate 270°", 
                  command=self.rotate_270).pack(fill=tk.X, pady=2)
        
        ttk.Button(transform_frame, text="Flip Horizontal", 
                  command=self.flip_horizontal).pack(fill=tk.X, pady=2)
        
        ttk.Button(transform_frame, text="Flip Vertical", 
                  command=self.flip_vertical).pack(fill=tk.X, pady=2)
        
        # Reset button
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Button(control_frame, text="Reset to Original", command=self.reset_image).pack(fill=tk.X, pady=5)
        
        # Right frame for image display
        self.display_frame = ttk.LabelFrame(main_frame, text="Image Preview")
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Label to display the image
        self.image_label = ttk.Label(self.display_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
        )
        
        if file_path:
            try:
                self.current_filename = os.path.basename(file_path)
                self.original_image = Image.open(file_path)
                self.processed_image = self.original_image.copy()
                self.display_processed_image()
                self.status_var.set(f"Loaded: {self.current_filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), 
                           ("BMP files", "*.bmp"), ("TIFF files", "*.tif")]
            )
            
            if file_path:
                try:
                    self.processed_image.save(file_path)
                    messagebox.showinfo("Success", f"Image saved to {file_path}")
                    self.status_var.set(f"Saved to: {os.path.basename(file_path)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not save image: {str(e)}")
    
    def display_processed_image(self):
        if self.processed_image:
            # Resize image to fit the display area while maintaining aspect ratio
            display_width = self.display_frame.winfo_width() - 20
            display_height = self.display_frame.winfo_height() - 20
            
            if display_width <= 1 or display_height <= 1:
                # Window not fully created yet, use default size
                display_width = 600
                display_height = 400
            
            # Calculate new dimensions
            img_width, img_height = self.processed_image.size
            ratio = min(display_width/img_width, display_height/img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            # Resize image for display
            self.display_image = self.processed_image.resize((new_width, new_height), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.display_image)
            
            # Update label
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference
    
    def reset_image(self):
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.display_processed_image()
            self.status_var.set("Reset to original image")
    
    # Image processing functions
    def apply_blur(self):
        if self.processed_image:
            self.processed_image = self.processed_image.filter(ImageFilter.GaussianBlur(radius=2))
            self.display_processed_image()
            self.status_var.set("Applied: Gaussian Blur")
    
    def apply_sharpen(self):
        if self.processed_image:
            self.processed_image = self.processed_image.filter(ImageFilter.SHARPEN)
            self.display_processed_image()
            self.status_var.set("Applied: Sharpen")
    
    def apply_edge_detection(self):
        if self.processed_image:
            self.processed_image = self.processed_image.filter(ImageFilter.FIND_EDGES)
            self.display_processed_image()
            self.status_var.set("Applied: Edge Detection")
    
    def apply_emboss(self):
        if self.processed_image:
            self.processed_image = self.processed_image.filter(ImageFilter.EMBOSS)
            self.display_processed_image()
            self.status_var.set("Applied: Emboss")
    
    def enhance_brightness(self):
        if self.processed_image:
            factor = self.brightness_factor.get()
            enhancer = ImageEnhance.Brightness(self.processed_image)
            self.processed_image = enhancer.enhance(factor)
            self.display_processed_image()
            self.status_var.set(f"Applied: Brightness Enhancement (factor={factor:.1f})")
    
    def enhance_contrast(self):
        if self.processed_image:
            factor = self.contrast_factor.get()
            enhancer = ImageEnhance.Contrast(self.processed_image)
            self.processed_image = enhancer.enhance(factor)
            self.display_processed_image()
            self.status_var.set(f"Applied: Contrast Enhancement (factor={factor:.1f})")
    
    def convert_to_grayscale(self):
        if self.processed_image:
            self.processed_image = ImageOps.grayscale(self.processed_image)
            # Convert back to RGB mode for consistent processing
            self.processed_image = self.processed_image.convert('RGB')
            self.display_processed_image()
            self.status_var.set("Applied: Grayscale Conversion")
    
    def rotate_90(self):
        if self.processed_image:
            self.processed_image = self.processed_image.rotate(90, expand=True)
            self.display_processed_image()
            self.status_var.set("Applied: Rotate 90°")
    
    def rotate_180(self):
        if self.processed_image:
            self.processed_image = self.processed_image.rotate(180, expand=True)
            self.display_processed_image()
            self.status_var.set("Applied: Rotate 180°")
    
    def rotate_270(self):
        if self.processed_image:
            self.processed_image = self.processed_image.rotate(270, expand=True)
            self.display_processed_image()
            self.status_var.set("Applied: Rotate 270°")
    
    def flip_horizontal(self):
        if self.processed_image:
            self.processed_image = ImageOps.mirror(self.processed_image)
            self.display_processed_image()
            self.status_var.set("Applied: Horizontal Flip")
    
    def flip_vertical(self):
        if self.processed_image:
            self.processed_image = ImageOps.flip(self.processed_image)
            self.display_processed_image()
            self.status_var.set("Applied: Vertical Flip")

def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()