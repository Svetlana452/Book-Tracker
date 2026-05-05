import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.file_path = "books.json"
        self.books = self.load_data()

        
        tk.Label(root, text="Название:").grid(row=0, column=0, sticky="e")
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(root, text="Автор:").grid(row=1, column=0, sticky="e")
        self.author_entry = tk.Entry(root)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(root, text="Жанр:").grid(row=2, column=0, sticky="e")
        self.genre_entry = tk.Entry(root)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(root, text="Страниц:").grid(row=3, column=0, sticky="e")
        self.pages_entry = tk.Entry(root)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=2)

        tk.Button(root, text="Добавить книгу", command=self.add_book, bg="#e1e1e1").grid(row=4, column=0, columnspan=2, pady=10)

        
        tk.Label(root, text="ФИЛЬТРЫ", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        tk.Label(root, text="По жанру:").grid(row=6, column=0, sticky="e")
        self.filter_genre = tk.Entry(root)
        self.filter_genre.grid(row=6, column=1, padx=5, pady=2)

        tk.Label(root, text="Мин. страниц:").grid(row=7, column=0, sticky="e")
        self.filter_pages = tk.Entry(root)
        self.filter_pages.grid(row=7, column=1, padx=5, pady=2)

        tk.Button(root, text="Применить фильтры", command=self.update_table).grid(row=8, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Сбросить", command=self.reset_filters).grid(row=9, column=0, columnspan=2)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        
        
        self.tree.column("Pages", width=80, anchor="center")
        self.tree.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        self.update_table()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        
        if not (title and author and genre and pages):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {
            "title": title, 
            "author": author, 
            "genre": genre, 
            "pages": int(pages)
        }
        
        self.books.append(new_book)
        self.save_data()
        self.update_table()
        
        
        for entry in [self.title_entry, self.author_entry, self.genre_entry, self.pages_entry]:
            entry.delete(0, tk.END)

    def update_table(self):
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
       
        genre_crit = self.filter_genre.get().lower().strip()
        pages_crit_str = self.filter_pages.get().strip()
        
        
        min_pages = int(pages_crit_str) if pages_crit_str.isdigit() else 0
        
        for b in self.books:
            
            if genre_crit in b['genre'].lower() and b['pages'] >= min_pages:
                self.tree.insert("", tk.END, values=(b['title'], b['author'], b['genre'], b['pages']))

    def reset_filters(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_pages.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))

    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
