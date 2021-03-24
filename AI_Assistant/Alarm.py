import json
import brain
from datetime import datetime
from MessageBox import MessageBox


class Alarm:
    reminders = ""

    def __init__(self):
        self.reminders = json.loads(open("Data/Alarm/reminders.json", encoding="utf-8").read())

    def CheckAlarm(self):
        self.reminders = json.loads(open("Data/Alarm/reminders.json", encoding="utf-8").read())
        if not self.Date(datetime.now().strftime("%d/%m/%Y")):
            return
        self.Time(datetime.now().strftime("%H:%M"))

    def SetAlarm(self):
        messageBox = MessageBox()
        text = messageBox.ShowInputBox()
        brain.Response("Tarih nedir")
        date = brain.playerInput(mic=False).replace(" ", ";")
        brain.Response("saat kaçta")
        time = brain.playerInput(mic=False).replace(" ", ";")
        self.reminders["reminders"].append({"text": text, "date": date, "time": time})
        self.SaveReminder()

    def ShowAlarm(self):
        text = ""
        for reminder in self.reminders["reminders"]:
            text = text + f"{reminder['text']}\t{reminder['date']}\t{reminder['time']}\n"
        messageBox = MessageBox()
        messageBox.ShowTextBox(text)

    def Time(self, now_time):
        for i in range(len(self.reminders["reminders"])):
            if self.reminders["reminders"][i]["time"] == now_time:
                print(f"hatırlatıcı mesajı, {self.reminders['reminders'][i]['text']}")
                messageBox = MessageBox()
                messageBox.ShowAlarmBox(self.reminders["reminders"][i]["text"])
                del self.reminders["reminders"][i]
                self.SaveReminder()
                break
            else:
                if self.reminders["reminders"][i]["time"].split(":")[0] <= now_time.split(":")[0]:
                    print(f"hatırlatıcı mesajı, {self.reminders['reminders'][i]['text']}")
                    messageBox = MessageBox()
                    messageBox.ShowAlarmBox(self.reminders["reminders"][i]["text"])
                    del self.reminders["reminders"][i]
                    self.SaveReminder()
                    break

    def Date(self, now_date):
        for reminder in self.reminders["reminders"]:
            if reminder["date"] == now_date:
                return True
        return False

    def SaveReminder(self):
        with open("Data/Alarm/reminders.json", "w") as reminders_file:
            json.dump(self.reminders, reminders_file)
