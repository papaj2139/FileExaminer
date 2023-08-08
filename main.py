import os
import time
import argparse
import threading
from queue import Queue
import psutil

EXCLUDED_DIRS = ["C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)"]

def get_size_recursive(path, max_depth=None, include_hidden=False, min_file_size=None, valid_extensions=None):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        if not include_hidden:
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
            print(filepath)
    return total_size

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

def is_important_system_file(file_path):
    important_extensions = ['.sys', '.dll', '.exe']
    return any(file_path.lower().endswith(ext) for ext in important_extensions)

def process_directory(queue, directory, max_depth, include_hidden, min_file_size, valid_extensions, resource_level):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and not os.path.join(dirpath, d).startswith('.')]
            filenames = [f for f in filenames if not f.startswith('.') and not os.path.join(dirpath, f).startswith('.')]
        depth = dirpath[len(directory) + len(os.path.sep):].count(os.path.sep)
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
            queue.put((filepath, file_size))
        
        # Monitor resource usage based on the resource_level option
        if resource_level == "low":
            time.sleep(0.1)  # Simulate low resource usage
        elif resource_level == "medium":
            process = psutil.Process(os.getpid())
            process.cpu_percent(interval=0.1)
            time.sleep(0.05)  # Simulate moderate resource usage
        elif resource_level == "high":
            process = psutil.Process(os.getpid())
            process.cpu_percent(interval=0.01)
            time.sleep(0.01)  # Simulate high resource usage
    queue.put(None)

def main_threaded(scan_type, directory_to_scan, max_depth, include_hidden, min_file_size, valid_extensions,
                  num_files_to_display, output_file, resource_level):
    files = []
    folders = []
    num_files_scanned = 0
    total_files = sum(len(files) for _, _, files in os.walk(directory_to_scan))
    start_time = time.time()
    queue = Queue()

    scanner_thread = threading.Thread(target=process_directory, args=(queue, directory_to_scan, max_depth,
                                                                      include_hidden, min_file_size, valid_extensions, resource_level))
    scanner_thread.start()

    while True:
        result = queue.get()
        if result is None:
            break
        filepath, file_size = result
        if os.path.isfile(filepath):
            is_important = is_important_system_file(filepath)
            files.append((filepath, file_size, is_important))
        else:
            folders.append((filepath, file_size, True))
        num_files_scanned += 1
        elapsed_time = time.time() - start_time
        time_per_file = elapsed_time / max(1, num_files_scanned)
        estimated_remaining_time = (total_files - num_files_scanned) * time_per_file

        # Print progress to console
        print(f"Progress: {num_files_scanned}/{total_files} files scanned.")
        print(f"Estimated Time Remaining: {estimated_remaining_time:.2f} seconds")

        # Append progress to history.log
        with open('history.log', 'a') as history_file:
            history_file.write(f"Progress: {num_files_scanned}/{total_files} files scanned.\n")
            history_file.write(f"Estimated Time Remaining: {estimated_remaining_time:.2f} seconds\n")

    files.sort(key=lambda x: x[1], reverse=True)
    folders.sort(key=lambda x: x[1], reverse=True)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(f"\nTop {num_files_to_display} Largest Files:\n")
            for item, size, is_important in files[:num_files_to_display]:
                size_str = format_size(size)
                item_type = "File"
                if is_important:
                    item_type += " (Important System File)"
                f.write(f"{item_type}: {item} - Size: {size_str}\n")

            f.write(f"\nTop {num_files_to_display} Largest Folders:\n")
            for item, size, is_important in folders[:num_files_to_display]:
                size_str = format_size(size)
                item_type = "Folder"
                if is_important:
                    item_type += " (Important System Folder)"
                f.write(f"{item_type}: {item} - Size: {size_str}\n")

        # Append scan results to the history log
        with open('history.log', 'a') as history_file:
            history_file.write(f"\nScan Results - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            history_file.write(f"Directory: {directory_to_scan}\n")
            history_file.write(f"Scan Type: {scan_type}\n")
            history_file.write(f"Number of Files Displayed: {num_files_to_display}\n")
            history_file.write(f"Output File: {output_file}\n")
            history_file.write(f"Resource Level: {resource_level}\n\n")
            history_file.write("Top Files:\n")
            for item, size, is_important in files[:num_files_to_display]:
                size_str = format_size(size)
                item_type = "File"
                if is_important:
                    item_type += " (Important System File)"
                history_file.write(f"{item_type}: {item} - Size: {size_str}\n")
            history_file.write("\nTop Folders:\n")
            for item, size, is_important in folders[:num_files_to_display]:
                size_str = format_size(size)
                item_type = "Folder"
                if is_important:
                    item_type += " (Important System Folder)"
                history_file.write(f"{item_type}: {item} - Size: {size_str}\n")

    # Print the largest files and folders to the console
    print("\nTop Largest Files:")
    for item, size, is_important in files[:num_files_to_display]:
        size_str = format_size(size)
        item_type = "File"
        if is_important:
            item_type += " (Important System File)"
        print(f"{item_type}: {item} - Size: {size_str}")

    print("\nTop Largest Folders:")
    for item, size, is_important in folders[:num_files_to_display]:
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
    parser.add_argument("--resource-level", choices=["low", "medium", "high"], default="medium", help="Resource usage level: low, medium, high")
    args = parser.parse_args()

    scan_type = args.scan_type
    directory_to_scan = args.directory
    max_depth = args.max_depth
    include_hidden = args.include_hidden
    min_file_size = args.min_file_size
    valid_extensions = args.valid_extensions
    num_files_to_display = args.num_files
    output_file = args.output_file
    resource_level = args.resource_level

    if scan_type == "quick":
        main_threaded("quick", directory_to_scan, max_depth, include_hidden, min_file_size, valid_extensions,
                      num_files_to_display, output_file, resource_level)
    elif scan_type == "full":
        main_threaded("full", directory_to_scan, max_depth, include_hidden, min_file_size, valid_extensions,
                      num_files_to_display, output_file, resource_level)
    elif scan_type == "custom":
        main_threaded("custom", directory_to_scan, max_depth, include_hidden, min_file_size, valid_extensions,
                      num_files_to_display, output_file, resource_level)
