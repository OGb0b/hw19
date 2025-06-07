from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить заметку', callback_data='add')],
    [InlineKeyboardButton(text='Просмотреть все заметки', callback_data='show')],
    [InlineKeyboardButton(text='Удалить заметку', callback_data='delete')],
    [InlineKeyboardButton(text='Поддержать автора', callback_data='donate')]
])
donate_keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='100', callback_data='buy_100')],
    [InlineKeyboardButton(text='200', callback_data='buy_200')],
    [InlineKeyboardButton(text='300', callback_data='buy_300')]
])
