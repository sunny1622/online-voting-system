import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from theme import Theme
from PIL import Image, ImageTk
import os

class VoterInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Voter Interface - Online Voting System")
        self.db = Database()
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create menu bar
        self.create_menu()
        
        # Initially show login frame
        self.show_login_frame()

    def create_menu(self):
        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Create Home menu item
        self.menu_bar.add_command(label="Home", command=self.show_home_frame)

    def show_login_frame(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create login frame
        login_frame = ttk.LabelFrame(self.main_frame, text="Voter Login", padding="120")
        login_frame.grid(row=0, column=0, padx=130, pady=50)
        
        # Configure grid weights for login frame
        login_frame.grid_columnconfigure(1, weight=1)
        
        # Voter ID
        ttk.Label(login_frame, text="Voter ID:").grid(row=0, column=0, padx=3, pady=2)
        self.voter_id_entry = ttk.Entry(login_frame, width=20)
        self.voter_id_entry.grid(row=0, column=1, padx=3, pady=2, sticky=(tk.W, tk.E))

        # Add validation for numbers only
        vcmd = (self.root.register(self.validate_number), '%P')
        self.voter_id_entry.config(validate='key', validatecommand=vcmd)
        
        # Password
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=3, pady=2)
        self.password_entry = ttk.Entry(login_frame, show="•", width=20)
        self.password_entry.grid(row=1, column=1, padx=3, pady=2, sticky=(tk.W, tk.E))
        
        # Login button
        ttk.Button(login_frame, text="Login", 
                  style='Primary.TButton',
                  command=self.login).grid(row=2, column=0, columnspan=2, pady=8)
        
        # Registration link
        ttk.Button(login_frame, text="New Voter? Register Here", 
                  style='Success.TButton',
                  command=self.show_registration_frame).grid(row=3, column=0, columnspan=2, pady=3)
        
        # Center the login frame
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        login_frame.grid(row=0, column=0, sticky="nsew")

    def show_registration_frame(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create registration frame
        reg_frame = ttk.LabelFrame(self.main_frame, text="Voter Registration", padding="20")
        reg_frame.grid(row=0, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))
        
        # Configure grid weights for registration frame
        reg_frame.grid_columnconfigure(1, weight=1)
        
        # Name
        ttk.Label(reg_frame, text="Full Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(reg_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Email
        ttk.Label(reg_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(reg_frame, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Voter ID
        ttk.Label(reg_frame, text="Choose Voter ID:").grid(row=2, column=0, padx=5, pady=5)
        self.reg_voter_id_entry = ttk.Entry(reg_frame, width=30)
        self.reg_voter_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        # Add validation for numbers only
        vcmd = (self.root.register(self.validate_number), '%P')
        self.reg_voter_id_entry.config(validate='key', validatecommand=vcmd)
        
        # Password
        ttk.Label(reg_frame, text="Password:").grid(row=3, column=0, padx=5, pady=5)
        self.reg_password_entry = ttk.Entry(reg_frame, show="•", width=30)
        self.reg_password_entry.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Confirm Password
        ttk.Label(reg_frame, text="Confirm Password:").grid(row=4, column=0, padx=5, pady=5)
        self.confirm_password_entry = ttk.Entry(reg_frame, show="•", width=30)
        self.confirm_password_entry.grid(row=4, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Register button
        ttk.Button(reg_frame, text="Register", 
                  style='Success.TButton',
                  command=self.register).grid(row=5, column=0, columnspan=2, pady=15)
        
        # Back to login button
        ttk.Button(reg_frame, text="Back to Login", 
                  style='Primary.TButton',
                  command=self.show_login_frame).grid(row=6, column=0, columnspan=2, pady=5)

    def show_home_frame(self):
        # Only show home if logged in
        if not hasattr(self, 'current_voter_id'):
            messagebox.showinfo("Info", "Please login first to view live results")
            return
            
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create home frame
        home_frame = ttk.LabelFrame(self.main_frame, text="Live Vote Counts", padding="20")
        home_frame.grid(row=0, column=0, padx=20, pady=20, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for home frame
        home_frame.grid_rowconfigure(2, weight=1)
        home_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome message
        ttk.Label(home_frame, text=f"Welcome, Voter ID: {self.current_voter_id}", 
                 style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=10)
        
        # Voting status message
        status = self.db.get_voting_status()
        status_frame = ttk.Frame(home_frame)
        status_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        if status == 'not_started':
            ttk.Label(status_frame, text="Voting has not started yet. Please wait for the admin to begin the session.", 
                     foreground=Theme.WARNING).grid(row=0, column=0, pady=5)
        elif status == 'ended':
            ttk.Label(status_frame, text="Voting has ended. Thank you for your participation!", 
                     foreground=Theme.ERROR).grid(row=0, column=0, pady=5)
        
        # Create Treeview for results
        columns = ('ID', 'Name', 'Post', 'Votes')
        self.results_tree = ttk.Treeview(home_frame, columns=columns, show='tree headings', height=10)
        
        # Set column headings
        self.results_tree.heading('#0', text='Photo')  # First column for image
        for col in columns:
            self.results_tree.heading(col, text=col)
        
        # Set column widths with minimum widths
        self.results_tree.column('#0', width=80, minwidth=80, anchor='center')  # Increased width for image column
        self.results_tree.column('ID', width=50, minwidth=50, anchor='center')
        self.results_tree.column('Name', width=150, minwidth=150)
        self.results_tree.column('Post', width=150, minwidth=150)
        self.results_tree.column('Votes', width=80, minwidth=80, anchor='center')
        
        self.results_tree.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(home_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Refresh button
        ttk.Button(home_frame, text="Refresh Results", 
                  style='Primary.TButton',
                  command=self.refresh_results).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Navigation buttons
        button_frame = ttk.Frame(home_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Only show Cast Vote button if voting is active and hasn't voted
        if status == 'active':
            has_voted = self.db.has_voted(self.current_voter_id)
            if not has_voted:
                ttk.Button(button_frame, text="Cast Vote", 
                          style='Success.TButton',
                          command=self.show_voting_frame).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Logout", 
                  style='Error.TButton',
                  command=self.logout).grid(row=0, column=1, padx=5)
        
        # Load initial results
        self.refresh_results()

    def show_voting_frame(self):
        # Check if voting is active
        if not self.db.can_vote():
            messagebox.showerror("Error", "Voting is not currently active")
            self.show_home_frame()
            return
            
        # Check if already voted
        if self.db.has_voted(self.current_voter_id):
            messagebox.showinfo("Info", "You have already cast your vote.")
            self.show_home_frame()
            return
            
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create main container frame that extends full width
        main_container = ttk.Frame(self.main_frame, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for main frame and container
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(2, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Top frame for header and buttons
        top_frame = ttk.Frame(main_container)
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        top_frame.grid_columnconfigure(1, weight=1)
        
        # Welcome message
        ttk.Label(top_frame, text=f"Welcome, Voter ID: {self.current_voter_id}", 
                 style='Header.TLabel').grid(row=0, column=0, padx=5)
        
        # Refresh button
        ttk.Button(top_frame, text="Refresh", 
                  style='Primary.TButton',
                  command=self.refresh_vote_counts).grid(row=0, column=2, padx=5)
        
        # Instructions
        ttk.Label(main_container, text="Please select your preferred candidate:", 
                 style='Header.TLabel').grid(row=1, column=0, pady=(0, 10))
        
        # Create canvas and scrollbar for candidates
        canvas = tk.Canvas(main_container, bg=Theme.BACKGROUND)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding="10", style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Grid the canvas and scrollbar
        canvas.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")
        
        # Configure scrollable frame to expand horizontally
        scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Get candidates
        candidates = self.db.get_candidates()
        
        # Create a frame for each candidate
        for idx, (_, row) in enumerate(candidates.iterrows()):
            # Create candidate card frame with consistent padding
            candidate_frame = ttk.Frame(scrollable_frame, style='Candidate.TFrame', padding="20")
            candidate_frame.grid(row=idx, column=0, pady=10, sticky="ew", padx=5)
            
            # Configure grid weights for candidate frame
            candidate_frame.grid_columnconfigure(2, weight=1)
            candidate_frame.grid_columnconfigure(3, weight=1)
            
            # Load and resize images
            try:
                # Load and resize photo
                photo_img = Image.open(row['photo_path'])
                photo_img = photo_img.resize((120, 120), Image.Resampling.LANCZOS)
                photo_tk = ImageTk.PhotoImage(photo_img)
                
                # Load and resize symbol
                symbol_img = Image.open(row['symbol_path'])
                symbol_img = symbol_img.resize((80, 80), Image.Resampling.LANCZOS)
                symbol_tk = ImageTk.PhotoImage(symbol_img)
                
                # Create labels for images
                photo_label = ttk.Label(candidate_frame, image=photo_tk)
                photo_label.image = photo_tk  # Keep a reference
                photo_label.grid(row=0, column=0, rowspan=2, padx=15)
                
                symbol_label = ttk.Label(candidate_frame, image=symbol_tk)
                symbol_label.image = symbol_tk  # Keep a reference
                symbol_label.grid(row=0, column=1, padx=15)
                
            except Exception as e:
                print(f"Error loading images: {e}")
                # Fallback if images can't be loaded
                ttk.Label(candidate_frame, text="[Photo]").grid(row=0, column=0, padx=15)
                ttk.Label(candidate_frame, text="[Symbol]").grid(row=0, column=1, padx=15)
            
            # Candidate info frame
            info_frame = ttk.Frame(candidate_frame)
            info_frame.grid(row=0, column=2, sticky="ew", padx=15)
            
            # Candidate info
            ttk.Label(info_frame, text=row['name'], 
                     style='Header.TLabel').grid(row=0, column=0, sticky="w")
            ttk.Label(info_frame, text=f"Post: {row['post']}").grid(row=1, column=0, sticky="w")
            
            # Vote count
            vote_label = ttk.Label(info_frame, text=f"Current Votes: {row['votes']}", 
                                 style='Header.TLabel')
            vote_label.grid(row=2, column=0, sticky="w")
            
            # Store reference to vote label for updating
            candidate_frame.vote_label = vote_label
            
            # Select button
            ttk.Button(candidate_frame, text="Vote for this Candidate", 
                      style='Success.TButton',
                      command=lambda cid=row['id']: self.select_candidate(cid)).grid(row=0, column=3, padx=15, sticky="e")
        
        # Bottom button frame
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=3, column=0, pady=10)
        
        ttk.Button(button_frame, text="View Results", 
                  style='Primary.TButton',
                  command=self.show_home_frame).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Logout", 
                  style='Error.TButton',
                  command=self.logout).grid(row=0, column=1, padx=5)
        
        # Start auto-refresh for live vote count
        self.start_vote_refresh()
        
        # Bind resize event to update canvas width
        def update_canvas_width(event):
            canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
        
        main_container.bind('<Configure>', update_canvas_width)

    def start_vote_refresh(self):
        self.refresh_vote_counts()
        self.root.after(5000, self.start_vote_refresh)

    def refresh_vote_counts(self):
        candidates = self.db.get_candidates()
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Canvas):
                        for frame in child.winfo_children():
                            if isinstance(frame, ttk.Frame):
                                for label in frame.winfo_children():
                                    if isinstance(label, ttk.Label) and "Current Votes:" in label.cget("text"):
                                        # Find corresponding candidate
                                        for _, row in candidates.iterrows():
                                            if row['name'] in frame.winfo_children()[2].cget("text"):
                                                label.configure(text=f"Current Votes: {row['votes']}")
                                                break

    def select_candidate(self, candidate_id):
        """Handle candidate selection"""
        if messagebox.askyesno("Confirm", "Are you sure you want to cast your vote for this candidate?\n\nNote: You cannot change your vote after submission."):
            if self.db.record_vote(self.current_voter_id, candidate_id):
                messagebox.showinfo("Success", "Your vote has been recorded successfully!\nThank you for participating in the election.")
                self.show_home_frame()
            else:
                messagebox.showerror("Error", "Failed to record your vote. Please try again.")

    def login(self):
        voter_id = self.voter_id_entry.get().strip()
        password = self.password_entry.get()
        
        if not voter_id or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Validate voter ID is integer
        try:
            voter_id = int(voter_id)
        except ValueError:
            messagebox.showerror("Error", "Voter ID must be a number")
            return
        
        # Verify voter and password
        if self.db.verify_voter(str(voter_id), password):
            self.current_voter_id = str(voter_id)
            
            # Check voting status
            status = self.db.get_voting_status()
            has_voted = self.db.has_voted(str(voter_id))
            
            if status == 'active' and not has_voted:
                # Show voting page directly if voting is active and hasn't voted
                self.show_voting_frame()
            elif has_voted:
                messagebox.showinfo("Info", "You have already cast your vote.")
                self.show_home_frame()
            elif status == 'not_started':
                messagebox.showinfo("Info", "Voting has not started yet. Please wait for the admin to begin the session.")
                self.show_home_frame()
            elif status == 'ended':
                messagebox.showinfo("Info", "Voting has ended. Thank you for your participation!")
                self.show_home_frame()
        else:
            messagebox.showerror("Error", "Invalid voter ID or password")
            # Clear password field
            self.password_entry.delete(0, tk.END)

    def logout(self):
        self.current_voter_id = None
        self.show_login_frame()

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        voter_id = self.reg_voter_id_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validate inputs
        if not all([name, email, voter_id, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        # Validate voter ID is integer
        try:
            voter_id = int(voter_id)
        except ValueError:
            messagebox.showerror("Error", "Voter ID must be a number")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Add voter to database
        if self.db.add_voter(str(voter_id), password, name, email):
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            # Clear all fields
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.reg_voter_id_entry.delete(0, tk.END)
            self.reg_password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            self.show_login_frame()
        else:
            messagebox.showerror("Error", "Voter ID already exists. Please choose a different one.")

    def refresh_results(self):
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Store image references
        self.tree_images = []
        
        # Get latest results
        results = self.db.get_results()
        for _, row in results.iterrows():
            try:
                # Load and resize images to stamp size (30x30 pixels)
                photo_img = Image.open(row['photo_path'])
                photo_img = photo_img.resize((30, 30), Image.Resampling.LANCZOS)
                photo_tk = ImageTk.PhotoImage(photo_img)
                
                # Store reference to prevent garbage collection
                self.tree_images.append(photo_tk)
                
                # Insert with photo in first column
                item = self.results_tree.insert('', tk.END, image=photo_tk, values=(
                    row['id'],
                    row['name'],
                    row['post'],
                    row['votes']
                ))
                
            except Exception as e:
                print(f"Error loading image: {e}")
                # Fallback if image can't be loaded
                self.results_tree.insert('', tk.END, values=(
                    row['id'],
                    row['name'],
                    row['post'],
                    row['votes']
                ))

    def validate_number(self, value):
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False 