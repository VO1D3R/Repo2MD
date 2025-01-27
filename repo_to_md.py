import os
import subprocess
import tempfile
import shutil
import sys

def clone_repo(repo_url, temp_dir):
    try:
        subprocess.run(
            ['git', 'clone', '--depth', '1', repo_url],
            check=True,
            cwd=temp_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except FileNotFoundError:
        print("Error: Git is not installed. Please install Git to clone repositories.")
        return False
    except subprocess.CalledProcessError:
        print(f"Error cloning repository: {repo_url}")
        return False

def generate_tree(directory):
    def _tree_helper(current_dir, prefix, is_last, is_root):
        if is_root:
            dir_name = os.path.basename(current_dir)
            lines = [f"{dir_name}/"]
        else:
            dir_name = os.path.basename(current_dir)
            lines = [f"{prefix}{'└── ' if is_last else '├── '}{dir_name}/"]

        try:
            entries = sorted(
                [e for e in os.listdir(current_dir) if e != '.git' and not os.path.islink(os.path.join(current_dir, e))],
                key=lambda x: (not os.path.isdir(os.path.join(current_dir, x)), x)
            )
        except PermissionError:
            return lines

        for i, entry in enumerate(entries):
            entry_path = os.path.join(current_dir, entry)
            entry_is_last = i == len(entries) - 1
            
            if os.path.isdir(entry_path):
                new_prefix = prefix + ('    ' if is_last else '│   ')
                lines.extend(_tree_helper(
                    entry_path,
                    new_prefix,
                    entry_is_last,
                    False
                ))
            else:
                lines.append(f"{prefix}{'    ' if is_last else '│   '}{'└── ' if entry_is_last else '├── '}{entry}")
                
        return lines

    return '\n'.join(_tree_helper(directory, '', False, True))

def read_file_content(file_path):
    max_size = 1 * 1024 * 1024  # 1MB
    try:
        if os.path.getsize(file_path) > max_size:
            return "File skipped (size exceeds 1MB)"
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (UnicodeDecodeError, PermissionError):
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def get_language(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return {
        '.py': 'python',
        '.js': 'javascript',
        '.md': 'markdown',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.txt': 'text',
        '.log': 'text',
    }.get(ext, '')

def main(repo_input, output_file):
    temp_dir = None
    try:
        if repo_input.startswith(('http://', 'https://')):
            temp_dir = tempfile.mkdtemp()
            print(f"Cloning repository: {repo_input}")
            if not clone_repo(repo_input, temp_dir):
                sys.exit(1)
            
            repo_clone_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            repo_dir = repo_clone_dir
        else:
            repo_dir = os.path.abspath(repo_input)
            if not os.path.isdir(repo_dir):
                print(f"Error: Directory not found: {repo_dir}")
                sys.exit(1)

        print("Generating file tree...")
        tree = generate_tree(repo_dir)
        md_content = f"# Repository Structure\n\n```\n{tree}\n```\n\n"

        print("Processing files...")
        processed_files = 0
        for root, dirs, files in os.walk(repo_dir):
            dirs[:] = [d for d in dirs if d != '.git']
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_dir)
                content = read_file_content(file_path)
                
                if content is None:
                    continue
                
                language = get_language(file_path)
                md_content += f"## File: {rel_path}\n\n```{language}\n{content}\n```\n\n"
                processed_files += 1

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Successfully created {output_file} with {processed_files} files")

    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python repo_to_md.py <repository_url_or_path> <output_file.md>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
