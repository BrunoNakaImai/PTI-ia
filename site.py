import flet as ft

class Message:
	def __init__(self, user_name: str, text: str, message_type: str):
		self.user_name = user_name
		self.text = text
		self.message_type = message_type

class ChatMessage(ft.Row):
	def __init__(self, message: Message):
		super().__init__()
		self.vertical_alignment = "start"
		self.controls = [
			ft.CircleAvatar(
				content=ft.Text(self.get_initials(message.user_name)),
				color=ft.colors.WHITE,
				bgcolor=self.get_avatar_color(message.user_name),
			),
			ft.Column(
				[
					ft.Text(message.user_name),
					ft.Text(message.text, selectable=True, width=400),
				]
			)
		]
	def get_initials(self, user_name: str):
		return user_name[:1].capitalize()

	def get_avatar_color(self, user_name: str):
		color_lookup = [
			ft.colors.AMBER,
			ft.colors.BLUE,
			ft.colors.BROWN,
			ft.colors.CYAN,
			ft.colors.GREEN,
			ft.colors.INDIGO,
			ft.colors.LIME,
			ft.colors.ORANGE,
			ft.colors.PINK,
			ft.colors.PURPLE,
			ft.colors.RED,
			ft.colors.TEAL,
			ft.colors.YELLOW,
		]
		return color_lookup[hash(user_name)%len(color_lookup)]

def main(page: ft.Page):
	page.theme_mode = "dark"

	def join_chat_click(e):
		if not join_user_name.value:
			join_user_name.error_text = "Você precisa me falar seu nome primeiro"
			join_user_name.update()
		else:
			page.session.set("user_name", join_user_name.value)
			page.dialog.open = False
			new_message.prefix = ft.Text(f"{join_user_name.value}: ")
			page.pubsub.send_all(Message(user_name=join_user_name.value, message_type="login_message", text=f"{join_user_name.value} has joined the chat"))
			page.pubsub.send_all(Message(user_name="Serene", message_type="chat_message", text="Olá meu nome é Serene e sou sua assistente virtual, como posso te ajudar?"))
			page.update()

	def send_mesage_click(e):
		if new_message != "":
			page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, message_type="chat_message"))
			page.pubsub.send_all(Message(user_name="Serene", message_type="chat_message", text="Obrigado pela sua mensagem!"))
			new_message.value = ""
			new_message.update()

	def on_message(message: Message):
		if message.message_type == "chat_message":
			m = ChatMessage(message)
		elif message.message_type == "login_message":
			m = ft.Text(message.text, italic=True, color=ft.colors.WHITE30, size=20)
		chat.controls.append(m)
		page.update()

	page.pubsub.subscribe(on_message)

	join_user_name = ft.TextField(
		label="Qual o seu nome?...",
		autofocus=True,
		on_submit=join_chat_click
	)

	page.dialog = ft.AlertDialog(
		open=True,
		modal=True,
		title=ft.Text("Bem vindo(a)"),
		content=ft.Column([join_user_name], width=300, height=70, tight=True),
		actions=[ft.ElevatedButton(text="Join Chat", on_click=join_chat_click)]
	)

	chat = ft.ListView(
		expand=True,
		spacing=40,
		auto_scroll=True
	)

	new_message = ft.TextField(
		hint_text='Escreva oque você está pensando...',
		autofocus=True,
		shift_enter=True,
		min_lines=1,
		max_lines=5,
		filled=True,
		expand=True,
		border_radius=20,
		on_submit=send_mesage_click,
		border_color=ft.colors.BLUE
	)

	page.add(
		ft.Row([ft.Text('Chatbot', style="headlineLarge", color='blue')], alignment="center"),
		ft.Container(
			content=chat,
			border=ft.border.all(2, ft.colors.BLUE),
			border_radius=20,
			padding=10,
			expand=True
		),
		ft.Row(
			[
				new_message,
				ft.IconButton(
					icon=ft.icons.SEND_ROUNDED,
					tooltip="Send message",
					on_click=send_mesage_click,
					icon_color=ft.colors.BLUE
				)
			]
		)
	)

ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)