# Documentation for `RaptorSight.py`

## Overview

`RaptorSight.py` is a project for educational purposes and is not intended to be used as a real tool. It is a port scanner tool named RaptorSight, designed to scan a specified range of ports on a given IP address or hostname. It utilizes multithreading for faster scanning and provides detailed reports of open ports and any errors encountered during the scan.

## Dependencies

- `socket`: For network connections and port scanning.
- `concurrent.futures.ThreadPoolExecutor`: For handling multithreading.
- `os`: For error code recognition.
- `tqdm`: For displaying progress bars during the scanning process.

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

1. Run the script in a Python environment.
2. Input the target IP address or hostname when prompted.
3. Specify the starting and ending ports for the scan (default values are 1 and 1666).
4. Optionally, specify the number of threads to use for scanning (default is no threading).
5. The script will validate the inputs and begin scanning the specified ports.

## Functions

- **`validate_int_input(user_input, default_value)`**

  - Validates user input for integer values.
  - Returns the input as an integer or a default value if the input is invalid.

- **`Raptor` Class**

  - **`__init__(self, host, port_start, port_end, threads)`**

    - Initializes the Raptor object with the target host, port range, and threading option.

  - **`validate_target(self)`**

    - Validates the target hostname and port range.
    - Ensures that the port range is within valid limits and prompts the user for corrections if necessary.

  - **`report(self)`**

    - Prints a report of the scan results, including open ports and any errors encountered.

  - **`scan_port(self, port)`**

    - Scans a single port to check if it is open.
    - Appends open ports and any errors to their respective lists.

  - **`scan(self)`**
    - Initiates the port scanning process.
    - Uses multithreading if specified; otherwise, scans ports sequentially.
    - Calls the `report` method to display results after scanning.

## Example

```python
if __name__ == "__main__":
    raptor = Raptor(host, port_start, port_end, threads)
    raptor.validate_target()
    input("Press any button when ready")
    print("Engaging target....")
    raptor.scan()
```

## Legal Disclaimer

This project is for educational purposes only. The author is not responsible for any misuse or damage caused by the use of this tool. Use it at your own risk.
