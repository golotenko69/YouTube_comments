from aiogram import Bot, executor, Dispatcher, types
from aiogram.dispatcher import FSMContext
from parser_comments import YoutubeParser
from neiroanalyscomments import sentiment_analysis
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from analysiscomments import Analysis
from keyboard import Keyboard
from dotenv import load_dotenv
import os

load_dotenv()


bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
pars = YoutubeParser()
kb = Keyboard()

class CommentsState(StatesGroup):
    comments = State()
    sentiment = State()
    choice_comments_quantity = State()

@dp.message_handler(commands=['start'])
async def send_description(message: types.Message):
    await message.answer('Отправьте ссылку на видео YouTube\nОбязательно должно быть поле ----> "watch?v=Rh-kQese_yyQ"\nПример: https://www.youtube.com/watch?v=Rh-kQese_yyQ')
    await CommentsState.comments.set()


@dp.message_handler(lambda message: "watch?v" in message.text, state=CommentsState.comments)
async def send_analysis(message: types.Message, state: FSMContext):
    await message.answer('Собираем комментарии\nПодождите это может занять до 5 минут')

    comments = pars.get_comments(message.text)
    comments_sentiments = sentiment_analysis(comments)

    async with state.proxy() as data:
        data["comments"] = comments_sentiments

    await message.answer("Анализ завершен, что будем делать?", reply_markup=kb.keyboard_first_step())
    await CommentsState.next()


@dp.message_handler(lambda message: message.text == 'Негативные комментарии', state=CommentsState.sentiment)
async def send_negative_comments(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["sentiment"] = 'NEGATIVE'

    await message.answer("Что вывести?", reply_markup=kb.keyboard_second_step())
    await CommentsState.next()


@dp.message_handler(lambda message: message.text == 'Положительные комментарии', state=CommentsState.sentiment)
async def send_negative_comments(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["sentiment"] = 'POSITIVE'

    await message.answer("Что вывести?", reply_markup=kb.keyboard_second_step())
    await CommentsState.next()


@dp.message_handler(lambda message: message.text == 'Нейтральные комментарии', state=CommentsState.sentiment)
async def send_negative_comments(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["sentiment"] = 'NEUTRAL'

    await message.answer("Что вывести?", reply_markup=kb.keyboard_second_step())
    await CommentsState.next()


@dp.message_handler(lambda message: message.text == 'Все', state=CommentsState.sentiment)
async def send_negative_comments(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['sentiment'] = "ALL"

    await message.answer("Что вывести?", reply_markup=kb.keyboard_second_step())
    await CommentsState.next()


@dp.message_handler(lambda message: message.text == 'В начало', state=CommentsState.sentiment)
async def send_negative_comments(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Для активации введите команду /start ", reply_markup=kb.keyboard_starting())


@dp.message_handler(lambda message: message.text == 'Количество', state=CommentsState.choice_comments_quantity)
async def send_length_comments(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        comments = data['comments']
        sentiment = data['sentiment']

    analysis = Analysis(comments)
    await message.answer(analysis.send_comments_length(sentiment))


@dp.message_handler(lambda message: message.text == 'Комментарии', state=CommentsState.choice_comments_quantity)
async def send_length_comments(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        comments = data['comments']
        sentiment = data['sentiment']

    analysis = Analysis(comments)
    analysis_comments = analysis.send_comments_sentiment(sentiment)
    for i in analysis_comments:
        await message.answer(i)


@dp.message_handler(lambda message: message.text == 'Вернуться', state=CommentsState.choice_comments_quantity)
async def send_length_comments(message: types.Message, state: FSMContext):

    await message.answer('Какие комментарии отобразить?', reply_markup=kb.keyboard_first_step())
    await CommentsState.sentiment.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



