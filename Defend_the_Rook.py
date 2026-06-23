import sys
import random

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget
)


class MenuScreen(QWidget):

    def __init__(self, game):
        super().__init__()

        self.game = game

        layout = QVBoxLayout()

        self.army_label = QLabel(
            "📦 YOUR ARMY"
        )

        self.army_label.setAlignment(
            Qt.AlignCenter
        )

        self.army_list = QListWidget()

        title = QLabel("🏰 ROOK DEFENSE")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)

        play_btn = QPushButton("⚔ PLAY")
        exit_btn = QPushButton("❌ EXIT")

        play_btn.setMinimumHeight(80)
        exit_btn.setMinimumHeight(80)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(play_btn)
        layout.addWidget(exit_btn)
        layout.addStretch()

        self.setLayout(layout)

        play_btn.clicked.connect(
            self.start_game
        )

        exit_btn.clicked.connect(
            self.game.close
        )



    def start_game(self):
        self.game.show_preparation()


class PreparationScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        self.coins = 1000
        self.gems = 50
        self.diamond = 5

        self.inventory = []

        self.time_left = 30

        self.timer = QTimer()
        self.timer.timeout.connect(
            self.update_timer
        )

        self.throwing_step = 0

        self.throw_animation = QTimer()

        self.throw_animation.timeout.connect(
            self.animate_throw
        )

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        # Judul
        title = QLabel("⏰ PREPARATION PHASE")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        # Uang
        self.currency_label = QLabel(
            f"🪙 {self.coins}    💎 {self.gems}    🔷 {self.diamond}"
        )

        self.currency_label.setAlignment(
            Qt.AlignCenter
        )

        self.currency_label.setStyleSheet("""
            font-size: 18px;
        """)

        # Timer
        self.timer_label = QLabel(
            "Time : 30"
        )

        self.timer_label.setAlignment(
            Qt.AlignCenter
        )

        self.timer_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
        """)

        # Area rarity
        rarity_layout = QHBoxLayout()

        grass = QLabel("🟩\nGRASS")
        silver = QLabel("⬜\nSILVER")
        gold = QLabel("🟨\nGOLD")
        crystal = QLabel("🟪\nCRYSTAL")
        diamond = QLabel("💎\nBLACK DIAMOND")
        immortal = QLabel("😈\nIMMORTAL")

        boxes = [
            grass,
            silver,
            gold,
            crystal,
            diamond,
            immortal
        ]

        damage_table = {
            "Stick Soldier": 5,
            "Stone": 2,
            "Wood Shield": 3,

            "Archer": 10,
            "Guard": 8,
            "Armor": 12,

            "Knight": 15,
            "Cannon": 25,
            "Healer": 0,

            "Elite Knight": 30,
            "Giant": 35,
            "Fire Mage": 40,

            "Titan": 50,
            "Dragon Rider": 45,
            "King Slayer": 70,

            "Devil angel": 72,
            "AK-47": 85,
            "Horeg": 99

        }

        for box in boxes:

            box.setAlignment(
                Qt.AlignCenter
            )

            box.setMinimumSize(
                180,
                140
            )

            box.setStyleSheet("""
                border: 3px solid black;
                font-size: 18px;
                font-weight: bold;
            """)

            rarity_layout.addWidget(box)

        # Tombol gacha
        self.throw_btn = QPushButton(
            "🎲 THROW"
        )

        self.throw_btn.setMinimumHeight(
            70
        )

        # Hasil
        self.result_label = QLabel(
            "Result : -"
        )

        self.result_label.setAlignment(
            Qt.AlignCenter
        )

        self.result_label.setStyleSheet("""
            font-size: 20px;
        """)

        # Inventory
        self.inventory_box = QTextEdit()

        self.inventory_box.setReadOnly(
            True
        )

        # Masukkan ke layout
        layout.addWidget(title)

        layout.addWidget(
            self.currency_label
        )

        layout.addWidget(
            self.timer_label
        )

        layout.addLayout(
            rarity_layout
        )

        layout.addWidget(
            self.throw_btn
        )

        layout.addWidget(
            self.result_label
        )

        layout.addWidget(
            self.inventory_box
        )

        self.setLayout(layout)

        self.throw_btn.clicked.connect(
            self.throw_ball
        )

        self.timer.start(1000)

    def update_timer(self):

        self.time_left -= 1

        self.timer_label.setText(
            f"Time : {self.time_left}"
        )

        if self.time_left <= 0:

            self.timer.stop()

            self.throw_btn.setEnabled(False)

            self.result_label.setText(
                "⚔ PREPARATION FINISHED!"
            )

            print("PINDAH KE BATTLE")

            self.game.battle_screen.load_inventory(
                self.inventory
            )

            self.game.setCurrentWidget(
                self.game.battle_screen
            )

    def animate_throw(self):

        self.throwing_step += 1

        self.result_label.setText(
            "🎲 Throwing" + "." * self.throwing_step
        )

        if self.throwing_step >= 1:

            self.throw_animation.stop()

            self.finish_throw()

    def throw_ball(self):

        self.throw_btn.setEnabled(False)

        self.throwing_step = 0

        self.throw_animation.start(1000)

    def finish_throw(self):

        roll = random.randint(
            1,
            100
        )

        if roll <= 50:

            rarity = "🟩 Grass"

            item = random.choice([
                "🪵 Stick Soldier",
                "🪨 Stone",
                "🛡️ Wood Shield"
            ])

        elif roll <= 75:

            rarity = "⬜ Silver"

            item = random.choice([
                "🏹 Archer",
                "🛡️ Guard",
                "🥋 Armor"
            ])

        elif roll <= 80:

            rarity = "🟨 Gold"

            item = random.choice([
                "⚔️ Knight",
                "💣 Cannon",
                "❤️ Healer"
            ])

        elif roll <= 90:

            rarity = "🟪 Crystal"

            item = random.choice([
                "🗡️ Elite Knight",
                "👹 Giant",
                "🔥 Fire Mage"
            ])

        elif roll <= 99:

            rarity = "💎 Black Diamond"

            item = random.choice([
                "🦾 Titan",
                "🐉 Dragon Rider",
                "☠️ King Slayer"
            ])

        else:
            rarity = "😈 Immortal"

            item = random.choice([
                "😈 Devil angel",
                "🔫 AK-47",
                "🎺 Horeg"
            ])

        self.inventory.append(item)

        self.result_label.setText(
            f"{rarity} → {item}"
        )

        self.inventory_box.setText(
            "\n".join(self.inventory)
        )

        self.throw_btn.setEnabled(True)


class BattleScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.player_hp = 100
        self.enemy_hp = 100

        self.player_units = []

        self.enemy_units = [
            "👹",
            "🏹",
            "🛡️"
        ]

        layout = QVBoxLayout()

        self.arena = QLabel()

        self.update_arena()

        self.player_label = QLabel(
            f"🏰 PLAYER CASTLE HP : {self.player_hp}"
        )

        self.player_label.setAlignment(
            Qt.AlignCenter
        )

        self.enemy_label = QLabel(
            f"🏰 ENEMY CASTLE HP : {self.enemy_hp}"
        )

        self.enemy_label.setAlignment(
            Qt.AlignCenter
        )

        self.log_label = QLabel(
            "⚔ Battle Started!"
        )

        self.log_label.setAlignment(
            Qt.AlignCenter
        )

        self.army_label = QLabel(
            "📦 YOUR ARMY"
        )

        self.army_label.setAlignment(
            Qt.AlignCenter
        )

        self.army_list = QListWidget()

        layout.addWidget(
            self.arena
        )

        self.spawn_btn = QPushButton(
            "⚔ SPAWN UNIT"
        )

        self.spawn_btn.setMinimumHeight(
            70
        )

        layout.addWidget(
            self.player_label
        )

        layout.addWidget(
            self.army_label
        )

        layout.addWidget(
            self.army_list
        )

        layout.addWidget(
            self.log_label
        )

        layout.addWidget(
            self.enemy_label
        )

        layout.addWidget(
            self.spawn_btn
        )

        self.setLayout(layout)

        self.spawn_btn.clicked.connect(
            self.spawn_unit
        )

    

    def update_arena(self):

        enemy = " ".join(
            self.enemy_units
        )

        player = " ".join(
            self.player_units
        )

        if player == "":
            player = "(No Unit)"

        self.arena.setText(
    f"""
    🏰 ENEMY CASTLE

    {enemy}

    ══════════════════════

    {player}

    🏰 PLAYER CASTLE
    """
        )

    

    def load_inventory(self, inventory):

        self.army_list.clear()

        for item in inventory:

            self.army_list.addItem(item)

    def spawn_unit(self):

        selected = self.army_list.currentItem()

        if selected is None:

            self.log_label.setText(
                "❌ Pilih unit dulu!"
            )

            return

        unit = selected.text()

        emoji = unit.split()[0]

        self.player_units.append(
            emoji
        )

        self.update_arena()

        damage = random.randint(
            10,
            25
        )

        self.enemy_hp -= damage

        self.enemy_label.setText(
            f"🏰 ENEMY CASTLE HP : {self.enemy_hp}"
        )

        self.log_label.setText(
            f"{unit} menyerang! Damage {damage}"
        )

        row = self.army_list.currentRow()

        self.army_list.takeItem(
            row
        )


class GameWindow(QStackedWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Rook Defense"
        )

        self.resize(
            1200,
            700
        )

        self.menu_screen = MenuScreen(
            self
        )

        self.preparation_screen = PreparationScreen(self)
        self.battle_screen = BattleScreen()

        self.addWidget(
            self.menu_screen
        )

        self.addWidget(
            self.preparation_screen
        )

        self.addWidget(
            self.battle_screen
        )

        self.setCurrentWidget(
            self.menu_screen
        )

    def show_preparation(self):

        self.preparation_screen.time_left = 30

        self.preparation_screen.timer.start(
            1000
        )

        self.setCurrentWidget(
            self.preparation_screen
        )


app = QApplication(
    sys.argv
)

game = GameWindow()



game.show()

sys.exit(
    app.exec_()
)


