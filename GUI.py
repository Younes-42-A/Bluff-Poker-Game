import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QDialog, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QProgressBar, QPushButton, QSlider, QVBoxLayout, QWidget,
    QSizePolicy
)
from BluffGame import BluffGame

STYLE_SHEET = """
QMainWindow { background-color: #060103; }
QFrame#mainContainer { border: 2px solid #FFD700; background-color: #080104; margin: 2px; }
QFrame#opponentFrame { border: 2px solid #D31238; background-color: #120208; border-radius: 6px; padding: 6px; }
QFrame#warningPanel { border: 2px solid #D31238; background-color: #18020A; border-radius: 8px; }
QLabel#warningTitle { color: #FFD700; font-size: 19px; font-weight: bold; }
QLabel#warningText { color: #EEEEEE; font-size: 14px; }
QLabel#warningStatus { color: #70DB88; font-size: 13px; font-weight: bold; }
QLabel#botAvatar { border: 2px solid #FFD700; background-color: #000000; }
QFrame#playingCard { border: 2px solid #FFD700; background-color: #38040E; border-radius: 10px; }
QLabel#cardQuestionMark { color: #FFD700; font-size: 36px; font-weight: bold; }
QFrame#bluffBox { border: 2px solid #FFD700; border-radius: 8px; background-color: #18020A; }
QLabel#bluffText { color: #FFD700; font-size: 20px; font-weight: bold; }
QLabel#riskLabel { color: #D31238; font-size: 13px; font-weight: bold; }
QFrame#playerFrame { border: 2px solid #FFD700; background-color: #120208; border-radius: 6px; }
QLabel#fleetTitle { color: #FFFFFF; font-size: 18px; font-weight: bold; }
QLabel#fleetCount { color: #FFD700; font-size: 16px; font-weight: bold; }
QProgressBar { border: 1px solid #FFD700; background-color: #1C030D; border-radius: 2px; text-align: center; }
QProgressBar::chunk#oppBar { background-color: #D31238; }
QProgressBar::chunk#playerBar { background-color: #FFD700; }
QPushButton#passBtn { background-color: #262930; color: #E0E0E0; border: 2px solid #555; border-radius: 8px; font-size: 13px; font-weight: bold; }
QPushButton#callBtn { background-color: #8C0A23; color: #FFFFFF; border: 2px solid #D31238; border-radius: 8px; font-size: 13px; font-weight: bold; }
QPushButton#raiseBtn { background-color: #FFC700; color: #000000; border: 2px solid #FFFFFF; border-radius: 8px; font-size: 13px; font-weight: bold; }
QPushButton#attackBtn { background-color: #28a745; color: #FFFFFF; border: 2px solid #FFFFFF; border-radius: 8px; font-size: 15px; font-weight: bold; }
QPushButton:disabled { background-color: #151515; color: #555555; border: 1px solid #333333; }
"""

ATTACK_DIALOG_STYLE = """
QDialog {
    background-color: #0c0206;
    border: 2px solid #FFD700;
}
QLabel {
    color: #FFD700;
    font-family: Arial;
}
QPushButton {
    background-color: #8C0A23;
    color: #FFFFFF;
    border: 2px solid #FFD700;
    border-radius: 6px;
    font-weight: bold;
    font-size: 14px;
    min-height: 35px;
}
QPushButton:hover {
    background-color: #D31238;
}
QSlider::groove:horizontal {
    border: 1px solid #FFD700;
    height: 8px;
    background: #1C030D;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #FFD700;
    border: 1px solid #FFFFFF;
    width: 18px;
    margin: -5px 0;
    border-radius: 9px;
}
"""

