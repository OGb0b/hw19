from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from hw19.keyboard.inline_kb import start_keyboard_inline, donate_keyboard_inline
from hw19.states.state_bot import NoteStates
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from hw19.data.connection import add_user, add_note, show_user_notes, show_notes_to_delete, delete_note
from aiogram import types
from aiogram.types import PreCheckoutQuery
from aiogram.filters import Command
from hw19.config import  PROVIDER_TOKEN
router = Router()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    if not add_user(message.from_user.id, message.from_user.username):
        await message.answer("Ошибка при добавлении пользователя, попробуйте запустить бота позднее.")
        return
    await message.answer(
        "Выберите действие:",
         reply_markup=start_keyboard_inline)
    await state.set_state(NoteStates.Start)


@router.callback_query(F.data == 'add', NoteStates.Start)
async def add_note_start(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.answer("Введите текст заметки:")
    await state.set_state(NoteStates.AddNote)

@router.message(NoteStates.AddNote)
async def save_note(message: Message, state: FSMContext):
    user_id = message.from_user.id
    note_text = message.text
    if not add_note(note_text, user_id):
        await message.answer("Ошибка при сохранении заметки.")
        await state.set_state(NoteStates.Start)
        await message.answer("Выберите действие:", reply_markup=start_keyboard_inline)
        return
    await message.answer(f"Заметка сохранена:\n\n{note_text}")
    await state.set_state(NoteStates.Start)
    await message.answer("Выберите действие:", reply_markup=start_keyboard_inline)


@router.callback_query(F.data == 'show', NoteStates.Start)
async def show_notes(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user_id = cb.from_user.id
    notes = show_user_notes(user_id)
    await cb.message.answer(notes)
    await cb.message.answer("Выберите действие:", reply_markup=start_keyboard_inline)


@router.callback_query(F.data == 'delete', NoteStates.Start)
async def select_notes_to_delete(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user_id = cb.from_user.id
    notes = show_notes_to_delete(user_id)
    if isinstance(notes, str):
        await cb.message.answer(notes)
        return
    if not notes:
        await cb.message.answer("📭 У вас пока нет заметок.")
        return
    buttons = []
    for note in notes:
        note_id = note[0]
        note_text = note[1]
        words = note_text.split()
        preview = ' '.join(words[:3]) + ("..." if len(words) > 3 else "")
        buttons.append(
            InlineKeyboardButton(
                text=preview,
                callback_data=str(note_id)
            )
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])
    await state.set_state(NoteStates.DeleteNote)
    await cb.message.answer(
        "Выберите заметку для удаления:",
        reply_markup=keyboard
    )


@router.callback_query(NoteStates.DeleteNote)
async def confirm_note_deletion(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user_id = cb.from_user.id
    note_id = int(cb.data)
    result = delete_note(note_id, user_id)
    if result is True:
        await cb.message.answer("🗑 Заметка успешно удалена")
    else:
        await cb.message.answer(f"⚠ {result}")
    await state.set_state(NoteStates.Start)
    await cb.message.answer(
        "Выберите действие:",
        reply_markup=start_keyboard_inline
    )

@router.callback_query(F.data == 'donate', NoteStates.Start)
async def donate_handler(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.answer(
        "Выберите размер доната:",
        reply_markup=donate_keyboard_inline
    )

@router.callback_query(F.data.startswith('buy_'), NoteStates.Start)
async def process_donate(cb: CallbackQuery, state: FSMContext):
    """Обработка нажатия на кнопку покупки"""
    amount = int(cb.data.split('_')[1])

    await cb.bot.send_invoice(
        chat_id=cb.message.chat.id,
        title=f"Донат {amount} ₽",
        description="Поддержка разработчика бота",
        payload=f"donate_{amount}",
        provider_token=PROVIDER_TOKEN,  # Из config.py
        currency="RUB",
        prices=[{"label": "Донат", "amount": amount * 100 }],
        start_parameter="donate"
    )
    await cb.answer()

@router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """Подтверждение запроса на оплату"""
    await pre_checkout_query.answer(ok=True)


@router.message(lambda message: message.successful_payment)
async def successful_payment(message: types.Message):
    """Обработка успешной оплаты"""
    await message.answer(
        f"Оплата прошла успешно! Спасибо за покупку")


