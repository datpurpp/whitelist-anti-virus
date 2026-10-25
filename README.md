# Custom Whitelist Antivirus 🛡️

An open-source, lightweight Python security utility that implements a strict whitelisting philosophy to protect Windows operating systems. Instead of relying on bloated virus signature databases that require constant updates, this script creates a baseline snapshot of your system's original, trusted files in highly targeted system directories. When run again, it checks the live directories against your baseline to immediately pinpoint modified, added, or missing files, allowing you to easily locate and manually remove malware.

## 🚀 Features
* **Baseline Cryptographic Whitelisting:** Generates a structured snapshot of trusted files when your system is verified clean.
* **Targeted Directory Monitoring:** Audits the most sensitive folder paths commonly targeted by stealthy malware, including:
  * `C:\Program Files`
  * `C:\Program Files (x86)`
  * `C:\ProgramData`
  * `C:\Users\<username>\AppData`
* **Integrity Discrepancy Flagging:** Instantly detects modifications, unexpected additions (potential payloads), or file deletions compared to your trusted baseline.
* **Manual Malware Isolation:** Displays the exact location of any detected folder anomalies so you can clean the file directory yourself.

## 🧠 How the Philosophy Works
Traditional antivirus software searches for known bad signatures. This program flips that logic around:
* **The Whitelist Rules:** Only explicitly trusted, original system files are permitted to exist within your monitored Windows paths.
* **Anomaly Isolation:** If a virus drops a malicious script or overrides a critical DLL file, the integrity check fails, immediately isolating the bad file path.
* **Updating the Baseline:** Intentionally installing a new game or tool? Simply delete the generated `trusted_system_snapshot.json` file and rerun the script to re-index a fresh baseline.

## 💻 Getting Started

### ⚠️ Crucial Step Before First Run
Ensure your Windows PC is completely clean and free of viruses before generating your baseline. Running the baseline generator on an infected PC will accidentally trust the malware!

### Installation
1. download
   ```
2. Navigate into the project folder:
   
   cd foldername
   ```

### Running the Program
1. run windows powershell & run the command:
   python antivirus2.py
   ```
2. **Verify System Integrity:** Run the script at any time thereafter to scan your active paths and verify they match your original snapshot layout.

## 🛠️ Contributing & Upgrades
This repository is an educational canvas designed to be modified and developed further. Developers are encouraged to fork the repository to add advanced automated file quarantine tools, multithreaded directory indexing, or persistent backup configurations. 

Pull Requests are welcomed for performance tweaks and engine improvements!
