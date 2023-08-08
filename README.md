

# FileExaminer - Scan and Find the Largest Files and Folders

FileExaminer is a command-line tool written in Python that allows you to scan a directory and find the largest files and folders within it. It provides three types of scans: quick, full, and custom, allowing you to customize the scan based on your specific requirements.

## Features

- Scan a directory and its subdirectories to find the largest files and folders.
- Three scan types: quick, full, and custom.
- Option to specify the maximum depth for custom scans.
- Ability to include hidden files and folders in the scan.
- Filter files by minimum size and specific file extensions.
- Option to output the results to a text file.

## Usage

1. Clone the repository to your local machine:

```
git clone https://github.com/papaj2139/FileExaminer.git
```

2. Navigate to the directory:

```
cd FileExaminer
```

3. Run the script with the following command:

```
python main.py scan_type directory [options]
```

Replace `scan_type` with one of the following options:
- `quick`: Perform a quick scan.
- `full`: Perform a full scan.
- `custom`: Perform a custom scan.

Replace `directory` with the path of the directory you want to scan.

### Options

- `--max-depth`: Maximum depth for custom scan (default is unlimited).
- `--include-hidden`: Include hidden files and folders in the scan (default is False).
- `--min-file-size`: Minimum file size (in bytes) to include in the results.
- `--valid-extensions`: List of valid file extensions to include in the results.
- `--num-files`: Number of top files and folders to display (default is 10).
- `--output-file`: Output file to store the results (optional).

### Examples

1. Perform a quick scan in the "Downloads" directory:
```
python main.py quick C:\Users\yourusername\Downloads
```

2. Perform a full scan and display the top 5 largest files and folders:
```
python main.py full C:\Users\yourusername\Downloads --num-files 5
```

3. Perform a custom scan with a maximum depth of 2, including hidden files and folders, and save the results to a file:
```
python main.py custom C:\Users\yourusername\Downloads --max-depth 2 --include-hidden --output-file scan_results.txt
```

## Notes

- The script will display the progress and estimated time remaining during the scan.
- If no options are specified, the script will perform a full scan by default and display the top 10 largest files and folders.
- It uses more cpu and ram (About 500 mb of ram per 150000 files) then it uses disk, but i still recommend a SSD for this

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.




