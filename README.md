# Dah Assistant SAI Flask Dashboard

## Quick Start

1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**  
   ```bash
   python app.py
   ```

3. **Access the dashboard**  
   Open [http://localhost:5000](http://localhost:5000) in your browser.

## Default Credentials

- Username: `admin`
- Password: `password123`

## Deployment

For production, set a secure `app.secret_key`, use a proper WSGI server, and configure environment variables.

## File Structure

```
app.py
requirements.txt
templates/
    base.html
    login.html
    dashboard.html
.gitignore
README.md
```