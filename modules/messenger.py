import time
import pywhatkit as pwk
from modules.storage import log_message

def send_whatsapp_messages(messages, dry_run=True, wait_time=15):
    for m in messages:
        phone = m["phone"]
        msg = m["message"]

        if dry_run:
            print(f"[DRY-RUN] Would send to {phone}: {msg}")
            log_message(phone, msg, status="DRY-RUN")
        else:
            try:
                pwk.sendwhatmsg_instantly(
                    phone_no=phone,
                    message=msg,
                    wait_time=wait_time,
                    tab_close=True
                )
                print(f"[SENT] {phone}: {msg}")
                log_message(phone, msg, status="SENT")
                time.sleep(2)
            except Exception as e:
                print(f"[ERROR] Could not send to {phone}: {e}")
                log_message(phone, msg, status="ERROR")
