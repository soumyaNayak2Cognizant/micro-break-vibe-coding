from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QSpacerItem, QSizePolicy, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer
import datetime
from db import get_db_connection, reset_db

class Dashboard(QWidget):
    def __init__(self, parent=None, edit_prefs_callback=None):
        super().__init__(parent)
        self.setWindowTitle('Focus Time')
        self.setFixedSize(400, 400)
        layout = QVBoxLayout()
        # Top bar with reset and edit preferences buttons
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        self.edit_prefs_btn = QPushButton('Edit Preferences')
        self.edit_prefs_btn.setFixedWidth(120)
        if edit_prefs_callback:
            self.edit_prefs_btn.clicked.connect(edit_prefs_callback)
        top_bar.addWidget(self.edit_prefs_btn)
        self.reset_btn = QPushButton('Reset All Data')
        self.reset_btn.setFixedWidth(120)
        self.reset_btn.clicked.connect(self.confirm_reset)
        top_bar.addWidget(self.reset_btn)
        layout.addLayout(top_bar)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        # Timer label
        self.timer_label = QLabel('Time until next break: --:--')
        self.timer_label.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(self.timer_label)
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('Break History'))
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        self.setLayout(layout)
        self.refresh_history()
        self.timer_label.setVisible(False)
        # Timer for updating countdown
        self._main_window = parent
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update_time_left)
        self._timer.start(1000)
        self.update_time_left()

    def refresh_history(self):
        self.history_list.clear()
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT timestamp, break_type FROM break_history ORDER BY timestamp DESC LIMIT 50')
        for row in c.fetchall():
            ts = datetime.datetime.fromisoformat(row[0]).strftime('%Y-%m-%d %H:%M:%S')
            self.history_list.addItem(f"{ts}: {row[1]}")
        conn.close()

    def confirm_reset(self):
        reply = QMessageBox.question(self, 'Confirm Reset', 'Are you sure you want to reset all user data?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.reset_data()

    def reset_data(self):
        reset_db()
        self.refresh_history()

    def update_time_left(self):
        if self._main_window:
            try:
                interval = self._main_window.break_interval
                last_break = self._main_window.last_break
                import time
                now = time.time()
                seconds_left = int(interval - (now - last_break))
                if seconds_left < 0:
                    seconds_left = 0
                mins, secs = divmod(seconds_left, 60)
                self.timer_label.setText(f'Time until next break: {mins:02d}:{secs:02d}')
            except Exception:
                self.timer_label.setText('Time until next break: --:--')
        else:
            self.timer_label.setText('Time until next break: --:--')
