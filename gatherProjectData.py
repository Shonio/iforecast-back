import os

import pyclip

include_files = []

exceptions = [
    ".\\logs",
    ".\\.git",
    ".\\venv",
    ".\\.idea",
    "gunicorn_config.py",
    "requirements.txt",
    "run.py",
    "__pycache__",
    "README.md",
    "gatherProjectData.py",
    "passGenerator.py",
    "format.bat",
    "requirements-dev.txt",
    ".gitignore",
]


def collect_all_project_files():
    # Collect all files in the project ./
    files = []
    for root, dirs, filenames in os.walk("."):
        for filename in filenames:
            if (
                (
                    filename in include_files
                    or root.startswith(tuple(include_files))
                    or any(include_file in root for include_file in include_files)
                )
                and (
                    not root.startswith(
                        tuple(
                            [
                                ".\\.git",
                                ".\\venv",
                                ".\\.idea",
                            ]
                        )
                    )
                )
            ) or (
                not root.startswith(tuple(exceptions))
                and not any(exception in root for exception in exceptions)
                and filename not in exceptions
            ):
                files.append((root, filename))

    return files


def gather_file_content(files):
    # Go through all files and collect their content to array
    file_content = []
    for file in files:
        with open(file[0] + "\\" + file[1], "r") as f:
            # Trim content and remove empty lines and spaces from the end of the file
            # Skip file if it is empty
            content = f.read().strip()
            if content:
                # Insert filename as a comment in the beginning of the file to content
                content = f"# Path: '{file[0]}\\{file[1]}\n" + content
                file_content.append(content)

    # Add '---' in file_content to start and end of array
    file_content.insert(0, "")
    file_content.append("")

    # Convert array to string with separator '\n---\n'
    file_content = "\n---\n".join(file_content)

    return file_content.strip()


if __name__ == "__main__":
    project_files = collect_all_project_files()
    print(project_files)
    project_content = gather_file_content(project_files)

    # Set project_content to clipboard
    pyclip.clear()
    pyclip.copy(project_content)

    print("===================================")
    print(project_content)
    print("===================================")
