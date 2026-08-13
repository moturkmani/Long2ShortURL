"""
URL Shortener
A simple, modern Tkinter GUI that shortens long URLs using the TinyURL API.
Automatically copies the shortened URL to your clipboard.
"""

import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.parse
import threading

# ---------- Color palette ----------
BG = "#f4f5f7"
ACCENT = "#2563eb"
ACCENT_HOVER = "#1d4ed8"
TEXT = "#1f2937"
SUBTEXT = "#6b7280"
BORDER = "#d1d5db"
SUCCESS = "#16a34a"
ERROR = "#dc2626"
COPY_BG = "#e5e7eb"
COPY_HOVER = "#d1d5db"


class URLShortenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Shortener")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.root.minsize(560, 400)

        self.center_window(720, 420)
        self.build_ui()

    def center_window(self, width, height):
        """Centers the window on whichever screen/monitor Tk reports as active."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def build_ui(self):
        container = tk.Frame(self.root, bg=BG, padx=32, pady=26)
        container.pack(fill="both", expand=True)

        # Header
        tk.Label(
            container, text="🔗 URL Shortener",
            font=("Segoe UI", 18, "bold"), bg=BG, fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            container, text="Paste a long URL below and shorten it instantly via TinyURL",
            font=("Segoe UI", 10), bg=BG, fg=SUBTEXT
        ).pack(anchor="w", pady=(2, 18))

        # --- Long URL input ---
        tk.Label(
            container, text="LONG URL",
            font=("Segoe UI", 9, "bold"), bg=BG, fg=SUBTEXT
        ).pack(anchor="w", pady=(0, 5))

        self.url_entry = tk.Entry(
            container, font=("Segoe UI", 11), bd=1, relief="solid",
            highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT
        )
        self.url_entry.pack(fill="x", ipady=9)
        self.url_entry.bind("<Return>", lambda e: self.shorten_url())
        self.url_entry.focus_set()

        # --- Shorten button ---
        self.shorten_btn = tk.Button(
            container, text="Shorten URL", command=self.shorten_url,
            bg=ACCENT, fg="white", font=("Segoe UI", 11, "bold"),
            relief="flat", bd=0, cursor="hand2",
            activebackground=ACCENT_HOVER, activeforeground="white"
        )
        self.shorten_btn.pack(fill="x", pady=(16, 6), ipady=9)
        self.shorten_btn.bind("<Enter>", lambda e: self.shorten_btn.config(bg=ACCENT_HOVER))
        self.shorten_btn.bind("<Leave>", lambda e: self.shorten_btn.config(bg=ACCENT))

        # --- Status message ---
        self.status_label = tk.Label(
            container, text="", font=("Segoe UI", 9), bg=BG, fg=SUBTEXT
        )
        self.status_label.pack(anchor="w")

        # --- Result field ---
        tk.Label(
            container, text="SHORTENED URL",
            font=("Segoe UI", 9, "bold"), bg=BG, fg=SUBTEXT
        ).pack(anchor="w", pady=(16, 5))

        result_frame = tk.Frame(container, bg=BG)
        result_frame.pack(fill="x")

        self.result_entry = tk.Entry(
            result_frame, font=("Segoe UI", 11, "bold"), bd=1, relief="solid",
            highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT,
            fg=ACCENT, readonlybackground="#f9fafb", state="readonly"
        )
        self.result_entry.pack(side="left", fill="x", expand=True, ipady=9)
        # Allow click-drag select + Ctrl+C even though it's readonly
        self.result_entry.bind("<1>", lambda e: self.result_entry.focus_set())

        self.copy_btn = tk.Button(
            result_frame, text="Copy", command=self.copy_to_clipboard,
            bg=COPY_BG, fg=TEXT, font=("Segoe UI", 10, "bold"),
            relief="flat", bd=0, cursor="hand2", width=9
        )
        self.copy_btn.pack(side="left", padx=(8, 0), ipady=9)
        self.copy_btn.bind("<Enter>", lambda e: self.copy_btn.config(bg=COPY_HOVER))
        self.copy_btn.bind("<Leave>", lambda e: self.copy_btn.config(bg=COPY_BG))

    # ---------- Logic ----------
    def shorten_url(self):
        long_url = self.url_entry.get().strip()
        if not long_url:
            messagebox.showwarning("Missing URL", "Please paste a URL to shorten.")
            return

        if not (long_url.startswith("http://") or long_url.startswith("https://")):
            long_url = "https://" + long_url

        self.shorten_btn.config(state="disabled", text="Shortening...")
        self.status_label.config(text="", fg=SUBTEXT)
        self.set_result("")

        threading.Thread(target=self._call_api, args=(long_url,), daemon=True).start()

    def _call_api(self, long_url):
        try:
            api_url = "https://tinyurl.com/api-create.php?" + urllib.parse.urlencode({"url": long_url})
            with urllib.request.urlopen(api_url, timeout=10) as response:
                short_url = response.read().decode("utf-8").strip()
            if not short_url.startswith("http"):
                raise ValueError(short_url or "Unexpected response from TinyURL")
            self.root.after(0, self._on_success, short_url)
        except Exception as e:
            self.root.after(0, self._on_error, str(e))

    def _on_success(self, short_url):
        self.set_result(short_url)
        self.copy_to_clipboard(silent=True)
        self.status_label.config(text="✅ Copied to clipboard!", fg=SUCCESS)
        self.shorten_btn.config(state="normal", text="Shorten URL")

    def _on_error(self, error_msg):
        self.status_label.config(text=f"❌ Error: {error_msg}", fg=ERROR)
        self.shorten_btn.config(state="normal", text="Shorten URL")

    def set_result(self, text):
        self.result_entry.config(state="normal")
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, text)
        self.result_entry.config(state="readonly")

    def copy_to_clipboard(self, silent=False):
        text = self.result_entry.get()
        if not text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        if not silent:
            self.status_label.config(text="✅ Copied to clipboard!", fg=SUCCESS)


def main():
    root = tk.Tk()
    URLShortenerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()