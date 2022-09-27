from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout 
#from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.codeinput import CodeInput
from kivy.uix.popup import Popup
from kivy.config import Config


from random import randint # Импортируем из стандартной библиотеки 
							 #функцию randint, которая генерирует раномное число
from math import sqrt #Импорт функции квадратного корня

from crypto import *

from random import randint

Config.set('graphics','resizable',0)
Config.set("graphics","width","700")
Config.set("graphics","height","500")
Window.size = (750, 500)


class CryptoApp(App):

####################################################################################################	
	def key_generator_rsa(self, instance):
		try:	
			num = []	
			while len(num) < 2:	
				num = simple(self.literal_p.text)

			e, n, Fn = exp(num) #Генерация e n Fn
			k = CloseKey(Fn, e) #Генерация K
			d = int((k * Fn + 1)/ e) # d

			open_key = str(n) + " " + str(e)
			self.Open_Key_Text.text = "".join(open_key)

			close_key = str(n) + " " + str(d)
			self.Closed_Key_Text.text = "".join(close_key)
		except ValueError:
			return "#########################\nОшибка в ключе!\n#########################"		


	def key_generator_gamal(self, instance):
		try:
			if ((self.literal_p.text != "") and \
				(self.literal_k.text != "") and \
				(self.literal_x.text != "")): 
				
				if int(self.literal_x.text) >= int(self.literal_p.text) and \
					int(self.literal_k.text) >= int(self.literal_p.text) and \
					int(self.literal_p.text) <= 64:
					self.Open_Key_Text.text = "Error"
					self.Closed_Key_Text.text = "Error"
				else:
					p = int(self.literal_p.text)
					x = int(self.literal_x.text)
					k = int(self.literal_k.text)

					g = p - 1
					temp = 1
					list_ = []

					while True:
							
						if ((g ** temp) % p) not in list_:
								#print(list)
							list_.append((g ** temp) % p)
							temp += 1
						else:
							g -= 1;
							if g == 0:
								self.Open_Key_Text.text = "G not found"
								break
							temp = 1;
							list_ = []
						
						if len(list_) == p - 1:
							break

					y = (g ** x) % p

					self.Open_Key_Text.text = str(g) + " " + str(k) + " " \
												+ str(p) + " " + str(x)
					self.Closed_Key_Text.text = str(p) + " " + str(x) + " " + str(g)
						
			else: 
				self.Open_Key_Text.text = "Error"
				self.Closed_Key_Text.text = "Error"
		except ValueError:
				self.Open_Key_Text.text = "Error"
				self.Closed_Key_Text.text = "Error"
