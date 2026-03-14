import pandas as pd
import os
import bcrypt
from datetime import datetime

class Database:
    def __init__(self):
        self.candidates_file = 'data/candidates.xlsx'
        self.voters_file = 'data/voters.xlsx'
        self.votes_file = 'data/votes.xlsx'
        self.registration_file = 'data/registration.xlsx'
        self.session_file = "data/session.xlsx"
        self.create_data_directory()
        self.initialize_files()
        self.migrate_data()

    def create_data_directory(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists('images'):
            os.makedirs('images')

    def initialize_files(self):
        # Initialize candidates file
        if not os.path.exists(self.candidates_file):
            df = pd.DataFrame(columns=['id', 'name', 'post', 'photo_path', 'symbol_path', 'votes'])
            df.to_excel(self.candidates_file, index=False)

        # Initialize voters file
        if not os.path.exists(self.voters_file):
            df = pd.DataFrame(columns=['voter_id', 'password_hash', 'has_voted'])
            df.to_excel(self.voters_file, index=False)

        # Initialize votes file
        if not os.path.exists(self.votes_file):
            df = pd.DataFrame(columns=['voter_id', 'candidate_id', 'timestamp'])
            df.to_excel(self.votes_file, index=False)

        # Initialize registration file
        if not os.path.exists(self.registration_file):
            df = pd.DataFrame(columns=['voter_id', 'full_name', 'email', 'registration_date'])
            df.to_excel(self.registration_file, index=False)

        # Initialize session file
        if not os.path.exists(self.session_file):
            df = pd.DataFrame(columns=['start_time', 'end_time'])
            df.loc[0] = [None, None]  # Add initial row with None values
            df.to_excel(self.session_file, index=False)
        else:
            # Ensure session file has at least one row
            df = pd.read_excel(self.session_file)
            if df.empty:
                df = pd.DataFrame(columns=['start_time', 'end_time'])
                df.loc[0] = [None, None]  # Add initial row with None values
                df.to_excel(self.session_file, index=False)

    def migrate_data(self):
        try:
            # Migrate candidates file
            if os.path.exists(self.candidates_file):
                df = pd.read_excel(self.candidates_file)
                if 'position' in df.columns and 'post' not in df.columns:
                    df = df.rename(columns={'position': 'post'})
                    df.to_excel(self.candidates_file, index=False)
        except Exception as e:
            print(f"Migration error: {e}")

    def add_candidate(self, name, post, photo_path, symbol_path):
        df = pd.read_excel(self.candidates_file)
        
        # Check if candidate already exists
        if len(df[df['name'] == name]) > 0:
            return False
        
        # Generate new ID
        new_id = 1 if len(df) == 0 else df['id'].max() + 1
        
        # Add new candidate
        new_row = pd.DataFrame({
            'id': [new_id],
            'name': [name],
            'post': [post],
            'photo_path': [photo_path],
            'symbol_path': [symbol_path],
            'votes': [0]
        })
        
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(self.candidates_file, index=False)
        return True

    def get_candidates(self):
        df = pd.read_excel(self.candidates_file)
        return df

    def update_candidate(self, candidate_id, name, post):
        df = pd.read_excel(self.candidates_file)
        mask = df['id'] == candidate_id
        df.loc[mask, 'name'] = name
        df.loc[mask, 'post'] = post
        df.to_excel(self.candidates_file, index=False)

    def delete_candidate(self, candidate_id):
        df = pd.read_excel(self.candidates_file)
        df = df[df['id'] != candidate_id]
        df.to_excel(self.candidates_file, index=False)

    def add_voter(self, voter_id, password, name, email):
        try:
            # Read existing data
            voters_df = pd.read_excel(self.voters_file)
            reg_df = pd.read_excel(self.registration_file)
            
            # Check if voter already exists
            if len(voters_df[voters_df['voter_id'] == voter_id]) > 0:
                return False
            
            # Hash the password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Add new voter to voters file
            new_voter = pd.DataFrame({
                'voter_id': [voter_id],
                'password_hash': [password_hash],
                'has_voted': [False]
            })
            voters_df = pd.concat([voters_df, new_voter], ignore_index=True)
            voters_df.to_excel(self.voters_file, index=False)
            
            # Add registration details
            new_reg = pd.DataFrame({
                'voter_id': [voter_id],
                'full_name': [name],
                'email': [email],
                'registration_date': [datetime.now()]
            })
            reg_df = pd.concat([reg_df, new_reg], ignore_index=True)
            reg_df.to_excel(self.registration_file, index=False)
            
            return True
            
        except Exception as e:
            return False

    def verify_voter(self, voter_id, password):
        try:
            # Read voters file
            voters_df = pd.read_excel(self.voters_file)
            
            # Convert voter_id to string for comparison
            voters_df['voter_id'] = voters_df['voter_id'].astype(str)
            
            # Find the voter
            voter = voters_df[voters_df['voter_id'] == str(voter_id)]
            
            if len(voter) == 0:
                return False
            
            # Get stored hash
            stored_hash = voter.iloc[0]['password_hash']
            
            if pd.isna(stored_hash):
                return False
            
            # Verify password
            try:
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
            except Exception as e:
                return False
            
        except Exception as e:
            return False

    def has_voted(self, voter_id):
        try:
            df = pd.read_excel(self.voters_file)
            
            # Convert voter_id to string for comparison
            df['voter_id'] = df['voter_id'].astype(str)
            voter_id = str(voter_id)
            
            voter = df[df['voter_id'] == voter_id]
            
            if len(voter) == 0:
                return False
                
            return voter.iloc[0]['has_voted']
            
        except Exception as e:
            return False

    def record_vote(self, voter_id, candidate_id):
        try:
            # Record vote
            votes_df = pd.read_excel(self.votes_file)
            new_vote = pd.DataFrame({
                'voter_id': [voter_id],
                'candidate_id': [candidate_id],
                'timestamp': [datetime.now()]
            })
            votes_df = pd.concat([votes_df, new_vote], ignore_index=True)
            votes_df.to_excel(self.votes_file, index=False)
            
            # Update candidate vote count
            candidates_df = pd.read_excel(self.candidates_file)
            candidates_df.loc[candidates_df['id'] == candidate_id, 'votes'] += 1
            candidates_df.to_excel(self.candidates_file, index=False)
            
            # Mark voter as voted
            voters_df = pd.read_excel(self.voters_file)
            voters_df['voter_id'] = voters_df['voter_id'].astype(str)
            voters_df.loc[voters_df['voter_id'] == str(voter_id), 'has_voted'] = True
            voters_df.to_excel(self.voters_file, index=False)
            
            return True
            
        except Exception as e:
            return False

    def get_results(self):
        return self.get_candidates()

    def export_results(self, filename):
        results = self.get_results()
        results.to_excel(filename, index=False)

    def delete_voter(self, voter_id):
        # Read voters file
        voters_df = pd.read_excel(self.voters_file)
        
        # Remove the voter
        voters_df = voters_df[voters_df['voter_id'] != voter_id]
        
        # Save back to file
        voters_df.to_excel(self.voters_file, index=False)
        
        # Also remove any votes cast by this voter
        votes_df = pd.read_excel(self.votes_file)
        votes_df = votes_df[votes_df['voter_id'] != voter_id]
        votes_df.to_excel(self.votes_file, index=False)

        # Remove from registration data
        reg_df = pd.read_excel(self.registration_file)
        reg_df = reg_df[reg_df['voter_id'] != voter_id]
        reg_df.to_excel(self.registration_file, index=False)

    def get_voting_status(self):
        try:
            df = pd.read_excel(self.session_file)
            if df.empty or pd.isna(df.iloc[0]['start_time']):
                return 'not_started'
            elif pd.isna(df.iloc[0]['end_time']):
                return 'active'
            else:
                return 'ended'
        except Exception as e:
            return 'not_started'

    def start_voting_session(self):
        try:
            df = pd.read_excel(self.session_file)
            # Clear any existing data
            df = pd.DataFrame(columns=['start_time', 'end_time'])
            # Set start time
            df.loc[0] = [datetime.now(), None]
            df.to_excel(self.session_file, index=False)
            return True
        except Exception as e:
            return False

    def end_voting_session(self):
        try:
            df = pd.read_excel(self.session_file)
            # Update end time
            df.loc[0, 'end_time'] = datetime.now()
            df.to_excel(self.session_file, index=False)
            return True
        except Exception as e:
            return False

    def can_vote(self):
        return self.get_voting_status() == 'active' 