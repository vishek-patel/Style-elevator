from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown


import os
import re
import hashlib
from collections import defaultdict
from colorama import Fore, init
import pyfiglet
import hashlib
import time
import uuid


# Initialize colorama for colored output
init(autoreset=True)


# Initialize rich console
console = Console()

# Initialize colorama for colored output
init(autoreset=True)

def print_header(first_time=True):
    if first_time:
        header = pyfiglet.figlet_format("CSS Inline Style Remover", font="slant")
        print(Fore.CYAN + header)

def display_header():
    header_markdown = """
**Author**: Vishek-Patel

This tool automatically moves inline styles to a global CSS file, helping in cleaning up **HTML**,**HTM**,**JS** and **JSP** files by extracting inline CSS into separate CSS files.\n
"""
    console.print(Markdown(header_markdown))

def get_user_input():
    file_type_prompt = """
Select the file type to process:

1) HTML (*.html)
2) HTM (*.htm)
3) JSP (*.jsp)
4) JS (*.js)

"""
    console.print((file_type_prompt))
    file_extension_choices = {"1": "html", "2": "htm", "3": "jsp","4": "js" }
    file_extension = Prompt.ask("[bold yellow]\nEnter your choice[/]", choices=["1", "2","3","4"], default="1", show_choices=True)
    
    directory = Prompt.ask("[bold cyan]\nEnter the directory to process[/]")
    css_directory = Prompt.ask("[bold cyan]Enter the output CSS directory[/]")
    separator = Prompt.ask("[bold cyan]Enter a separator to use in the 'global.css' file[/]", default="Update")

    return file_extension_choices[file_extension], directory, css_directory, separator

def display_completion_message():
    completion_message = "Processing complete. Check 'global.css' for the consolidated styles."
    console.print(Panel(completion_message, expand=False))

def display_continue_prompt():
    continue_prompt = "\nWould you like to process another directory? Press [bold]5[/] to continue or [bold]9[/] to exit."
    choice = Prompt.ask(continue_prompt, choices=["5", "9"], default="9")
    return choice == "5"

def generate_class_name(filename, counter):
    # Replace . with _ in filename for Angular components
    print(filename)
    filename = filename.replace('.', '_')
    base_name = os.path.splitext(os.path.basename(filename))[0]
    return f"{base_name}_{counter}"

def has_variables(style):
    # Patterns to match various templating languages, embedded expressions, and React JSX
    patterns = [
        r'\$\{[^}]+\};?' # JavaScript Template Literals, JSP ${}
        r'@\{[^}]+\}',   # ASP.NET Razor Syntax
        r'\{\{[^}]+\}\}', # Angular, Vue, Handlebars, etc.
        r'<%=[^%>]+%>',  # JSP Scriptlet Expressions
        r'#{[^}]+}',     # Ruby on Rails, Spring EL
        r'\{[^}]+\}',    # React JSX expression (simplified single curly braces for any embedded JS expression)
    ]
    
    # Check if the style contains any of the patterns
    for pattern in patterns:
        if re.search(pattern, style):
            return True
    return False

def generate_hash(style_content):
    """Generate a unique identifier for a given style content using MD5 and a unique timestamp."""
    # MD5 hash of the style content for consistency.
    content_hash = hashlib.md5(style_content.encode()).hexdigest()[:8]
    # Generate a unique identifier based on the current time in milliseconds.
    unique_id = uuid.uuid1().hex[:8]  # Using UUID version 1 for a time-based unique component.
    # Combine both to ensure uniqueness even if the style content repeats.
    return f"{unique_id}"
    
# Define critical properties that absolutely need `!important`
# Leave this list empty to apply `!important` to all properties.
critical_properties = ["position", "z-index", "top", "right", "bottom", "left"]

def apply_important_if_critical(style_content):
    important_style = ""
    for property in style_content.split(";"):
        property = property.strip()
        if property:
            # Split the property to analyze its name and value
            prop_name = property.split(":")[0].strip()
            # If critical_properties is empty or the property name is in the list, add `!important`
            if not critical_properties or prop_name in critical_properties:
                if "!" not in property:
                    important_style += f"{property} !important; "
                else:
                    important_style += f"{property}; "
            else:
                important_style += f"{property}; "
    return important_style.strip()

# The rest of your script, including the `process_files` function, remains the same.


def check_for_ngStyle(line, filename, line_number, manual_files):
    """
    Check if the given line contains [ngStyle] or *ngStyle.
    If found, add the file and line number to manual_files list.
    """
    if '[ngStyle]' in line or '*ngStyle' in line:
        manual_files.append(f"{filename} at line {line_number} requires manual checking for [ngStyle] or *ngStyle.")

