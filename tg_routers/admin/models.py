from aiogram.fsm.state import StatesGroup, State

editor_data = {}
editor_answers_data = {}
class editStates(StatesGroup):
    edit = State()
    edit_answer = State()