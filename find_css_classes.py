
def find_classes():
    file_path = r"p:\AI-website-clone\node_site\public\assets\css\style.css"
    targets = ['.btn-1', '.btn-2', '.mission-inner-sec', '.tp-right-btn', '.apply']
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        for t in targets:
            if t in line:
                print(f"Line {i+1}: {line.strip()}")

if __name__ == "__main__":
    find_classes()
