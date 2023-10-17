import tkinter as tk

import tkinter.ttk as ttk

from tkhtmlview import HTMLScrolledText

class WebBrowser:

    def __init__(self, master):

        self.master = master

        self.master.title("web")

        self.history = []

        self.current_url = None

        self.create_widgets()

    def create_widgets(self):

        url_frame = ttk.Frame(self.master)

        url_frame.pack(fill=tk.X)

        back_button = ttk.Button(url_frame, text="Back", command=self.navigate_back)

        back_button.pack(side=tk.LEFT, padx=5, pady=5)

        forward_button = ttk.Button(url_frame, text="Forward", command=self.navigate_forward)

        forward_button.pack(side=tk.LEFT, padx=5, pady=5)

        refresh_button = ttk.Button(url_frame, text="Refresh", command=self.reload_page)

        refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.url_entry = ttk.Entry(url_frame)

        self.url_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        go_button = ttk.Button(url_frame, text="Go", command=self.load_webpage)

        go_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.status_bar = ttk.Label(self.master, text="", anchor=tk.W)

        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.html_view = HTMLScrolledText(self.master, width=80, height=40)

        self.html_view.pack(fill=tk.BOTH, expand=True)

        self.search_entry = ttk.Entry(self.master, width=80)

        self.search_entry.pack(padx=5, pady=5)

        search_button = ttk.Button(self.master, text="Search", command=self.search_text)

        search_button.pack(padx=5, pady=5)

    def navigate_back(self):

        if len(self.history) > 1:

            self.history.pop()

            url = self.history[-1]

            self.load_webpage(url)

    def navigate_forward(self):

        if len(self.history) > 1:

            self.history.pop(0)

            url = self.history[0]

            self.load_webpage(url)

    def reload_page(self):

        if self.current_url:

            self.load_webpage(self.current_url)

    def load_webpage(self, url=None):

        if not url:

            url = self.url_entry.get()

        self.status_bar.config(text=f"Loading {url}...")

        self.master.update()

        html_content = f'<iframe src="{url}" width="100%" height="100%"></iframe>'

        self.html_view.set_html(html_content)

        self.current_url = url

        self.history.append(url)

        self.status_bar.config(text=f"Loaded {url}")

    def search_text(self):

        query = self.search_entry.get()

        start_pos = self.html_view.index(tk.INSERT)

        search_result = self.html_view.search(query, start_pos, stopindex=tk.END, nocase=True)

        if search_result:

            self.html_view.tag_add("search", search_result, f"{search_result} + {len(query)}c")

            self.html_view.tag_configure("search", background="yellow")

            self.html_view.mark_set(tk.INSERT, search_result)

            self.html_view.see(tk.INSERT)

    def clear_search_results(self):

        self.html_view.tag_remove("search", "1.0", tk.END)

root = tk.Tk()

browser = WebBrowser(root)

root.mainloop()