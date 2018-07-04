import sublime
import sublime_plugin
import os

class JumpFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for s in self.view.sel():
			if s.empty() or s.size() < 1:
				break
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
			files = []
			for folder in project_folders:
				files += self.files(folder)

			matched = False
			for file in files:
				if new_path in file:
					new_path = file
					matched = True
					break
			if not matched:
				for file in files:
					if str in file:
						new_path = file
						matched = True
						break
			if not matched:
				sublime.error_message("No file found")
			else:
				self.view.window().open_file(new_path)

	def files(self,file_dir):   
		L=[]   
		for root, dirs, files in os.walk(file_dir):
		    for file in files:
		    	path = os.path.join(root, file)
		    	L.append(path) 
		return L






