from pyrogram import Client

api_id = 35201131 
api_hash = "97c583f940630bd892cffaae45808d62" 

# הפונקציה export_session_string תבקש ממך מספר טלפון וקוד אימות פעם אחת.
with Client("my_session_for_railway", api_id=api_id, api_hash=api_hash) as app:
    # הפלט הוא המחרוזת הארוכה והמכילה את הסשן
    session_string = app.export_session_string()
    print("\n--- Session String ---")
    print(session_string)
    print("----------------------\n")