import re

from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class Questions:
    name = ""
    text = ""
    pattern = ""
    message_type = None

    def __init__(self, name="_", text="", question="", pattern="", answer_type=types.Message, case=None):
        self.name = name
        self.text = text
        self.question = question
        self.pattern = pattern
        self.answer_type = answer_type
        self.case = case

    def check(self, text):
        text = re.sub("\s", " ", text)
        if self.case == "lower":
            text.lower()
        elif self.case == "upper":
            text.upper()
        elif self.case == "title":
            text.title()

        return re.match(self.pattern, text)


class Form1(StatesGroup):
    fio = State()
    number = State()

    data = {
        1: Questions(text="Данные абонента для подключения тарифа\n", answer_type=None),
        "Form1:fio": Questions(text="ФИО абонента: ", question="Введите ФИО абонента:"
                               , pattern="([а-яА-Я-]+)(\s+([а-яА-Я-]+)){1,3}"),
        "Form1:number": Questions(text="Номер телефона: ", question="Введите номер телефона абонента:"
                                  , pattern="(\+7|8)[0-9]{10}"),
    }

    async def get_text(state: FSMContext, error_text=None):
        res: str = ""
        data = await state.get_data()
        current_state = await state.get_state()
        current_question = Form1.data.__getitem__(current_state)

        for key in Form1.data.keys():
            question = Form1.data.__getitem__(key)
            if question.answer_type is None:
                res += question.text + "\n"
            else:
                answer = data.get(key)
                if answer is not None:
                    res += "✅ " + "<code>" + question.text + "</code>" + f"{answer or ''}" + "\n"
                else:
                    if error_text is not None and current_state == key:
                        res += "❌ " + "<code>" + question.text + "</code>" + f"{error_text or '-'}" + "\n"
                    else:
                        res += "✔️ " + "<code>" + question.text + "</code>" + f"{answer or '-'}" + "\n"

        if current_question is not None:
            res += "\n" + current_question.question + "\n"
            answer = data.get(current_state)
            if answer is not None:
                res += "Текущее значение: " + f"<b>{answer}</b>" + "\n"

        return res


class Form(StatesGroup):
    name = State()
    email = State()
    phone = State()
