from Upload import Upload
import os, sys, time

class SuppressPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

print("Logging in...")
with SuppressPrints():
    driver = Upload.login()
if driver == "error":
    print("There was a problem, please retry.")
else:
    print("Login success!")
    print("Beginning upload...")
    try:
        Upload.upload(driver,"C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\vid.mp4")

    except Exception:
        print("ERROR UPLOADING")
        print(Exception)
        time.sleep(300)
        driver.quit()