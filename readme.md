# PyLaunch `pre-1.1`

[![Static Badge](https://img.shields.io/badge/Stable_Version-1.0-yellow)](https://github.com/KRWCLASSIC/PyLaunch/)
[![Static Badge](https://img.shields.io/badge/Code_Version-pre--1.1-yellow)](https://github.com/KRWCLASSIC/PyLaunch/tree/3d0765fa88b80df7ba4a9a841791e06a73186d21)
[![Static Badge](https://img.shields.io/badge/Maintainer-KRWCLASSIC-green)](https://github.com/KRWCLASSIC)

[![Static Badge](https://img.shields.io/badge/Current_State-Usable-red)](where_u_goin_dawg)

![App Icon](icon.ico)

PyLaunch is a simple launcher application for Python scripts that allows users to easily run their Python files in a specified IDE or console. It provides a user-friendly interface for configuring the paths to the IDE and console.

## Features

- **IDE Integration**: Open Python scripts directly in your preferred IDE.
- **Console Execution**: Run Python scripts in a console window with options to keep the console open or run silently (.pyw only).
- **Configuration Management**: Easily set and save paths for the IDE and console through a setup dialog.
- **Cross-Platform Support**: Designed to work on both Windows and Unix-like systems. (NOT TESTED!)

## User Interface

<details>
<summary>Preview of the GUI.</summary>

![Screenshot 1](https://i.imgur.com/gnAZVlv.png)
![Screenshot 2](https://i.imgur.com/9xqf8AX.png)
![Screenshot 3](https://i.imgur.com/MXN6vG8.png)

</details>

## Installation

1. **Clone the Repository**:
    Make sure to put it somewhere safe like User Folder or Program Files to prevent accidental removal! To clone it with git:
    `git clone https://github.com/KRWCLASSIC/PyLaunch`
    `cd PyLaunch`

2. **Install Dependencies**:
   Ensure you have Python installed on your system. You may need to install the `PySide6` library if it's not already installed: `pip install PySide6` or `pip install -r requirements.txt`.

3. **Run the Application**:
   You can run the application using `setup.bat` on Windows and `setup.sh` on Linux.

4. **Setup Configuration**:
   On the first run, the application will prompt you to set the paths for your IDE and console. Follow the instructions in the dialog to configure these settings.

## Recommended Actions

- **Set as Default Application**: You can set the launcher as the default application for `.py` files on Windows. This can be done through the setup dialog in the application. (Not figured out Linux way yet.)

- **Keep Console Open**: If you want to see the output of your scripts, check the "Keep console window open" option.

- **Silent Mode**: If you prefer to run scripts without a console window appearing, enable the "Silent mode" option. (.pyw files only!)

## Usage

- **Open in IDE**: Click the "Open in IDE" button to open the currently selected Python script in your configured IDE.

- **Run in Console**: Click the "Run in Console" button to execute the script in the console.

- **Select New File**: Use the file selection button to choose a different Python script to work with.

- **Edit Configuration**: Access the configuration dialog to change the IDE or console paths at any time.

## Troubleshooting

- If you encounter issues with finding the Python executable, ensure that Python is installed and added to your system's PATH.

## License

Idk, open source but tag me if you steal and do not fork.
