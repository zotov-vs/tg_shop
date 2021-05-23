from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")


DB_CONNECTION_STRING = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# https://qiwi.com/api
# https://qiwi.com/p2p-admin/transfers/api
QIWI_TOKEN = env.str("QIWI_TOKEN")
QIWI_WALLET= env.str("QIWI_WALLET")
QIWI_PUBLIC_KEY = env.str("QIWI_PUBLIC_KEY")
QIWI_SECRET_KEY = env.str("QIWI_SECRET_KEY")
