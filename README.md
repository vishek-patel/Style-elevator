![image](https://github.com/vishek-patel/Style-elevator/assets/85006315/600146c3-4b34-46f7-baab-433ca4f1a511)

# Style Elevator (CSS Inline Style Remover Tool)

The CSS Inline Style Remover Tool is a Python utility designed to streamline the process of removing inline styles from HTML, HTM, JSP, and JS files and consolidating them into a single, reusable CSS file. This tool promotes the separation of concerns between content and presentation, making it easier to maintain and organize web projects.

## Key Features

- **Automatic Extraction:** Automatically identifies and extracts inline CSS styles from specified files.
- **Consolidation:** Consolidates extracted styles into a global CSS file for easy management. ( In case of Angular , it will move the extracted styles to respective 'scss/css' files )
- **User-Friendly Interface:** Utilizes the command-line interface with enhanced features for clear interaction.
- **Customization:** Allows users to specify input and output directories, file types, and separator for CSS consolidation.

## Prerequisites

- Python 3.x installed on your system.
- Basic understanding of working with command-line interfaces.

## Installation

1. Clone or download the repository from GitHub:

    ```
    git clone https://github.com/your_username/css-inline-style-remover.git
    ```

2. Install the required dependencies from the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```
3. Create the virtual environment:

    ```bash
    python3 -m venv venv
    ```
4. Activate the virtual environment:

    - **Windows:**

    ```bash
    venv\Scripts\activate
    ```

    - **Unix/macOS:**

    ```bash
    source venv/bin/activate
    ```
5. Run the script:

    ```bash
    python3 style_elevator.py
    ```



## Getting Started

1. Open your terminal or command prompt.
2. Navigate to the directory where you have cloned or downloaded the tool.

## Usage

Run the script `style_elevator.py` using Python:
 ```
 python3 style_elevator.py
 ```

