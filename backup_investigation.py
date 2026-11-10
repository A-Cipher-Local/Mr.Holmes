import os
import shutil
from datetime import datetime

DB_PATH = "GUI/Database/osint_intelligence.db"
REPORTS_DIR = "GUI/Reports"
BACKUP_DIR = "GUI/Backups"

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    zip_filename = os.path.join(BACKUP_DIR, f"osint_investigation_backup_{timestamp}")
    
    print(f"[*] Preparing backup archive...")
    
    # Create a temporary staging folder for the archive contents
    staging_dir = f"temp_backup_{timestamp}"
    os.makedirs(staging_dir, exist_ok=True)
    
    # Copy database if it exists
    if os.path.exists(DB_PATH):
        db_dest_dir = os.path.join(staging_dir, "GUI", "Database")
        os.makedirs(db_dest_dir, exist_ok=True)
        shutil.copy2(DB_PATH, db_dest_dir)
        print(f"[+] Included database: {DB_PATH}")
    else:
        print(f"[-] Warning: Database not found at {DB_PATH}")

    # Copy reports directory if it exists
    if os.path.exists(REPORTS_DIR):
        reports_dest = os.path.join(staging_dir, "GUI", "Reports")
        shutil.copytree(REPORTS_DIR, reports_dest)
        print(f"[+] Included reports directory: {REPORTS_DIR}")
    else:
        print(f"[-] Warning: Reports directory not found at {REPORTS_DIR}")

    # Create zip archive
    shutil.make_archive(zip_filename, 'zip', staging_dir)
    
    # Cleanup staging directory
    shutil.rmtree(staging_dir)
    
    final_zip_path = f"{zip_filename}.zip"
    print(f"\n[+] Backup successfully created: {final_zip_path}")

if __name__ == "__main__":
    main()
