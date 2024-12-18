# VK Link Shortener

This Python script shortens URLs and tracks the number of clicks using the [VK API](https://vk.com). The script is designed for quick link shortening and monitoring their popularity in a convenient text format.

---

## Features
- Shortens links using the VK API.
- Tracks the number of clicks on shortened links.
- Handles both shortened (`vk.cc`) and regular URLs.
- Provides clear and concise output.

---

## Prerequisites
- Python 3.6 or later
- A `requirements.txt` file specifying dependencies

---

## Installation and Setup

1. **Clone the repository or download the script:**  
   Ensure you have the `main.py` script and the `requirements.txt` file.

2. **(Optional) Create and activate a virtual environment:**  
   While not strictly required, using a virtual environment is recommended to avoid conflicts with other Python packages.
   ```bash
   python -m venv venv
   source venv/bin/activate       # Linux/macOS
   venv\Scripts\activate          # Windows
   
3. **Install dependencies from requirements.txt:**
This ensures consistent and tested versions of the packages.
   ```bash
   pip install -r requirements.txt
   
4. **Configure environment variables:**
Before running this application, you need to properly configure your environment variables. This is done by creating a `.env` file in the project root directory (the same directory where you run the script) and defining the required variables.

   Required Environment Variables
   
   - **VK_API_TOKEN**  
     *Type:* String  
     *Description:* This variable holds your VK API token, which grants you access to VK's URL shortening and link statistics methods. Without a valid token, the program will not be able to shorten links or retrieve click counts.  
     *Example:*  
     ```env
     VK_API_TOKEN=your_vk_api_access_token_here


5. **Usage:**
   ```bash
   python main.py <url>
   ```
 ```
(.venv) (base) % python main.py https://google.com  
Shorted link:  https://vk.cc/c8PCB4
(.venv) (base) % python main.py https://vk.cc/c8PCB4
Your link was clicked 0 times
```