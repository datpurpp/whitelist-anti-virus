import os
import hashlib
import json
from pathlib import Path

# --- CONFIGURATION ---
TARGET_DIRECTORIES = [
    os.environ.get("ProgramFiles", r"C:\Program Files"),
    os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
    os.environ.get("ProgramData", r"C:\ProgramData"),  # Added ProgramData folder
    os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Default"), "AppData")
]

TARGET_EXTENSIONS = {'.exe', '.dll', '.sys', '.bat', '.cmd', '.vbs', '.ps1', '.scr', '.pif'}
SNAPSHOT_FILE = "trusted_system_snapshot.json"

def calculate_sha256(file_path):
    """Calculates the SHA-256 hash of a file, handling system and reparse point errors."""
    sha256_hash = hashlib.sha256()
    try:
        # Check if it's a symbolic link or Windows App Execution Alias reparse point
        if os.path.islink(file_path):
            return "VIRTUAL_SYSTEM_LINK"
            
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError):
        return "PERMISSION_DENIED"
    except OSError as e:
        # Catches Errno 22 (Invalid Argument) for Microsoft Store execution links
        if e.errno == 22:
            return "WINDOWS_APP_ALIAS"
        return f"ERROR_{e.errno}"

def scan_system():
    """Scans target directories and indexes all executable files and their hashes."""
    file_manifest = {}
    print("Scanning system directories... This may take a few moments.")
    
    for base_dir in TARGET_DIRECTORIES:
        if not os.path.exists(base_dir):
            continue
            
        for root, _, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    ext = os.path.splitext(file).lower()
                    if ext in TARGET_EXTENSIONS:
                        norm_path = os.path.normpath(file_path)
                        file_manifest[norm_path] = calculate_sha256(norm_path)
                except Exception:
                    # Keep going even if a single weird file breaks string processing
                    continue
                    
    return file_manifest

def save_snapshot(manifest):
    """Saves the scanned system state as your trusted baseline."""
    with open(SNAPSHOT_FILE, 'w') as f:
        json.dump(manifest, f, indent=4)
    print(f"\n[+] Success! Trusted baseline saved with {len(manifest)} files indexed.")
    print(f"Keep '{SNAPSHOT_FILE}' safe. Run this script again to verify integrity.")

def verify_system(current_scan):
    """Compares the current system state against your trusted baseline."""
    with open(SNAPSHOT_FILE, 'r') as f:
        baseline = json.load(f)
        
    new_files = []
    modified_files = []
    missing_files = []
    
    # Check for modifications and missing items
    for path, trusted_hash in baseline.items():
        if path in current_scan:
            # Only flag as modified if it isn't an unreadable system file link
            if current_scan[path] != trusted_hash and "DENIED" not in trusted_hash and "ALIAS" not in trusted_hash:
                modified_files.append(path)
        else:
            missing_files.append(path)
            
    # Check for entirely new/unknown executables
    for path in current_scan:
        if path not in baseline:
            new_files.append(path)
            
    # --- DISPLAY RESULTS ---
    print("\n" + "="*50)
    print("             INTEGRITY VERIFICATION RESULTS            ")
    print("="*50)
    
    if not new_files and not modified_files and not missing_files:
        print("[✓] Perfect Match! No unexpected changes detected in your directories.")
        return

    if new_files:
        print(f"\n[!] WARNING: {len(new_files)} UNKNOWN / NEW executables found:")
        for f in new_files:
            print(f"  -> {f}")
            
    if modified_files:
        print(f"\n[!] WARNING: {len(modified_files)} TRUSTED files have been MODIFIED:")
        for f in modified_files:
            print(f"  -> {f}")
            
    if missing_files:
        print(f"\n[*] NOTICE: {len(missing_files)} expected files are MISSING (Likely uninstalled):")
        for f in missing_files:
            print(f"  -> {f}")

def main():
    if not os.path.exists(SNAPSHOT_FILE):
        print("No trusted baseline found. Creating your first system snapshot...")
        current_scan = scan_system()
        save_snapshot(current_scan)
    else:
        print("Trusted baseline detected. Verifying system integrity against snapshot...")
        current_scan = scan_system()
        verify_system(current_scan)

if __name__ == "__main__":
    main()
