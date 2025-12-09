# handlers/start.py
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from db import get_rules
try:
    # якщо вже маєш готову клаву з телефоном — юзаємо її
    from keyboards.phone import phone_kb
except Exception:
    # fallback: проста клава запиту номера
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    phone_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поділитися номером ☎️", request_contact=True)]],
        resize_keyboard=True,
    )

router = Router()

WELCOME = (
    "🎉 Вітаємо в розіграші від <b>Soska Bar</b>!\n\n"
    "Щоб взяти участь:\n"
    "1️⃣ Купи будь-який товар у нашому магазині\n"
    "2️⃣ Збережи чек\n"
    "3️⃣ Відправ фото чека сюди 📸\n\n"
    "Далі бот попросить твоє ім’я та номер телефону 💜"
)

def _rules_block() -> str:
    rules = get_rules()
    if not rules:
        return "ℹ️ Правила ще не встановлені адміністратором."
    # компактне оформлення правил з бази
    return f"📋 <b>Актуальні правила:</b>\n{rules}"

@router.message(CommandStart())
async def start_cmd(m: Message):
    # 1) Вітання
    await m.answer(WELCOME)

    # 2) Правила з БД
    await m.answer(_rules_block())

    # 3) Заклик почати (попросимо одразу номер, якщо треба)
    await m.answer("Коли будеш готовий — кидай фото чека або поділись номером 👇", reply_markup=phone_kb)

# опціонально: коротка команда для швидкого перегляду правил
@router.message(Command("rules"))
@router.message(Command("get_rules"))
async def show_rules_cmd(m: Message):
    await m.answer(_rules_block())
