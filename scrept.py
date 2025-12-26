from playwright.sync_api import sync_playwright
import time

def automate_login():
    # استخدام Playwright مع إعدادات تضمن الرؤية وتجاوز الأخطاء
    with sync_playwright() as p:
        # تشغيل المتصفح في وضع مرئي مع تبطئة العمليات لرؤيتها
        browser = p.chromium.launch(headless=False, slow_mo=800, ignore_https_errors=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        try:
            # --- المرحلة 1: تسجيل الدخول الأول ---
            print("الخطوة 1: الانتقال إلى بوابة SSL-VPN...")
            page.goto("https://82.151.70.88:10443/remote/login?lang=en")

            print("الخطوة 2: إدخال بيانات ven169...")
            page.wait_for_selector("#username")
            page.fill("#username", "ven169")
            page.fill("#credential", "V@112025")

            print("الخطوة 3: النقر على Login...")
            page.click("#login_button")

            # --- المرحلة 2: النقر على E-Select ---
            print("الخطوة 4: انتظار ظهور E-Select والنقر عليه...")
            # ننتظر ظهور العنصر الذي يحتوي على نص E-Select
            # قد تفتح هذه الخطوة صفحة جديدة أو تغير محتوى الصفحة الحالية
            page.wait_for_selector("text=E-Select", timeout=45000)
            
            # التعامل مع احتمال فتح صفحة في تبويب جديد
            with context.expect_page() as new_page_info:
                page.click("text=E-Select")
            
            # الصفحة الجديدة (تبويب E-Select)
            e_select_page = new_page_info.value
            e_select_page.wait_for_load_state("networkidle")
            print("الخطوة 5: تم فتح صفحة E-Select بنجاح.")

            # --- المرحلة 3: تسجيل الدخول الثاني (E-Select) ---
            print("الخطوة 6: إدخال بيانات a.beddi@gmail.com...")
            
            # استخدام محددات CSS قوية بناءً على الكود المرفق
            # ننتظر ظهور الحقل باستخدام ID لضمان الدقة
            e_select_page.wait_for_selector("#email", timeout=30000)
            
            # محاولة التركيز على الحقل قبل الكتابة لضمان التفاعل
            e_select_page.focus("#email")
            e_select_page.fill("#email", "a.beddi@gmail.com")
            
            e_select_page.focus("#password")
            e_select_page.fill("#password", "87654321")

            print("الخطوة 7: النقر على زر Connexion...")
            # النقر على الزر باستخدام فئته (class) أو النص الموجود عليه
            e_select_page.click("button.btn-outline-primary")

            print("اكتملت العملية بنجاح. السكربت سيظل مفتوحاً حتى تغلقه يدوياً.")
            # منع السكربت من الإغلاق
            while True:
                time.sleep(1)

        except Exception as e:
            print(f"حدث خطأ: {e}")
            print("سيظل المتصفح مفتوحاً للمعاينة.")
            while True:
                time.sleep(1)

if __name__ == "__main__":
    automate_login()
