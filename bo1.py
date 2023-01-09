from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from city import *
from metro import *
from restaurants import *
from random import randint
import os
from typing import Dict

# grafs
print(1)
street_graph: OsmnxGraph = load_osmnx_graph("barcelona.grf")
print(2)
metro_graph: MetroGraph = get_metro_graph()
print(3)
city_graph: CityGraph = build_city_graph(street_graph, metro_graph)


# restaurants
print(4)
list_restaurants: Restaurants = read_restaurants()

# bromes
print(5)
jokes = pandas.read_csv("reddit-cleanjokes.csv", usecols=["ID", "Joke"], dtype={"ID": int, "Joke": str})

# diccionaris
help_dic: Dict[str, str] = {
    "start": "Inicia la conversa amb mi.",
    "help": """Ofereix ajuda sobre les comandes disponibles. Si necessites
    informació addicional d'alguna d'aquestes comandes pots fer-ho fent
    help <comanda>. Per exemple, /help help o /help info.""",
    "author": "Mostra el nom de les autores del projecte.",
    "find": """Cerca quins restaurants satisfan la cerca realitzada i
    n'escriu una llista numerada de 12 elements com a molt. També ofereix
    la possibilitat d'expandir fins a 6 possibilitats de més. Quan s'ha
    realitzat una demanda, es pot requerir més informació sobre un
    restaurant concret utilitzant la comanda info (veure /help info).
    Exemples de cerca: /find pizza, /find pasta sants.""",
    "info": """Mostra la informació sobre el restaurant especificat pel seu
    número (triat de la darrera llista numerada obtinguda amb /find). Exemple /info 4.""",
    "guide": """Mostra un mapa amb el camí més curt per anar del punt actual on et
    trobes al restaurant especificat pel seu número (triat de la darrera llista
    numerada obtinguda amb /find) conjuntament amb una breu descripció del trajecte.
    Exemple: /guide 4. Agafa la targeta de metro i a degustar!"""
}

emojis_dic: Dict[str, str] = {
    'Restaurants': "🍽️",
    'Tablaos flamencs': "💃",
    'Cocteleries': "🍸",
    'Xampanyeries': "🍾",
    'Bars i pubs musicals': "🍺",
    'Discoteques': "🌐",
    'Karaokes': "🎤",
    'Teatres': "🎭"
}

##############################
#   Funcions implementades   #
##############################


def _write_info_of_restaurant(r: Restaurant) -> str:

    """Retorna la informació del restaurant demanat per la comanda info."""

    name: str = "Nom del restaurant: " + r.name + "\n"
    category: str = "Categoria: " + r.category + " " + emojis_dic[r.category] + "\n"
    district: str = "Districte: " + r.address.district + "\n"
    neighbourhood: str = "Barri: " + r.address.neighbourhood + "\n"
    address: str = "Adreça: Carrer " + r.address.address_name + " número " + r.address.address_num + "\n"
    return name + category + district + neighbourhood + address


def _where(update, context) -> None:

    """Guarda la ubicació de l'ususari quan aquest li passa."""

    lat: float = update.effective_message.location.latitude
    lon: float = update.effective_message.location.longitude
    context.user_data["location"] = Coord(lon, lat)


def _handler_more(update, context) -> None:

    """S'encarrega de gestionar el cas en què es clica el botó
    de Veure més opcions."""

    if not context.user_data["more"][0]:
        context.user_data["more"][0] = True
        context.bot.send_message(chat_id=update.effective_chat.id, text=context.user_data["more"][1])


def _text_rest(begin: int, end: int, possibilities: List[Restaurant]) -> str:

    """Retorna un text amb els restaurants requerits per l'entrada de la llista de possibilities."""

    text: str = ""
    for i in range(begin, end):
        text += str(i + 1) + " " + emojis_dic[possibilities[i].category] + " - " + possibilities[i].name + '\n'
    return text


def _max_possibilities(context) -> int:

    """Retorna el número fins el qual es pot obtenir informació o guia."""

    possibilities: Restaurants = context.user_data['found']
    return min(12 + (context.user_data["more"][0])*min(6, len(possibilities) - 12), len(possibilities))


