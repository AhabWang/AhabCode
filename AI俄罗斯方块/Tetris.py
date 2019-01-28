
import sys
import random
from modules.utils import *
from modules.ai import TetrisAI
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QHBoxLayout, QLabel


'''
Function:
	定义俄罗斯方块游戏类
'''
class TetrisGame(QMainWindow):
	def __init__(self):
		super().__init__()
		# 是否暂停ing
		self.is_paused = False
		# 是否开始ing
		self.is_started = False
		self.initUI()
	'''界面初始化'''
	def initUI(self):
		# 块大小
		self.grid_size = 22
		# 游戏帧率
		self.fps = 100
		self.timer = QBasicTimer()
		# 焦点
		self.setFocusPolicy(Qt.StrongFocus)
		# 水平布局
		layout_horizontal = QHBoxLayout()
		self.inner_board = InnerBoard()
		self.external_board = ExternalBoard(self, self.grid_size, self.inner_board)
		layout_horizontal.addWidget(self.external_board)
		self.side_panel = SidePanel(self, self.grid_size, self.inner_board)
		layout_horizontal.addWidget(self.side_panel)
		self.status_bar = self.statusBar()
		self.external_board.score_signal[str].connect(self.status_bar.showMessage)
		self.start()
		self.center()
		self.setWindowTitle('公众号:Ahab杂货铺')
		self.show()
		self.setFixedSize(self.external_board.width() + self.side_panel.width(),
						  self.side_panel.height() + self.status_bar.height())
		# AI控制
		self.tetris_ai = TetrisAI(self.inner_board)
		self.next_action = None
		self.pre_tetris = tetrisShape().shape_empty
	'''游戏界面移动到屏幕中间'''
	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
	'''更新界面'''
	def updateWindow(self):
		self.external_board.updateData()
		self.side_panel.updateData()
		self.update()
	'''开始'''
	def start(self):
		if self.is_started:
			return
		self.is_started = True
		self.inner_board.createNewTetris()
		self.timer.start(self.fps, self)
	'''暂停/不暂停'''
	def pause(self):
		if not self.is_started:
			return
		self.is_paused = not self.is_paused
		if self.is_paused:
			self.timer.stop()
			self.external_board.score_signal.emit('Paused')
		else:
			self.timer.start(self.fps, self)
		self.updateWindow()
	'''计时器事件'''
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			if not self.next_action:
				self.next_action = self.tetris_ai.getNextAction()
			if self.next_action:
				while self.inner_board.current_direction != self.next_action[0]:
					self.inner_board.rotateAnticlockwise()
				count = 0
				while self.inner_board.current_coord[0] != self.next_action[1] and count < 5:
					if self.inner_board.current_coord[0] > self.next_action[1]:
						self.inner_board.moveLeft()
					else:
						self.inner_board.moveRight()
					count += 1
			removed_lines = self.inner_board.moveDown()
			self.external_board.score += removed_lines
			if self.pre_tetris != self.inner_board.current_tetris:
				self.next_action = None
				self.pre_tetris = self.inner_board.current_tetris
			self.updateWindow()
		else:
			super(TetrisGame, self).timerEvent(event)
	'''按键事件'''
	def keyPressEvent(self, event):
		if not self.is_started or self.inner_board.current_tetris == tetrisShape().shape_empty:
			super(TetrisGame, self).keyPressEvent(event)
			return
		key = event.key()
		# P键暂停
		if key == Qt.Key_P:
			self.pause()
			return
		if self.is_paused:
			return
		else:
			super(TetrisGame, self).keyPressEvent(event)
		self.updateWindow()


if __name__ == '__main__':
	app = QApplication([])
	tetris = TetrisGame()
	sys.exit(app.exec_())