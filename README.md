

# FileExaminer 1.3 - Scan and Find the Largest Files and Folders

FileExaminer is a command-line tool written in Python that enables you to scan a directory and discover the largest files and folders it contains. With three distinct scan types—quick, full, and custom—you can tailor your scans to meet specific requirements.

## New in Version 1.1

- **Resource Usage Control**: Choose from three resource levels—low, medium, or high—to control the speed and efficiency of your scans. Higher levels consume more resources for faster scans.

- **Enhanced Progress Visualization**: Monitor progress in real-time through the console while scanning. Results are also recorded in the `history.log` file for future reference.

- **Optimized Resource Management**: The tool now simulates different levels of resource usage, enhancing the balance between performance and resource consumption.

## New in Version 1.2

- **Pause and Resume**: Pause and resume your scan process interactively, allowing you to control when the scan runs.

- **Memory Usage Monitoring**: Monitor memory usage during scans to ensure efficient resource allocation.

## New in Version 1.3

- **Parallel Scanning**: Introducing parallel scanning, which allows FileExaminer to utilize multiple threads for faster scans on multi-core systems.

- **Multiple Output Formats**: Choose from multiple output formats, including plain text, CSV, and JSON, to export scan results.

## Features

- Scan a directory and its subdirectories to find the largest files and folders.
- Three scan types: quick, full, and custom.
- Specify maximum depth for custom scans.
- Option to include hidden files and folders in the scan.
- Filter files by minimum size and specific file extensions.
- Output results in various formats: plain text, CSV, or JSON.
- Interactive pause and resume functionality.
- Monitor memory usage during scans.
- Detailed history logging (optional).

## Usage

1. Clone the repository to your local machine:

```bash
git clone https://github.com/papaj2139/FileExaminer.git
```

2. Navigate to the directory:

```bash
cd FileExaminer
```

3. Run the script with the following command:

```bash
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
- `--output-format`: Choose the output format: `text` (default), `csv`, or `json`.
- `--resource-level`: Resource usage level: low, medium, high (default is medium).
- `--no-history`: Disable history logging.

### Examples

1. Perform a quick scan in the "Downloads" directory and export results to CSV:
```bash
python main.py quick C:\Users\yourusername\Downloads --output-format csv
```

2. Perform a full scan and display the top 5 largest files and folders in JSON format:
```bash
python main.py full C:\Users\yourusername\Downloads --num-files 5 --output-format json
```

3. Perform a custom scan with a maximum depth of 2, include hidden files and folders, and save the results to a file in plain text format:
```bash
python main.py custom C:\Users\yourusername\Downloads --max-depth 2 --include-hidden --output-file scan_results.txt
```

## Notes

- The script will display the progress and estimated time remaining during the scan.
- If no options are specified, the script will perform a full scan by default and display the top 10 largest files and folders.
- It uses more CPU and RAM than it uses disk. Still an SSD is recommended for optimal performance.
- The history.log files can become very large, up to 25000 times the code size. It is optional.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



