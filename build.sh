#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- بدء تنفيذ سكربت البناء (build.sh) ---"

echo "1. تثبيت اعتماديات Python من requirements.txt..."
pip install -r requirements.txt

echo "2. إنشاء مجلد محلي للاعتماديات (deps)..."
mkdir -p deps

echo "3. تحميل وتثبيت Google Chrome و ChromeDriver في المجلد المحلي..."
# نستخدم نقطة نهاية JSON الجديدة للحصول على أحدث إصدارات Chrome المستقرة
JSON_URL="https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

echo "جلب أحدث روابط التحميل من $JSON_URL"

# جلب بيانات JSON مرة واحدة وتخزينها
JSON_DATA=$(curl -sS "$JSON_URL")

# استخراج روابط التحميل لـ Chrome و ChromeDriver لمنصة linux64
# نفترض أن jq مثبت في بيئة البناء
CHROME_URL=$(echo "$JSON_DATA" | jq -r '.channels.Stable.downloads.chrome[] | select(.platform=="linux64") | .url')
CHROME_DRIVER_URL=$(echo "$JSON_DATA" | jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url')

# تحميل ملفات Chrome و ChromeDriver المضغوطة
echo "تحميل Chrome من: $CHROME_URL"
wget -N "$CHROME_URL" -O ./deps/chrome-linux64.zip

echo "تحميل ChromeDriver من: $CHROME_DRIVER_URL"
wget -N "$CHROME_DRIVER_URL" -O ./deps/chromedriver-linux64.zip

# فك ضغط الملفات في المجلد المحلي
unzip ./deps/chrome-linux64.zip -d ./deps
unzip ./deps/chromedriver-linux64.zip -d ./deps

# حذف الملفات المضغوطة لتوفير المساحة
rm ./deps/chrome-linux64.zip ./deps/chromedriver-linux64.zip

# إعطاء صلاحيات التنفيذ للملفات
chmod +x ./deps/chromedriver-linux64/chromedriver
chmod +x ./deps/chrome-linux64/chrome

echo "--- اكتمل التثبيت المحلي لـ Chrome و ChromeDriver بنجاح ---"
