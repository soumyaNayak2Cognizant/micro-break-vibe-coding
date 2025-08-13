from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QCheckBox, QPushButton

class OnboardingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Welcome to Micro Breaks!')
        self.setFixedSize(350, 300)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Set your break interval (minutes):'))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 120)
        self.interval_spin.setValue(20)
        layout.addWidget(self.interval_spin)
        layout.addWidget(QLabel('Select break types:'))
        self.cb_flower = QCheckBox('🌸 Find a flower')
        self.cb_stretch = QCheckBox('🧘 Do a stretch')
        self.cb_walk = QCheckBox('🚶 Take a 2-minute walk')
        self.cb_breath = QCheckBox('🎯 Breathing exercise')
        self.cb_music = QCheckBox('🎵 Listen to music')
        for cb in [self.cb_flower, self.cb_stretch, self.cb_walk, self.cb_breath, self.cb_music]:
            cb.setChecked(True)
            layout.addWidget(cb)
        self.save_btn = QPushButton('Save Preferences')
        layout.addWidget(self.save_btn)
        self.setLayout(layout)
        self.save_btn.clicked.connect(self.accept)

    def get_preferences(self):
        types = []
        if self.cb_flower.isChecked(): types.append('flower')
        if self.cb_stretch.isChecked(): types.append('stretch')
        if self.cb_walk.isChecked(): types.append('walk')
        if self.cb_breath.isChecked(): types.append('breath')
        if self.cb_music.isChecked(): types.append('music')
        return self.interval_spin.value(), types
