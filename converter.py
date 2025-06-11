import tkinter as tk
from tkinter import ttk

length_units = {
    'Километр': 1000, 'Метр': 1, 'Сантиметр': 0.01, 'Миллиметр': 0.001,
    'Миля': 1609.344, 'Ярд': 0.9144, 'Фут': 0.3048, 'Дюйм': 0.0254
}
weight_units = {
    'Тонна': 1000, 'Килограмм': 1, 'Грамм': 0.001, 'Центнер': 100,
    'Фунт': 0.45359237, 'Унция': 0.0283495
}
time_units = {
    'Час': 60,'Секунда': 0.016667, 'Минута': 1, '1 сутки':1440,
    '1 неделя': 10080, '1 месяц': 43829.1, '1 год': 525960
}

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Конвертер единиц измерения')
        self.root.geometry('400x300')
        self.root.resizable(False, False)

        style = ttk.Style(self.root)
        style.theme_use('vista')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TRadiobutton', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TCombobox', padding=5)

        self.unit_type = tk.StringVar(value='Длина')
        self.from_unit = tk.StringVar()
        self.to_unit = tk.StringVar()
        self.input_value = tk.StringVar()
        self.result_value = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.grid(row=0, column=0, sticky='nsew')

        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky='ew')
        ttk.Label(type_frame, text='Выберите тип единиц:', font=('Arial', 11, 'bold')).grid(row=0, column=0, columnspan=2)
        ttk.Radiobutton(type_frame, text='Длина', variable=self.unit_type, value='Длина', command=self.update_units).grid(row=1, column=0, padx=5)
        ttk.Radiobutton(type_frame, text='Вес', variable=self.unit_type, value='Вес', command=self.update_units).grid(row=1, column=1, padx=5)
        ttk.Radiobutton(type_frame, text='Время', variable=self.unit_type, value='Время', command=self.update_units).grid(row=1, column=2, padx=5)

        ttk.Label(main_frame, text='Введите значение:').grid(row=1, column=0, sticky='w')
        ttk.Entry(main_frame, textvariable=self.input_value, font=('Arial', 10)).grid(row=1, column=1, columnspan=2, sticky='ew', pady=3)

        ttk.Label(main_frame, text='Из:').grid(row=2, column=0, sticky='w')
        self.from_combobox = ttk.Combobox(main_frame, textvariable=self.from_unit, state='readonly', font=('Arial', 10))
        self.from_combobox.grid(row=2, column=1, sticky='ew', padx=5)

        ttk.Label(main_frame, text='В:').grid(row=3, column=0, sticky='w')
        self.to_combobox = ttk.Combobox(main_frame, textvariable=self.to_unit, state='readonly', font=('Arial', 10))
        self.to_combobox.grid(row=3, column=1, sticky='ew', padx=5)

        swap_btn = ttk.Button(main_frame, text='↔', width=3, command=self.swap_units)
        swap_btn.grid(row=3, column=2, sticky='w', padx=2)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=15)
        ttk.Button(btn_frame, text='Перевести', command=self.convert).grid(row=0, column=0, padx=5, ipadx=20)
        ttk.Button(btn_frame, text='Очистить', command=self.clear).grid(row=0, column=1, padx=5, ipadx=20)

        ttk.Label(main_frame, text='Результат:').grid(row=5, column=0, sticky='w')
        result_entry = ttk.Entry(main_frame, textvariable=self.result_value, state='readonly', font=('Arial', 10))
        result_entry.grid(row=5, column=1, columnspan=2, sticky='ew', pady=3)
        result_entry.bind('<Double-Button-1>', self.copy_result)

        self.update_units()

    def update_units(self):
        if self.unit_type.get() == 'Длина':
            units = list(length_units.keys())
        elif self.unit_type.get() == 'Вес':
            units = list(weight_units.keys())
        else:
            units = list(time_units.keys())
        self.from_combobox.config(values=units)
        self.to_combobox.config(values=units)
        self.from_unit.set(units[0] if units else '')
        self.to_unit.set(units[1] if len(units) > 1 else (units[0] if units else ''))

    def swap_units(self):
        current_from = self.from_unit.get()
        current_to = self.to_unit.get()
        self.from_unit.set(current_to)
        self.to_unit.set(current_from)

    def convert(self):
        try:
            input_str = self.input_value.get().replace(',', '.').strip()
            if not input_str:
                self.result_value.set('Введите число')
                return
            value = float(input_str)
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            unit_type = self.unit_type.get()

            if unit_type == 'Длина':
                coeff = length_units[from_unit] / length_units[to_unit]
            elif unit_type == 'Вес':
                coeff = weight_units[from_unit] / weight_units[to_unit]
            else:
                coeff = time_units[from_unit] /time_units[to_unit]

            result = value * coeff
            self.result_value.set(f'{result:.3f}')
        except ValueError:
            self.result_value.set('Ошибка: неверный формат числа')

    def clear(self):
        self.input_value.set('')
        self.result_value.set('')

    def copy_result(self,event):
        result = self.result_value.get()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)

if __name__ == '__main__':
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
