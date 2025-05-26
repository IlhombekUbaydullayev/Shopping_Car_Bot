import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import BotCommand
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

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


def get_model_keyboard():
    buttons = [
    [InlineKeyboardButton(text="Spark", callback_data="model_Spark"),
     InlineKeyboardButton(text="Cobalt", callback_data="model_Cobalt")],
    [InlineKeyboardButton(text="Gentra", callback_data="model_Gentra"),
     InlineKeyboardButton(text="Malibu 1", callback_data="model_Malibu1")],
    [InlineKeyboardButton(text="Malibu 2", callback_data="model_Malibu2"),
     InlineKeyboardButton(text="Kia", callback_data="model_Kia")],
    [InlineKeyboardButton(text="Monza", callback_data="model_Monza"),
     InlineKeyboardButton(text="Nexia 3", callback_data="model_Nexia3")],
    [InlineKeyboardButton(text="Nexia 2", callback_data="model_Nexia2"),
     InlineKeyboardButton(text="Nexia 3", callback_data="model_Nexia3")],
    [InlineKeyboardButton(text="Damas", callback_data="model_Damas"),
     InlineKeyboardButton(text="Labo", callback_data="model_Labo")],
    [InlineKeyboardButton(text="Tracker", callback_data="model_Tracker"),
     InlineKeyboardButton(text="Equinox", callback_data="model_Equinox")],
    [InlineKeyboardButton(text="Onix", callback_data="model_Onix"),
     InlineKeyboardButton(text="Traverse", callback_data="model_Traverse")],
    [InlineKeyboardButton(text="Tahoe", callback_data="model_Tahoe"),
     InlineKeyboardButton(text="Trailblazer", callback_data="model_Trailblazer")],
    [InlineKeyboardButton(text="Captiva", callback_data="model_Captiva"),
     InlineKeyboardButton(text="Orlando", callback_data="model_Orlando")],
    [InlineKeyboardButton(text="Matiz", callback_data="model_Matiz"),
     InlineKeyboardButton(text="Epica", callback_data="model_Epica")],
    [InlineKeyboardButton(text="Rezzo", callback_data="model_Rezzo"),
     InlineKeyboardButton(text="Lacetti", callback_data="model_Lacetti"),],
     [InlineKeyboardButton(text="Tiggo 2", callback_data="model_Tiggo2"),
     InlineKeyboardButton(text="Tiggo 4", callback_data="model_Tiggo4")],
    [InlineKeyboardButton(text="Tiggo 5", callback_data="model_Tiggo5"),
     InlineKeyboardButton(text="Tiggo 7", callback_data="model_Tiggo7")],
    [InlineKeyboardButton(text="Tiggo 8", callback_data="model_Tiggo8"),
     InlineKeyboardButton(text="Arrizo 5", callback_data="model_Arrizo5")],
    [InlineKeyboardButton(text="Arrizo 6", callback_data="model_Arrizo6"),
     InlineKeyboardButton(text="Arrizo 8", callback_data="model_Arrizo8")],
    [InlineKeyboardButton(text="QQ", callback_data="model_QQ"),
     InlineKeyboardButton(text="Bonus", callback_data="model_Bonus")],
    [InlineKeyboardButton(text="Very", callback_data="model_Very"),
     InlineKeyboardButton(text="E5", callback_data="model_E5")],
]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_position_keyboard():
    buttons = []
    for i in range(1, 11, 2):  # Har qatorga 2 tadan tugma
        row = [
            InlineKeyboardButton(text=str(i), callback_data=f"position_{i}"),
            InlineKeyboardButton(text=str(i+1), callback_data=f"position_{i+1}")
        ]
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_confirm_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="confirm_no"),
        ]
    ])

def get_location_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Toshkent", callback_data="loc_Toshkent"),
     InlineKeyboardButton(text="Andijon", callback_data="loc_Andijon")],
    [InlineKeyboardButton(text="Farg'ona", callback_data="loc_Fargona"),
     InlineKeyboardButton(text="Namangan", callback_data="loc_Namangan")],
    [InlineKeyboardButton(text="Samarqand", callback_data="loc_Samarqand"),
     InlineKeyboardButton(text="Buxoro", callback_data="loc_Buxoro")],
    [InlineKeyboardButton(text="Qarshi", callback_data="loc_Qarshi"),
     InlineKeyboardButton(text="Nukus", callback_data="loc_Nukus")],
    [InlineKeyboardButton(text="Jizzax", callback_data="loc_Jizzax"),
     InlineKeyboardButton(text="Xorazm", callback_data="loc_Xorazm")],
])

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Assalomu alaykum! Mashina e'loni berish uchun /elon yozig'ini bosing.\n\n Mashina elon yaratish : 📩 /elon 📩")

@dp.message(Command("elon"))
async def elon_cmd(message: Message, state: FSMContext):
    await state.set_state(CarForm.model)
    await message.answer("🚗 Mashina modelini tanlang:", reply_markup=get_model_keyboard())

@dp.message(CarForm.model)
async def process_model(message: Message, state: FSMContext):
    text = message.text.strip()
    await message.answer("🚗 Mashina modelini tugmada tanlang\n\ntugmalarda mashina modeli bo'lmasa adminga murojat qiling\n\n💁 @ilhombek1997",reply_markup=get_model_keyboard())

