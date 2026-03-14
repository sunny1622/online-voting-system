import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
import pandas as pd
from tkinter import filedialog
from theme import Theme
import shutil
import os
from datetime import datetime
from PIL import Image, ImageTk

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel - Online Voting System")
        self.db = Database()
        
        # Define available posts
        self.available_posts = [
            "President",
            "Vice President",
            "General Secretary",
            "Joint Secretary",
            "Treasurer",
            "Cultural Secretary",
            "Sports Secretary"
        ]
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create tabs
        self.tab_control = ttk.Notebook(self.main_frame)
        self.tab_control.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Candidates tab
        self.candidates_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.candidates_tab, text='Candidates')
        self.setup_candidates_tab()
        
        # Voters tab
        self.voters_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.voters_tab, text='Voters')
        self.setup_voters_tab()
        
        # Results tab
        self.results_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.results_tab, text='Results')
        self.setup_results_tab()
        
        # Session Control tab
        self.session_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.session_tab, text='Session Control')
        self.setup_session_tab()
        
        self.tab_control.pack(expand=1, fill="both")

    def setup_candidates_tab(self):
        # Configure grid weights for candidates tab
        self.candidates_tab.grid_rowconfigure(1, weight=1)
        self.candidates_tab.grid_columnconfigure(0, weight=1)
        
        # Add Candidate Section
        add_frame = ttk.LabelFrame(self.candidates_tab, text="Add New Candidate", padding="20")
        add_frame.grid(row=0, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))
        
        # Configure grid weights for add frame
        add_frame.grid_columnconfigure(1, weight=1)
        add_frame.grid_columnconfigure(3, weight=1)
        
        # Name field
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(add_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Post field (now a dropdown)
        ttk.Label(add_frame, text="Post:").grid(row=0, column=2, padx=5, pady=5)
        self.post_var = tk.StringVar()
        self.post_dropdown = ttk.Combobox(add_frame, textvariable=self.post_var, values=self.available_posts, width=27, state="readonly")
        self.post_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.post_dropdown.set(self.available_posts[0])  # Set default value
        
        # Photo upload
        ttk.Label(add_frame, text="Photo:").grid(row=1, column=0, padx=5, pady=5)
        self.photo_path = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.photo_path, width=30).grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(add_frame, text="Browse Photo", 
                  command=lambda: self.browse_image(self.photo_path)).grid(row=1, column=2, padx=5, pady=5)
        
        # Symbol upload
        ttk.Label(add_frame, text="Symbol:").grid(row=2, column=0, padx=5, pady=5)
        self.symbol_path = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.symbol_path, width=30).grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(add_frame, text="Browse Symbol", 
                  command=lambda: self.browse_image(self.symbol_path)).grid(row=2, column=2, padx=5, pady=5)
        
        # Add button
        ttk.Button(add_frame, text="Add Candidate", 
                  style='Success.TButton',
                  command=self.add_candidate).grid(row=3, column=0, columnspan=4, pady=10)
        
        # Candidates List Section
        list_frame = ttk.LabelFrame(self.candidates_tab, text="Candidates List", padding="20")
        list_frame.grid(row=1, column=0, padx=20, pady=20, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for list frame
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Create Treeview with image column
        columns = ('ID', 'Name', 'Post', 'Votes')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=10)
        
        # Set column headings and widths
        self.tree.heading('#0', text='Photo')  # First column for image
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Post', text='Post')
        self.tree.heading('Votes', text='Votes')
        
        self.tree.column('#0', width=80, minwidth=80, anchor='center')  # Increased width for image column
        self.tree.column('ID', width=50, minwidth=50, anchor='center')
        self.tree.column('Name', width=150, minwidth=150)
        self.tree.column('Post', width=150, minwidth=150)
        self.tree.column('Votes', width=80, minwidth=80, anchor='center')
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons for edit and delete
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(btn_frame, text="Edit Selected", 
                  style='Primary.TButton',
                  command=self.edit_candidate).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", 
                  style='Error.TButton',
                  command=self.delete_candidate).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh List", 
                  style='Warning.TButton',
                  command=self.refresh_candidates).pack(side=tk.LEFT, padx=5)
        
        self.refresh_candidates()

    def setup_voters_tab(self):
        # Configure grid weights for voters tab
        self.voters_tab.grid_rowconfigure(0, weight=1)
        self.voters_tab.grid_columnconfigure(0, weight=1)
        
        # Voters List Section
        list_frame = ttk.LabelFrame(self.voters_tab, text="Registered Voters", padding="20")
        list_frame.grid(row=0, column=0, padx=20, pady=20, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for list frame
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Create Treeview
        columns = ('Voter ID', 'Name', 'Email', 'Has Voted')
        self.voters_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        # Set column headings and widths
        self.voters_tree.heading('Voter ID', text='Voter ID')
        self.voters_tree.heading('Name', text='Name')
        self.voters_tree.heading('Email', text='Email')
        self.voters_tree.heading('Has Voted', text='Has Voted')
        
        self.voters_tree.column('Voter ID', width=100, anchor='center')
        self.voters_tree.column('Name', width=200)
        self.voters_tree.column('Email', width=250)
        self.voters_tree.column('Has Voted', width=100, anchor='center')
        
        self.voters_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.voters_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.voters_tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons for edit and delete
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(btn_frame, text="Delete Selected", 
                  style='Error.TButton',
                  command=self.delete_voter).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh List", 
                  style='Warning.TButton',
                  command=self.refresh_voters).pack(side=tk.LEFT, padx=5)
        
        self.refresh_voters()

    def setup_results_tab(self):
        # Configure grid weights for results tab
        self.results_tab.grid_rowconfigure(0, weight=1)
        self.results_tab.grid_columnconfigure(0, weight=1)
        
        # Results display
        results_frame = ttk.LabelFrame(self.results_tab, text="Voting Results", padding="20")
        results_frame.grid(row=0, column=0, padx=20, pady=20, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for results frame
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Create Treeview for results
        columns = ('ID', 'Name', 'Post', 'Votes')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='tree headings', height=15)
        
        # Set column headings and widths
        self.results_tree.heading('#0', text='Photo')
        self.results_tree.heading('ID', text='ID')
        self.results_tree.heading('Name', text='Name')
        self.results_tree.heading('Post', text='Post')
        self.results_tree.heading('Votes', text='Votes')
        
        self.results_tree.column('#0', width=80, minwidth=80, anchor='center')  # Increased width for image column
        self.results_tree.column('ID', width=50, minwidth=50, anchor='center')
        self.results_tree.column('Name', width=150, minwidth=150)
        self.results_tree.column('Post', width=150, minwidth=150)
        self.results_tree.column('Votes', width=80, minwidth=80, anchor='center')
        
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons
        btn_frame = ttk.Frame(results_frame)
        btn_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(btn_frame, text="Refresh Results", 
                  style='Primary.TButton',
                  command=self.refresh_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export Results", 
                  style='Success.TButton',
                  command=self.export_results).pack(side=tk.LEFT, padx=5)
        
        self.refresh_results()

    def setup_session_tab(self):
        # Configure grid weights for session tab
        self.session_tab.grid_rowconfigure(1, weight=1)
        self.session_tab.grid_columnconfigure(0, weight=1)
        
        # Session Control Frame
        control_frame = ttk.LabelFrame(self.session_tab, text="Voting Session Control", padding="20")
        control_frame.grid(row=0, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))
        
        # Configure grid weights for control frame
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)
        
        # Status display
        self.status_label = ttk.Label(control_frame, text="Current Status: Checking...", style='Header.TLabel')
        self.status_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Buttons
        self.start_button = ttk.Button(control_frame, text="Start Voting Session", 
                                     style='Success.TButton',
                                     command=self.start_voting)
        self.start_button.grid(row=1, column=0, padx=5, pady=10, sticky=(tk.W, tk.E))
        
        self.end_button = ttk.Button(control_frame, text="End Voting Session", 
                                   style='Error.TButton',
                                   command=self.end_voting)
        self.end_button.grid(row=1, column=1, padx=5, pady=10, sticky=(tk.W, tk.E))
        
        # Session Info Frame
        info_frame = ttk.LabelFrame(self.session_tab, text="Session Information", padding="20")
        info_frame.grid(row=1, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))
        
        self.start_time_label = ttk.Label(info_frame, text="Start Time: Not started")
        self.start_time_label.grid(row=0, column=0, pady=5)
        
        self.end_time_label = ttk.Label(info_frame, text="End Time: Not ended")
        self.end_time_label.grid(row=1, column=0, pady=5)
        
        # Refresh button
        ttk.Button(info_frame, text="Refresh Status", 
                  style='Primary.TButton',
                  command=self.refresh_session_status).grid(row=2, column=0, pady=10)
        
        # Initial status refresh
        self.refresh_session_status()

    def refresh_session_status(self):
        status = self.db.get_voting_status()
        self.status_label.config(text=f"Current Status: {status.upper()}")
        
        # Update button states
        self.start_button.config(state='normal' if status == 'not_started' else 'disabled')
        self.end_button.config(state='normal' if status == 'active' else 'disabled')
        
        # Update session info
        df = pd.read_excel(self.db.session_file)
        start_time = df.iloc[0]['start_time']
        end_time = df.iloc[0]['end_time']
        
        self.start_time_label.config(text=f"Start Time: {start_time if pd.notna(start_time) else 'Not started'}")
        self.end_time_label.config(text=f"End Time: {end_time if pd.notna(end_time) else 'Not ended'}")

    def start_voting(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to start the voting session?"):
            self.db.start_voting_session()
            self.refresh_session_status()
            messagebox.showinfo("Success", "Voting session has started!")

    def end_voting(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to end the voting session?"):
            self.db.end_voting_session()
            self.refresh_session_status()
            messagebox.showinfo("Success", "Voting session has ended!")

    def browse_image(self, path_var):
        filename = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        if filename:
            path_var.set(filename)

    def add_candidate(self):
        name = self.name_entry.get().strip()
        post = self.post_var.get()
        photo_path = self.photo_path.get()
        symbol_path = self.symbol_path.get()
        
        if not all([name, post, photo_path, symbol_path]):
            messagebox.showerror("Error", "Please fill in all fields and upload both images")
            return
        
        # Create images directory if it doesn't exist
        if not os.path.exists("images"):
            os.makedirs("images")
        
        # Generate unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_filename = f"photo_{timestamp}.{photo_path.split('.')[-1]}"
        symbol_filename = f"symbol_{timestamp}.{symbol_path.split('.')[-1]}"
        
        # Copy files
        photo_dest = os.path.join("images", photo_filename)
        symbol_dest = os.path.join("images", symbol_filename)
        shutil.copy2(photo_path, photo_dest)
        shutil.copy2(symbol_path, symbol_dest)
        
        # Add to database with image paths
        self.db.add_candidate(name, post, photo_dest, symbol_dest)
        self.refresh_candidates()
        
        # Clear fields
        self.name_entry.delete(0, tk.END)
        self.post_var.set(self.available_posts[0])
        self.photo_path.set("")
        self.symbol_path.set("")
        
        messagebox.showinfo("Success", "Candidate added successfully")

    def edit_candidate(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a candidate to edit")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        if not values:
            messagebox.showerror("Error", "Invalid candidate data")
            return
            
        candidate_id = values[0]  # ID is in the first column
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Candidate")
        edit_window.geometry("500x600")
        edit_window.configure(bg=Theme.BACKGROUND)
        
        # Make window modal
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Center the window
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x = (edit_window.winfo_screenwidth() // 2) - (width // 2)
        y = (edit_window.winfo_screenheight() // 2) - (height // 2)
        edit_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Main container
        main_frame = ttk.Frame(edit_window, padding="20", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        edit_window.grid_rowconfigure(0, weight=1)
        edit_window.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        ttk.Label(main_frame, text="Edit Candidate Information", 
                 style='Title.TLabel').grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Get current candidate data
        candidates_df = pd.read_excel(self.db.candidates_file)
        candidate_data = candidates_df[candidates_df['id'] == candidate_id]
        
        if candidate_data.empty:
            messagebox.showerror("Error", "Candidate not found in database")
            edit_window.destroy()
            return
            
        candidate = candidate_data.iloc[0]
        
        # Preview frame for current images
        preview_frame = ttk.LabelFrame(main_frame, text="Current Images", padding="10")
        preview_frame.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        try:
            # Load and resize current images
            photo_img = Image.open(candidate['photo_path'])
            photo_img = photo_img.resize((100, 100), Image.Resampling.LANCZOS)
            photo_tk = ImageTk.PhotoImage(photo_img)
            
            symbol_img = Image.open(candidate['symbol_path'])
            symbol_img = symbol_img.resize((100, 100), Image.Resampling.LANCZOS)
            symbol_tk = ImageTk.PhotoImage(symbol_img)
            
            # Display current images
            ttk.Label(preview_frame, text="Current Photo:").grid(row=0, column=0, padx=5)
            ttk.Label(preview_frame, image=photo_tk).grid(row=1, column=0, padx=5)
            preview_frame.photo = photo_tk  # Keep reference
            
            ttk.Label(preview_frame, text="Current Symbol:").grid(row=0, column=1, padx=5)
            ttk.Label(preview_frame, image=symbol_tk).grid(row=1, column=1, padx=5)
            preview_frame.symbol = symbol_tk  # Keep reference
            
        except Exception as e:
            print(f"Error loading preview images: {e}")
            ttk.Label(preview_frame, text="Error loading images").grid(row=0, column=0, columnspan=2)
        
        # Form fields
        # Name field
        ttk.Label(main_frame, text="Name:", style='Header.TLabel').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(main_frame, width=30)
        name_entry.insert(0, candidate['name'])
        name_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Post field (now a dropdown)
        ttk.Label(main_frame, text="Post:", style='Header.TLabel').grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        post_var = tk.StringVar()
        post_dropdown = ttk.Combobox(main_frame, textvariable=post_var, values=self.available_posts, width=27, state="readonly")
        post_dropdown.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        post_dropdown.set(candidate['post'])  # Set current post as default
        
        # Photo upload
        ttk.Label(main_frame, text="New Photo:", style='Header.TLabel').grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        photo_path = tk.StringVar(value=candidate['photo_path'])
        ttk.Entry(main_frame, textvariable=photo_path, width=30).grid(row=4, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Browse Photo", 
                  style='Primary.TButton',
                  command=lambda: self.browse_image(photo_path)).grid(row=4, column=2, padx=5, pady=5)
        
        # Symbol upload
        ttk.Label(main_frame, text="New Symbol:", style='Header.TLabel').grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        symbol_path = tk.StringVar(value=candidate['symbol_path'])
        ttk.Entry(main_frame, textvariable=symbol_path, width=30).grid(row=5, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Browse Symbol", 
                  style='Primary.TButton',
                  command=lambda: self.browse_image(symbol_path)).grid(row=5, column=2, padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        def save_changes():
            name = name_entry.get().strip()
            post = post_var.get()
            new_photo_path = photo_path.get()
            new_symbol_path = symbol_path.get()
            
            if not all([name, post, new_photo_path, new_symbol_path]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            # Copy new images if they've changed
            if new_photo_path != candidate['photo_path']:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                photo_filename = f"photo_{timestamp}.{new_photo_path.split('.')[-1]}"
                photo_dest = os.path.join("images", photo_filename)
                shutil.copy2(new_photo_path, photo_dest)
                new_photo_path = photo_dest
            
            if new_symbol_path != candidate['symbol_path']:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                symbol_filename = f"symbol_{timestamp}.{new_symbol_path.split('.')[-1]}"
                symbol_dest = os.path.join("images", symbol_filename)
                shutil.copy2(new_symbol_path, symbol_dest)
                new_symbol_path = symbol_dest
            
            try:
                # Update database with proper data types
                candidates_df = pd.read_excel(self.db.candidates_file)
                
                # Ensure proper data types
                candidates_df['id'] = candidates_df['id'].astype(int)
                candidates_df['votes'] = candidates_df['votes'].astype(int)
                candidates_df['name'] = candidates_df['name'].astype(str)
                candidates_df['post'] = candidates_df['post'].astype(str)
                candidates_df['photo_path'] = candidates_df['photo_path'].astype(str)
                candidates_df['symbol_path'] = candidates_df['symbol_path'].astype(str)
                
                # Update the candidate data
                mask = candidates_df['id'] == candidate_id
                candidates_df.loc[mask, 'name'] = name
                candidates_df.loc[mask, 'post'] = post
                candidates_df.loc[mask, 'photo_path'] = new_photo_path
                candidates_df.loc[mask, 'symbol_path'] = new_symbol_path
                
                # Save to Excel
                candidates_df.to_excel(self.db.candidates_file, index=False)
                
                self.refresh_candidates()
                edit_window.destroy()
                messagebox.showinfo("Success", "Candidate updated successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update candidate: {str(e)}")
        
        # Save and Cancel buttons
        ttk.Button(button_frame, text="Save Changes", 
                  style='Success.TButton',
                  command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  style='Error.TButton',
                  command=edit_window.destroy).pack(side=tk.LEFT, padx=5)

    def delete_candidate(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a candidate to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this candidate?"):
            item = self.tree.item(selected[0])
            candidate_id = item['values'][0]
            self.db.delete_candidate(candidate_id)
            self.refresh_candidates()
            self.refresh_results()
            messagebox.showinfo("Success", "Candidate deleted successfully")

    def refresh_candidates(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Store image references
        self.tree_images = []
        
        # Add candidates from database
        candidates = self.db.get_candidates()
        for _, row in candidates.iterrows():
            try:
                # Load and resize images to stamp size (30x30 pixels)
                photo_img = Image.open(row['photo_path'])
                photo_img = photo_img.resize((30, 30), Image.Resampling.LANCZOS)
                photo_tk = ImageTk.PhotoImage(photo_img)
                
                # Store reference to prevent garbage collection
                self.tree_images.append(photo_tk)
                
                # Insert with photo in first column
                item = self.tree.insert('', tk.END, image=photo_tk, values=(
                    row['id'],
                    row['name'],
                    row['post'],
                    row['votes']
                ))
                
            except Exception as e:
                print(f"Error loading image: {e}")
                # Fallback if image can't be loaded
                self.tree.insert('', tk.END, values=(
                    row['id'],
                    row['name'],
                    row['post'],
                    row['votes']
                ))

    def refresh_results(self):
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Store image references
        self.results_images = []
        
        # Add results from database
        results = self.db.get_results()
        for _, row in results.iterrows():
            try:
                # Load and resize images to stamp size (30x30 pixels)
                photo_img = Image.open(row['photo_path'])
                photo_img = photo_img.resize((30, 30), Image.Resampling.LANCZOS)
                photo_tk = ImageTk.PhotoImage(photo_img)
                
                # Store reference to prevent garbage collection
                self.results_images.append(photo_tk)
                
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

    def export_results(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            self.db.export_results(filename)
            messagebox.showinfo("Success", "Results exported successfully")

    def delete_voter(self):
        selected = self.voters_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a voter to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this voter?"):
            item = self.voters_tree.item(selected[0])
            voter_id = item['values'][0]
            self.db.delete_voter(voter_id)
            self.refresh_voters()
            messagebox.showinfo("Success", "Voter deleted successfully")

    def refresh_voters(self):
        try:
            # Clear existing items
            for item in self.voters_tree.get_children():
                self.voters_tree.delete(item)
            
            # Read both files
            voters_df = pd.read_excel(self.db.voters_file)
            reg_df = pd.read_excel(self.db.registration_file)
            
            # Convert voter_id to string in both dataframes
            voters_df['voter_id'] = voters_df['voter_id'].astype(str)
            reg_df['voter_id'] = reg_df['voter_id'].astype(str)
            
            # Merge the data
            for _, voter in voters_df.iterrows():
                voter_id = str(voter['voter_id'])
                has_voted = "Yes" if voter['has_voted'] else "No"
                
                # Get registration details
                reg_data = reg_df[reg_df['voter_id'] == voter_id]
                if not reg_data.empty:
                    name = reg_data.iloc[0]['full_name']
                    email = reg_data.iloc[0]['email']
                else:
                    name = "N/A"
                    email = "N/A"
                
                self.voters_tree.insert('', tk.END, values=(
                    voter_id,
                    name,
                    email,
                    has_voted
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load voter data: {str(e)}")