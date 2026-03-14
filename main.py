import tkinter as tk
from tkinter import ttk, messagebox
from admin_panel import AdminPanel
from voter_interface import VoterInterface
from theme import Theme

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Voting System")
        
        # Set window size
        window_width = 600
        window_height = 500
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position for center of screen
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.root.minsize(window_width, window_height)  # Set minimum window size
        
        # Apply theme
        Theme.apply_theme(root)
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome message
        ttk.Label(
            self.main_frame,
            text="Welcome to Online Voting System",
            style='Title.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Description
        ttk.Label(
            self.main_frame,
            text="A secure and efficient way to conduct elections",
            style='Header.TLabel'
        ).grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Admin login section
        admin_frame = ttk.LabelFrame(self.main_frame, text="Admin Access", padding="15")
        admin_frame.grid(row=2, column=0, padx=20, pady=10, sticky=(tk.W, tk.E))
        
        # Configure grid weights for admin frame
        admin_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(admin_frame, text="Password:").grid(row=0, column=0, padx=5, pady=5)
        self.admin_password = ttk.Entry(admin_frame, show="•", width=25)
        self.admin_password.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(
            admin_frame,
            text="Login as Admin",
            style='Primary.TButton',
            command=self.admin_login
        ).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Voter section
        voter_frame = ttk.LabelFrame(self.main_frame, text="Voter Access", padding="5")
        voter_frame.grid(row=3, column=0, padx=20, sticky=(tk.W, tk.E))
        
        ttk.Button(
            voter_frame,
            text="Enter as Voter",
            style='Success.TButton',
            command=self.open_voter_interface
        ).grid(row=0, column=0, pady=10)
        
        # Footer
        ttk.Label(
            self.main_frame,
            text="© 2025 Online Voting System",
            style='TLabel'
        ).grid(row=4, column=0, columnspan=2, pady=(20, 0))

    def admin_login(self):
        if self.admin_password.get() == "admin123":
            self.root.withdraw()
            admin_window = tk.Toplevel()
            
            # Set window size
            window_width = 1000
            window_height = 700
            
            # Get screen dimensions
            screen_width = admin_window.winfo_screenwidth()
            screen_height = admin_window.winfo_screenheight()
            
            # Calculate position for center of screen
            center_x = int(screen_width/2 - window_width/2)
            center_y = int(screen_height/2 - window_height/2)
            
            # Set window size and position
            admin_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
            admin_window.minsize(window_width, window_height)  # Set minimum window size
            
            Theme.apply_theme(admin_window)
            AdminPanel(admin_window)
            admin_window.protocol("WM_DELETE_WINDOW", lambda: self.on_admin_close(admin_window))
            
            # Clear password field
            self.admin_password.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid admin password")
            # Clear password field on failed attempt
            self.admin_password.delete(0, tk.END)

    def open_voter_interface(self):
        self.root.withdraw()
        voter_window = tk.Toplevel()
        
        # Set window size
        window_width = 900
        window_height = 650
        
        # Get screen dimensions
        screen_width = voter_window.winfo_screenwidth()
        screen_height = voter_window.winfo_screenheight()
        
        # Calculate position for center of screen
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        # Set window size and position
        voter_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        voter_window.minsize(window_width, window_height)  # Set minimum window size
        
        Theme.apply_theme(voter_window)
        VoterInterface(voter_window)
        voter_window.protocol("WM_DELETE_WINDOW", lambda: self.on_voter_close(voter_window))

    def on_admin_close(self, window):
        window.destroy()
        self.root.deiconify()

    def on_voter_close(self, window):
        window.destroy()
        self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop() 