
import os

def simple_search():
    base_dir = r"p:\AI-website-clone\node_site\public\assets\css"
    files = ["style.css", "index.css", "responsive.css"]
    keywords = ["linear-gradient", "radial-gradient", ".cta", ".highlight", ".faq", ".apply"]

    for fname in files:
        fpath = os.path.join(base_dir, fname)
        if not os.path.exists(fpath): continue
        
        print(f"--- {fname} ---")
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except:
             with open(fpath, 'r', encoding='latin-1') as f:
                lines = f.readlines()

        for i, line in enumerate(lines):
            for k in keywords:
                if k in line.lower():
                    print(f"{i+1}: {line.strip()}")

if __name__ == "__main__":
    simple_search()
