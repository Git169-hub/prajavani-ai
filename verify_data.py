import os

data_dir = "data"
files = os.listdir(data_dir)
print(f"Files found: {len(files)}")
print()

for filename in files:
    if filename.endswith(".txt"):
        path = os.path.join(data_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        status = "✓ OK" if len(content) > 3000 else "✗ TOO SHORT"
        print(f"{filename}: {len(content)} characters — {status}")