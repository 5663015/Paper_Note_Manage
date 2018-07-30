import wx
import wx.xrc
import os
import History_Frame
import Setting_Frame
import pandas as pd
import numpy as np
import datetime
import json

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"文献阅读记录管理工具", pos = wx.DefaultPosition, size = wx.Size( 1200,810 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		# 读取设置
		json_file = open('setting.json')
		json_file = json.load(json_file)
		class_name = json_file['class_name']
		default_path = json_file['default_path']

		self.SetSizeHintsSz( wx.Size(1200, 810), wx.Size(1200, 810) )
		self.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		# 设置图标
		self.icon = wx.Icon('paper.ico', wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)


		# 文件树
		self.m_genericDirCtrl = wx.GenericDirCtrl( self, wx.ID_ANY, default_path, wx.DefaultPosition, wx.Size( 350,700 ), wx.DIRCTRL_3D_INTERNAL|wx.SIMPLE_BORDER, wx.EmptyString, 0 )
		self.m_genericDirCtrl.ShowHidden( False )
		self.m_genericDirCtrl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.m_genericDirCtrl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_genericDirCtrl.SetMinSize( wx.Size( 350,700 ) )
		#self.m_genericDirCtrl.SetMaxSize( wx.Size( 350,800 ) )
		self.m_genericDirCtrl.Bind(wx.EVT_DIRCTRL_FILEACTIVATED, self.show_note)

		gbSizer1.Add( self.m_genericDirCtrl, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer4.SetMinSize( wx.Size( 800,-1 ) )
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		# 显示未读或类别
		bSizer5.SetMinSize( wx.Size( 800,40 ) )
		self.read_or_not_text = wx.StaticText( self, wx.ID_ANY, u"未读", wx.DefaultPosition, wx.Size(140, 30), 0|wx.SIMPLE_BORDER )
		self.read_or_not_text.Wrap( -1 )
		self.read_or_not_text.SetFont( wx.Font( 15, 70, 90, 92, False, wx.EmptyString ) )
		self.read_or_not_text.SetForegroundColour( wx.Colour(255, 0, 0) )
		self.read_or_not_text.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer5.Add( self.read_or_not_text, 0, wx.ALL, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer5.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		# 更新笔记按钮
		self.updata_button = wx.Button( self, wx.ID_ANY, u"更新笔记信息", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.updata_button.Bind(wx.EVT_BUTTON, self.updata)
		bSizer5.Add( self.updata_button, 0, wx.ALL, 5 )

		# 删除笔记按钮
		self.del_button = wx.Button( self, wx.ID_ANY, u"删除笔记", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		self.del_button.Bind(wx.EVT_BUTTON, self.delete)
		bSizer5.Add( self.del_button, 0, wx.ALL, 5 )

		# 打开文件按钮
		self.open_button = wx.Button( self, wx.ID_ANY, u"打开文件", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.open_button.Bind(wx.EVT_BUTTON, self.open_file)
		bSizer5.Add( self.open_button, 0, wx.ALL, 5 )

		# 类别选择
		self.class_choiceChoices = ['请选择类别'] + class_name
		self.class_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.class_choiceChoices, 0 )
		self.class_choice.SetSelection( 0 )
		bSizer5.Add( self.class_choice, 0, wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer5.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		# 查看历史按钮
		self.history_button = wx.Button( self, wx.ID_ANY, u"历史记录", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.history_button.Bind(wx.EVT_BUTTON, self.open_history)
		bSizer5.Add( self.history_button, 0, wx.ALL, 5 )

		# 设置按钮
		self.setting_button = wx.Button( self, wx.ID_ANY, u"设置", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.setting_button.Bind(wx.EVT_BUTTON, self.open_setting)
		bSizer5.Add( self.setting_button, 0, wx.ALL, 5 )


		bSizer4.Add( bSizer5, 0, wx.EXPAND|wx.TOP, 5 )

		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		# 文本框
		self.note_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 800,700 ), wx.TE_MULTILINE|wx.SIMPLE_BORDER )
		self.note_text.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer4.Add( self.note_text, 0, wx.ALL, 5 )


		gbSizer1.Add( bSizer4, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		bSizer1.Add( gbSizer1, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		self.read_data()
		self.file_path = ''

	# 读取笔记记录信息
	def read_data(self):
		self.data = pd.read_csv('paper.csv')
		self.file_path_list = self.data['file_path'].values
		self.class_name_list = self.data['class'].values
		self.time_list = self.data['time'].values

	# 更新笔记信息
	def updata(self, event):
		# 重读一下笔记记录信息
		self.read_data()
		# 如果路径为空或文件不存在
		if self.file_path == '':
			wx.MessageBox('请选择一个文件')
		elif not os.path.exists(self.file_path):
			wx.MessageBox('文件不存在')
		else:
			new_note = self.note_text.GetValue()	# 获取新笔记
			new_class_name = self.class_choice.GetItems()[self.class_choice.GetSelection()]	# 获取新类别
			new_time = str(datetime.datetime.now())	# 获取修改时间
			# 如果此文件之前没有添加过笔记
			if self.file_path not in self.file_path_list:
				new_data = pd.DataFrame()
				new_data['file_path'] = [self.file_path]
				new_data['class'] = [new_class_name]
				new_data['time'] = [new_time]
				self.data = pd.concat([self.data, new_data])
				self.data.to_csv('paper.csv', index=False)
				# 按路径命名将笔记存入文件中
				np.save('./data/'+self.file_path.replace(':', '_').replace('\\', '_').replace('/', '_'), new_note)
			# 如果此文件之前添加过笔记
			else:
				index = self.data[self.data['file_path'] == self.file_path].index.tolist()
				self.data.loc[index[0]]['class'] = new_class_name
				self.data.loc[index[0]]['time'] = new_time
				self.data.to_csv('paper.csv', index=False)
				# 按路径命名将笔记存入文件中
				np.save('./data/'+self.file_path.replace(':', '_').replace('\\', '_').replace('/', '_'), new_note)
			# 标记为已读
			self.read_or_not_text.SetLabel(new_class_name)
			self.read_or_not_text.SetForegroundColour( wx.Colour(0, 0, 0) )
			wx.MessageBox('笔记已保存')

	# 删除笔记
	def delete(self,event):
		# 删除笔记文件
		os.remove('./data/' + self.file_path.replace(':', '_').replace('\\', '_').replace('/', '_') + '.npy')
		# 在数据文件中删除记录
		index = self.data[self.data['file_path'] == self.file_path].index.tolist()
		self.data.drop(index[0], axis=0, inplace=True)
		self.data.to_csv('paper.csv', index=False)

		wx.MessageBox('笔记已删除')

	# 双击文件树时显示笔记信息
	def show_note(self, event):
		# 重读一下笔记记录信息
		self.read_data()
		# 双击后获取文件路径
		self.file_path = self.m_genericDirCtrl.GetFilePath()
		if self.file_path in self.file_path_list:
			index = self.data[self.data['file_path'] == self.file_path].index.tolist()
			# 下拉选择显示类别
			print(self.data.loc[index[0]]['class'])
			self.class_choice.SetSelection(self.class_choiceChoices.index(self.data.loc[index[0]]['class']))
			# 读取笔记文件
			try:
				note = np.load('./data/' + self.file_path.replace(':', '_').replace('\\', '_').replace('/', '_') + '.npy')
				self.note_text.Value = str(note)
			except:
				wx.MessageBox('笔记文件不存在')
			# 标记为已读， 显示类别
			self.read_or_not_text.SetLabel(self.data.loc[index[0]]['class'])
			self.read_or_not_text.SetForegroundColour( wx.Colour(0, 0, 0) )
		else:
			# 文本框空
			self.note_text.Value = ''
			# 下拉选择显示默认的
			self.class_choice.SetSelection(0)
			# 标记为未读
			self.read_or_not_text.SetLabel('未读')
			self.read_or_not_text.SetForegroundColour( wx.Colour(255, 0, 0) )

	# 打开文件
	def open_file(self, event):
		if self.file_path == '':
			wx.MessageBox('请选择一个文件')
		elif os.path.exists(self.file_path):
			os.startfile(self.file_path)
		else:
			wx.MessageBox('文件不存在')

	# 打开历史记录窗口
	def open_history(self, event):
		history = History_Frame.HistoryFrame(None)
		history.Show()

	# 打开设置窗口
	def open_setting(self, event):
		setting = Setting_Frame.SettingFrame(None)
		setting.Show()