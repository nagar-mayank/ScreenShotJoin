import os.path
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
from database import *


def browse_images():
    filenames = filedialog.askopenfilenames(initialdir=os.path.join(os.path.expanduser('~'), 'Pictures'),
                                            title="Select Images",
                                            filetypes=(("Images", "*.png *.jpg *.jpeg *.bmp"), ("All Files", "*.*")))

    # It returns a tuple of selected files
    return list(filenames)


class App:
    def __init__(self, master):
        self.main_panel = master

        self.mode = StringVar(value='Original')
        self.image_bg_color = StringVar(value='Black')
        self.combined_image = None
        self.final_width = None
        self.final_height = None
        self.move_down_button_image = None
        self.move_up_button_image = None
        self.delete_button_image = None
        self.add_button_image = None
        self.new_direction = None
        self.new_output_dir = None
        self.theme_value = None
        self.font_value_var = None
        self.current_page = None
        self.right_bottom_frame = None
        self.right_top_frame = None
        self.left_option_frame = None
        self.setting_window = None
        self.image_preview_label = None
        self.third_right_frame = None
        self.new_im = None

        self.browse_images_button = None
        self.images = None
        self.image_string = None
        self.list_box = None
        self.direction = None

        self.font_list = Database.font_list

        self.variables = get_variable_values()
        self.output_dir = self.variables['output_dir']
        self.theme = self.variables['theme'][:-5]  # Remove 'Theme' from Light or Dark

        self.theme_values = get_theme_values(self.variables['theme'])

        self.fg_color = self.theme_values['fg_color']
        self.entry_bg_color = self.theme_values['entry_bg_color']
        self.bg_color = self.theme_values['bg_color']
        self.font = self.theme_values['font']
        self.font_size = self.theme_values['font_size']
        self.button_size = int(self.theme_values['button_size'])

        # Name of images depending on theme
        if self.theme == 'Dark':
            self.move_up_image_name = './images/white_move_up.png'
            self.move_down_image_name = './images/white_move_down.png'
            self.delete_button_image_name = './images/white_delete.png'
            self.add_button_image_name = './images/white_add.png'
        else:
            self.move_up_image_name = './images/dark_move_up.png'
            self.move_down_image_name = './images/dark_move_down.png'
            self.delete_button_image_name = './images/dark_delete.png'
            self.add_button_image_name = './images/dark_add.png'

        # Start building main window
        self.main_panel.title('Screen Shot Join')
        self.main_panel.iconbitmap('./images/logo.ico')

        # Creating Menubar
        menu_bar = Menu(self.main_panel, background=self.bg_color, fg=self.fg_color)
        # File menu
        file_menu = Menu(menu_bar, tearoff=0, background=self.bg_color, fg=self.fg_color)
        menu_bar.add_cascade(label="Settings", menu=file_menu)

        file_menu.add_command(label='Options', command=self.options)
        file_menu.add_separator()
        file_menu.add_command(label="New...", command=lambda: [new_app_instance()])
        file_menu.add_command(label="Exit", command=lambda: [self.main_panel.destroy()])

        self.main_panel.config(bg=self.bg_color, menu=menu_bar)

        self.direction = "Horizontal"

        first_frame = Frame(self.main_panel, bg=self.bg_color)
        Label(master=first_frame,
              bg=self.bg_color,
              fg=self.fg_color,
              font=(self.font, 14),
              text="Select and Join Images").grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        second_frame = Frame(self.main_panel, bg=self.bg_color)

        self.browse_images_button = Button(master=second_frame,
                                           bg=self.bg_color,
                                           fg=self.fg_color,
                                           font=(self.font, self.button_size),
                                           bd=2,
                                           height=1,
                                           width=15,
                                           text='Browse Images',
                                           command=lambda: [self.list_of_images(browse_images())])
        self.browse_images_button.grid(row=1, column=0, padx=5, pady=5)

        first_frame.pack(side='top')
        second_frame.pack(side='top')
        self.main_panel.minsize(1000, 150)
        self.main_panel.mainloop()

    def options(self):
        self.setting_window = Toplevel()
        self.setting_window.title('Settings')
        # Icon of the main window
        self.setting_window.iconbitmap('./images/setting.ico')

        border_color = "black" if self.theme == 'Light' else "white"
        left_frame = Frame(master=self.setting_window, bg=self.bg_color, highlightbackground=border_color,
                           highlightthickness=1)
        self.left_option_frame = Frame(master=left_frame, bg='#789bff', highlightbackground=border_color,
                                       highlightthickness=1, name='left_option_frame')

        self.left_option_frame.pack(side=TOP, fill=BOTH)

        Label(master=self.left_option_frame,
              bg='#789bff',
              fg=self.fg_color,
              font=(self.font, self.font_size),
              text='Options',
              name='options').grid(row=0, column=0, padx=20, pady=10, sticky=N)

        right_frame = Frame(master=self.setting_window, bg=self.bg_color,
                            highlightbackground=border_color, highlightthickness=1)
        self.right_top_frame = Frame(master=self.setting_window, bg=self.bg_color,
                                     highlightbackground=border_color, highlightthickness=1)

        self.right_bottom_frame = Frame(master=self.setting_window, bg=self.bg_color,
                                        highlightbackground=border_color, highlightthickness=1)

        self.font_value_var = StringVar(value=self.font)
        self.theme_value = StringVar(value=self.theme)

        Label(master=self.right_top_frame,
              text="Theme",
              font=(self.font, self.font_size),
              fg=self.fg_color,
              bg=self.bg_color).grid(row=0, column=0, padx=10, pady=4, sticky=E)

        theme_option_menu = OptionMenu(self.right_top_frame, self.theme_value, *['Light', 'Dark'])
        theme_option_menu.config(font=(self.font, self.button_size),
                                 bd=2,
                                 fg=self.fg_color,
                                 bg=self.entry_bg_color)
        theme_option_menu.grid(padx=10, pady=5, row=0, column=1, sticky=W)
        theme_option_menu["menu"]["background"] = self.entry_bg_color
        theme_option_menu["menu"]["font"] = (self.font, self.font_size)
        for x in range(int(theme_option_menu['menu'].index('end')) + 1):
            theme_option_menu['menu'].entryconfig(x, font=(self.font, self.font_size))
            theme_option_menu.children['menu'].entryconfig(x, foreground=self.fg_color)
        theme_option_menu["menu"]["activeborderwidth"] = '2'

        Label(master=self.right_top_frame, text="Font", font=(self.font, self.font_size), fg=self.fg_color,
              bg=self.bg_color).grid(row=1, column=0, padx=10, pady=4, sticky=E)

        font_option_menu = OptionMenu(self.right_top_frame, self.font_value_var, *self.font_list)
        font_option_menu.config(font=(self.font, self.button_size),
                                bd=2,
                                fg=self.fg_color,
                                bg=self.entry_bg_color)
        font_option_menu.grid(padx=10, pady=5, row=1, column=1, sticky=W)
        font_option_menu["menu"]["background"] = self.entry_bg_color
        font_option_menu["menu"]["font"] = (self.font, self.font_size)
        for x in range(int(font_option_menu['menu'].index('end')) + 1):
            font_option_menu['menu'].entryconfig(x, font=(self.font_list[x], self.font_size))
            font_option_menu.children['menu'].entryconfig(x, foreground=self.fg_color)
        font_option_menu["menu"]["activeborderwidth"] = '2'

        Label(master=self.right_top_frame, text="Mode", font=(self.font, self.font_size), fg=self.fg_color,
              bg=self.bg_color).grid(row=2, column=0, padx=10, pady=4, sticky=E)

        mode_option_menu = OptionMenu(self.right_top_frame, self.mode, *['Original', 'Stretch'])
        mode_option_menu.config(font=(self.font, self.button_size),
                                bd=2,
                                fg=self.fg_color,
                                bg=self.entry_bg_color)
        mode_option_menu.grid(padx=10, pady=5, row=2, column=1, sticky=W)
        mode_option_menu["menu"]["background"] = self.entry_bg_color
        for x in range(int(mode_option_menu['menu'].index('end')) + 1):
            mode_option_menu['menu'].entryconfig(x, font=(self.font, self.font_size), foreground=self.fg_color)
        mode_option_menu["menu"]["activeborderwidth"] = '2'

        Label(master=self.right_top_frame,
              bg=self.bg_color,
              fg=self.fg_color,
              font=(self.font, 14),
              text="Choose Orientation").grid(row=3, column=0, padx=10, pady=5, sticky=E)

        self.new_direction = StringVar(value=self.direction)
        font_drop = OptionMenu(self.right_top_frame, self.new_direction, *["Vertical", "Horizontal"])
        font_drop.config(bg=self.entry_bg_color, font=(self.font, self.button_size), bd=2, fg=self.fg_color)
        font_drop.grid(row=3, column=1, padx=10, pady=5, sticky=W)
        font_drop["menu"]["background"] = self.entry_bg_color
        for x in range(int(font_drop['menu'].index('end')) + 1):
            font_drop['menu'].entryconfig(x, font=(self.font, 14), foreground=self.fg_color)
        font_drop["menu"]["activeborderwidth"] = '2'

        Label(master=self.right_top_frame,
              bg=self.bg_color,
              fg=self.fg_color,
              font=(self.font, 14),
              text="Image Background Color").grid(row=4, column=0, padx=10, pady=5, sticky=E)

        image_bg_drop = OptionMenu(self.right_top_frame, self.image_bg_color, *["Black", "White"])
        image_bg_drop.config(bg=self.entry_bg_color, font=(self.font, self.button_size), bd=2, fg=self.fg_color)
        image_bg_drop.grid(row=4, column=1, padx=10, pady=5, sticky=W)
        image_bg_drop["menu"]["background"] = self.entry_bg_color
        for x in range(int(image_bg_drop['menu'].index('end')) + 1):
            image_bg_drop['menu'].entryconfig(x, font=(self.font, 14), foreground=self.fg_color)
        image_bg_drop["menu"]["activeborderwidth"] = '2'

        Label(master=self.right_top_frame,
              bg=self.bg_color,
              fg=self.fg_color,
              font=(self.font, 14),
              text=f"Current Output Directory").grid(row=5, column=0, padx=10, pady=5, sticky=E)

        output_dir_label = Label(master=self.right_top_frame,
                                 bg=self.bg_color,
                                 fg='gray',
                                 font=(self.font, 10),
                                 text=self.output_dir,
                                 name='output_dir_label')
        output_dir_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky=E)

        Button(master=self.right_top_frame,
               bg=self.bg_color,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               bd=2,
               height=1,
               width=15,
               text="Change Directory",
               command=lambda: [output_dir_label.config(text=self.change_output_dir())])\
            .grid(row=5, column=1, padx=10, pady=5, sticky=W)

        # Buttons
        Button(master=self.right_bottom_frame,
               bd=2,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               text='Cancel',
               height=1,
               width=10,
               bg=self.bg_color,
               command=lambda: [self.setting_window.destroy()]
               ).pack(side=RIGHT, padx=4, pady=10)
        Button(master=self.right_bottom_frame,
               bd=2,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               text='Apply',
               height=1,
               width=10,
               bg=self.bg_color,
               command=lambda: [self.change_settings(window_destroy=False)]).pack(side=RIGHT, padx=4, pady=10)
        Button(master=self.right_bottom_frame,
               bd=2,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               text='Ok',
               height=1,
               width=10,
               bg=self.bg_color,
               command=lambda: [self.change_settings(window_destroy=True)]).pack(side=RIGHT, padx=4, pady=10)

        left_frame.pack(side=LEFT, fill=Y)
        right_frame.pack(side=LEFT)
        self.right_top_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.right_bottom_frame.pack(side=TOP, fill=X)

        # Configure setting_window
        self.setting_window.config(bg=self.bg_color)
        self.setting_window.minsize(650, 400)
        self.setting_window.grab_set()
        self.setting_window.mainloop()

    def change_settings(self, window_destroy):
        # If orientation changed refresh the preview window
        if self.direction != self.new_direction.get():
            self.direction = self.new_direction.get()

        # If output directory is changed
        if self.output_dir != self.new_output_dir and self.new_output_dir is not None:
            self.output_dir = self.new_output_dir
            self.variables['output_dir'] = self.output_dir
            Database.update_meta_value('output_dir', self.output_dir)

        if self.theme != self.theme_value.get() or self.theme_values['font'] != self.font_value_var.get():
            # Updating theme value in database
            self.variables['theme'] = self.theme_value.get() + 'Theme'
            Database.update_meta_value('theme', self.variables['theme'])
            self.theme_values = get_theme_values(self.variables['theme'])
            self.theme = self.variables['theme'][:-5]

            # Updating font value
            Database.update_theme_value(self.variables['theme'], 'font', self.font_value_var.get())\
                if self.font_value_var.get() != self.font else None
            self.theme_values['font'] = self.font_value_var.get()

            # Changing profile values from current theme values
            self.fg_color = self.theme_values['fg_color']
            self.entry_bg_color = self.theme_values['entry_bg_color']
            self.bg_color = self.theme_values['bg_color']
            self.font = self.theme_values['font']

            # Updating the names of the button's images according to the theme
            if self.theme == 'Dark':
                self.move_up_image_name = './images/white_move_up.png'
                self.move_down_image_name = './images/white_move_down.png'
                self.delete_button_image_name = './images/white_delete.png'
                self.add_button_image_name = './images/white_add.png'
            else:
                self.move_up_image_name = './images/dark_move_up.png'
                self.move_down_image_name = './images/dark_move_down.png'
                self.delete_button_image_name = './images/dark_delete.png'
                self.add_button_image_name = './images/dark_add.png'

            # Changing theme of currently open widgets
            self.change_theme(self.main_panel)
            self.change_theme(self.setting_window, flag='setting_window')

        # Refresh Preview window
        self.show_preview()
        if window_destroy:
            self.setting_window.destroy()

    def change_theme(self, window, flag=''):
        if flag == 'setting_window':
            border_color = "black" if self.theme == 'Light' else "white"
            window.config(bg=self.bg_color, highlightbackground=border_color)
        if str(window).split('.')[-1] == 'left_option_frame':
            window.config(bg='#789bff')
        else:
            window.config(bg=self.bg_color)
        for widget in window.winfo_children():
            if widget.winfo_class() == 'Label':
                if str(widget).split('.')[-1] == 'output_dir_label':
                    widget.config(font=(self.font, 10), bg=self.bg_color, fg='gray')
                elif str(widget).split('.')[-1] == 'options':
                    widget.config(bg='#789bff', fg=self.fg_color, font=(self.font, self.font_size))
                else:
                    widget.config(font=(self.font, self.font_size), bg=self.bg_color, fg=self.fg_color)
            elif widget.winfo_class() == 'Button':
                if str(widget).split('.')[-1] == 'add_button':
                    self.add_button_image = PhotoImage(master=self.main_panel, file=self.add_button_image_name)
                    widget.config(image=self.add_button_image, bg=self.bg_color)
                elif str(widget).split('.')[-1] == 'delete_button':
                    self.delete_button_image = PhotoImage(master=self.main_panel, file=self.delete_button_image_name)
                    widget.config(image=self.delete_button_image, bg=self.bg_color)
                elif str(widget).split('.')[-1] == 'move_up':
                    self.move_up_button_image = PhotoImage(master=self.main_panel, file=self.move_up_image_name)
                    widget.config(image=self.move_up_button_image, bg=self.bg_color)
                elif str(widget).split('.')[-1] == 'move_down':
                    self.move_down_button_image = PhotoImage(master=self.main_panel, file=self.move_down_image_name)
                    widget.config(image=self.move_down_button_image, bg=self.bg_color)
                else:
                    widget.config(font=(self.font, self.button_size), bg=self.bg_color, fg=self.fg_color)
            elif widget.winfo_class() == 'Menu':
                widget.winfo_children()[0].config(background=self.bg_color, fg=self.fg_color)
            elif widget.winfo_class() == 'Entry':
                widget.config(font=(self.font, self.font_size), fg=self.fg_color, bg=self.entry_bg_color)
            elif widget.winfo_class() == 'Menubutton':
                widget.config(fg=self.fg_color, bg=self.entry_bg_color, font=(self.font, self.button_size))
                widget["menu"]["background"] = self.entry_bg_color
                widget["menu"]["font"] = (self.font, self.font_size)
                for x in range(int(widget['menu'].index('end')) + 1):
                    widget['menu'].entryconfig(x, font=(self.font, self.font_size))
                    widget.children['menu'].entryconfig(x, foreground=self.fg_color)
            elif widget.winfo_class() == 'Frame':
                self.change_theme(widget, flag=flag)

    def combine_images(self, save=False):
        self.main_panel.minsize(1000, 700)
        self.main_panel.state('zoomed')
        if not self.images:
            return None
        elif len(self.images) == 1:
            messagebox.showerror(master=self.main_panel, title="Error", message="Please select more than one image")
            return None
        images = [Image.open(x) for x in self.images]
        widths, heights = zip(*(i.size for i in images))

        if self.direction == "Horizontal":
            x_offset = 0
            y_offset = 0
            self.final_width = sum(widths)
            self.final_height = max(heights)

            if self.image_bg_color.get() == 'White':
                self.new_im = Image.new(mode='RGB', size=(self.final_width, self.final_height), color=(255, 255, 255))
            elif self.image_bg_color.get() == 'Black':
                self.new_im = Image.new(mode='RGB', size=(self.final_width, self.final_height), color=(0, 0, 0))

            for im in images:
                if self.mode.get() == 'Stretch':
                    im = im.resize((im.size[0], self.final_height), Image.ANTIALIAS)
                elif self.mode.get() == 'Original':
                    pass
                self.new_im.paste(im, (x_offset, y_offset))
                x_offset += im.size[0]

            self.new_im.resize(
                (self.main_panel.winfo_width() // 2,
                 int((self.main_panel.winfo_width() / 2)*self.final_height/self.final_width)),
                Image.ANTIALIAS).save(os.path.join(app_data_location, 'temp.png'))

        elif self.direction == "Vertical":
            x_offset = 0
            y_offset = 0
            self.final_height = sum(heights)
            self.final_width = max(widths)

            if self.image_bg_color.get() == 'White':
                self.new_im = Image.new(mode='RGB', size=(self.final_width, self.final_height), color=(255, 255, 255))
            elif self.image_bg_color.get() == 'Black':
                self.new_im = Image.new(mode='RGB', size=(self.final_width, self.final_height), color=(0, 0, 0))

            for im in images:
                if self.mode.get() == 'Stretch':
                    im = im.resize((self.final_width, im.size[1]), Image.ANTIALIAS)
                elif self.mode.get() == 'Original':
                    pass
                self.new_im.paste(im, (x_offset, y_offset))
                y_offset += im.size[1]
            self.new_im.resize(
                (int((self.main_panel.winfo_height() / 2)*self.final_width/self.final_height),
                 self.main_panel.winfo_height() // 2),
                Image.ANTIALIAS).save(os.path.join(app_data_location, 'temp.png'))

        if save:
            # Create output folder if not exist
            if not os.path.exists(self.output_dir):
                os.mkdir(self.output_dir)
            # Get a unique output file_name
            file_name = os.path.join(self.output_dir, self.images[0].split('/')[-1].split('.')[0] + '_joined.png')
            while os.path.exists(file_name):
                file_name = file_name[:-11] + '_' + file_name[-11:]

            # Save output image
            self.new_im.save(file_name)
            messagebox.showinfo(master=self.main_panel, title="Success", message="Combined image is saved!")
            self.clear_list_box()

        return os.path.join(app_data_location, 'temp.png')

    def move_up(self):
        idx = self.list_box.curselection()
        if not idx:
            return
        pos = idx[0]
        if pos != 0:
            text = self.list_box.get(pos)
            self.list_box.delete(pos)
            self.list_box.insert(pos - 1, text)
            image_path_name = self.images.pop(pos)
            self.images.insert(pos - 1, image_path_name)
            self.list_box.selection_set(pos - 1)

            self.show_preview()

    def move_down(self):
        idx = self.list_box.curselection()
        if not idx:
            return
        pos = idx[0]
        if pos != len(self.images) - 1:
            text = self.list_box.get(pos)
            self.list_box.delete(pos)
            self.list_box.insert(pos+1, text)
            image_path_name = self.images.pop(pos)
            self.images.insert(pos+1, image_path_name)
            self.list_box.selection_set(pos + 1)

            self.show_preview()

    def delete(self):
        idx = self.list_box.curselection()
        if not idx:
            return
        pos = idx[0]
        self.list_box.delete(pos)
        self.images.pop(pos)

        self.show_preview()

    def show_preview(self):
        # If any widgets are already there in self.third_right_frame then delete it first
        try:
            for widget in self.third_right_frame.winfo_children():
                widget.destroy()
        except AttributeError:
            pass

        Label(master=self.third_right_frame,
              text='Output Image Preview',
              fg=self.fg_color,
              bg=self.bg_color,
              font=(self.font, self.font_size)).pack(side='top', padx=5, pady=5, fill=X)

        preview_img = self.combine_images()
        if preview_img:
            self.combined_image = PhotoImage(master=self.main_panel, file=preview_img)
            self.image_preview_label = Label(master=self.third_right_frame, image=self.combined_image, bg=self.bg_color)
            self.image_preview_label.pack(side='top', fill=BOTH, expand=True)

    def list_of_images(self, images):
        self.browse_images_button.config(state=DISABLED)
        self.images = images
        image_names_list = [image.split('/')[-1] for image in self.images]

        third_frame = Frame(self.main_panel, bg=self.bg_color)
        third_left_frame = Frame(third_frame, bg=self.bg_color)
        self.third_right_frame = Frame(third_frame, bg=self.bg_color)

        button_frame = Frame(third_left_frame, bg=self.bg_color)
        image_list_frame = Frame(third_left_frame, bg=self.bg_color)

        self.delete_button_image = PhotoImage(master=self.main_panel, file=self.delete_button_image_name)
        Button(master=button_frame,
               bg=self.bg_color,
               bd=0,
               image=self.delete_button_image,
               name='delete_button',
               command=lambda: [self.delete()]).pack(side='right', padx=(0, 25))

        self.add_button_image = PhotoImage(master=self.main_panel, file=self.add_button_image_name)
        Button(master=button_frame,
               bg=self.bg_color,
               bd=0,
               image=self.add_button_image,
               name='add_button',
               command=lambda: [self.add_more_images()]).pack(side='right', padx=4)

        self.move_down_button_image = PhotoImage(master=self.main_panel, file=self.move_down_image_name)
        Button(master=button_frame,
               bg=self.bg_color,
               bd=0,
               image=self.move_down_button_image,
               name='move_down',
               command=lambda: [self.move_down()]).pack(side='right', padx=4)

        self.move_up_button_image = PhotoImage(master=self.main_panel, file=self.move_up_image_name)
        Button(master=button_frame,
               bg=self.bg_color,
               bd=0,
               image=self.move_up_button_image,
               name='move_up',
               command=lambda: [self.move_up()]).pack(side='right', padx=4)

        scrollbar_y = Scrollbar(image_list_frame)
        scrollbar_y.pack(side='right', fill='y')

        self.list_box = Listbox(master=image_list_frame,
                                selectmode="single",
                                yscrollcommand=scrollbar_y.set,
                                font=(self.font, 14))
        self.list_box.pack(side='top', padx=5, fill="both", expand=True)
        [self.list_box.insert(idx, item) for idx, item in enumerate(image_names_list)]

        button_frame.pack(side='top', padx=0, pady=0, fill='x')
        image_list_frame.pack(side='top', fill='both', expand=True)

        fourth_frame = Frame(self.main_panel, bg=self.bg_color)
        Button(master=fourth_frame,
               bg=self.bg_color,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               bd=2,
               height=1,
               width=10,
               text="Merge",
               command=lambda: [self.combine_images(save=True)]).pack(side='left', padx=5)

        Button(master=fourth_frame,
               bg=self.bg_color,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               bd=2,
               height=1,
               width=20,
               text="Open Output Folder",
               command=lambda: [os.startfile(self.output_dir)]).pack(side='left', padx=5)

        self.show_preview()

        third_frame.pack(side=TOP, fill=BOTH, expand=True)
        third_left_frame.pack(side='left', padx=10, pady=10, fill=BOTH, expand=True)
        self.third_right_frame.pack(side='left', padx=10, pady=10, fill=BOTH, expand=True)
        fourth_frame.pack(side=TOP, pady=10)

    def add_more_images(self):
        new_images = list(browse_images())
        self.images += new_images
        for img in new_images:
            self.list_box.insert(END, img.split('/')[-1])

        self.show_preview()

    def change_output_dir(self):
        self.new_output_dir = filedialog.askdirectory(initialdir=self.output_dir)
        if self.new_output_dir:
            return self.new_output_dir
        return self.output_dir

    def clear_list_box(self):
        for _ in range(len(self.images)):
            self.list_box.delete(0)
        self.images = []
        self.image_preview_label.config(image='')


def new_app_instance():
    new_instance = Tk()
    App(new_instance)
    # Removing temporary files
    if os.path.exists(os.path.join(app_data_location, 'temp.png')):
        os.remove(os.path.join(app_data_location, 'temp.png'))


if __name__ == '__main__':
    new_app_instance()
    # Removing temporary files
    if os.path.exists(os.path.join(app_data_location, 'temp.png')):
        os.remove(os.path.join(app_data_location, 'temp.png'))
