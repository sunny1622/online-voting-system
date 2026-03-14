import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class Theme:
    # Color palette - Modern Blue and Emerald theme
    PRIMARY = "#1A237E"  # Deep Indigo
    SECONDARY = "#00695C"  # Deep Teal
    ACCENT = "#FF6F00"  # Amber
    SUCCESS = "#00C853"  # Emerald
    WARNING = "#FFD600"  # Amber
    ERROR = "#D50000"  # Deep Red
    BACKGROUND = "#FAFAFA"  # Off White
    TEXT = "#1A237E"  # Deep Indigo
    WHITE = "#FFFFFF"
    
    # Font configurations
    TITLE_FONT = ('Segoe UI', 20, 'bold')
    HEADER_FONT = ('Segoe UI', 14, 'bold')
    NORMAL_FONT = ('Segoe UI', 10)
    BUTTON_FONT = ('Segoe UI', 10, 'bold')
    
    @staticmethod
    def apply_theme(root):
        style = ttk.Style()
        
        # Configure the theme
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background=Theme.BACKGROUND)
        style.configure('TLabel', background=Theme.BACKGROUND, foreground=Theme.TEXT, font=Theme.NORMAL_FONT)
        style.configure('TButton', 
                       background=Theme.SECONDARY,
                       foreground=Theme.WHITE,
                       font=Theme.BUTTON_FONT,
                       padding=12)
        style.configure('Title.TLabel', 
                       font=Theme.TITLE_FONT,
                       foreground=Theme.PRIMARY)
        style.configure('Header.TLabel', 
                       font=Theme.HEADER_FONT,
                       foreground=Theme.PRIMARY)
        
        # Configure Treeview
        style.configure('Treeview',
                       background=Theme.WHITE,
                       foreground=Theme.TEXT,
                       fieldbackground=Theme.WHITE,
                       font=Theme.NORMAL_FONT,
                       rowheight=30)
        style.configure('Treeview.Heading',
                       background=Theme.PRIMARY,
                       foreground=Theme.WHITE,
                       font=Theme.BUTTON_FONT,
                       padding=5)
        
        # Add hover effect for Treeview heading
        style.map('Treeview.Heading',
                 background=[('active', '#0C1954')],
                 foreground=[('active', Theme.WHITE)])
        
        # Configure LabelFrame
        style.configure('TLabelframe', 
                       background=Theme.BACKGROUND,
                       foreground=Theme.TEXT)
        style.configure('TLabelframe.Label', 
                       background=Theme.BACKGROUND,
                       foreground=Theme.PRIMARY,
                       font=Theme.HEADER_FONT)
        
        # Configure Entry
        style.configure('TEntry',
                       fieldbackground=Theme.WHITE,
                       foreground=Theme.TEXT,
                       font=Theme.NORMAL_FONT,
                       padding=5)
        
        # Configure Notebook
        style.configure('TNotebook',
                       background=Theme.BACKGROUND)
        style.configure('TNotebook.Tab',
                       background=Theme.PRIMARY,
                       foreground=Theme.WHITE,
                       padding=[15, 5],
                       font=Theme.BUTTON_FONT)
        
        # Configure root window
        root.configure(bg=Theme.BACKGROUND)
        
        # Configure custom button styles
        style.configure('Primary.TButton',
                       background=Theme.PRIMARY,
                       foreground=Theme.WHITE)
        style.configure('Success.TButton',
                       background=Theme.SUCCESS,
                       foreground=Theme.WHITE)
        style.configure('Warning.TButton',
                       background=Theme.WARNING,
                       foreground=Theme.TEXT)
        style.configure('Error.TButton',
                       background=Theme.ERROR,
                       foreground=Theme.WHITE)
        
        # Configure disabled states
        style.map('TButton',
                 background=[('disabled', Theme.BACKGROUND)],
                 foreground=[('disabled', Theme.TEXT)])
        
        # Configure hover effects
        style.map('TButton',
                 background=[('active', Theme.ACCENT)],
                 foreground=[('active', Theme.WHITE)])
        
        # Configure Treeview selection with image support
        style.map('Treeview',
                 background=[('selected', Theme.SECONDARY)],
                 foreground=[('selected', Theme.WHITE)])
        
        # Configure Treeview cell padding for images
        style.layout('Treeview', [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])
        
        # Configure Candidate Card style
        style.configure('Candidate.TFrame',
                       background='#F5F5F5',
                       relief='solid',
                       borderwidth=1) 