import telebot
from telebot import types
import requests
from datetime import datetime

# Ganti dengan token bot Anda dari @BotFather
BOT_TOKEN = 'GANTI_DENGAN_TOKEN_BOT_ANDA'

bot = telebot.TeleBot(BOT_TOKEN)

# Membuat keyboard menu utama (Reply Keyboard)
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🔍 Cek IP')
    btn2 = types.KeyboardButton('📡 Ping Server')
    btn3 = types.KeyboardButton('ℹ️ Info Pengguna')
    btn4 = types.KeyboardButton('🛡️ Fitur Cyber')
    return markup

# Perintah /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user.first_name
    welcome_text = (
        f"👋 Halo, {user}!\n\n"
        f"Selamat datang di *FixCyber Bot (Clone)*.\n"
        f"Bot ini menyediakan berbagai alat utilitas dan informasi cybersecurity dasar.\n\n"
        f"Gunakan tombol di bawah atau ketik /help untuk melihat daftar perintah."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

# Perintah /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "📜 *Daftar Perintah:*\n\n"
        "/start - Memulai bot\n"
        "/help - Menampilkan menu bantuan ini\n"
        "/cekip - Mengecek informasi IP publik Anda\n"
        "/ping - Mengecek latency/respon bot\n"
        "/info - Menampilkan informasi akun Telegram Anda\n\n"
        "💡 *Tips:* Anda juga bisa menggunakan tombol menu yang tersedia di keyboard."
    )
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# Fitur: Cek IP Publik
@bot.message_handler(commands=['cekip'])
def check_ip(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        # Mengambil IP publik
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        ip = ip_data['ip']
        
        # Mengambil informasi geolokasi IP (menggunakan API publik gratis)
        geo_response = requests.get(f'http://ip-api.com/json/{ip}')
        geo_data = geo_response.json()
        
        if geo_data['status'] == 'success':
            result = (
                f"🌐 *Informasi IP Anda:*\n\n"
                f"🔹 IP: `{ip}`\n"
                f"🔹 Negara: {geo_data['country']}\n"
                f"🔹 Kota: {geo_data['city']}\n"
                f"🔹 ISP: {geo_data['isp']}\n"
                f"🔹 Zona Waktu: {geo_data['timezone']}"
            )
        else:
            result = f"🔹 IP Publik Anda: `{ip}`\n_(Detail lokasi tidak tersedia)_"
            
        bot.send_message(message.chat.id, result, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Terjadi kesalahan saat mengambil data IP: {str(e)}")

# Fitur: Ping Bot
@bot.message_handler(commands=['ping'])
def ping_bot(message):
    start_time = datetime.now()
    msg = bot.send_message(message.chat.id, "📡 Menguji koneksi...")
    end_time = datetime.now()
    latency = (end_time - start_time).microseconds // 1000
    bot.edit_message_text(
        chat_id=message.chat.id, 
        message_id=msg.message_id, 
        text=f"📡 *Pong!*\nLatensi: `{latency}` ms", 
        parse_mode='Markdown'
    )

# Fitur: Info Pengguna
@bot.message_handler(commands=['info'])
def user_info(message):
    user = message.from_user
    info_text = (
        f"ℹ️ *Informasi Pengguna:*\n\n"
        f"👤 Nama: {user.first_name} {user.last_name or ''}\n"
        f"🆔 ID Pengguna: `{user.id}`\n"
        f"👤 Username: @{user.username or 'Tidak ada'}\n"
        f"💬 Tipe Chat: {message.chat.type}"
    )
    bot.send_message(message.chat.id, info_text, parse_mode='Markdown')

# Handler untuk tombol keyboard (agar sesuai dengan fungsi perintah)
@bot.message_handler(func=lambda message: message.text == '🔍 Cek IP')
def handle_cekip_btn(message):
    check_ip(message)

@bot.message_handler(func=lambda message: message.text == '📡 Ping Server')
def handle_ping_btn(message):
    ping_bot(message)

@bot.message_handler(func=lambda message: message.text == 'ℹ️ Info Pengguna')
def handle_info_btn(message):
    user_info(message)

@bot.message_handler(func=lambda message: message.text == '🛡️ Fitur Cyber')
def handle_cyber_btn(message):
    bot.send_message(
        message.chat.id, 
        "🛡️ *Fitur Cyber Lanjutan*\n\n"
        "Fitur ini masih dalam pengembangan. Contoh fitur yang bisa ditambahkan:\n"
        "- Port Scanner\n"
        "- DNS Lookup / Whois Domain\n"
        "- Pengecekan Kebocoran Data (Breach Check)\n\n"
        "Hubungi admin untuk permintaan fitur khusus.", 
        parse_mode='Markdown'
    )

# Handler default untuk pesan yang tidak dikenali
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(
        message.chat.id, 
        "⚠️ Perintah tidak dikenali. Silakan gunakan /help untuk melihat daftar perintah yang tersedia.", 
        reply_markup=get_main_keyboard()
    )

if __name__ == '__main__':
    print("🤖 Bot sedang berjalan... Tekan Ctrl+C untuk berhenti.")
    # Menggunakan polling (cocok untuk pengembangan). 
    # Untuk produksi skala besar, disarankan menggunakan Webhook.
    bot.polling(none_stop=True)
