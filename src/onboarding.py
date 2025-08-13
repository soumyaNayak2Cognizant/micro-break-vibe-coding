ACTIVITIES = {
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

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QCheckBox, QPushButton, QScrollArea, QWidget

class OnboardingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Welcome to Micro Breaks!')
        self.setFixedSize(550, 500)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Set your break interval (minutes):'))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 120)
        self.interval_spin.setValue(20)
        layout.addWidget(self.interval_spin)
        layout.addWidget(QLabel('Select break types:'))
        # Scroll area for activities
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        self.checkboxes = {}
        for key, label in ACTIVITIES.items():
            cb = QCheckBox(label)
            cb.setChecked(True)
            scroll_layout.addWidget(cb)
            self.checkboxes[key] = cb
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        self.save_btn = QPushButton('Save Preferences')
        layout.addWidget(self.save_btn)
        self.setLayout(layout)
        self.save_btn.clicked.connect(self.accept)

    def get_preferences(self):
        types = [k for k, cb in self.checkboxes.items() if cb.isChecked()]
        return self.interval_spin.value(), types
