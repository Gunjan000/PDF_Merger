import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfWriter
import os


class PDFMergerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Merger")
        self.master.geometry("400x300")  # Fixed window size

        self.file_listbox = tk.Listbox(self.master, selectmode=tk.EXTENDED)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)

        self.file_listbox.bind("<Button-1>", self.on_select_start)
        self.file_listbox.bind("<B1-Motion>", self.on_drag)
        self.file_listbox.bind("<ButtonRelease-1>", self.on_select_end)

        self.create_widgets()

        self.dragged_items = []
        self.drag_start_index = None

    def create_widgets(self):
        self.select_files_btn = tk.Button(self.master, text="Select Files", command=self.select_files)
        self.select_files_btn.pack(pady=10)

        self.merge_btn = tk.Button(self.master, text="Merge", command=self.merge_pdfs)
        self.merge_btn.pack(pady=5)

        # Configure custom styles
        self.master.tk_setPalette(background='#f0f0f0')  # Set background color
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)  # Kill on exit

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file_path in files:
            self.file_listbox.insert(tk.END, os.path.basename(file_path))

    def merge_pdfs(self):
        files_to_merge = [self.file_listbox.get(idx) for idx in range(self.file_listbox.size())]
        if files_to_merge:
            merger = PdfWriter()
            for file in files_to_merge:
                merger.append(file)
            merged_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if merged_filename:
                merger.write(merged_filename)
                merger.close()
                messagebox.showinfo("Success", "PDFs merged successfully!")
        else:
            messagebox.showerror("Error", "No files selected!")

    def close_window(self):
        self.master.destroy()

    def on_select_start(self, event):
        self.drag_start_index = self.file_listbox.nearest(event.y)
        self.dragged_items = [self.file_listbox.get(idx) for idx in self.file_listbox.curselection()]

    def on_drag(self, event):
        if self.drag_start_index is not None:
            index = self.file_listbox.nearest(event.y)
            for item in self.dragged_items:
                self.file_listbox.delete(self.file_listbox.get(0, tk.END).index(item))
            if index < self.drag_start_index:
                for item in self.dragged_items:
                    self.file_listbox.insert(index, item)
            else:
                for item in self.dragged_items:
                    self.file_listbox.insert(index + 1, item)

    def on_select_end(self, event):
        self.drag_start_index = None
        self.dragged_items = []


def main():
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