class AttackDialog(QDialog):
    def __init__(self, actual_sum, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Your Bluff")
        self.setFixedSize(380, 260)
        self.setStyleSheet(ATTACK_DIALOG_STYLE)

        self.selected_value = actual_sum

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_label = QLabel("⚔️ DECLARE YOUR BLUFF SUM")
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFD700;")
        layout.addWidget(title_label)

        self.info_label = QLabel(f"Your actual cards sum: [ {actual_sum} ]")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("font-size: 13px; color: #CCCCCC;")
        layout.addWidget(self.info_label)

        self.value_display = QLabel(str(actual_sum))
        self.value_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_display.setStyleSheet("font-size: 28px; font-weight: bold; color: #FFFFFF; border: 1px solid #555; background-color: #18020A; border-radius: 6px;")
        layout.addWidget(self.value_display)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(2, 20)
        self.slider.setValue(actual_sum)
        self.slider.valueChanged.connect(self.on_slider_changed)
        layout.addWidget(self.slider)

        self.confirm_btn = QPushButton("CONFIRM CLAIM")
        self.confirm_btn.clicked.connect(self.accept)
        layout.addWidget(self.confirm_btn)

    def on_slider_changed(self, value):
        self.selected_value = value
        self.value_display.setText(str(value))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bluff Poker Game")
        self.setGeometry(100, 100, 1120, 620)
        self.setStyleSheet(STYLE_SHEET)

        self.game = BluffGame() 

        self.setMaximumSize(1300, 750)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        outer_layout = QHBoxLayout(central_widget)
        outer_layout.setContentsMargins(5, 5, 5, 5)

        main_container = QFrame(objectName="mainContainer")
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)
        outer_layout.addWidget(main_container, 1)

        warning_panel = QFrame(objectName="warningPanel")
        warning_panel.setFixedWidth(235)
        warning_layout = QVBoxLayout(warning_panel)
        warning_layout.setContentsMargins(16, 20, 16, 20)
        warning_layout.setSpacing(14)

        self.warning_title = QLabel(
            "⚠️ LOSS WARNING", objectName="warningTitle"
        )
        self.warning_title.setWordWrap(True)
        self.warning_text = QLabel(
            "Lose the game and you'll see a dramatic system-wipe warning.\n\n"
            "This is only a game effect. No system commands run, and your "
            "operating system and files are never touched.",
            objectName="warningText",
        )
        self.warning_text.setWordWrap(True)
        self.warning_status = QLabel(
            "SIMULATED THREAT ONLY",
            objectName="warningStatus",
        )
        self.warning_status.setWordWrap(True)

        warning_layout.addWidget(self.warning_title)
        warning_layout.addWidget(self.warning_text)
        warning_layout.addStretch()
        warning_layout.addWidget(self.warning_status)
        outer_layout.addWidget(warning_panel)

        opponent_frame = QFrame(objectName="opponentFrame")
        opponent_h_layout = QHBoxLayout(opponent_frame)

        self.avatar_label = QLabel(objectName="botAvatar")
        self.avatar_label.setFixedSize(70, 70)
        self.load_avatar_image()

        opponent_info_layout = QVBoxLayout()
        opp_name = self.game.bot.name.upper() if self.game else "YOMEKO"
        opponent_title = QLabel(f"{opp_name} (AI OPPONENT)")
        opponent_title.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 16px; border: none;")
        opponent_title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        bar_row_layout = QHBoxLayout()
        self.opp_bar = QProgressBar(objectName="oppBar")
        self.opp_bar.setFixedHeight(16)
        self.opp_bar.setTextVisible(False)
        self.opp_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.opp_count_label = QLabel("100 / 100 CHIPS")
        self.opp_count_label.setStyleSheet("color: #D31238; font-weight: bold; font-size: 14px; border: none;")
        self.opp_count_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        bar_row_layout.addWidget(QLabel("Chip Balance", styleSheet="color: #CCC; font-size: 12px; border: none;"))
        bar_row_layout.addWidget(self.opp_bar, 1)
        bar_row_layout.addWidget(self.opp_count_label)

        opponent_info_layout.addWidget(opponent_title)
        opponent_info_layout.addLayout(bar_row_layout)
        opponent_h_layout.addWidget(self.avatar_label)
        opponent_h_layout.addLayout(opponent_info_layout)

        main_layout.addWidget(opponent_frame)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(30)
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card_labels = []
        for _ in range(2):
            card_frame = QFrame(objectName="playingCard")
            card_frame.setFixedSize(110, 150)
            card_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            card_inner_layout = QVBoxLayout(card_frame)
            q_mark = QLabel("?", objectName="cardQuestionMark")
            q_mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_inner_layout.addWidget(q_mark)
            cards_layout.addWidget(card_frame)
            self.card_labels.append(q_mark)
        main_layout.addLayout(cards_layout)

        bluff_container = QVBoxLayout()
        bluff_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bluff_box = QFrame(objectName="bluffBox")
        bluff_box.setFixedWidth(550)
        bluff_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        bluff_layout = QHBoxLayout(bluff_box)

        self.bluff_label = QLabel("DECLARED BLUFF SUM: [ 0 ]", objectName="bluffText")
        self.bluff_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bluff_layout.addWidget(self.bluff_label)

        self.risk_label = QLabel("Game Started!", objectName="riskLabel")
        self.risk_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bluff_container.addWidget(bluff_box)
        bluff_container.addWidget(self.risk_label)
        main_layout.addLayout(bluff_container)

        player_frame = QFrame(objectName="playerFrame")
        player_layout = QHBoxLayout(player_frame)

        self.player_bar = QProgressBar(objectName="playerBar")
        self.player_bar.setFixedHeight(20)
        self.player_bar.setTextVisible(False)
        self.player_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.player_count_label = QLabel("100 / 100 CHIPS", objectName="fleetCount")


        player_layout.addWidget(QLabel("Chip Balance", styleSheet="color: #CCC; font-size: 12px; border: none;"))
        player_layout.addWidget(self.player_bar, 1)
        player_layout.addWidget(self.player_count_label)


        player_layout.addWidget(QLabel("YOUR STAKE", objectName="fleetTitle"))
        player_layout.addWidget(self.player_bar, 1)
        player_layout.addWidget(self.player_count_label)
        main_layout.addWidget(player_frame)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.attack_button = QPushButton("DECLARE BLUFF / ATTACK ⚔️", objectName="attackBtn")
        self.pass_button = QPushButton("PASS / FOLD\n(-10 Chips)", objectName="passBtn")
        self.call_button = QPushButton("CALL BLUFF!\n(Stake 10)", objectName="callBtn")
        self.raise_button = QPushButton("RAISE BET! 🗲\n(Stake 25)", objectName="raiseBtn")

        for btn in (self.attack_button, self.pass_button, self.call_button, self.raise_button):
            btn.setFixedHeight(55)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)

        self.attack_button.clicked.connect(self.prompt_player_attack)
        self.attack_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pass_button.clicked.connect(lambda: self.make_move("pass"))
        self.pass_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.call_button.clicked.connect(lambda: self.make_move("call"))
        self.call_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.raise_button.clicked.connect(lambda: self.make_move("raise"))
        self.raise_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.update_ui()

    def load_avatar_image(self):
        if getattr(sys, 'frozen', False):
            script_dir = os.path.dirname(sys.executable)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))

        image_path = os.path.join(script_dir, "yomeko.png")
        pixmap = QPixmap(image_path)
        self.avatar_label.setPixmap(pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.avatar_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def prompt_player_attack(self):
        if not self.game or self.game.is_game_over:
            return

        actual = self.game.player1.actual_sum
        dialog = AttackDialog(actual, self)
        if dialog.exec() == QDialog.Accepted:
            self.game.set_player_bluff(dialog.selected_value)
            self.update_ui()

    def make_move(self, decision: str):
        if self.game and not self.game.is_game_over:
            self.game.play_human_defense(decision)
            self.update_ui()

    def update_ui(self):
        if not self.game:
            return

        p1_chips = getattr(self.game.player1, 'chips', getattr(self.game.player1, 'ships', 0))
        opp_chips = getattr(self.game.bot, 'chips', getattr(self.game.bot, 'ships', 0))

        self.player_bar.setValue(max(0, p1_chips))
        self.player_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.player_count_label.setText(f"{p1_chips} / 100 CHIPS")
        self.opp_bar.setValue(max(0, opp_chips))
        self.opp_count_label.setText(f"{opp_chips} / 100 CHIPS")
        self.opp_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if hasattr(self.game.player1, 'cards') and len(self.game.player1.cards) >= 2:
            self.card_labels[0].setText(str(self.game.player1.cards[0]))
            self.card_labels[1].setText(str(self.game.player1.cards[1]))
        else:
            self.card_labels[0].setText("?")
            self.card_labels[1].setText("?")

        round_str = f"[ Round {min(self.game.round_number, 12)} / 12 ] " if not self.game.is_game_over else ""
        self.bluff_label.setText(f"{round_str}DECLARED BLUFF: [ {self.game.current_bluff} ]")
        self.risk_label.setText(self.game.last_message)

        is_player_turn_to_attack = (self.game.attacker == self.game.player1)

        if self.game.is_game_over:
            self.attack_button.setEnabled(False)
            self.pass_button.setEnabled(False)
            self.call_button.setEnabled(False)
            self.raise_button.setEnabled(False)
            if self.game.winner == self.game.bot.name:
                self.warning_title.setText("💀 YOU LOST!")
                self.warning_text.setText(
                    "SYSTEM WIPE SEQUENCE: FAKE.\n\n"
                    "Just kidding! No commands were run, and nothing was "
                    "changed or deleted."
                )
                self.warning_status.setText("SYSTEM STATUS: SAFE")
        elif is_player_turn_to_attack:
            self.attack_button.setEnabled(True)
            self.pass_button.setEnabled(False)
            self.call_button.setEnabled(False)
            self.raise_button.setEnabled(False)
        else:
            self.attack_button.setEnabled(False)
            self.pass_button.setEnabled(True)
            self.call_button.setEnabled(True)
            self.raise_button.setEnabled(True)
