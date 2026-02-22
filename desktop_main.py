import webview
import threading
import uvicorn
import sys
import os
import time
import requests
import logging

# Setup Logging to Console and File
handlers = [logging.FileHandler("desktop_debug.log")]
if sys.stdout:
    handlers.append(logging.StreamHandler(sys.stdout))

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=handlers
)

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}/?app=desktop"

def wait_for_server():
    """Waits for the server to be up."""
    retries = 10
    while retries > 0:
        try:
            response = requests.get(URL)
            if response.status_code == 200:
                logging.info("Server is up and running!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        logging.info(f"Waiting for server... ({retries})")
        time.sleep(1)
        retries -= 1
    logging.error("Server failed to start.")
    return False

def start_server():
    from backend.main import app
    try:
        logging.info("Starting Uvicorn...")
        uvicorn.run(app, host=HOST, port=PORT, log_level="info")
    except Exception as e:
        logging.error(f"Uvicorn error: {e}")

if __name__ == '__main__':
    # Support for PyInstaller
    if getattr(sys, 'frozen', False):
        # If run as exe, change cwd to the executable folder
        base_dir = os.path.dirname(sys.executable)
        # In PyInstaller 6+, assets are often in _internal
        internal_dir = os.path.join(base_dir, '_internal')
        if os.path.exists(internal_dir):
            os.chdir(internal_dir)
        else:
            os.chdir(base_dir)
        
    logging.info("--- Launching Convertly Desktop ---")
    
    # Fix Taskbar Icon on Windows
    # This decouples the app from the python.exe icon
    if os.name == 'nt':
        try:
            import ctypes
            appid = 'convertly.background.remover.v1' 
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
        except Exception as e:
            logging.error(f"Failed to set AppUserModelID: {e}")

    # Start Backend
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # Wait for Backend
    if not wait_for_server():
        logging.error("Could not connect to backend. Exiting.")
        sys.exit(1)

    # Icon Path
    # Windows typically requires .ico
    icon_path = os.path.join(os.path.abspath(os.getcwd()), 'frontend', 'assets', 'logo.ico')
    if not os.path.exists(icon_path):
        logging.warning(f"Icon not found at {icon_path}. Trying png...")
        icon_path = os.path.join(os.path.abspath(os.getcwd()), 'frontend', 'assets', 'logo.png')
        
    logging.info(f"Using icon: {icon_path}")

    def set_icon_windows():
        import ctypes
        import time
        
        # Wait for window to invoke
        time.sleep(1) 
        
        title = "Convertly - Background Remover"
        
        # Retry finding window
        retries = 20
        hwnd = None
        while retries > 0:
            hwnd = ctypes.windll.user32.FindWindowW(None, title)
            if hwnd:
                break
            time.sleep(0.5)
            retries -= 1
            
        if hwnd:
            logging.info(f"Found window handle: {hwnd}. Setting icon...")
            # Load Image
            # LR_LOADFROMFILE (0x10) | LR_DEFAULTSIZE (0x40)
            h_icon = ctypes.windll.user32.LoadImageW(
                None, 
                icon_path, 
                1, # IMAGE_ICON
                0, 0, 
                0x00000010
            )
            
            if h_icon:
                # WM_SETICON = 0x80
                # ICON_SMALL (0) and ICON_BIG (1)
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 0, h_icon)
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 1, h_icon)
                logging.info("Icon set successfully via ctypes.")
            else:
                logging.error(f"Failed to load icon via ctypes. Error: {ctypes.GetLastError()}")
        else:
            logging.error("Could not find window to set icon.")

    # Start Icon Thread
    if os.name == 'nt' and icon_path and os.path.exists(icon_path):
        threading.Thread(target=set_icon_windows, daemon=True).start()

    logging.info("Creating window...")
    try:
        window = webview.create_window(
            'Convertly - Background Remover', 
            f"{URL}&cb={int(time.time())}", 
            width=1200, 
            height=800,
            resizable=True
        )
        logging.info("Window created. Starting loop...")
        webview.start(debug=False)
        logging.info("Application loop finished.")
    except Exception as e:
        logging.exception("Critical error in main loop:")
        input("Press Enter to close window...") # Keep console open on error