def _path(context, entry) -> Path:

    """Retorna el camí més curt des de la ubicació de l'usuari fins al restaurant demanat."""

    possibilities = context.user_data['found']
    coordinate_restaurant: Coord = possibilities[entry - 1].position
    current_location: Coord = context.user_data["location"]
    return find_path(street_graph, city_graph, current_location, coordinate_restaurant)

########################
#   Comandes del xat   #
########################


def start(update, context):

    """Funció que saluda i que s'executa quan el bot reb el missatge /start."""

    text = """Hola! Benvingut/da a Fast and Furious.
    Se t'ha cremat la paella 🥘 i no saps on menjar avui? Aquest bot
    t'ajudarà a trobar el lloc ideal i com arribar-hi.
    Per funcionar correctament m'hauràs de compartir la teva ubicació. 📍
    No pateixis, no penso vendre les teves dades ;). \n
    Per veure totes les comandes que tinc pots fer servir la comanda /help."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    username = update.effective_chat.username
    fullname = update.effective_chat.first_name + ' ' + update.effective_chat.last_name


def help(update, context):

    """Ofereix ajuda a l'usuari i especificacions de les diferents accions
    que pot realitzar el bot."""

    if len(context.args) == 0:
        # cas en què es demana la comanda /help simple
        context.bot.send_message(chat_id=update.effective_chat.id, text=
        """Hola, soc Fast & Furious (Ràpida i Furiosa) i soc aquí per ajudar!
        Aquest bot implementa les següents comandes:
                1. /start - inici
                2. /find - búsqueda restaurants
                3. /info - informació restaurants
                4. /guide - guiar a restaurant
                5. /help - ajuda
                6. /author - autores del projecte
        Si necessites informació addicional d'alguna d'aquestes comandes
        pots fer-ho fent /help <comanda>. Exemple: /help info
        Molta sort recorrent-me. 🚇
        """)

    elif context.args[0] in help_dic:
        # cas en què es demana /help <comanda> per una comanda vàlida
        context.bot.send_message(chat_id=update.effective_chat.id, text=help_dic[context.args[0]])
    else:
        # cas en què es demana /help <comanda> per una comanda no vàlida
        error = "No reconec aquesta comanda."
        context.bot.send_message(chat_id=update.effective_chat.id, text=error)


def author(update, context):

    """Escriu pel xat el nom de les autores del projecte."""

    text = "Hola! Aquest bot l'han creat Sílvia Fàbregas i Laura Solà."
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def find(update, context):

    """Cerca quins restaurants satisfan la cerca realitzada i n'escriu
    una llista numerada de 12 elements com a molt. També ofereix la
    possibilitat d'expandir fins a 6 possibilitats de més. ."""

    if len(context.args) > 0:
        # actualitzem i guardem les possibilitats associades a
        # l'últim found realitzat.
        queries: List[str] = [entry for entry in context.args]
        possibilities: Restaurants = find_restaurants(queries, list_restaurants)
        context.user_data['found'] = possibilities

        num_outputs: int = min(len(possibilities), 12)
        if num_outputs == 0:
            error = "Oh no... 😢 No s'ha trobat cap restaurant amb aquesta entrada... Prova-ho amb una altra... 😊"
            context.bot.send_message(chat_id=update.effective_chat.id, text=error)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=_text_rest(0, num_outputs, possibilities))

            # encara no s'ha clicat al botó de more
            context.user_data["more"] = [False, ""]
            if len(possibilities) > 12:
                # guardar el text de les opcions de més (màx 6)
                more: str = _text_rest(12, 12 + min(len(possibilities)-12, 6), possibilities)
                context.user_data["more"] = [False, more]
                keyboard = [[InlineKeyboardButton("Veure més opcions", callback_data="more")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text("No estàs convençut/da? Si vols més opcions clica a Veure més opcions.", reply_markup=reply_markup)

    elif len(context.args) == 0:
        error = """Ups, si no em dius què vols no podré trobar-te el millor per a tu. ;)
        Si vols saber què fa la comanda find, fes /help find."""
        context.bot.send_message(chat_id=update.effective_chat.id, text=error)


def info(update, context):

    """"Mostra la informació sobre el restaurant especificat pel seu
    número (triat de la darrera llista numerada obtinguda amb /find)."""

    # s'ha hagut de fer /find primer
    if 'found' in context.user_data:
        possibilities: Restaurants = context.user_data['found']
        try:
            entry = int(context.args[0])
            # assegurar-se que l'entrada es troba entre el mínim i el màxim,
            # que depèn de si s'han demanat més opcions o no
            if 0 < entry <= _max_possibilities(context):
                restaurant: Restaurant = possibilities[entry-1]
                context.bot.send_message(chat_id=update.effective_chat.id, text=_write_info_of_restaurant(restaurant))
            else:
                error = 'Ups. Prova amb un número dins el rang de possibilitats.'
                context.bot.send_message(chat_id=update.effective_chat.id, text=error)
        except Exception:
            error = 'Ups. L\'entrada no és vàlida...'
            context.bot.send_message(chat_id=update.effective_chat.id, text=error)

    else:
        error = 'Ups. Prova a fer /find primer... Si vols saber què fa la comanda /info fes /help info.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=error)


def guide(update, context):

    """Mostra un mapa amb el camí més curt per anar del punt actual
    on et trobes al restaurant especificat pel seu número (triat de la
    darrera llista numerada obtinguda amb /find) conjuntament amb una
    breu descripció del trajecte."""

    if 'location' in context.user_data is not None:
        # s'ha hagut de fer /find primer
        if 'found' in context.user_data:
            possibilities: Restaurants = context.user_data['found']
            entry = int(context.args[0])

            if 0 < entry <= _max_possibilities(context):
                text_espera = "Això pot trigar uns segons...⌛\nAquí tens una broma per l'espera..."
                context.bot.send_message(chat_id=update.effective_chat.id, text=text_espera)
                # trobar el camí més curt
                path: Path = _path(context, entry)
                # broma
                context.bot.send_message(chat_id=update.effective_chat.id, text=jokes.values[randint(0, 99999) % 1623][1])
                # guardar camí a fitxer de nom aleatori (no solapament)
                filename: str = "%d.png" % randint(0, 9999999)
                plot_path(city_graph, path, filename)
                # mostrar els resultats obtinguts a l'usuari
                context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO)
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(filename, "rb"))  # imatge de recorregut
                context.bot.send_message(chat_id=update.effective_chat.id, text=get_path_description(city_graph, path))  # descripció recorregut
                text_temps = "Temps aproximat de trajecte: " + str(get_time_path(city_graph, path)) + " min.\nBona sort nano! RUm RUm."
                context.bot.send_message(chat_id=update.effective_chat.id, text=text_temps)  # temps de recorregut
                os.remove(filename)
            else:
                error = 'Ups. Prova amb un número dins el rang de possibilitats.'
                context.bot.send_message(chat_id=update.effective_chat.id, text=error)
        else:
            error = 'Ups. Prova a fer find primer.'
            context.bot.send_message(chat_id=update.effective_chat.id, text=error)
    else:
        error = """Ups, alguna cosa ha fallat.
        Sisplau, envia'm la teva ubicació 📍 perquè pugui guiar-te."""
        context.bot.send_message(chat_id=update.effective_chat.id, text=error)


def main() -> None:

    print(6)
    # declara una constant amb el access token que llegeix de token.txt
    TOKEN = open('token.txt').read().strip()

    # crea objectes per treballar amb Telegram
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # indica que quan el bot rebi una comanda s'executi la funció
    # associada a aquesta
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('find', find))
    dispatcher.add_handler(CommandHandler('info', info))
    dispatcher.add_handler(CommandHandler('guide', guide))
    dispatcher.add_handler(CommandHandler('author', author))

    dispatcher.add_handler(MessageHandler(Filters.location, _where))
    dispatcher.add_handler(CallbackQueryHandler(_handler_more))

    # engega el bot
    print("Inici bot")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    """Executar funció main"""

    main()
