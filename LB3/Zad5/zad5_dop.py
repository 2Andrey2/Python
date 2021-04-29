import wx
class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Обработка строк", size=(400, 320))

        panel = wx.Panel(self, -1)
        wx.StaticText(panel, -1, "Строка:", pos=(5, 20))
        self.entry_text = wx.TextCtrl(panel, -1, "", size=(300, -1), pos=(70, 20))
        wx.StaticText(panel, -1, "Результат:", pos=(5, 230))
        self.result_text = wx.TextCtrl(panel, -1, "", size=(300, -1), pos=(70, 230))

        self.size_spin = sc = wx.SpinCtrl(panel, -1, "", (295, 55), (40, -1))
        sc.SetRange(1, 20)
        sc.SetValue(5)

        self.clean_checkbox = wx.CheckBox(panel, -1, "Удалить слова размером меньше", (70, 60), (250, 20))
        wx.StaticText(panel, -1, "букв", pos=(340, 62))
        self.replace_checkbox = wx.CheckBox(panel, -1, "Заменить все цифры на *", (70, 80), (220, 20))
        self.insert_spaces_checkbox = wx.CheckBox(panel, -1, "Вставить пробелы между символами", (70, 100), (280, 20))
        self.sort_checkbox = wx.CheckBox(panel, -1, "Сортировать слова в строке", (70, 120), (220, 20))

        self.radio_by_size = wx.RadioButton(
            panel, -1, "По размеру", (100, 140), (150, 20))
        self.radio_by_lex = wx.RadioButton(
            panel, -1, "Лексикографически", (100, 160), (150, 20))
        self.radio_by_size.SetValue(True)
        self.radio_by_size.Disable()
        self.radio_by_lex.Disable()

        format_button = wx.Button(panel, -1, "Форматирование", size=(300, 30), pos=(70, 190))

        self.Bind(wx.EVT_BUTTON, self.on_format_click, format_button)
        self.Bind(wx.EVT_CHECKBOX, self.sort_check, self.sort_checkbox)

    def on_format_click(self, event):
        result = self.entry_text.Value

        if self.sort_checkbox.IsChecked():
            if self.radio_by_size.GetValue():
                words =  result.split(' ')
                result = ' '.join(sorted(words, key=lambda word: len(word))).lstrip()
            else:
                words =  result.split(' ')
                result = ' '.join(sorted(words)).lstrip()

        if self.clean_checkbox.IsChecked():
            words = result.split(' ')
            for i in range(len(words)):
                if (len(words[i])<int(self.size_spin.Value)):
                    words[i] = ''
            result = ' '.join(words)

        if self.replace_checkbox.IsChecked():
            words = result.split(' ')
            for i in range(len(words)):
                lit = list(words[i])
                for j in range(len(lit)):
                    if lit[j].isdigit():
                        lit[j]='*'
                words[i] = ''.join(lit)
            result = ' '.join(words)

        if self.insert_spaces_checkbox.IsChecked():
            words = result.split(' ')
            for i in range(len(words)):
                lit = list(words[i])
                words[i] = ' '.join(lit)
            result = ' '.join(words)

        self.result_text.Value = result

    def sort_check(self, event):
        if self.sort_checkbox.IsChecked():
            self.radio_by_size.Enable()
            self.radio_by_lex.Enable()
        else:
            self.radio_by_size.Disable()
            self.radio_by_lex.Disable()