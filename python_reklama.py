import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher(storage=MemoryStorage())

class CarForm(StatesGroup):
    model = State()
    position = State()
    kraska = State()
    color = State()
    year = State()
    probeg = State()
    fuel = State()
    price = State()
    phone = State()
    location = State()
    images = State()

def get_confirm_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="confirm_no"),
        ]
    ])

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Assalomu alaykum! Mashina e'loni berish uchun /elon buyrug'ini yozing.")

@dp.message(Command("elon"))
async def elon_cmd(message: Message, state: FSMContext):
    await state.set_state(CarForm.model)
    await message.answer("🚗 Mashina modelini kiriting (masalan: Spark):")

@dp.message(CarForm.model)
async def process_model(message: Message, state: FSMContext):
    text = message.text.strip()
    if len(text) < 2 or len(text) > 30:
        await message.answer("❌ Model nomi 2 dan 30 tagacha belgidan iborat bo‘lishi kerak.")
        return
    await state.update_data(model=text)
    await state.set_state(CarForm.position)
    await message.answer("🔢 Pozitsiyasi (1–10 oralig‘ida):")

@dp.message(CarForm.position)
async def process_position(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Pozitsiya faqat raqam bo‘lishi kerak.")
        return
    pos = int(message.text)
    if pos < 1 or pos > 10:
        await message.answer("❌ Pozitsiya 1 dan 10 gacha bo‘lishi kerak.")
        return
    await state.update_data(position=str(pos))
    await state.set_state(CarForm.kraska)
    await message.answer("🚰 Kraska holati (masalan: 3-4 detalda):")

@dp.message(CarForm.kraska)
async def process_kraska(message: Message, state: FSMContext):
    await state.update_data(kraska=message.text.strip())
    await state.set_state(CarForm.color)
    await message.answer("🎨 Rangi:")

@dp.message(CarForm.color)
async def process_color(message: Message, state: FSMContext):
    await state.update_data(color=message.text.strip())
    await state.set_state(CarForm.year)
    await message.answer("📆 Yili (1990–2025):")

@dp.message(CarForm.year)
async def process_year(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Yil faqat raqam bo‘lishi kerak.")
        return
    year = int(message.text)
    if year < 1990 or year > 2025:
        await message.answer("❌ Yil 1990 va 2025 oralig‘ida bo‘lishi kerak.")
        return
    await state.update_data(year=str(year))
    await state.set_state(CarForm.probeg)
    await message.answer("📊 Probeg (0–1,000,000):")

@dp.message(CarForm.probeg)
async def process_probeg(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Probeg faqat raqam bo‘lishi kerak.")
        return
    probeg = int(message.text)
    if probeg < 0 or probeg > 1_000_000:
        await message.answer("❌ Probeg 0 dan 1,000,000 gacha bo‘lishi kerak.")
        return
    await state.update_data(probeg=str(probeg))
    await state.set_state(CarForm.fuel)
    await message.answer("⛽ Yonilg‘i turi (masalan: Benzin gaz):")

@dp.message(CarForm.fuel)
async def process_fuel(message: Message, state: FSMContext):
    await state.update_data(fuel=message.text.strip())
    await state.set_state(CarForm.price)
    await message.answer("💵 Narxi (100–50,000 $):")

@dp.message(CarForm.price)
async def process_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Narx faqat raqam bo‘lishi kerak.")
        return
    price = int(message.text)
    if price < 100 or price > 50000:
        await message.answer("❌ Narx 100 dan 50,000 gacha bo‘lishi kerak.")
        return
    await state.update_data(price=str(price))
    await state.set_state(CarForm.phone)
    await message.answer("📞 Telefon raqamni kiriting (+998 bilan):")

@dp.message(CarForm.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.replace(" ", "")
    if not phone.startswith("+998") or not phone[1:].isdigit() or len(phone) != 13:
        await message.answer("❌ Raqam noto‘g‘ri. Iltimos, +998 bilan boshlanuvchi to‘g‘ri raqam kiriting.")
        return
    await state.update_data(phone=phone)
    await state.set_state(CarForm.location)
    await message.answer("📍 Manzilingiz (masalan: Toshkent):")

@dp.message(CarForm.location)
async def process_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text, images=[])
    await state.set_state(CarForm.images)
    await message.answer("🖼 Endi 1 tadan 5 tagacha rasm yuboring. Tugatganingizda '✅ Tugatdim' tugmasini bosing.")

@dp.message(CarForm.images)
async def process_images(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("❗️ Iltimos, faqat rasm yuboring.")
        return

    data = await state.get_data()
    images = data.get("images", [])

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tugatdim", callback_data="done_images")]
    ])

    if len(images) >= 5:
        await message.answer(
            "❌ Siz maksimal 5 ta rasm yuborishingiz mumkin.",
            reply_markup=keyboard
        )
        return

    images.append(message.photo[-1].file_id)
    await state.update_data(images=images)

    await message.answer(
        f"✅ {len(images)} ta rasm qabul qilindi. Yana yuborishingiz mumkin yoki 'Tugatdim' tugmasini bosing.",
        reply_markup=keyboard
    )


@dp.callback_query(F.data == "done_images")
async def confirm_preview(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    images = data.get("images", [])

    if not images:
        await callback.answer("❗️ Hech qanday rasm topilmadi.")
        return

    summary = (
        f"📢 *Yangi mashina e'loni:*\n\n"
        f"🚘 *Moshina modeli:* #{data['model']}\n"
        f"🔢 *Pozitsiya:* {data['position']}\n"
        f"🚰 *Kraska:* {data['kraska']}\n"
        f"🎨 *Rangi:* {data['color']}\n"
        f"📆 *Yili:* {data['year']}\n"
        f"📊 *Probeg:* {data['probeg']} km\n"
        f"⛽ *Yonilg‘i:* {data['fuel']}\n"
        f"💵 *Narxi:* {data['price']}$\n"
        f"📞 *Tel:* {data['phone']}\n"
    )

    media = [
        InputMediaPhoto(media=img, caption=summary if i == 0 else "")
        for i, img in enumerate(images)
    ]
    await bot.send_media_group(chat_id=callback.message.chat.id, media=media)

    await bot.send_message(
        callback.message.chat.id,
        "📋 Yuqoridagi e'lon ma'lumotlari to‘g‘rimi?",
        reply_markup=get_confirm_keyboard()
    )
    await callback.message.delete()

@dp.callback_query(F.data.in_(["confirm_yes", "confirm_no"]))
async def process_confirmation(callback: CallbackQuery, state: FSMContext):
    if callback.data == "confirm_yes":
        data = await state.get_data()

        summary = (
            f"📢 *Yangi mashina e'loni:*\n\n"
            f"🚘 *Moshina modeli:* #{data['model']}\n"
            f"🔢 *Pozitsiya:* {data['position']}\n"
            f"🚰 *Kraska:* {data['kraska']}\n"
            f"🎨 *Rangi:* {data['color']}\n"
            f"📆 *Yili:* {data['year']}\n"
            f"📊 *Probeg:* {data['probeg']} km\n"
            f"⛽ *Yonilg‘i:* {data['fuel']}\n"
            f"💵 *Narxi:* {data['price']}$\n"
            f"📞 *Tel:* {data['phone']}\n"
            f"📍 *Manzil:* {data['location']}\n"
        )

        media = [
            InputMediaPhoto(media=img, caption=summary if i == 0 else "")
            for i, img in enumerate(data['images'])
        ]
        await bot.send_media_group(chat_id=ADMIN_ID, media=media)

        user_info = f"👤 *Foydalanuvchi:* @{callback.from_user.username or 'Noma’lum'} ({callback.from_user.id})"
        await bot.send_message(chat_id=ADMIN_ID, text=user_info)

        await callback.message.edit_reply_markup()
        await callback.message.answer("✅ E'loningiz adminga yuborildi!")
    else:
        await callback.message.edit_reply_markup()
        await callback.message.answer("❌ E'lon bekor qilindi. Qaytadan /elon buyrug'ini yozing.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
