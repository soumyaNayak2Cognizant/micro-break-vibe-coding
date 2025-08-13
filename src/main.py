import sys
import threading
import time
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QPushButton, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from plyer import notification
from activity_monitor import ActivityMonitor
from onboarding import OnboardingDialog
from dashboard import Dashboard
from db import init_db, get_db_connection
from autostart import add_to_startup
import datetime

APP_NAME = 'MicroBreaksApp'
ICON_PATH = os.path.join(os.path.dirname(__file__), 'icon.ico') if os.path.exists(os.path.join(os.path.dirname(__file__), 'icon.ico')) else None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Micro Breaks')
        self.setGeometry(100, 100, 400, 400)
        label = QLabel('Welcome to Micro Breaks!', self)
        label.setGeometry(100, 50, 200, 40)

        # Move Show Dashboard button to Edit Preferences button location
        self.dashboard_btn = QPushButton('Show Dashboard', self)
        self.dashboard_btn.setGeometry(160, 20, 130, 30)
        self.dashboard_btn.clicked.connect(self.open_dashboard)
        self.dashboard_btn.setVisible(True)
        # Remove Edit Preferences button from main window
        # ...existing code...

        # System tray
        self.tray_icon = QSystemTrayIcon(self)
        if ICON_PATH:
            self.tray_icon.setIcon(QIcon(ICON_PATH))
        else:
            self.tray_icon.setIcon(self.style().standardIcon(QSystemTrayIcon.SP_ComputerIcon))
        tray_menu = QMenu()
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.show_main)
        tray_menu.addAction(open_action)
        dash_action = QAction('Dashboard', self)
        dash_action.triggered.connect(self.open_dashboard)
        tray_menu.addAction(dash_action)
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

        # Show dashboard if user data exists
        if self.user_data_exists():
            self.open_dashboard()

        # Add to startup
        add_to_startup(APP_NAME, os.path.abspath(sys.argv[0]))

        init_db()
        self.load_preferences()
        self.activity_monitor = ActivityMonitor(idle_threshold=60)
        self.activity_monitor.start()
        self.last_break = time.time()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_break)
        self.timer.start(10000)  # check every 10 seconds

    def user_data_exists(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT 1 FROM user_preferences WHERE id=1')
        exists = c.fetchone() is not None
        conn.close()
        return exists

    def load_preferences(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT break_interval, break_types FROM user_preferences WHERE id=1')
        row = c.fetchone()
        if not row:
            dlg = OnboardingDialog(self)
            if dlg.exec_():
                interval, types = dlg.get_preferences()
                c.execute('INSERT INTO user_preferences (id, break_interval, break_types) VALUES (1, ?, ?)', (interval, ','.join(types)))
                conn.commit()
                self.break_interval = interval * 60
                self.break_types = types
            else:
                self.break_interval = 20 * 60
                self.break_types = ['flower', 'stretch', 'walk', 'breath', 'music', 'hydrate', 'window', 'gratitude', 'posture']
        else:
            self.break_interval = row[0] * 60
            self.break_types = row[1].split(',')
        conn.close()

    def check_for_break(self):
        idle_time = self.activity_monitor.get_idle_time()
        now = time.time()
        if idle_time < 60 and (now - self.last_break) > self.break_interval:
            self.show_break_notification()
            self.last_break = now

    def show_break_notification(self):
        import random
        break_type = random.choice(self.break_types)
        msg_map = {
            'flower': '🌸 Find a flower (look away and spot something beautiful)',
            'stretch': '🧘 Do a stretch (stand up and stretch your body)',
            'walk': '🚶 Take a 2-minute walk (move away from your desk)',
            'breath': '🎯 Breathing exercise (close your eyes and breathe deeply)',
            'music': '🎵 Listen to a short music clip (relax your mind)',
            'hydrate': '💧 Drink a glass of water (hydrate yourself)',
            'window': '🌤️ Look out the window (rest your eyes and mind)',
            'gratitude': '🙏 Think of something you are grateful for',
            'posture': '🪑 Check your posture (sit up straight and relax your shoulders)',
            'nature': '🌳 Visualize a peaceful nature scene',
            'affirmation': '💬 Say a positive affirmation to yourself',
            'light': '🔆 Adjust your lighting (reduce screen glare)',
            'journal': '📓 Jot down a quick thought or feeling',
            'laugh': '😂 Watch or recall something funny',
            'clean': '🧹 Tidy up your desk for a minute',
            'silence': '🤫 Sit in silence and observe your breath',
            'balance': '🧘‍♂️ Try a simple balance pose (e.g., stand on one leg)',
            'color': '🎨 Look at something colorful around you',
            'memory': '🧠 Recall a happy memory',
            'smell': '👃 Smell something pleasant (e.g., essential oil, coffee)',
            'light_walk': '🚶‍♂️ Walk to a different room and back',
            'sunlight': '☀️ Get some sunlight if possible',
            'pet': '🐶 Spend a minute with your pet (if available)'
        }
        notification.notify(
            title='Micro Break Reminder',
            message=f'Time for a micro break! {msg_map.get(break_type, "Look away from your screen!")}',
            timeout=10
        )
        # Log break
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO break_history (timestamp, break_type) VALUES (?, ?)', (datetime.datetime.now().isoformat(), break_type))
        conn.commit()
        conn.close()
        # Refresh dashboard if open
        if hasattr(self, 'dash') and self.dash.isVisible():
            self.dash.refresh_history()

    def open_dashboard(self):
        if not hasattr(self, 'dash') or not self.dash.isVisible():
            self.dash = Dashboard(self, edit_prefs_callback=self.edit_preferences)
            self.dashboard_btn.setVisible(False)
            self.dash.destroyed.connect(lambda: self.dashboard_btn.setVisible(True))
        self.dash.show()
        self.dash.raise_()
        self.dash.activateWindow()

    def edit_preferences(self):
        # Hide edit button on dashboard while editing
        if hasattr(self, 'dash') and hasattr(self.dash, 'edit_prefs_btn'):
            self.dash.edit_prefs_btn.setVisible(False)
        dlg = OnboardingDialog(self)
        if dlg.exec_():
            interval, types = dlg.get_preferences()
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('SELECT break_interval, break_types FROM user_preferences WHERE id=1')
            old = c.fetchone()
            if old and (old[0] != interval or old[1] != ','.join(types)):
                reply = QMessageBox.question(self, 'Confirm Changes', 'Save changes to your preferences?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    c.execute('UPDATE user_preferences SET break_interval=?, break_types=? WHERE id=1', (interval, ','.join(types)))
                    conn.commit()
                    self.break_interval = interval * 60
                    self.break_types = types
                    QMessageBox.information(self, 'Preferences Updated', 'Your preferences have been updated.')
            elif not old:
                c.execute('INSERT INTO user_preferences (id, break_interval, break_types) VALUES (1, ?, ?)', (interval, ','.join(types)))
                conn.commit()
                self.break_interval = interval * 60
                self.break_types = types
                QMessageBox.information(self, 'Preferences Updated', 'Your preferences have been updated.')
            conn.close()
        # Show edit button again after editing
        if hasattr(self, 'dash') and hasattr(self.dash, 'edit_prefs_btn'):
            self.dash.edit_prefs_btn.setVisible(True)

    def reset_user_data(self):
        reply = QMessageBox.question(self, 'Confirm Reset', 'Are you sure you want to reset all user data?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            from db import reset_db
            reset_db()
            QMessageBox.information(self, 'Reset', 'User data has been reset. Please restart the app.')

    def closeEvent(self, event):
        self.hide()
        self.tray_icon.showMessage('Micro Breaks', 'App is still running in the system tray.', QSystemTrayIcon.Information, 1000)
        event.ignore()

    def show_main(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def exit_app(self):
        self.activity_monitor.stop()
        QApplication.quit()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_main()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
