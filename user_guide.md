
![image](https://github.com/vishek-patel/Style-elevator/assets/85006315/b64afff2-afd6-43c5-8721-25aa5ecd203f)



Follow the prompts to select file type, specify input directory, output CSS directory, and optional separator for the global CSS file.

Upon completion, review the processed files and the generated global CSS file in the specified output directory.

If any files require manual processing (due to inline styles with dynamic content), they will be listed after processing. Review these files and make necessary adjustments.

## Example Usage

Suppose you have a directory named `home/web` containing HTML files with inline styles. To process these files and generate a global CSS file:

1. Run the script `style_elevator.py`.
2. Select the file type (HTML).
3. Enter the directory path (`home/web` or the `src` directory in case of angular application) containing your HTML files.
4. Specify the output CSS directory (e.g., `home/web/css` or the `src` directory in case of angular application).
5. Optionally, provide a separator for the global CSS file.
6. Review the processed files and the generated global CSS file in the `home/web/css` or the `src` directory in case of angular application.

## Contribution

Contributions are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This tool utilizes the `rich` library for enhanced console output.

