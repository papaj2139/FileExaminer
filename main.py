import os
import time
import argparse

# Directories to exclude from the full and quick scans
EXCLUDED_DIRS = ["C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)"]

def get_size_recursive(path, max_depth=None, include_hidden=False, min_file_size=None, valid_extensions=None):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        if not include_hidden:
            # Exclude hidden directories and files
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and not os.path.join(dirpath, d).startswith('.')]
            filenames = [f for f in filenames if not f.startswith('.') and not os.path.join(dirpath, f).startswith('.')]
        depth = dirpath[len(path) + len(os.path.sep):].count(os.path.sep)
        if max_depth is not None and depth >= max_depth:
            continue
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_size = os.path.getsize(filepath)
            if min_file_size is not None and file_size < min_file_size:
                continue
            if valid_extensions and not any(filename.lower().endswith(ext) for ext in valid_extensions):
                continue
            total_size += file_size
            print(filepath)  # Print the path of each file as it's scanned
    return total_size

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

def is_important_system_file(file_path):
    
    important_extensions = ['.sys', '.dll', '.exe']
    return any(file_path.lower().endswith(ext) for ext in important_extensions)

def get_largest_files_and_folders(path, num_files=10, quick_scan=False, custom_scan=False, max_depth=None,
                                 include_hidden=False, min_file_size=None, valid_extensions=None, output_file=None):
    files = []
    folders = []
    num_files_scanned = 0
    total_files = sum(len(files) for _, _, files in os.walk(path))
    start_time = time.time()

    for dirpath, dirnames, filenames in os.walk(path):
        if custom_scan and not quick_scan:
            dirnames[:] = [d for d in dirnames if os.path.join(dirpath, d) not in EXCLUDED_DIRS]
        else:
            dirnames[:] = [d for d in dirnames if os.path.join(dirpath, d) not in EXCLUDED_DIRS]

        for dirname in dirnames:
            dir_size = get_size_recursive(os.path.join(dirpath, dirname), max_depth=max_depth, include_hidden=include_hidden,
                                          min_file_size=min_file_size, valid_extensions=valid_extensions) if not quick_scan else 0
            folders.append((dirname, dir_size, True))  # Mark folders as important by default
            num_files_scanned += 1
            if quick_scan:
                break  # Stop scanning subdirectories in quick scan mode

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            is_important = is_important_system_file(file_path)
            files.append((filename, file_size, is_important))
            num_files_scanned += 1

        elapsed_time = time.time() - start_time
        time_per_file = elapsed_time / max(1, num_files_scanned)
        estimated_remaining_time = (total_files - num_files_scanned) * time_per_file

        print(f"Progress: {num_files_scanned}/{total_files} files scanned.")
        print(f"Estimated Time Remaining: {estimated_remaining_time:.2f} seconds")

    files.sort(key=lambda x: x[1], reverse=True)
    folders.sort(key=lambda x: x[1], reverse=True)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(f"\nTop {num_files} Largest Files:\n")
            for item, size, is_important in files[:num_files]:
                size_str = format_size(size)
                item_type = "File"
                if is_important:
                    item_type += " (Important System File)"
                f.write(f"{item_type}: {item} - Size: {size_str}\n")

            f.write(f"\nTop {num_files} Largest Folders:\n")
            for item, size, is_important in folders[:num_files]:
                size_str = format_size(size)
                item_type = "Folder"
                if is_important:
                    item_type += " (Important System Folder)"
                f.write(f"{item_type}: {item} - Size: {size_str}\n")
    else:
        print(f"\nTop {num_files} Largest Files:")
        for item, size, is_important in files[:num_files]:
            size_str = format_size(size)
            item_type = "File"
            if is_important:
                item_type += " (Important System File)"
            print(f"{item_type}: {item} - Size: {size_str}")

        print(f"\nTop {num_files} Largest Folders:")
        for item, size, is_important in folders[:num_files]:
            size_str = format_size(size)
            item_type = "Folder"
            if is_important:
                item_type += " (Important System Folder)"
            print(f"{item_type}: {item} - Size: {size_str}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan and find the largest files and folders.")
    parser.add_argument("scan_type", choices=["quick", "full", "custom"], help="Type of scan: quick, full, or custom")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--max-depth", type=int, help="Maximum depth for custom scan (default is unlimited)")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files and folders in the scan")
    parser.add_argument("--min-file-size", type=int, help="Minimum file size (in bytes) to include in the results")
    parser.add_argument("--valid-extensions", nargs="+", help="List of valid file extensions to include in the results")
    parser.add_argument("--num-files", type=int, default=10, help="Number of top files and folders to display (default is 10)")
    parser.add_argument("--output-file", help="Output file to store the results (optional)")
    args = parser.parse_args()

    scan_type = args.scan_type
    directory_to_scan = args.directory
    max_depth = args.max_depth
    include_hidden = args.include_hidden
    min_file_size = args.min_file_size
    valid_extensions = args.valid_extensions
    num_files_to_display = args.num_files
    output_file = args.output_file

    if scan_type == "quick":
        get_largest_files_and_folders(directory_to_scan, num_files=num_files_to_display, quick_scan=True, output_file=output_file)
    elif scan_type == "full":
        get_largest_files_and_folders(directory_to_scan, num_files=num_files_to_display, output_file=output_file)
    elif scan_type == "custom":
        get_largest_files_and_folders(directory_to_scan, num_files=num_files_to_display, custom_scan=True, max_depth=max_depth,
                                      include_hidden=include_hidden, min_file_size=min_file_size,
                                      valid_extensions=valid_extensions, output_file=output_file)
