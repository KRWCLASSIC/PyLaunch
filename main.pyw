from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QMessageBox,
    QDialog, QLineEdit, QFormLayout, QCheckBox, QHBoxLayout, QFileDialog, QComboBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import subprocess
import shutil
import json
import sys
import os

CONFIG_PATH = "config.json"

DARK_THEME = {
    "background": "#2e2e2e",
    "text": "#ffffff"
}

DEFAULT_CONFIG = {
    "ide": "",
    "console": "",
    "keep_console": True,
    "silent_mode": False
}

base_title = "PyLaunch 1.1"

WINDOW_WIDTH = 400
WINDOW_HEIGHT_DEFAULT = 120
WINDOW_HEIGHT_WITH_ARGUMENTS = 147
WINDOW_HEIGHT_WITH_PYW = 140
WINDOW_HEIGHT_WITH_PYW_AND_ARGUMENTS = 163

CONFIG_DIALOG_WIDTH = 400
CONFIG_DIALOG_HEIGHT = 150

class SetupDialog(QDialog):
    def __init__(self, existing_config=None):
        super().__init__()
        self.setWindowTitle("Config")
        self.setFixedSize(CONFIG_DIALOG_WIDTH, CONFIG_DIALOG_HEIGHT)
        
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        form_layout = QFormLayout()
        
        self.ide_name = QLineEdit()
        self.ide_name.setPlaceholderText("e.g. code, cursor, pycharm, sublime_text, notepad")
        self.ide_name.setToolTip("""Make sure your preffered IDE is in PATH
You can check that by trying to run it thru cmd just by running its name""")
        
        self.console_combo = QComboBox()
        self.console_combo.addItems(self.detect_consoles(existing_config))
        self.console_combo.setToolTip("""Select the console to run your scripts (e.g., cmd.exe, powershell.exe).
Linux ones might not work!""")
        
        if existing_config and existing_config.get("console"):
            self.console_combo.setCurrentText(os.path.basename(existing_config["console"]))
        else:
            default_console = "cmd.exe" if os.name == 'nt' else "terminal"
            self.console_combo.setCurrentText(default_console)
        
        if existing_config and existing_config.get("ide"):
            self.ide_name.setText(os.path.basename(existing_config["ide"]))
        
        form_layout.addRow("IDE Name:", self.ide_name)
        form_layout.addRow("Console:", self.console_combo)
        
        layout.addLayout(form_layout)
        
        notice = QLabel(
            "⚠️ Important: Move this launcher to a safe location\n"
            "(e.g., Program Files or User folder) before setting as default app."
        )
        notice.setStyleSheet("color: #FFA500;")
        notice.setAlignment(Qt.AlignCenter)
        layout.addWidget(notice)
        
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)
        
        set_default_button = QPushButton("Set as Default .py App")
        set_default_button.clicked.connect(self.set_as_default_app)
        button_layout.addWidget(set_default_button)
        
        layout.addLayout(button_layout)

    def detect_consoles(self, existing_config):
        """Detect available consoles based on the operating system."""
        consoles = []
        if os.name == 'nt':  # Windows
            consoles = ["cmd.exe", "powershell.exe"]  # Removed wt.exe
        else:  # Linux and macOS
            consoles = ["gnome-terminal", "xterm", "konsole", "terminator", "terminal"]  # Add more if needed
        
        return consoles

    def set_as_default_app(self):
        """Set this script as the default app for .py files (Windows only)."""
        if os.name != 'nt':
            QMessageBox.warning(self, "Not Supported", "This feature works only on Windows.")
            return

        try:
            script_path = os.path.abspath(sys.argv[0])
            launcher_dir = os.path.dirname(script_path)
            bat_path = os.path.join(launcher_dir, "launcher.bat")

            python_path = shutil.which("pythonw")
            if not python_path:
                QMessageBox.critical(self, "Error", "Could not find Pythonw in PATH.")
                return

            bat_contents = f'''@echo off
start /b "" "{python_path}" "{script_path}" "%*"
'''
            with open(bat_path, "w") as f:
                f.write(bat_contents)

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Set Default App")
            msg.setText(f"The launcher.bat file has been created. Please manually set it as the default application for .py (and optionally .pyw) files.")
            msg.setInformativeText(f"To do so, go to Windows Settings > Apps > Default Apps, and choose '{bat_path}' for .py (and optionally .pyw) files.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec()

            subprocess.run(['start', 'ms-settings:defaultapps'], shell=True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to set as default app: {e}")

    def find_executable(self, name):
        """Find the full path of an executable using where/which."""
        if os.name == 'nt':
            try:
                result = subprocess.run(['where', name], capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip().split('\n')[0]
            except Exception:
                pass
        else:
            path = shutil.which(name)
            if path:
                return path
        return ""

    def get_paths(self):
        """Get the paths of the IDE and console from the user input."""
        ide_path = self.find_executable(self.ide_name.text())
        console_path = self.find_executable(self.console_combo.currentText())
        
        if not ide_path:
            QMessageBox.warning(self, "Warning", f"Could not find IDE: {self.ide_name.text()}")
        if not console_path:
            QMessageBox.warning(self, "Warning", f"Could not find Console: {self.console_combo.currentText()}")
            
        return {
            "ide": ide_path,
            "console": console_path
        }

def load_config():
    """Load the configuration from the JSON file or create a new one."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, CONFIG_PATH)

    if not os.path.exists(config_path):
        dialog = SetupDialog()
        if dialog.exec():
            config = dialog.get_paths()
            config["keep_console"] = True
            with open(config_path, "w") as file:
                json.dump(config, file, indent=4)
            return config
        else:
            sys.exit(0)
    
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            if config.get("ide") and not os.path.exists(config["ide"]):
                config["ide"] = ""
            if config.get("console") and not os.path.exists(config["console"]):
                config["console"] = ""
            return config
    except Exception as e:
        return DEFAULT_CONFIG

class LauncherApp(QMainWindow):
    def __init__(self, file_path=None):
        super().__init__()
        
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        if len(sys.argv) > 1:
            self.file_path = sys.argv[1]
        else:
            self.file_path = None

        self.config = load_config()

        if self.file_path:
            filename = os.path.basename(self.file_path)
            self.setWindowTitle(f"{base_title} | {filename}")
        else:
            self.setWindowTitle(base_title)

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT_DEFAULT)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        button_layout = QHBoxLayout()
        
        self.ide_button = QPushButton("Open in IDE")
        self.ide_button.clicked.connect(self.open_in_ide)
        self.ide_button.setMinimumHeight(50)
        button_layout.addWidget(self.ide_button)

        file_config_layout = QVBoxLayout()

        config_button = QPushButton("⚙️")
        config_button.setFixedSize(22, 22)
        config_button.setToolTip("Open the configuration dialog to edit settings.")
        config_button.clicked.connect(self.edit_config)
        file_config_layout.addWidget(config_button)

        file_button = QPushButton("📄")
        file_button.setFixedSize(22, 22)
        file_button.setToolTip("Select a new Python script to run.")
        file_button.clicked.connect(self.select_new_file)
        file_config_layout.addWidget(file_button)

        button_layout.addLayout(file_config_layout)

        self.console_button = QPushButton("Run in Console")
        self.console_button.clicked.connect(self.run_in_console)
        self.console_button.setMinimumHeight(50)
        button_layout.addWidget(self.console_button)
        
        self.layout.addLayout(button_layout)

        bottom_layout = QHBoxLayout()
        
        checkbox_layout = QVBoxLayout()
        
        self.keep_console = QCheckBox("Keep console window open")
        self.keep_console.setChecked(self.config.get("keep_console", True))
        self.keep_console.stateChanged.connect(self.save_checkbox_state)
        checkbox_layout.addWidget(self.keep_console)
        
        self.silent_mode = QCheckBox("Silent mode (hide console)")
        self.silent_mode.setChecked(self.config.get("silent_mode", False))
        self.silent_mode.stateChanged.connect(self.toggle_keep_console)
        self.silent_mode.stateChanged.connect(self.save_checkbox_state)
        self.silent_mode.setVisible(self.is_pyw_file())
        checkbox_layout.addWidget(self.silent_mode)

        self.add_arguments = QCheckBox("Custom Arguments")
        self.add_arguments.stateChanged.connect(self.toggle_argument_input)
        checkbox_layout.addWidget(self.add_arguments)

        self.argument_input = QLineEdit()
        self.argument_input.setPlaceholderText("Enter script arguments here... (e.g. -v)")
        self.argument_input.setEnabled(False)
        self.argument_input.setVisible(False)
        checkbox_layout.addWidget(self.argument_input)

        bottom_layout.addLayout(checkbox_layout)
        
        self.layout.addLayout(bottom_layout)

        self.apply_theme()

        # Perform initial checks to set the correct state and size
        self.toggle_keep_console()
        self.update_window_height()

    def get_file_from_dialog(self):
        """Open file dialog to select a Python script."""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Python files (*.py *.pyw)")
        dialog.setViewMode(QFileDialog.Detail)
        
        if dialog.exec():
            files = dialog.selectedFiles()
            if files:
                return files[0]
        return None

    def open_in_ide(self):
        """Open the selected file in the configured IDE."""
        if not self.file_path:
            self.show_error("No file selected to open in IDE.")
            return
        ide_path = self.config.get("ide", "")
        if not ide_path:
            self.show_error("IDE path not configured in config.json.")
            return
        
        try:
            subprocess.run(f'"{ide_path}" "{self.file_path}"', shell=True, check=True)
            self.close()
        except Exception as e:
            self.show_error(f"Error opening IDE: {e}")

    def run_in_console(self):
        """Run the selected file in the configured console."""
        if not self.file_path:
            self.show_error("No file selected to run in Console.")
            return

        console_path = self.config.get("console", "")
        if not console_path:
            self.show_error("Console path not configured in config.json.")
            return

        python_path = self.find_python_executable()
        if not python_path:
            self.show_error("Could not find Python executable in PATH")
            return

        file_dir = os.path.dirname(os.path.abspath(self.file_path))
        arguments = self.argument_input.text().strip()

        try:
            if self.silent_mode.isChecked():
                pythonw_path = python_path.replace("python.exe", "pythonw.exe")
                if not os.path.exists(pythonw_path):
                    self.show_error("Could not find pythonw.exe for silent execution")
                    return
                
                command = f'start /b "" "{pythonw_path}" "{self.file_path}" {arguments}'
            else:
                if "powershell" in console_path.lower():
                    no_exit_flag = "-NoExit" if self.keep_console.isChecked() else ""
                    command = f'start "" "{console_path}" {no_exit_flag} -Command "cd \'{file_dir}\' ; & \'{python_path}\' \'{self.file_path}\' {arguments}"'
                else:  # Default to cmd
                    keep_flag = "/K" if self.keep_console.isChecked() else "/C"
                    command = f'start "" cmd {keep_flag} "cd /d {file_dir} && "{python_path}" "{self.file_path}" {arguments}"'
            
            subprocess.run(command, shell=True, check=True)
            self.close()
        except Exception as e:
            self.show_error(f"An error occurred while launching: {e}")

    def find_python_executable(self):
        """Find the Python executable path."""
        if os.name == 'nt':
            try:
                result = subprocess.run(['where', 'python'], capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip().split('\n')[0]
            except Exception:
                pass
        else:
            path = shutil.which('python3') or shutil.which('python')
            if path:
                return path
        return None

    def apply_theme(self):
        """Apply the dark theme to the application."""
        background = DARK_THEME["background"]
        text = DARK_THEME["text"]
        self.setStyleSheet(f"background-color: {background}; color: {text};")

    def show_error(self, message):
        """Show an error message in a message box."""
        QMessageBox.critical(self, "Error", message)

    def save_checkbox_state(self):
        """Save the state of the checkboxes to the config."""
        self.config["keep_console"] = self.keep_console.isChecked()
        self.config["silent_mode"] = self.silent_mode.isChecked()
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, CONFIG_PATH)
            with open(config_path, "w") as file:
                json.dump(self.config, file, indent=4)
        except Exception as e:
            self.show_error(f"Error saving config: {e}")

    def edit_config(self):
        """Open setup dialog to edit configuration."""
        dialog = SetupDialog(existing_config=self.config)
        if dialog.exec():
            new_config = dialog.get_paths()
            new_config["keep_console"] = self.config.get("keep_console", True)
            if not new_config["ide"] and self.config.get("ide"):
                new_config["ide"] = self.config["ide"]
            if not new_config["console"] and self.config.get("console"):
                new_config["console"] = self.config["console"]
            self.config = new_config
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                config_path = os.path.join(script_dir, CONFIG_PATH)
                with open(config_path, "w") as file:
                    json.dump(self.config, file, indent=4)
            except Exception as e:
                self.show_error(f"Error saving config: {e}")

    def select_new_file(self):
        """Open file dialog to select a new Python script."""
        new_file = self.get_file_from_dialog()
        if new_file:
            self.file_path = new_file
            filename = os.path.basename(self.file_path)
            self.setWindowTitle(f"{base_title} | {filename}")
            self.silent_mode.setVisible(self.is_pyw_file())
            self.toggle_keep_console()

    def is_pyw_file(self):
        """Check if current file has .pyw extension."""
        return bool(self.file_path) and self.file_path.lower().endswith('.pyw')

    def toggle_keep_console(self):
        """Enable or disable the keep_console checkbox based on silent_mode state."""
        if self.silent_mode.isChecked() and self.silent_mode.isVisible():
            self.keep_console.setEnabled(False)
        else:
            self.keep_console.setEnabled(True)

        self.update_window_height()  # Update height based on current state

    def toggle_argument_input(self):
        """Enable or disable the argument input box based on the checkbox state."""
        is_checked = self.add_arguments.isChecked()
        self.argument_input.setEnabled(is_checked)
        self.argument_input.setVisible(is_checked)

        self.update_window_height()  # Update height based on current state

    def update_window_height(self):
        """Update the window height based on the visibility of checkboxes."""
        if self.add_arguments.isChecked() and self.is_pyw_file():
            self.setFixedHeight(WINDOW_HEIGHT_WITH_PYW_AND_ARGUMENTS)  # Height when both are checked
        elif self.add_arguments.isChecked():
            self.setFixedHeight(WINDOW_HEIGHT_WITH_ARGUMENTS)  # Height when only arguments are checked
        elif self.is_pyw_file():  # Check if the current file is a .pyw file
            self.setFixedHeight(WINDOW_HEIGHT_WITH_PYW)  # Height when .pyw file is selected
        else:
            self.setFixedHeight(WINDOW_HEIGHT_DEFAULT)  # Reset height when neither is checked

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    launcher = LauncherApp(file_path)
    launcher.show()
    sys.exit(app.exec())
