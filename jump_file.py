import sublime
import sublime_plugin
import os
import json

class JumpFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		str = ''
		for s in self.view.sel():
			if s.empty() or s.size() < 1:
				return
			# 选中的文本
			str = self.view.substr(s)  #'/Context.sublime-menu'

		# 选中的路径
		new_pathItems = str.split('/')

		# 当前文件路径
		cur_pathItems = self.view.file_name().split('/')
		cur_pathItems.pop()

		for item in new_pathItems:
			if item == '..':
				cur_pathItems.pop()
			elif item and item != '.':
				cur_pathItems.append(item)

		# 要打开的完整路径
		new_path = '/'.join(cur_pathItems)

		project_folders = self.view.window().folders()
		config = {}
		if len(project_folders):
			config = self.load_config(project_folders[0])

		files = []
		for folder in project_folders:
			files += self.files(folder,config)

		new_path = self.matchFile(new_path, files)
		
		if not new_path:
			new_path = self.matchFile(str, files)

		if not new_path:
			sublime.error_message("No file found")
		else:
			self.view.window().open_file(new_path)

	def matchFile(self,path,files):
		for file in files:
			if path in file:
				return file

	def files(self,file_dir,config):   
		L=[]   
		for root, dirs, files in os.walk(file_dir):
			if not self.isIgnore(root,config):
			    for file in files:
			    	path = os.path.join(root, file)
			    	L.append(path) 
		return L

	# 获取配置文件
	def load_config(self,path):
		config_path = os.path.join(path, 'jump.config')
		if os.path.exists(config_path):
			f = open(config_path, 'r')
			config = json.load(f)
			return config
		return {}

	def isIgnore(self,root,config):
		ignores = config.get('ignore')
		if ignores:
			for ignore in ignores:
				if ignore in root:
					return True
		return False






