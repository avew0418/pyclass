# Flask Blog Demo

A minimal Flask blog supporting:
- 發表文章（可上傳照片）
- 留言功能
- 個人檔案（上傳照片、自我介紹）

目錄：
```
flask_blog/
  app.py
  blog.db (will be created)
  templates/
  static/
  requirements.txt
  README.md
```

快速啟動（Windows PowerShell）：
```powershell
cd d:\code_file\pyclass\flask_blog
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

開啟瀏覽器： http://127.0.0.1:5000/

- 發表文章：點選 New Post
- 個人檔案：Profile
- 留言：在文章頁面底下留言

注意：上傳的照片會儲存在 `flask_blog/static/uploads/`，可在報告中一併帶上該資料夾的內容作示範。