def check_for_jsp(line, filename, line_number, manual_files):
    """
    Check if any style attribute within the line contains JSP variables.
    If found, add the file and line number to manual_files list.
    """
    # Find all style attributes in the line
    style_attributes = re.findall(r'style="([^"]*)"', line)

    for style in style_attributes:
        # Check if the style string contains JSP variables or similar patterns
        if has_variables(style):
            manual_files.append(f"{filename} at line {line_number} requires manual checking for JSP variables in style attributes")
            break  # Stop after finding the first instance to avoid duplicate messages for the same line


def process_files(directory, file_extension, css_directory, manual_files, separator):
    global_css_filename = 'global.css'
    global_css_path = os.path.join(css_directory, global_css_filename)
    os.makedirs(css_directory, exist_ok=True)
    styles_to_classname = defaultdict(lambda: defaultdict(str))

    need_separator = os.path.exists(global_css_path) and os.path.getsize(global_css_path) > 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(f".{file_extension}"):
                is_angular_component = filename.endswith(".component.html")
                scss_path = os.path.join(root, filename.replace(".component.html", ".component.scss")) if is_angular_component else None
                
                file_path = os.path.join(root, filename)

                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                unique_styles = {}
                modified = False
 
                matches = re.finditer(r'<[^>]*?\s*style\s*=\s*(["\'])(.*?)\1[^>]*?>', content, re.DOTALL)



                for match in matches:
                    full_tag = match.group(0)
                    inline_style = match.group(2).strip()

                    if '[ngStyle]' in full_tag or '*ngStyle' in full_tag:
                        # manual_files.append(f"{filename} requires manual checking for [ngStyle] or *ngStyle.")
                        continue

                    if has_variables(inline_style):
                        # manual_files.append(f"{filename} requires manual review due to variables in inline style.")
                        continue

                    style_hash = generate_hash(inline_style)
                    new_class_name = f"{os.path.splitext(os.path.basename(filename))[0].replace('.', '_')}_{style_hash}"
                    
                    # if inline_style not in unique_styles:
                    unique_styles[new_class_name] = inline_style
                    modified = True

                        # Detect existing class attribute and prepare modifications
                    class_attr_match = re.search(r'class="([^"]*)"', full_tag)
                    if class_attr_match:
                        existing_classes = class_attr_match.group(1)
                        new_classes = f"{existing_classes} {new_class_name}"
                        new_tag = re.sub(r'class="[^"]*"', f'class="{new_classes}"', full_tag, 1)
                    else:
                        # If class attribute does not exist, add one
                        new_tag = re.sub(r'style="[^"]*"', f'class="{new_class_name}"', full_tag, 1)

                    new_tag = re.sub(r'\s*style\s*=\s*(["\']).*?\1', '', new_tag, flags=re.DOTALL, count=1)



                    content = content.replace(full_tag, new_tag)
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)

                css_output_path = scss_path if scss_path and os.path.exists(scss_path) else global_css_path
                need_separator = os.path.exists(css_output_path) and os.path.getsize(css_output_path) > 0

                with open(css_output_path, 'a' if need_separator else 'w', encoding='utf-8') as css_file:
                    if need_separator and unique_styles:
                        css_file.write(f"\n\n/* {separator} */\n")
                    for class_name, style in unique_styles.items():
                        important_style = apply_important_if_critical(style)
                        css_file.write(f".{class_name} {{ {important_style} }}\n")

def check_files(directory, file_extension, css_directory, manual_files, separator):

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(f".{file_extension}"):

                file_path = os.path.join(root, filename)
                unique_styles = {}

                with open(file_path, 'r') as file:
                    lines = file.readlines()
                for line_number, line in enumerate(lines, 1):
                    check_for_ngStyle(line, filename, line_number, manual_files)
                    check_for_jsp(line, filename, line_number, manual_files)

def print_manual_files(manual_files):
    if manual_files:
        print(Fore.RED + "\nThe following files may require manual processing:")
        for file in manual_files:
            print(Fore.RED + file)


def main():
    print_header()
    display_header()
    while True:

        file_extension, directory, css_directory, separator = get_user_input()
        manual_files = []  # Initialize manual_files list for each run
        check_files(directory, file_extension, css_directory, manual_files, separator)
        process_files(directory, file_extension, css_directory, manual_files, separator)
        print_manual_files(manual_files)
        display_completion_message()
        
        if not display_continue_prompt():
            break

if __name__ == "__main__":
    main()
