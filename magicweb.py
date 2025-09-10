import sys
import traceback
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, 
                            QSplitter, QPushButton, QVBoxLayout, QWidget,
                            QHBoxLayout, QLabel, QLineEdit, QMessageBox,
                            QTextBrowser)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
import webbrowser
from datetime import datetime

class MagicWeb:
    """Самый простой язык в мире - MagicWeb"""
    
    @staticmethod
    def compile_to_html(code):
        """
        Компилирует MagicWeb код в HTML
        """
        logs = []
        html = []
        css = []
        js = []
        
        try:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                line = line.strip()
                
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('//'):
                    continue
                
                try:
                    # СУПЕР-ПРОСТОЙ АНАЛИЗ
                    if ':' in line and not line.startswith('<'):
                        # CSS стиль - проверяем валидные свойства
                        valid_properties = ['background', 'color', 'font', 'padding', 'margin', 
                                          'text-align', 'border', 'width', 'height', 'display',
                                          'flex-direction', 'justify-content', 'align-items',
                                          'opacity', 'border-radius', 'box-shadow', 'position']
                        
                        prop = line.split(':')[0].strip()
                        if prop in valid_properties:
                            if not line.endswith(';'):
                                line += ';'
                            css.append(line)
                            logs.append(f"🎨 Строка {i}: CSS - {line}")
                        else:
                            logs.append(f"⚠️ Строка {i}: Неизвестное свойство - {prop}")
                    
                    elif line.startswith(('alert ', 'log ')):
                        # JavaScript
                        if line.startswith('log '):
                            msg = line[4:].strip().replace('"', "'")
                            line = f'console.log("{msg}");'
                        elif line.startswith('alert '):
                            msg = line[6:].strip().replace('"', "'")
                            line = f'alert("{msg}");'
                        js.append(line)
                        logs.append(f"⚡ Строка {i}: JS - {line}")
                    
                    elif line.startswith('<'):
                        # HTML тег
                        html.append(line)
                        logs.append(f"📄 Строка {i}: HTML - {line}")
                    
                    else:
                        # Простой текст - превращаем в параграф
                        html.append(f"<p>{line}</p>")
                        logs.append(f"📝 Строка {i}: Текст -> {line}")
                        
                except Exception as e:
                    logs.append(f"⚠️ Строка {i}: Ошибка - {e}")
                    continue
            
            # Автогенерация красивого дизайна
            if not css:
                css = [
                    "body: background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);",
                    "body: color: white;",
                    "body: font-family: Arial, sans-serif;",
                    "body: text-align: center;",
                    "body: padding: 50px;",
                    "body: margin: 0;",
                    "h1: font-size: 48px;",
                    "h1: margin: 20px 0;",
                    "p: font-size: 20px;",
                    "p: opacity: 0.9;",
                    "button: background: #ff6b6b;",
                    "button: color: white;",
                    "button: border: none;",
                    "button: padding: 15px 30px;",
                    "button: font-size: 18px;",
                    "button: margin: 10px;",
                    "button: border-radius: 25px;",
                    "button: cursor: pointer;"
                ]
                logs.append("🎨 Автогенерация красивого CSS")
            
            # Форматируем CSS правильно
            formatted_css = []
            current_selector = None
            current_rules = []
            
            for line in css:
                if ':' in line:
                    selector, rule = line.split(':', 1)
                    selector = selector.strip()
                    rule = rule.strip()
                    
                    if current_selector != selector:
                        if current_selector and current_rules:
                            formatted_css.append(f"{current_selector} {{ {' '.join(current_rules)} }}")
                        current_selector = selector
                        current_rules = []
                    
                    current_rules.append(rule)
            
            if current_selector and current_rules:
                formatted_css.append(f"{current_selector} {{ {' '.join(current_rules)} }}")
            
            # Добавляем базовый HTML если пусто
            if not html:
                html = [
                    "<h1>🚀 MagicWeb</h1>",
                    "<p>Самый простой язык веб-разработки!</p>",
                    "<button onclick=\"alert('Всё работает! 🎉')\">Нажми меня</button>"
                ]
                logs.append("📄 Автогенерация HTML")
            
            final_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>MagicWeb</title>
                <style>
                {chr(10).join(formatted_css)}
                </style>
            </head>
            <body>
                {' '.join(html)}
                <script>
                {chr(10).join(js)}
                </script>
            </body>
            </html>
            """
            
            logs.append("✅ Компиляция успешна!")
            return final_html, logs
            
        except Exception as e:
            error_msg = f"❌ Ошибка: {e}"
            logs.append(error_msg)
            error_html = f"""
            <html><body style="background: #ffebee; color: #d32f2f; padding: 50px; font-family: Arial;">
                <h1>⚠️ Ошибка</h1>
                <p>{str(e)}</p>
                <p>Сайт всё равно работает! 🎉</p>
            </body></html>
            """
            return error_html, logs

class SimpleWebServer:
    """Упрощенный HTTP сервер"""
    def __init__(self, port=8000):
        self.port = port
        self.server = None
        self.is_running = False
        self.current_html = "<h1>Server starting...</h1>"
    
    def start_server(self):
        """Запускает сервер"""
        class CustomHandler(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(self.server.current_html.encode('utf-8'))
                else:
                    super().do_GET()
        
        class CustomTCPServer(socketserver.TCPServer):
            def __init__(self, server_address, handler_class, main_server):
                super().__init__(server_address, handler_class)
                self.current_html = main_server.current_html
        
        try:
            self.server = CustomTCPServer(("", self.port), CustomHandler, self)
            self.is_running = True
            print(f"🌐 Сервер запущен: http://localhost:{self.port}")
            self.server.serve_forever()
        except Exception as e:
            print(f"❌ Ошибка сервера: {e}")
            self.is_running = False
    
    def stop_server(self):
        """Останавливает сервер"""
        if self.server:
            self.is_running = False
            self.server.shutdown()
            print("⏹️ Сервер остановлен")
    
    def update_content(self, html_content):
        """Обновляет содержимое сервера"""
        self.current_html = html_content
        if self.server:
            self.server.current_html = html_content

class MagicIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.web_server = SimpleWebServer()
        self.server_thread = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('✨ MagicWeb IDE - Самый простой язык!')
        self.setGeometry(100, 100, 1400, 900)
        
        # Устанавливаем стиль
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2c3e50, stop: 1 #34495e);
            }
            QWidget {
                background: transparent;
            }
            QTextEdit, QTextBrowser {
                background: rgba(255, 255, 255, 0.95);
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Courier New';
                font-size: 12px;
                color: #2c3e50;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #3498db, stop: 1 #2980b9);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #2980b9, stop: 1 #3498db);
            }
            QPushButton:pressed {
                background: #21618c;
            }
            QLineEdit {
                background: white;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 6px;
                color: #2c3e50;
                font-size: 11px;
            }
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 11px;
            }
            QSplitter::handle {
                background: #7f8c8d;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Панель управления
        control_panel = QHBoxLayout()
        control_panel.setSpacing(8)
        
        self.port_input = QLineEdit("8000")
        self.port_input.setFixedWidth(60)
        self.port_input.setPlaceholderText("Порт")
        
        self.start_btn = QPushButton('🌐 Запуск сервера')
        self.start_btn.clicked.connect(self.toggle_server)
        
        self.preview_btn = QPushButton('👁️ Preview')
        self.preview_btn.clicked.connect(self.update_preview)
        
        self.open_btn = QPushButton('🚀 Открыть в браузере')
        self.open_btn.clicked.connect(self.open_in_browser)
        
        control_panel.addWidget(QLabel("Порт:"))
        control_panel.addWidget(self.port_input)
        control_panel.addWidget(self.start_btn)
        control_panel.addWidget(self.preview_btn)
        control_panel.addWidget(self.open_btn)
        control_panel.addStretch()
        
        # Основной сплиттер
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Левый сплиттер (редактор + консоль)
        left_splitter = QSplitter(Qt.Vertical)
        
        # Редактор
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("""🎉 Добро пожаловать в MagicWeb! 🎉

