import wx
import wx.xrc
import json
import pandas as pd
import numpy as np
import os
import re

###########################################################################
## Class HistoryFrame
###########################################################################

class HistoryFrame(wx.Frame):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"历史记录", pos = wx.DefaultPosition, size = wx.Size( 1500,800 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		# 设置图标
		self.icon = wx.Icon('paper.ico', wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)

		# 读取设置
		json_file = open('setting.json')
		json_file = json.load(json_file)
		class_name = json_file['class_name']

		# 读取历史记录
		self.data = pd.read_csv('paper.csv')
		self.show_data = self.data


		self.SetSizeHintsSz( wx.Size( 1500,800 ), wx.Size( 1500,800 ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		# 类别选择
		class_choiceChoices = ['请选择类别'] + class_name
		self.class_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, class_choiceChoices, 0 )
		self.class_choice.SetSelection( 0 )
		bSizer5.Add( self.class_choice, 0, wx.ALL, 5 )

		# 筛选按钮
		self.select_button = wx.Button( self, wx.ID_ANY, u"筛选", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.select_button.Bind(wx.EVT_BUTTON, self.select)
		bSizer5.Add( self.select_button, 0, wx.ALL, 5 )

		self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer5.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )

		# 搜索框
		self.search_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		self.search_text.SetMinSize( wx.Size( 200,-1 ) )

		bSizer5.Add( self.search_text, 0, wx.ALL, 5 )

		# 搜索按钮
		self.search_button = wx.Button( self, wx.ID_ANY, u"搜索", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.search_button.Bind(wx.EVT_BUTTON, self.search)
		bSizer5.Add( self.search_button, 0, wx.ALL, 5 )

		self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer5.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )

		# 打开文件按钮
		self.open_button = wx.Button( self, wx.ID_ANY, u"打开", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.open_button.Bind(wx.EVT_BUTTON, self.open)
		bSizer5.Add( self.open_button, 0, wx.ALL, 5 )


		bSizer4.Add( bSizer5, 0, wx.EXPAND, 5 )

		self.m_staticline6 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer4.Add(bSizer6)

		# 选择列表
		self.list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(900,800), style=wx.LC_REPORT)
		self.list.InsertColumn(0, '论文路径', width=630)
		self.list.InsertColumn(1, '类别', width=100)
		self.list.InsertColumn(2, '时间', width=170)
		#index = self.list.InsertStringItem(sys.maxint)
		for i in range(self.show_data.shape[0]):
			index = self.list.InsertStringItem(self.list.GetItemCount(), self.show_data['file_path'].values[i])
			self.list.SetStringItem(index, 1, self.show_data['class'].values[i])
			self.list.SetStringItem(index, 2, self.show_data['time'].values[i])
		self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.show)
		self.list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.deshow)

		bSizer6.Add(self.list, 1, wx.ALL, 5 )

		# 笔记显示
		self.note_show = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 600,800 ), wx.TE_MULTILINE|wx.SIMPLE_BORDER)
		self.note_show.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

		self.note_show.SetEditable(False)
		bSizer6.Add(self.note_show, 1, wx.ALL, 5)

		self.SetSizer( bSizer4 )
		self.Layout()

		self.file_path = ''

		self.Centre( wx.BOTH )

	# 显示笔记内容
	def show(self, event):
		index = self.list.GetFirstSelected()
		self.file_path = self.show_data['file_path'].values[index]
		note = np.load('./data/' + self.file_path.replace(':', '_').replace('\\', '_').replace('/', '_') + '.npy')
		self.note_show.Value = str(note)

	# 取消了选择则路径和内容恢复默认
	def deshow(self, event):
		self.file_path = ''
		self.note_show.Value = ''

	# 按类别筛选
	def select(self, event):
		# 按类别选出笔记内容
		selected_class = self.class_choice.GetItems()[self.class_choice.GetSelection()]
		selected_data = self.data[self.data['class'] == selected_class]
		if not selected_data.empty:
			# 删除之前的内容
			self.list.DeleteAllItems()
			self.show_data = selected_data
			# 显示筛选后的内容
			for i in range(self.show_data.shape[0]):
				index = self.list.InsertStringItem(self.list.GetItemCount(), self.show_data['file_path'].values[i])
				self.list.SetStringItem(index, 1, self.show_data['class'].values[i])
				self.list.SetStringItem(index, 2, self.show_data['time'].values[i])
		else:
			wx.MessageBox('未找到相关内容')

	# 搜索
	def search(self, event):
		text = self.search_text.Value
		# 如果搜索内容不为空
		if text != '':
			self.tmp_show_data = []
			for index in range(self.show_data.shape[0]):
				if re.search(text, self.data.loc[index]['file_path']):
					self.tmp_show_data.append(self.data.loc[index])
			if self.tmp_show_data:
				self.list.DeleteAllItems()
				for show in self.tmp_show_data:
					index = self.list.InsertStringItem(self.list.GetItemCount(), show['file_path'])
					self.list.SetStringItem(index, 1, show['class'])
					self.list.SetStringItem(index, 2, show['time'])
			else:
				wx.MessageBox('未搜索到相关内容')


	# 打开文件
	def open(self, event):
		if self.file_path == '':
			wx.MessageBox('请选择一个文件')
		elif os.path.exists(self.file_path):
			os.startfile(self.file_path)
		else:
			wx.MessageBox('文件不存在')