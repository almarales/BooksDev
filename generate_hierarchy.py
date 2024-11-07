import os
import urllib.parse

def generate_hierarchy(directory, base_url, indent="", ignore_git=True, ignore_files=None):
    """Recursively generate a hierarchy of files and folders for a given directory."""
    hierarchy = ""
    book_count = 0
    folder_count = 0
    total_size = 0  # Track the total size of the files
    
    if ignore_files is None:
        ignore_files = {".git", ".github", "generate_hierarchy.py", "README.md"}
    
    items = sorted(os.listdir(directory))
    
    for index, item in enumerate(items):
        if item in ignore_files:
            continue  # Skip ignored files or directories
        
        item_path = os.path.join(directory, item)
        is_last_item = (index == len(items) - 1)
        
        if os.path.isdir(item_path):
            # Folder representation with tree structure
            folder_count += 1
            hierarchy += f"{indent}📂 {item}\n"
            sub_hierarchy, sub_book_count, sub_folder_count, sub_size = generate_hierarchy(
                item_path, base_url, indent + ("    " if is_last_item else "|   "), ignore_git, ignore_files
            )
            hierarchy += sub_hierarchy
            book_count += sub_book_count
            folder_count += sub_folder_count
            total_size += sub_size  # Add subdirectory size to total size
        else:
            # File representation with clickable links and size
            book_count += 1
            file_size = os.path.getsize(item_path)
            readable_size = f"{file_size / (1024 * 1024):.2f} MB"  # Size in MB
            total_size += file_size  # Add file size to total size
            file_url = urllib.parse.quote(f"https://github.com/Abdalrahman-Alhamod/Books/raw/main/{item}")  # Modify with your GitHub repo path
            hierarchy += f"{indent}├── <a href='{file_url}'>{item}</a> - Size: {readable_size}\n"
    
    return hierarchy, book_count, folder_count, total_size

def format_size(size_in_bytes):
    """Convert bytes into a human-readable format (KB, MB, GB)."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024

def update_readme(content, book_count, folder_count, total_size):
    """Update README.md with the generated file hierarchy content."""
    start_marker = "<!-- FILE_STRUCTURE_START -->"
    end_marker = "<!-- FILE_STRUCTURE_END -->"

    # Read the current README.md
    with open("README.md", "r", encoding="utf-8") as readme_file:
        readme_content = readme_file.read()

    # Summary section - at the top, outside the <pre> block
    readable_size = format_size(total_size)
    summary_content = f"""
# 📚 E-Book Library Summary

- **Total Books**: {book_count}
- **Total Folders**: {folder_count}
- **Total Library Size**: {readable_size}
- **Book List**: The following is the directory structure of available books. You can click on each book to download it directly from GitHub.
    """

    # Ensure both markers are present
    if start_marker in readme_content and end_marker in readme_content:
        # Replace the content between markers
        new_content = (
            readme_content.split(start_marker)[0] + start_marker + "\n\n" + summary_content + "\n\n" + "<pre>" + content + "</pre>" + "\n\n" + end_marker +
            readme_content.split(end_marker)[1]
        )
    else:
        # Add markers and content if missing
        new_content = (
            readme_content + "\n\n" + start_marker + "\n\n" + summary_content + "\n\n" + "<pre>" + content + "</pre>" + "\n\n" + end_marker
        )

    # Write the updated content back to README.md with UTF-8 encoding
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(new_content)

# Set the base URL for your GitHub repository
base_url = "https://github.com/Abdalrahman-Alhamod/Books/raw/main/"

# Generate the hierarchy and update README
hierarchy_content, book_count, folder_count, total_size = generate_hierarchy(".", base_url)
update_readme(hierarchy_content, book_count, folder_count, total_size)
