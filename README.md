# URL Shortener

This Python script provides a GUI application to shorten long URLs into compact versions using the TinyURL service. The tool is user-friendly and allows users to easily input a long URL, generate a shortened URL, and copy it to their clipboard.

## Features

- **TinyURL Integration**: Utilizes the TinyURL API to generate shortened URLs.
- **Interactive GUI**: Built with `Tkinter` for a simple and intuitive interface.
- **Error Handling**: Alerts users about invalid inputs or network issues.
- **Copy Functionality**: Copy the generated shortened URL directly from the app.

## How to Use

### Prerequisites

- Python 3.x installed on your system.
- `requests` library installed. Install it via pip if you don't have it:
  ```bash
  pip install requests
  ```

### Running the Script

1. Download the script from here:
2. Open Powershell and Run the script:
   ```bash
   python long2shortURL.py
   ```

3. Enter a long URL in the text field and click **Shorten URL**.
4. A new window will display the shortened URL, which can be copied easily.

### Example Usage

1. Enter a URL in the input field:
   ```
   https://www.example.com/a-very-long-url-to-shorten
   ```

2. Click the **Shorten URL** button.
3. View the shortened URL in a new window:
   ```
   http://tinyurl.com/shortened-url
   ```
4. Use the **Copy URL** button to copy the shortened URL to your clipboard.

## File Structure

```
url-shortener/
├── long2shortURL.py   # Main script for URL shortening
```

## Customization

- **API**: Replace the TinyURL API endpoint with another URL shortening service if desired.
- **GUI Elements**: Enhance the UI with additional features like a history of shortened URLs.
- **Input Validation**: Expand validation to include edge cases or support for specific URL formats.

## Troubleshooting

- **Invalid Input**: Ensure you enter a properly formatted URL.
- **Network Issues**: Check your internet connection if the script fails to connect to the API.
- **Dependencies**: Verify that the `requests` library is installed.
