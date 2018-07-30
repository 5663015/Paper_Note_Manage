import wx
import wx.xrc
import pandas as pd
import Main_Frame
import json
import os

###########################################################################
## Class SettingFrame
###########################################################################

class SettingFrame(wx.Frame):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"设置", pos = wx.DefaultPosition, size = wx.Size( 300,200 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHintsSz( wx.Size( 300,200 ), wx.Size( 300,200 ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		# 设置图标
		self.icon = wx.Icon('paper.ico', wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)

		# 文本框添加新类别
		self.new_class_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.new_class_text, 0, wx.ALL, 5 )

		self.add_calss_button = wx.Button( self, wx.ID_ANY, u"添加新类别", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.add_calss_button, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer7, 0, wx.EXPAND, 5 )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		#选择文件夹
		self.m_dirPicker = wx.DirPickerCtrl( self, wx.ID_ANY, u"选择默认文件夹", u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer9.Add( self.m_dirPicker, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer9, 0, wx.EXPAND, 5 )

		self.m_staticline8 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer6.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )

		# 确定按钮
		self.enter_button = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.enter_button.Bind(wx.EVT_BUTTON, self.enter)
		bSizer6.Add( self.enter_button, 0, wx.ALL, 5 )


		self.SetSizer( bSizer6 )
		self.Layout()

		self.Centre( wx.BOTH )

	# 确定按钮
	def enter(self, event):
		#setting = pd.read_csv('setting.csv')
		json_file = open('setting.json')
		json_file = json.load(json_file)
		class_name = json_file['class_name']
		default_path = json_file['default_path']

		new_class = self.new_class_text.GetValue()
		new_path = self.m_dirPicker.GetPath()

		if new_class != '':
			class_name.append(new_class)

		if os.path.exists(new_path):
			default_path = new_path

		setting_dic = {
			'class_name': class_name,
			'default_path': default_path
		}
		js = json.dumps(setting_dic)
		file = open('setting.json', 'w')
		file.write(js)
		file.close()