ПРОСТО ПИШИТЕ ЧТО УГОДНО:

Привет мир! 🚀
Самый простой язык!

body: background: linear-gradient(135deg, #667eea, #764ba2)
body: color: white
body: font-size: 24px
body: text-align: center

alert Это работает!
log Сообщение в консоль

<button>Нажми меня</button>

Ура! 🎉

// Комментарии начинаются с //
// Система сама всё поймёт!""")
        
        # Консоль
        self.console = QTextBrowser()
        self.console.setPlaceholderText("Консоль появится после запуска Preview...")
        
        left_splitter.addWidget(self.editor)
        left_splitter.addWidget(self.console)
        left_splitter.setSizes([600, 200])
        
        # Preview
        self.preview = QWebEngineView()
        self.preview.setHtml("""<html><body style="background: #ecf0f1; padding: 20px; font-family: Arial;">
            <h1 style="color: #2c3e50;">✨ MagicWeb IDE</h1>
            <p style="color: #7f8c8d;">Просто пишите код - система всё поймет!</p>
            <p style="color: #7f8c8d;">Нажмите "Preview" чтобы увидеть магию! 🎯</p>
        </body></html>""")
        
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(self.preview)
        main_splitter.setSizes([600, 600])
        
        # Статус
        self.status_label = QLabel("✅ Готов к работе! Напишите код и нажмите Preview")
        self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 12px;")
        
        layout.addLayout(control_panel)
        layout.addWidget(main_splitter)
        layout.addWidget(self.status_label)
        
        # Таймер автообновления
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.auto_update)
        self.update_timer.start(1000)
        
    def toggle_server(self):
        """Запуск/остановка сервера"""
        if self.web_server.is_running:
            self.stop_server()
        else:
            self.start_server()
    
    def start_server(self):
        """Запускает сервер"""
        try:
            port = int(self.port_input.text())
            self.web_server.port = port
            self.server_thread = threading.Thread(target=self.web_server.start_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.start_btn.setText('🛑 Остановить сервер')
            self.status_label.setText(f"🌐 Сервер запущен: http://localhost:{port}")
            
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректный номер порта")
    
    def stop_server(self):
        """Останавливает сервер"""
        self.web_server.stop_server()
        self.start_btn.setText('🌐 Запуск сервера')
        self.status_label.setText("⏹️ Сервер остановлен")
    
    def update_preview(self):
        """Обновляет preview и консоль"""
        try:
            code = self.editor.toPlainText()
            html_output, logs = MagicWeb.compile_to_html(code)
            
            # Обновляем консоль
            self.console.clear()
            self.console.append(f"🕒 {datetime.now().strftime('%H:%M:%S')} - MagicWeb Компилятор")
            self.console.append("=" * 50)
            
            for log in logs:
                self.console.append(log)
                print(log)
            
            self.console.append("=" * 50)
            self.console.append("✅ Готово! Ошибки игнорируются! 🎉")
            
            # Обновляем preview
            self.preview.setHtml(html_output)
            
            # Обновляем сервер
            if self.web_server.is_running:
                self.web_server.update_content(html_output)
            
            self.status_label.setText("✅ Компиляция успешна! Консоль обновлена.")
            
        except Exception as e:
            error_msg = f"❌ Ошибка: {e}"
            self.console.append(error_msg)
            print(error_msg)
            self.status_label.setText("⚠️ Ошибка - смотрите консоль")
    
    def auto_update(self):
        """Автообновление при сервере"""
        if self.web_server.is_running:
            try:
                code = self.editor.toPlainText()
                html_output, _ = MagicWeb.compile_to_html(code)
                self.web_server.update_content(html_output)
            except:
                pass
    
    def open_in_browser(self):
        """Открывает в браузере"""
        if self.web_server.is_running:
            webbrowser.open(f"http://localhost:{self.web_server.port}")
        else:
            QMessageBox.warning(self, "Ошибка", "Сначала запустите сервер")
    
    def closeEvent(self, event):
        """При закрытии"""
        if self.web_server.is_running:
            self.stop_server()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    font = QFont("Arial", 10)
    app.setFont(font)
    
    ide = MagicIDE()
    ide.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()