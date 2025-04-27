import subprocess
import re
import os

def run_nmap_scan(target):
    try:
        command = ["nmap", "--script", "ssl-enum-ciphers", "-p", "443", target]
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"[ERROR] Failed to run Nmap: {e}"

def analyze_ciphers(nmap_output):
    vulnerabilities = []

    if re.search(r"SSLv2|SSLv3", nmap_output):
        vulnerabilities.append("**Outdated SSL/TLS Version (SSLv2 or SSLv3)** - Vulnerable to POODLE attack.")

    if re.search(r"RC4", nmap_output):
        vulnerabilities.append("**RC4 Cipher Detected** - Vulnerable to BEAST attack.")

    if re.search(r"3DES|DES-CBC3", nmap_output):
        vulnerabilities.append("**3DES Cipher Detected** - Vulnerable to SWEET32 attack.")

    if re.search(r"TLSv1.0", nmap_output) and re.search(r"AES_.*_CBC", nmap_output):
        vulnerabilities.append("**CBC Cipher with TLS 1.0 Detected** - Vulnerable to BEAST attack.")

    if re.search(r"AES_.*_CBC", nmap_output):
        vulnerabilities.append("**CBC-mode Cipher Detected** - Potentially Vulnerable to Lucky Thirteen attack.")

    if "DHE" not in nmap_output and "ECDHE" not in nmap_output:
        vulnerabilities.append("**No Perfect Forward Secrecy (PFS)** - Vulnerable to key reuse attacks.")

    output = f"**SSL Cipher Scan Results for Target**\n\n{nmap_output}\n\n"

    if vulnerabilities:
        output += "**Vulnerabilities Found:**\n" + "\n".join(vulnerabilities) + "\n"
    else:
        output += "No critical vulnerabilities detected!\n"

    results_path = os.path.expanduser("~/Official-SauceDemo/Security/Compiled/Results/CipherEnum.txt")
    with open(results_path, "w") as file:
        file.write(output)

    print("\n📄 Results saved to **Cipher-Scan-Results.txt**")

if __name__ == "__main__":
    target_site = "saucedemo.com" 
    print(f"🔎 Running SSL Cipher Scan on {target_site}...\n")
    
    scan_output = run_nmap_scan(target_site)
    if scan_output:
        print(scan_output)  
        analyze_ciphers(scan_output)
