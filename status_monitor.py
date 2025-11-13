# pip install pyrogram
# pip install tgcrypto # מומלץ להצפנה מהירה יותר

import asyncio
from pyrogram import Client
from pyrogram.enums import UserStatus
from datetime import datetime
import time
import os

# # --- 1. הגדרות ופרטים אישיים ---
# # החלף בפרטים האישיים שקיבלת מ-my.telegram.org
# API_ID = 35201131 
# API_HASH = "97c583f940630bd892cffaae45808d62" 

# # המשתמש שאחריו נרצה לעקוב (שם משתמש או ID מספרי)
# TARGET_USER = "@Eitamooom" 

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH") 
TARGET_USER = os.environ.get("TARGET_USER", "@DefaultUser") # אם אין משתנה, השתמש בברירת מחדל

# הוסף את המשתנים הבאים כדי להימנע מאימות אינטראקטיבי
PHONE_NUMBER = os.environ.get("PHONE_NUMBER") 
SESSION_STRING = os.environ.get("SESSION_STRING", "my_session") # ניתן להשתמש ב-Session String (ראה הערה 2)


# כמה זמן לחכות בין בדיקות (בשניות)
CHECK_INTERVAL = 5

# קובץ לתיעוד השינויים (LOG)
LOG_FILE = "status_log.txt"
# -----------------------------------

# יצירת מופע של ה-Client
app = Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

async def monitor_status():
    """פונקציה אסינכרונית לביצוע המעקב."""
    print("🤖 מתחבר לטלגרם כמשתמש...")
    await app.start()
    print("✅ מחובר בהצלחה!")
    
    # 1. משיכת אובייקט המשתמש בפעם הראשונה
    try:
        user = await app.get_users(TARGET_USER)
    except Exception as e:
        print(f"❌ שגיאה במשיכת המשתמש {TARGET_USER}: {e}")
        await app.stop()
        return

    # אתחול סטטוס נוכחי
    current_status = user.status
    print(f"🔄 מתחיל מעקב")


    while True:
        try:
            # 2. בדיקת הסטטוס המעודכן
            updated_user = await app.get_users(TARGET_USER)
            new_status = updated_user.status
            
            # 3. השוואת הסטטוסים ותיעוד שינויים
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if new_status == UserStatus.ONLINE:
                print(f"[{timestamp}] online")
            else:
                if updated_user.last_online_date:
                    print(f"[{timestamp}] last seem at: {updated_user.last_online_date}, status: {new_status}")
                else:
                    print(f"[{timestamp}] next_offline_date: {updated_user.next_offline_date}")

            current_status = new_status
            
            # 5. המתנה לבדיקה הבאה
            await asyncio.sleep(CHECK_INTERVAL)

        except Exception as e:
            print(f"🛑 אירעה שגיאה במהלך הלולאה: {e}")
            print("מנסה להתחבר שוב בעוד 30 שניות...")
            await asyncio.sleep(30)
        
if __name__ == "__main__":
            
    # הרצת הפונקציה האסינכרונית
    app.run(monitor_status())