@dp.message(CarForm.position)
async def process_position(message: Message, state: FSMContext):
    await message.answer("🔢 Pozitsiyasi ni tanlang:",reply_markup=get_position_keyboard())

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
    
    probeg = message.text
    if len(probeg) > 20:
        await message.answer("❌ Probeg 0 dan 1 000 000 gacha bo‘lishi kerak.")
        return
    await state.update_data(probeg=str(probeg))
    await state.set_state(CarForm.fuel)
    await message.answer("⛽ Yonilg‘i turi (masalan: Benzin gaz):")

@dp.message(CarForm.fuel)
async def process_fuel(message: Message, state: FSMContext):
    await state.update_data(fuel=message.text.strip())
    await state.set_state(CarForm.price)
    await message.answer("💵 Narxi (100–1 000 000 $):")

@dp.message(CarForm.price)
async def process_price(message: Message, state: FSMContext):
    price = message.text
    if len(price) > 9:
        await message.answer("❌ Narx 100$ dan 1 000 000$ gacha bo‘lishi kerak.")
        return
    await state.update_data(price=str(price))
    await state.set_state(CarForm.phone)
    await message.answer("📞 Telefon raqamni kiriting : \n\n Misollar:\n👉 99 555-55-55\n994444444\n94 6222222 ")

@dp.message(CarForm.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = ''.join(ch for ch in message.text if ch.isdigit())
    if len(phone) != 9:
        await message.answer("❌ Raqam noto‘g‘ri.\n\nMisollar:\n99 555-55-55\n994444444\n94 6222222")
        return
    await state.update_data(phone=phone)
    await state.set_state(CarForm.location)
    await message.answer("📍 Manzilingiz:",reply_markup=get_location_keyboard())

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


@dp.callback_query(F.data.startswith("model_"))
async def select_model(callback: CallbackQuery, state: FSMContext):
    model_name = callback.data.replace("model_", "")
    await state.update_data(model=model_name)
    await callback.message.edit_text(f"🚗 Model tanlandi: {model_name}")
    await state.set_state(CarForm.position)
    await callback.message.answer("🔢 Pozitsiyasi ni tanlang:",reply_markup=get_position_keyboard())

@dp.callback_query(F.data.startswith("position_"))
async def process_position_callback(callback: CallbackQuery, state: FSMContext):
    pos = callback.data.split("_")[1]
    await state.update_data(position=pos)
    await state.set_state(CarForm.kraska)
    await callback.message.edit_text("🚰 Kraska holatini yozing\n\n masalan: Kraskasi toza\n1,2 joyida bor")
    await callback.answer()

@dp.callback_query(F.data.startswith("loc_"))
async def process_location_callback(callback: CallbackQuery, state: FSMContext):
    city = callback.data.split("_")[1]
    await state.update_data(location=city)
    await callback.message.answer(f"📍 Manzil tanlandi: {city}")
    await state.set_state(CarForm.images)
    await callback.message.delete()
    await callback.message.answer("🖼 Endi 1 tadan 5 tagacha rasm yuboring. Tugatganingizda '✅ Tugatdim' tugmasini bosing.")


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
        f"📊 *Probeg:* {data['probeg']}\n"
        f"⛽ *Yonilg‘i:* {data['fuel']}\n"
        f"💵 *Narxi:* {data['price']}\n"
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
    # Foydalanuvchiga javobni zudlik bilan qaytaring
    await callback.answer()

    # Ma'lumotni olish va keyin darhol state ni tozalash
    data = await state.get_data()
    await state.clear()

    # Tugmalarni olib tashlash (xatolik ehtimoliga qarshi)
    try:
        await callback.message.edit_reply_markup()
    except Exception as e:
        logging.warning(f"❗️ Tugmalarni o‘chirishda xatolik: {e}")

    if callback.data == "confirm_yes":
        summary = (
            f"📢 *Yangi mashina e'loni:*\n\n"
            f"🚘 *Moshina modeli:* #{data['model']}\n"
            f"🔢 *Pozitsiya:* {data['position']}\n"
            f"🚰 *Kraska:* {data['kraska']}\n"
            f"🎨 *Rangi:* {data['color']}\n"
            f"📆 *Yili:* {data['year']}\n"
            f"📊 *Probeg:* {data['probeg']}\n"
            f"⛽ *Yonilg‘i:* {data['fuel']}\n"
            f"💵 *Narxi:* {data['price']}\n"
            f"📞 *Tel:* +998{data['phone']}\n"
            f"📍 *Manzil:* {data['location']}\n"
        )

        media = [
            InputMediaPhoto(media=img, caption=summary if i == 0 else "")
            for i, img in enumerate(data['images'])
        ]

        try:
            await bot.send_media_group(chat_id=ADMIN_ID, media=media)
        except Exception as e:
            logging.error(f"❌ Media yuborishda xatolik: {e}")
            await callback.message.answer("❌ E'lonni yuborishda xatolik yuz berdi. Keyinroq qayta urinib ko'ring.")
            return

        user_info = f"👤 *Foydalanuvchi:* @{callback.from_user.username or 'Nomalum'} ({callback.from_user.id})"
        await bot.send_message(chat_id=ADMIN_ID, text=user_info)

        await callback.message.answer("✅ E'loningiz adminga yuborildi!")

    else:
        await callback.message.answer("❌ E'lon bekor qilindi. Qaytadan /elon buyrug'ini yozing.")


from aiogram.types import BotCommand

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni boshlash"),
        BotCommand(command="elon", description="Mashina e'lonini joylash"),
    ]
    await bot.set_my_commands(commands)


async def main():
    await set_bot_commands(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
