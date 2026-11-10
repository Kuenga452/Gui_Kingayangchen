from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class HelloApp(App):

    def build(self):

        # Create vertical layout
        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        # Create a label
        self.label = Label(
            text="Hello, World!",
            font_size=24
        )

        # Create a button
        button = Button(
            text="Click Me",
            size_hint=(1, 0.3)
        )

        # Connect button click event
        button.bind(on_press=self.show_message)

        # Add widgets to layout
        layout.add_widget(self.label)
        layout.add_widget(button)

        return layout

    def show_message(self, instance):
        self.label.text = "Welcome to Kivy!"


# Run the application
if __name__ == "__main__":
    HelloApp().run()