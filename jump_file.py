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

		self.new_paths = self.matchFile(new_path, files)
		
		self.new_paths += self.matchFile(str, files)

		if len(self.new_paths) == 0:
			sublime.error_message("No file found")
		elif len(self.new_paths) == 1:
			self.view.window().open_file(self.new_paths[0])
		else:
			self.view.window().show_quick_panel(self.new_paths, self.open_file)

	def open_file(self, selected_index):
 		if selected_index != -1:
 			file = self.new_paths[selected_index]
 			self.view.window().open_file(file)
	def matchFile(self,path,files):
		fileList = []
		for file in files:
			if path in file:
				fileList.append(file)
		return fileList

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






