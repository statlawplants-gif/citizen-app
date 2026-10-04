from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
import requests
import json
import threading

# آدرس سرور - اگر روی همان گوشی است از localhost استفاده کنید
SERVER_URL = "http://bore.pub:29270"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        layout.add_widget(Label(text='ورود به سیستم شهروند', font_size='22sp', size_hint_y=0.2, color=(0, 0.5, 1, 1)))
        
        self.username_input = TextInput(hint_text='نام کاربری', multiline=False, size_hint_y=0.12, font_size='16sp')
        layout.add_widget(self.username_input)
        
        self.password_input = TextInput(hint_text='رمز عبور', password=True, multiline=False, size_hint_y=0.12, font_size='16sp')
        layout.add_widget(self.password_input)
        
        login_btn = Button(text='ورود', size_hint_y=0.15, background_color=(0, 0.8, 0, 1), font_size='18sp')
        login_btn.bind(on_press=self.do_login)
        layout.add_widget(login_btn)
        
        register_btn = Button(text='ثبت نام', size_hint_y=0.12, background_color=(0, 0.5, 1, 1), font_size='16sp')
        register_btn.bind(on_press=self.go_register)
        layout.add_widget(register_btn)
        
        self.add_widget(layout)
    
    def do_login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if not username or not password:
            self.show_error('لطفاً نام کاربری و رمز عبور را وارد کنید')
            return
        
        try:
            response = requests.post(f'{SERVER_URL}/api/login', 
                                   json={'username': username, 'password': password},
                                   timeout=10)
            result = response.json()
            
            if result.get('success'):
                App.get_running_app().user_data = result.get('user')
                App.get_running_app().root.current = 'main'
            else:
                self.show_error(result.get('message', 'خطا در ورود'))
        except Exception as e:
            self.show_error(f'خطا در اتصال: {str(e)}')
    
    def login_error(self, req, error):
        self.show_error('خطا در اتصال به سرور')
    
    def show_error(self, message):
        popup = Popup(title='خطا', content=Label(text=message, font_size='16sp'), size_hint=(0.8, 0.4))
        popup.open()
    
    def go_register(self, instance):
        App.get_running_app().root.current = 'register'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=12)
        
        layout.add_widget(Label(text='ثبت نام شهروند', font_size='22sp', size_hint_y=0.12, color=(0, 0.5, 1, 1)))
        
        self.username_input = TextInput(hint_text='نام کاربری', multiline=False, size_hint_y=0.1, font_size='16sp')
        layout.add_widget(self.username_input)
        
        self.password_input = TextInput(hint_text='رمز عبور', password=True, multiline=False, size_hint_y=0.1, font_size='16sp')
        layout.add_widget(self.password_input)
        
        self.name_input = TextInput(hint_text='نام و نام خانوادگی', multiline=False, size_hint_y=0.1, font_size='16sp')
        layout.add_widget(self.name_input)
        
        self.neighborhood_input = TextInput(hint_text='نام محله', multiline=False, size_hint_y=0.1, font_size='16sp')
        layout.add_widget(self.neighborhood_input)
        
        register_btn = Button(text='ثبت نام', size_hint_y=0.12, background_color=(0, 0.8, 0, 1), font_size='16sp')
        register_btn.bind(on_press=self.do_register)
        layout.add_widget(register_btn)
        
        back_btn = Button(text='بازگشت', size_hint_y=0.1, background_color=(1, 0.3, 0, 1), font_size='16sp')
        back_btn.bind(on_press=lambda x: setattr(App.get_running_app().root, 'current', 'login'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def do_register(self, instance):
        try:
            response = requests.post(f'{SERVER_URL}/api/register',
                                   json={
                                       'username': self.username_input.text.strip(),
                                       'password': self.password_input.text.strip(),
                                       'role': 'citizen',
                                       'name': self.name_input.text.strip(),
                                       'neighborhood': self.neighborhood_input.text.strip()
                                   },
                                   timeout=10)
            result = response.json()
            
            if result.get('success'):
                popup = Popup(title='موفق', content=Label(text='ثبت نام موفق بود', font_size='16sp'), size_hint=(0.8, 0.4))
                popup.open()
                App.get_running_app().root.current = 'login'
            else:
                popup = Popup(title='خطا', content=Label(text=result.get('message', 'خطا'), font_size='16sp'), size_hint=(0.8, 0.4))
                popup.open()
        except Exception as e:
            popup = Popup(title='خطا', content=Label(text=f'خطا در اتصال: {str(e)}', font_size='14sp'), size_hint=(0.8, 0.4))
            popup.open()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_image = None
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # هدر
        header = BoxLayout(size_hint_y=0.1)
        header.add_widget(Label(text='پیام‌های من', font_size='18sp', color=(0, 0.5, 1, 1)))
        layout.add_widget(header)
        
        # دکمه ارسال پیام جدید
        new_msg_btn = Button(text=' ارسال پیام جدید', size_hint_y=0.1, background_color=(0, 0.8, 0, 1), font_size='16sp')
        new_msg_btn.bind(on_press=self.show_send_form)
        layout.add_widget(new_msg_btn)
        
        # لیست پیام‌ها
        scroll = ScrollView(size_hint_y=0.7)
        self.messages_layout = GridLayout(cols=1, size_hint_y=None, spacing=8, padding=5)
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        scroll.add_widget(self.messages_layout)
        layout.add_widget(scroll)
        
        # دکمه خروج
        logout_btn = Button(text='خروج', size_hint_y=0.1, background_color=(1, 0.3, 0, 1), font_size='16sp')
        logout_btn.bind(on_press=lambda x: setattr(App.get_running_app().root, 'current', 'login'))
        layout.add_widget(logout_btn)
        
        self.add_widget(layout)
    
    def on_enter(self):
        self.load_messages()
    
    def load_messages(self):
        user_data = App.get_running_app().user_data
        if not user_data:
            return
        user_id = user_data.get('id')
        
        self.messages_layout.clear_widgets()
        
        try:
            response = requests.get(f'{SERVER_URL}/api/messages', 
                                  params={'user_id': user_id, 'role': 'citizen'},
                                  timeout=10)
            messages = response.json()
            
            if not messages:
                self.messages_layout.add_widget(Label(text='هنوز پیامی ارسال نکرده‌اید', size_hint_y=None, height=60, color=(0.5, 0.5, 0.5, 1)))
                return
            
            for msg in messages:
                msg_box = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=10, spacing=5)
                
                status_text = '🆕 جدید' if msg.get('status') == 'new' else ' ارجاع شده' if msg.get('status') == 'assigned' else '✅ تکمیل شده'
                status_color = (1, 0.8, 0, 1) if msg.get('status') == 'new' else (0, 0.5, 1, 1) if msg.get('status') == 'assigned' else (0, 0.8, 0, 1)
                
                msg_box.add_widget(Label(text=f" {msg.get('content', '')[:60]}", size_hint_y=0.4, halign='right', font_size='14sp'))
                msg_box.add_widget(Label(text=f"وضعیت: {status_text}", size_hint_y=0.3, color=status_color, font_size='13sp'))
                msg_box.add_widget(Label(text=f"📅 {msg.get('created_at', '')}", size_hint_y=0.3, font_size='11sp', color=(0.5, 0.5, 0.5, 1)))
                
                self.messages_layout.add_widget(msg_box)
        except Exception as e:
            self.messages_layout.add_widget(Label(text=f'خطا: {str(e)}', color=(1, 0, 0, 1)))
    
    def show_send_form(self, instance):
        popup = Popup(title='ارسال پیام جدید', size_hint=(0.9, 0.7))
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text='متن پیام خود را بنویسید:', size_hint_y=0.1, font_size='14sp'))
        
        self.msg_content = TextInput(hint_text='مثال: خرابی چراغ خیابان اصلی محله...', multiline=True, size_hint_y=0.4, font_size='14sp')
        layout.add_widget(self.msg_content)
        
        self.image_label = Label(text='📷 تصویری انتخاب نشده (اختیاری)', size_hint_y=0.1, font_size='13sp', color=(0.5, 0.5, 0.5, 1))
        layout.add_widget(self.image_label)
        
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        send_btn = Button(text='ارسال', background_color=(0, 0.8, 0, 1), font_size='16sp')
        send_btn.bind(on_press=lambda x: self.send_message(popup))
        btn_layout.add_widget(send_btn)
        
        cancel_btn = Button(text='انصراف', background_color=(1, 0.3, 0, 1), font_size='16sp')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        layout.add_widget(btn_layout)
        
        popup.content = layout
        popup.open()
    
    def send_message(self, popup):
        user_data = App.get_running_app().user_data
        if not user_data:
            return
        user_id = user_data.get('id')
        content = self.msg_content.text.strip()
        
        if not content:
            popup_err = Popup(title='خطا', content=Label(text='لطفاً متن پیام را وارد کنید'), size_hint=(0.8, 0.3))
            popup_err.open()
            return
        
        try:
            response = requests.post(f'{SERVER_URL}/api/messages',
                                   json={
                                       'sender_id': user_id,
                                       'content': content,
                                       'image_path': self.selected_image,
                                       'category': 'general'
                                   },
                                   timeout=10)
            result = response.json()
            
            if result.get('success'):
                popup.dismiss()
                self.load_messages()
                popup_ok = Popup(title='موفق', content=Label(text='پیام شما ارسال شد'), size_hint=(0.8, 0.3))
                popup_ok.open()
            else:
                popup_err = Popup(title='خطا', content=Label(text=result.get('message', 'خطا')), size_hint=(0.8, 0.3))
                popup_err.open()
        except Exception as e:
            popup_err = Popup(title='خطا', content=Label(text=f'خطا: {str(e)}'), size_hint=(0.8, 0.3))
            popup_err.open()

class CitizenApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data = None
    
    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    CitizenApp().run()
