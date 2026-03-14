# Online Voting System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

A robust, secure, and user-friendly online voting system designed for educational institutions and organizations. Built with Python and Tkinter, this application streamlines the process of conducting elections while maintaining transparency and security.

</div>

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Login Credentials](#login-credentials)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Data Management](#data-management)
- [Security Features](#security-features)
- [Contributing](#contributing)
- [License](#license)

## 📖 Overview

The Online Voting System is a comprehensive solution for institutions seeking to digitize their election process. Built with Python and utilizing Excel for data persistence, it offers a perfect balance between simplicity and functionality.

### Core Capabilities
- Multi-user role management (Admin/Voters)
- Dynamic candidate management
- Real-time vote counting
- Comprehensive results tracking
- Excel-based data persistence
- Secure authentication system

## ✨ Key Features

### 👨‍💼 Admin Dashboard
- **Candidate Management**
  - Add candidates with photos and symbols
  - Edit candidate information
  - Delete candidates
  - View candidate list
- **Voter Management**
  - View registered voters
  - Delete voters
  - Track voting status
- **Session Control**
  - Start voting session
  - End voting session
  - View session status
- **Results Management**
  - Live vote counting
  - Export results to Excel
  - View detailed results

### 👥 Voter Interface
- **Voting Process**
  - Secure voter registration
  - Easy login system
  - Cast vote with candidate photos
  - View live results
- **Status Tracking**
  - Check voting status
  - View personal voting history
  - Access election results

## 🔐 Login Credentials

### Admin Login
- Password: `admin123`
- Access: Admin Dashboard
- Features:
  - Candidate Management
  - Voter Management
  - Session Control
  - Results Management

### Voter Login
- Voters Name: voter1
- Voters ID: `1111`
- Password: `1111`
- Voters Name: voter2
- Voters ID: `2222`
- Password: `2222`
- Voters Name: voter3 (has_voted)
- Voters ID: `3333`
- Password: `3333`
- Access: Voter Interface
- Features:
  - Cast vote
  - View results
  - Check voting status

## 🏗 System Architecture

### Database Structure
The application utilizes a modular Excel-based storage system:

| File | Purpose | Key Components |
|------|---------|----------------|
| `candidates.xlsx` | Candidate Management | Candidate profiles, photos, symbols |
| `voters.xlsx` | Voter Management | Voter credentials, voting status |
| `votes.xlsx`| Vote Records | Vote data, timestamps |
| `registration.xlsx` | Voter Registration | Voter details, registration info |
| `session.xlsx` | Session Control | Session status, timestamps |

### Technical Stack
- Backend: `Python 3.x`
- GUI: `Tkinter`
- Data Storage: Excel (`openpyxl`)
- Image Processing: `Pillow` (PIL)
- Security: `bcrypt`

## 🚀 Installation

### Prerequisites
- `Python 3.x`
- pip (Python package manager)

### Setup Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/sabbirahmad12/online-voting-system.git
    cd online-voting-system
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python main.py
    ```

## 📊 Data Management

### Database Schema

#### Candidates Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique identifier |
| name | String | Candidate name |
| post | String | Position |
| photo_path | String | Photo location |
| symbol_path | String | Symbol location |
| votes | Integer | Vote count |

#### Voters Table
| Field | Type | Description |
|-------|------|-------------|
| voter_id | String | Unique identifier |
| password_hash | String | Encrypted password |
| has_voted | Boolean | Voting status |

## 🔒 Security Features

### Current Implementation
- Password hashing using bcrypt
- Secure session management
- One-time voting system
- Admin authentication
- Voter authentication
- Excel file data storage

### Recommended Enhancements
- Implement database encryption
- Add two-factor authentication
- Enable secure data backup
- Regular security audits
- Backup and recovery procedures

## 🤝 Contributing

We welcome contributions to enhance the Online Voting System. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write comprehensive tests
- Update documentation
- Maintain backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ for education
</div>