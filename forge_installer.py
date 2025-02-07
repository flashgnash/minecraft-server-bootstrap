import tomllib
import requests
import subprocess
import sys
import os

def extract_forge_version(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch TOML file from {url}")
        sys.exit(1)
    
    data = tomllib.loads(response.text)
    forge_ver = data["versions"]["forge"]
    mc_ver = data["versions"]["minecraft"]
    
    return mc_ver, forge_ver

def download_forge(dir_path, minecraft_ver, forge_ver):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    download_url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{minecraft_ver}-{forge_ver}-{minecraft_ver}/forge-{minecraft_ver}-{forge_ver}-{minecraft_ver}-installer.jar"
    
    response = requests.get(download_url, allow_redirects=True)
    
    if response.status_code == 200:
        filename = response.url.split("/")[-1]
        file_path = os.path.join(dir_path, filename)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return os.path.abspath(file_path)
    else:
        print(f"Failed to download forge from {download_url}")
        return None

def install_forge(installer_path, dir_path):
    if not os.path.exists(installer_path):
        print("Forge executable not found")
        return
    
    command = ["java", "-jar", installer_path, "--installServer"]
    subprocess.run(command, cwd=dir_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <http_url_to_toml>")
        sys.exit(1)
    
    toml_url = sys.argv[1]
    mc_ver, forge_ver = extract_forge_version(toml_url)
    installer = download_forge(os.getcwd(), mc_ver, forge_ver)
    install_forge(installer, os.getcwd())