####################################################################################################


	def clear_widget(self, instance):
		try:
			instance.remove_widget(self.Box)
		except:
			pass

	def clear(self, instance):
		try:
			self.message.text = ""
		except: pass
		try:
			self.key.text = ""
		except:
			pass
		try:
			self.Open_Key_Text.text = ""			
		except:
			pass
		try:
			self.Closed_Key_Text.text = ""
		except:
			pass
		try:
			self.literal_p.text = ""
		except:
			pass
		try:
			self.literal_x.text = ""
		except:
			pass
		try:
			self.literal_k.text = ""
		except:
			pass
		try:
			self.tbl.text_input.text = ""
		except: pass


	def resize(self, instance):

		comments = ["### PASS_GENERATOR ###",
		"### ШИФР ПРОСТОЙ ОДИНАРНОЙ ПЕРЕСТАНОВКИ ###",
		"### ШИРФ БЛОЧНОЙ ОДИНАРНОЙ ПЕРЕСТАНОВКИ ###",
		"### ШИФР ТАБЛИЧНОЙ МАРШРУТНОЙ ПЕРЕСТАНОВКИ ###",
		"### ШИФР ВЕРТИКАЛЬНОЙ ПЕРЕСТАНОВКИ ###","### ШИФР ЦЕЗАРЯ ###",
		"### ШИФР ВИЖЕНЕРА ###","### ШИФР ПЛЕЙФЕРА ###",
		"### ШИФР ТРИСЕМУСА ###","### ШИФР ЭЛЬ ГАМАЛЯ ###", "### ГОСТ ###",
		"### RSA ###", "### Решетка ###"]

		self.code = ""
		code = ""
		switch = False
		with open("crypto.py", encoding="utf8") as file:
			for string in file:
				if switch:
					if comments[int(self.button_down_index)] not in string:
						code += string
					else: break
				if comments[int(self.button_down_index)] in string:
					switch = True
		self.code += code

		cont = BoxLayout(orientation="vertical")

		code = CodeInput(font_size=11, allow_copy=False)
		code.text = self.code
	
		btn = Button(text="Exit",size_hint=[1, .1])
		
		cont.add_widget(code)
		cont.add_widget(btn)
	
		pop = Popup(title='code listing', content=cont, auto_dismiss=False)
		btn.bind(on_press=pop.dismiss)
		
		pop.open()



	def get_cipher(self, mode):

		if mode.id in ['E','D','R']:
			#self.code.font_size = 14

			if not self.message.text: 
				self.code = ":: Message is not found ::";
			else:
				if self.button_down_index == "0":
					self.message.text = pass_generator(self.message.text)

				elif self.button_down_index == "1":
					self.message.text = simple_shuffle(self.key.text, 
													mode.id, self.message.text)
				elif self.button_down_index == "2":
					self.message.text = simple_block_shuffle(self.key.text, 
													mode.id, self.message.text)
				elif self.button_down_index == "3":
					self.message.text = table_route(self.key.text, self.message.text, mode.id)

				elif self.button_down_index == "4":
					self.message.text = vertical_route(self.key.text, 
													mode.id, self.message.text)
				elif self.button_down_index == "5":
					self.message.text = cesar(self.key.text, mode.id, 
															self.message.text)
				elif self.button_down_index == "6":
					self.message.text = vijener(self.key.text, mode.id, 
															self.message.text)
				elif self.button_down_index == "7":
					self.message.text = playfair(mode.id, self.message.text, 
															self.key.text)
				elif self.button_down_index == "8":
					self.message.text = tritemus(mode.id, self.message.text, 
															self.key.text)
				elif self.button_down_index == "9":
					self.message.text = gamal(self.key.text, mode.id, 
															self.message.text)
				elif self.button_down_index == "10":
					self.message.text = RSA(self.message.text, mode.id,  
																self.key.text)

	def get_form(self, instance):
		resizeble = Button(text="Листинг кода", size_hint_y=None, 
										height=30,
										on_press=self.resize,
										background_color = [.3, .3, .3, 1])

		#self.code = CodeInput(readonly = True, hint_text = "Листинг:", 
		#								font_size = 14, 
		#								background_color = [1,1,1,.8],
		#								size_hint=[1, .7],
		#								allow_copy=False)			
			
		btn_enc = Button(text="Зашифровать", id="E", size_hint_y=None, 
										height=30,
										on_press=self.get_cipher,
										background_color = [.3, .3, .3, 1])

		btn_dec = Button(text="Расшифровать", id="D", size_hint_y=None, 
										height=30,
										on_press=self.get_cipher,
										background_color = [.3, .3, .3, 1])

		#btn_list = Button(text="Листинг", id="C", size_hint_y=None, 
		#								height=30, 
		#								on_press = self.get_cipher,
		#								background_color = [.3, .3, .3, 1])

		btn_clear = Button(text="Очистить", size_hint_y=None, height=30,
										on_press=self.clear,
										background_color = [.3, .3, .3, 1])
		
		btn_run = Button(text="Выполнить", id="R", size_hint_y=None, height=30,
										on_press=self.get_cipher,
										background_color = [.3, .3, .3, 1])		
			

		if self.Buttons_List[0].state == "down":
			
			self.clear_widget(self.right_form)

			buttons = GridLayout(cols=1, rows=4, padding=5, spacing=5, 
										size_hint=[1, .25])

			self.message = TextInput(hint_text="Сообщение", size_hint=[1, .25])
			
			#self.code = CodeInput(readonly = True, 
			#						hint_text = "Листинг:", 
			#						font_size = 14, 
			#						background_color = [1,1,1,.8],
			#						size_hint=[1, .7],
			#						allow_copy=False)
			
			buttons.add_widget(btn_run)
			#buttons.add_widget(btn_list)
			buttons.add_widget(btn_clear)
			buttons.add_widget(resizeble)

			self.Box = BoxLayout(orientation="vertical", padding=5, spacing=5)	

			self.Box.add_widget( self.message)
			#self.Box.add_widget( self.code)
			self.Box.add_widget(buttons)

			self.right_form.add_widget(self.Box)
			self.button_down_index = instance.id
		
		elif self.Buttons_List[1].state == "down" or \
			 self.Buttons_List[2].state == "down" or \
			 self.Buttons_List[3].state == "down" or \
			 self.Buttons_List[4].state == "down" or \
			 self.Buttons_List[5].state == "down" or \
			 self.Buttons_List[6].state == "down" or \
			 self.Buttons_List[7].state == "down" or \
			 self.Buttons_List[8].state == "down":

			self.clear_widget(self.right_form)

			self.message = TextInput(hint_text="Сообщение", size_hint=[1, .10])
			self.key = TextInput(hint_text="Ключ", size_hint=[1, .10])
	
			self.Box = BoxLayout(orientation="vertical", padding=5, spacing=5)	

			#self.code.size_hint=[1, .5]

			self.Box.add_widget( self.key)
			self.Box.add_widget( self.message)
			#self.Box.add_widget( self.code)

			buttons = GridLayout(cols=1, rows=5, padding=5, spacing=5, 
										size_hint=[1, .25])
	
			buttons.add_widget(btn_enc)
			buttons.add_widget(btn_dec)
			#buttons.add_widget(btn_list)
			buttons.add_widget(btn_clear)
			buttons.add_widget(resizeble)
			
			self.Box.add_widget(buttons)
			self.right_form.add_widget(self.Box)
			self.button_down_index = instance.id
		
		elif self.Buttons_List[9].state == "down":

			self.clear_widget(self.right_form)

			self.Box = BoxLayout(orientation="vertical", padding=5, spacing=5)	

			self.Open_Key_Text = TextInput(hint_text="Открытый ключ", 
											font_size=12)
			self.Closed_Key_Text = TextInput(hint_text="Закрытый ключ", 
											font_size=12)
						
			Generator_form = BoxLayout(orientation="vertical", size_hint=[1, 1])
				#{
			Top_Box = BoxLayout()
			
			self.literal_p = TextInput(hint_text="Простое число > 64", 
										font_size=12)
			self.literal_x = TextInput(hint_text="(X), (1 < X < P-1)", 
										font_size=12)
			self.literal_k = TextInput(hint_text="(K), (1 < K < P-1)",
										font_size=12)
			Button_run = Button(text="Gen", font_size=14, 
								background_color = [.3, .3, .3, 1],
								on_press=self.key_generator_gamal)
			
			Top_Box.add_widget(self.literal_p)
			Top_Box.add_widget(self.literal_x)
			Top_Box.add_widget(self.literal_k)
			Top_Box.add_widget(Button_run)
			
			Generator_form.add_widget(Top_Box)
			Generator_form.add_widget(self.Open_Key_Text)
			Generator_form.add_widget(self.Closed_Key_Text)
				#}
				#{
			Center_Form = BoxLayout(orientation="vertical", 
										padding=[5, 0, 5, 0])
			
			self.key = TextInput(size_hint=[1, None], height=40, 
									hint_text="Ключ", font_size=14)

			self.message = TextInput(hint_text="Сообщение", font_size=14)
			Center_Form.add_widget(self.key)
			Center_Form.add_widget(self.message)

			#self.code.size_hint = [1, 1]

			#Code_Form = BoxLayout(padding=5, size_hint=[1, 1.2])
			#Code_Form.add_widget(self.code)
			
			buttons = GridLayout(cols=1, rows=5, padding=5, spacing=5)

			buttons.add_widget(btn_enc)
			buttons.add_widget(btn_dec)
			#buttons.add_widget(btn_list)
			buttons.add_widget(btn_clear)
			buttons.add_widget(resizeble)
			
			dick_form = BoxLayout()
			dick_form.add_widget(Generator_form)
			dick_form.add_widget(Center_Form)

			self.Box.add_widget(dick_form)
			#self.Box.add_widget(Code_Form)
			self.Box.add_widget(buttons)
			
			self.right_form.add_widget(self.Box)
			self.button_down_index = instance.id
			###
		elif self.Buttons_List[10].state == "down":

			self.clear_widget(self.right_form)
			self.Box = Button(text="Листинг", 
							on_press=self.resize, font_size=14,
							background_color = [.3, .3, .3, 1],)
			
			self.right_form.add_widget(self.Box)
			self.button_down_index = 10

		elif self.Buttons_List[11].state == "down":

			self.clear_widget(self.right_form)

			self.Box = BoxLayout(orientation="vertical", padding=5, spacing=5)	

			self.Open_Key_Text = TextInput(hint_text="Открытый ключ", 
											font_size=12)
			self.Closed_Key_Text = TextInput(hint_text="Закрытый ключ", 
											font_size=12)
						
			Generator_form = BoxLayout(orientation="vertical")
		
			Top_Box = BoxLayout()
			
			self.literal_p = TextInput(hint_text="Диапазон чисел", 
										font_size=12)
		
			Button_run = Button(text="Сгенирировать", font_size=14,
								background_color = [.3, .3, .3, 1],
								on_press=self.key_generator_rsa)

			Top_Box.add_widget(self.literal_p)
			Top_Box.add_widget(Button_run)

			Center_Form = BoxLayout(orientation="vertical", 
										padding=[5, 0, 5, 0])
			
			self.key = TextInput(size_hint=[1, None], height=40, 
									hint_text="Ключ", font_size=14)

			self.message = TextInput(hint_text="Сообщение", font_size=14)
			Center_Form.add_widget(self.key)
			Center_Form.add_widget(self.message)

				#}
			#Code_Form = BoxLayout(padding=5)

			#self.code.size_hint = [1, 1]
			#Code_Form.add_widget(self.code)

			buttons = GridLayout(cols=1, rows=5, padding=5, spacing=5, size_hint=[1,.7])

			buttons.add_widget(btn_enc)
			buttons.add_widget(btn_dec)
			#buttons.add_widget(btn_list)
			buttons.add_widget(btn_clear)
			buttons.add_widget(resizeble)

			Generator_form.add_widget(Top_Box)
			Generator_form.add_widget(self.Open_Key_Text)
			Generator_form.add_widget(self.Closed_Key_Text)

			dick_from = BoxLayout(size_hint = [1, .8])
			dick_from.add_widget(Generator_form)
			dick_from.add_widget(Center_Form)

			self.Box.add_widget(dick_from)
			#self.Box.add_widget(Code_Form)
			self.Box.add_widget(buttons)
			
			self.right_form.add_widget(self.Box)
			self.button_down_index = instance.id

		elif self.btn_main_run.state == "down":
			self.clear_widget(self.right_form)

			self.tbl = TableApp 

			try:
				self.Box = self.tbl.build(self.tbl, self.button_chipers_text_input.text)
			except:
				self.Box = self.tbl.build(self.tbl, 6)
			#self.Box.add_widget(self.code)
			#self.Box.add_widget(btn_list)
			self.Box.add_widget(btn_clear)
			self.Box.add_widget(resizeble)

			self.right_form.add_widget(self.Box)
			self.button_down_index = 11
			
		#############
		for index in range(len(self.chiphers_Names)-1):
			self.Buttons_List[index].background_color = [.3, .3, .3, 1]
		
		self.btn_main_run.background_color = [.3, .3, .3, 1]	
		
		if self.button_down_index == 11:
			self.btn_main_run.background_color = [1,1,1,1]
		else:
			self.Buttons_List[int(self.button_down_index)].background_color= \
																	[1,1,1,1]
		

	def build(self):
		self.code = ""
		self.chiphers_Names = ["Генератор пароля [ru/en]",
		"Одинарная перестановка [ru/en]",
		"Блочная перестановка [ru/en]",
		"Табличная маршрутная пер-ка [ru/en]",
		"Вертикальная перестановка [ru/en]","Шифр Цезаря [ru]",
		"Шифр Виженера [ru]","Шифр Плейфера [ru/en]","Шифр Трисемуса [ru/en]",
		"Эль Гамаль [ru/en]", "ГОСТ", "RSA [ru/en]", "Поворотная Решетка"]

		Window.clearcolor = (.8, .8, .8, 0)
		root = BoxLayout()

		### LEFT BOX
		chiphers_Box = GridLayout(cols=1, rows=25, padding=5, spacing=2,
									 size_hint=[.5, 1])
		self.Buttons_List = [0 for _ in range(len(self.chiphers_Names))]

		for index in range(len(self.chiphers_Names) - 1):
			self.Buttons_List[index] = Button(text=self.chiphers_Names[index], 
										id=str(index),
										size_hint_y=None,
										height=30,
										font_size=13,
										on_press=self.get_form,
										background_color=[.3, .3, .3, 1])
			chiphers_Box.add_widget(self.Buttons_List[index])
		

		temp = BoxLayout(size_hint_y=None, height=30)
		self.btn_main_run = Button(text=self.chiphers_Names[-1], 
										id=str(len(self.chiphers_Names)),
										size_hint_y=None,
										height=30,
										font_size=13,
										on_press=self.get_form,
										background_color=[.3, .3, .3, 1])

		self.button_chipers_text_input = TextInput(size_hint_y=None,
												size_hint_x=.3,
												height=30,
												font_size=12,
												hint_text="Размер")

		temp.add_widget(self.btn_main_run)
		temp.add_widget(self.button_chipers_text_input)
		self.Buttons_List[-1] = temp
		chiphers_Box.add_widget(self.Buttons_List[-1])

		root.add_widget( chiphers_Box )
		###

		self.right_form = BoxLayout(padding=5)

		root.add_widget( self.right_form )
		
		self.main_form = BoxLayout()
		self.main_form.add_widget(root)

		return self.main_form


if __name__ == "__main__":
	CryptoApp().run()	