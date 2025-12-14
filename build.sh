#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- بدء تنفيذ سكربت البناء (build.sh) ---"

echo "1. تثبيت اعتماديات Python من requirements.txt..."
pip install -r requirements.txt

echo "2. إنشاء مجلد محلي للاعتماديات (deps)..."
mkdir -p deps

echo "3. تحميل وتثبيت Google Chrome و ChromeDriver في المجلد المحلي..."
# هذا السكربت مقتبس من مستودعات Render الرسمية للتعامل مع نظام الملفات للقراءة فقط
# تحديد أحدث إصدار متوافق من Chrome
CHROME_VERSION=$(curl -sS https://google-chrome-for-testing.appspot.com/latest-patch-versions-per-build | grep -E "125.0.6422" | cut -d'.' -f1-4)
# تحديد رابط تحميل ChromeDriver المطابق
CHROME_DRIVER_VERSION=$(curl -sS https://google-chrome-for-testing.appspot.com/latest-patch-versions-per-build-with-downloads | grep -A 5 "chromedriver" | grep "${CHROME_VERSION}" -A 4 | grep "linux64" -A 3 | grep "url" | cut -d'"' -f4)

# تحميل ملفات Chrome و ChromeDriver المضغوطة
wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chrome-linux64.zip -P ./deps
wget -N ${CHROME_DRIVER_VERSION} -P ./deps

# فك ضغط الملفات في المجلد المحلي
unzip ./deps/chrome-linux64.zip -d ./deps
unzip ./deps/chromedriver-linux64.zip -d ./deps

# حذف الملفات المضغوطة لتوفير المساحة
rm ./deps/chrome-linux64.zip ./deps/chromedriver-linux64.zip

# إعطاء صلاحيات التنفيذ للملفات
chmod +x ./deps/chromedriver-linux64/chromedriver
chmod +x ./deps/chrome-linux64/chrome

echo "--- اكتمل التثبيت المحلي لـ Chrome و ChromeDriver بنجاح ---"
