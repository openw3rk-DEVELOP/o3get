import tkinter as tk
from tkinter import scrolledtext, simpledialog, ttk
import os
from urllib.parse import urljoin, urlparse
import re
import threading
import platform

# ******************************
# * (c) 2024 - openw3rk        *
# * (c) 2024 - openw3rk INVENT *
# ****************************** 

def install(package):
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_libraries():
    libraries = ['requests', 'beautifulsoup4']
    for lib in libraries:
        try:
            __import__(lib)
        except ImportError:
            install(lib)

class o3get:
    def __init__(self, root):
        self.root = root
        self.root.title("o3get")

        self.tab_control = ttk.Notebook(root)
        
        self.status_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.status_tab, text="Status")
        
        self.info_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.info_tab, text="Info")
        
        self.tab_control.pack(expand=1, fill="both")

        self.status_label = tk.Label(self.status_tab, text="Status: Ready", bg="gray", fg="white", padx=10, pady=5)
        self.status_label.pack(fill=tk.X)

        self.input_frame = tk.Frame(self.status_tab)
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.input_text = tk.Entry(self.input_frame, bg="white", fg="black", width=80)
        self.input_text.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.submit_button = tk.Button(self.input_frame, text="Run", command=self.run_command)
        self.submit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.output_text = scrolledtext.ScrolledText(self.status_tab, height=20, wrap=tk.WORD)
        self.output_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.output_text.config(state=tk.DISABLED)  

        self.info_text = scrolledtext.ScrolledText(self.info_tab, height=20, wrap=tk.WORD) 
        self.info_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.info_text.insert(tk.END, (
            "o3get - Instructions\n\n"
		"This program downloads an entire website, including all linked pages, images, and CSS files.\n\n"
		"Usage:\n"
		"1. Enter the command 'get -all' in the input field to download the entire website.\n"
		"2. Enter the command 'get -all --css' to download only the CSS files.\n"
		"3. Enter the command 'get -all --html' to download only the HTML files.\n"
		"4. Enter the command 'get -only filename' to download a specific file from the URL.\n"
		"5. You will be prompted for the website's URL.\n"
		"6. The downloaded files will be saved in the system's default download folder. For 'get -all', a subfolder will be created; for 'get -only', the file will be saved directly.\n\n"
		"Explanation of functions:\n"
		"- 'Status': Displays the current status of the program and contains the input fields.\n"
		"- 'Info': Contains these instructions on how to use the program.\n\n"
		"Notes:\n"
		"- Ensure that you have the required libraries installed. The program will attempt to install them if needed.\n\n"
            "             ****************************************************\n" 
            "             * (c) 2024 - openw3rk / (c) 2024 - openw3rk INVENT *\n"
            "             ****************************************************\n" 
        ))
        self.info_text.config(state=tk.DISABLED)  

        self.check_libraries()
        self.display_ascii_art()

    def check_libraries(self):
        self.status_label.config(text="Checking libraries...")
        self.root.update()
        check_and_install_libraries()
        self.status_label.config(text="All required libraries installed.")
        self.root.update()

    def display_ascii_art(self):
        ascii_art = r"""
                              ____     __      _____  ___   _______  ________
    ___  ___  ___ ___ _    __|_  /____/ /__   /  _/ |/ / | / / __/ |/ /_  __/
   / _ \/ _ \/ -_) _ \ |/|/ //_ </ __/  '_/  _/ //    /| |/ / _//    / / /   
   \___/ .__/\__/_//_/__,__/____/_/ /_/\_\  /___/_/|_/ |___/___/_/|_/ /_/    
      /_/                                                            
                                Welcome to o3get
        """
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, ascii_art + "\n\n")
        self.output_text.config(state=tk.DISABLED)
        self.root.update()

    def run_command(self):
        command = self.input_text.get().strip()
        if command.startswith("get -all"):
            url = simpledialog.askstring("Enter URL", "Please enter URL:")
            if url:
                if command == "get -all":
                    threading.Thread(target=self.download_website, args=(url, 'all')).start()
                elif command == "get -all --css":
                    threading.Thread(target=self.download_website, args=(url, 'css')).start()
                elif command == "get -all --html":
                    threading.Thread(target=self.download_website, args=(url, 'html')).start()
                else:
                    self.output_text.config(state=tk.NORMAL)  
                    self.output_text.insert(tk.END, "Invalid command\n")
                    self.output_text.config(state=tk.DISABLED)  
        elif command.startswith("get -only"):
            url = simpledialog.askstring("Enter URL", "Please enter URL:")
            filename = command.split(" ")[-1]
            if url and filename:
                threading.Thread(target=self.download_specific_file, args=(url, filename)).start()
            else:
                self.output_text.config(state=tk.NORMAL)  
                self.output_text.insert(tk.END, "Invalid command or missing filename\n")
                self.output_text.config(state=tk.DISABLED)  
        else:
            self.output_text.config(state=tk.NORMAL)  
            self.output_text.insert(tk.END, "Invalid command\n")
            self.output_text.config(state=tk.DISABLED)  

    def download_website(self, url, mode):
        self.status_label.config(text="Download started...")
        self.output_text.config(state=tk.NORMAL)  
        self.output_text.insert(tk.END, f"Starting download of {url}...\n")
        self.output_text.config(state=tk.DISABLED)  
        self.root.update()

        if platform.system() == "Windows":
            downloads_folder = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        elif platform.system() == "Darwin":  
            downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        else:  # Linux
            downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        
        site_name = urlparse(url).netloc
        base_dir = os.path.join(downloads_folder, site_name)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        visited = set()

        def download_file(url, file_path):
            try:
                response = requests.get(url)
                response.raise_for_status()
                with open(file_path, 'wb') as file:
                    file.write(response.content)
            except requests.RequestException as e:
                self.output_text.config(state=tk.NORMAL)  
                self.output_text.insert(tk.END, f"Error downloading {url}: {e}\n")
                self.output_text.config(state=tk.DISABLED)  
                self.root.update()

        def save_html(content, path):
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)

        def process_page(url, path, mode):
            if url in visited:
                return
            visited.add(url)
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                if mode in ['all', 'html']:
                    save_html(response.text, path)

                if mode == 'all':
                    for img in soup.find_all('img'):
                        img_url = urljoin(url, img.get('src'))
                        img_path = os.path.join(base_dir, re.sub(r'\W+', '_', img.get('src')))
                        download_file(img_url, img_path)

                if mode in ['all', 'css']:
                    for link in soup.find_all('link', rel='stylesheet'):
                        css_url = urljoin(url, link.get('href'))
                        css_path = os.path.join(base_dir, re.sub(r'\W+', '_', link.get('href')) + '.css')
                        download_file(css_url, css_path)

                if mode in ['all', 'html']:
                    for link in soup.find_all('a', href=True):
                        full_url = urljoin(url, link['href'])
                        if site_name in urlparse(full_url).netloc:
                            path = os.path.join(base_dir, re.sub(r'\W+', '_', link['href']) + '.html')
                            process_page(full_url, path, mode)
            except requests.RequestException as e:
                self.output_text.config(state=tk.NORMAL)  
                self.output_text.insert(tk.END, f"Error processing the page {url}: {e}\n")
                self.output_text.config(state=tk.DISABLED)  
                self.root.update()

        initial_path = os.path.join(base_dir, 'index.html')
        process_page(url, initial_path, mode)

        self.status_label.config(text="Download Completed!")
        self.output_text.config(state=tk.NORMAL)  
        self.output_text.insert(tk.END, "Download Completed.\n")
        self.output_text.config(state=tk.DISABLED)  
        self.root.update()

    def download_specific_file(self, url, filename):
        self.status_label.config(text="Download started...")
        self.output_text.config(state=tk.NORMAL)  
        self.output_text.insert(tk.END, f"Download started File: {filename} of {url}...\n")
        self.output_text.config(state=tk.DISABLED)  
        self.root.update()

        if platform.system() == "Windows":
            downloads_folder = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        elif platform.system() == "Darwin":  
            downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        else:  
            downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

        file_url = urljoin(url, filename)
        file_path = os.path.join(downloads_folder, filename)

        try:
            response = requests.get(file_url)
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                file.write(response.content)
            self.status_label.config(text="Download Completed!")
            self.output_text.config(state=tk.NORMAL)  
            self.output_text.insert(tk.END, f"{filename} Download successful.n")
            self.output_text.config(state=tk.DISABLED)  
            self.root.update()
        except requests.RequestException as e:
            self.status_label.config(text="Error Download!")
            self.output_text.config(state=tk.NORMAL)  
            self.output_text.insert(tk.END, f"Download error File: {filename}: {e}\n")
            self.output_text.config(state=tk.DISABLED)  
            self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = o3get(root)
    root.mainloop()
