from website import create_app
import webbrowser
import threading
import sys

# создаем экземпляр приложения Flask
app = create_app()

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
   
    if getattr(sys, 'frozen', False):
        threading.Timer(1, open_browser).start()
    
    # запускаем Flask сервер
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)