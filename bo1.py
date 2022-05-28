from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from city import *
from metro import *
from restaurants import *
from random import randint
import os

# grafs
street_graph = load_osmnx_graph("barcelona.grf")
metro_graph = get_metro_graph()
city_graph = build_city_graph(street_graph, metro_graph)

# restaurants
list_restaurants = read_restaurants()

# bromes
jokes = pandas.read_csv("reddit-cleanjokes.csv", usecols=["ID", "Joke"], dtype={"ID": int, "Joke": str})

# diccionaris
help_dic = {
    "start" : "Inicia la conversa amb mi.",
    "help" : "Ofereix ajuda sobre les comandes disponibles. Si necessites informació addicional d'alguna d'aquestes comandes pots fer-ho fent help <comanda>. Per exemple, /help help o /help info.",
    "author" : "Mostra el nom de les autores del projecte.",
    "find" : """Cerca quins restaurants satisfan la cerca realitzada i n'escriu una llista numerada de 12 elements com a molt. També ofereix la possibilitat d'expandir fins a 6 possibilitats de més. Quan s'ha realitzat una demanda, es pot requerir més informació 
    sobre un restaurant concret utilitzant la comanda info (veure /help info). Exemples de cerca: /find pizza, /find pasta sants.""",
    "info" : "Mostra la informació sobre el restaurant especificat pel seu número (triat de la darrera llista numerada obtinguda amb /find). Exemple /info 4.",
    "guide" : """Mostra un mapa amb el camí més curt per anar del punt actual on et trobes al restaurant especificat pel seu número (triat de la darrera llista numerada obtinguda amb /find) conjuntament amb una breu descripció del trajecte. Exemple: /guide 4. Agafa la targeta de metro i a degustar!"""
}

emojis_dic = {
    'Restaurants' : "🍽️",
    'Tablaos flamencs' : "💃",
    'Cocteleries' : "🍸",
    'Xampanyeries' : "🍾",
    'Bars i pubs musicals' : "🍺" ,
    'Discoteques' : "🌐",
    'Karaokes': "🎤",
    'Teatres' : "🎭"
}

def _write_info_of_restaurant(restaurant):
    """Retorna la informació del restaurant demanat per la comanda info."""

    name = "Nom del restaurant: " + restaurant.name + "\n"
    category = "Categoria: " + restaurant.category + " " + emojis_dic[restaurant.category] + "\n"
    district = "Districte: " + restaurant.address.district + "\n"
    neighbourhood = "Barri: " + restaurant.address.neighbourhood + "\n"
    address = "Addressa: Carrer " + restaurant.address.address_name + " número " + restaurant.address.address_num + "\n"
    return name + category + district + neighbourhood + address


def _where(update, context):
    """Guarda la ubicació de l'ususari quan aquest li passa."""

    lat = update.effective_message.location.latitude
    lon = update.effective_message.location.longitude
    context.user_data["location"] = Coord(lon, lat)


def _handler_more(update, context):
    """S'encarrega de gestionar el cas en què es clica el botó de Veure més opcions."""

    if not context.user_data["more"][0]:
        context.user_data["more"][0] = True
        context.bot.send_message(chat_id=update.effective_chat.id, text = context.user_data["more"][1])


def start(update, context):
    """Funció que saluda i que s'executa quan el bot reb el missatge /start."""
    
    context.bot.send_message(chat_id=update.effective_chat.id, text= """Hola! Benvingut/da a Fast and Furious.
    Se t'ha cremat la paella 🥘 i no saps on menjar avui? Aquest bot t'ajudarà a trobar el lloc ideal i com arribar-hi.
    Per funcionar correctament m'hauràs de compartir la teva ubicació. 📍 No pateixis, no penso vendre les teves dades ;).
    A més a més, si necessites algun tipus d'ajuda, pots fer servir la comanda /help. """)
    username = update.effective_chat.username
    fullname =  update.effective_chat.first_name + ' ' + update.effective_chat.last_name


def help(update, context):
    """Ofereix ajuda a l'usuari i especificacions de les diferents accions que pot realitzar el bot."""

    if len(context.args) == 0:
        # cas en què es demana la comanda /help simple
        context.bot.send_message(chat_id=update.effective_chat.id, text = 
        """Hola, soc Fast & Furious (Ràpida i Furiosa) i soc aquí per ajudar! Aquest bot implementa les següents comandes:
                1. /start - inici
                2. /find - búsqueda restaurants
                3. /info - informació restaurants
                4. /guide - guiar a restaurant
                5. /help - ajuda
                6. /author - autores del projecte
        Si necessites informació addicional d'alguna d'aquestes comandes pots fer-ho fent /help <comanda>. Exemple: /help info
        Molta sort recorrent-me. 🚇
        """)
        
    elif context.args[0] in help_dic:
        # cas en què es demana /help <comanda> per una comanda vàlida
        context.bot.send_message(chat_id=update.effective_chat.id, text = help_dic[context.args[0]])
    else:
        # cas en què es demana /help <comanda> per una comanda no vàlida
        context.bot.send_message(chat_id=update.effective_chat.id, text = "No reconec aquesta comanda.")

def author(update, context):
    """Escriu pel xat el nom de les autores del projecte."""

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hola! Aquest bot l'han creat les millors programadores del món (pista: Sílvia Fàbregas i Laura Solà)")

def _text_rest(begin: int, end: int, possibilities):
    """Retorna un text amb els restaurants requerits per l'entrada de la llista de possibilities."""

    text = ""
    for i in range(begin, end):
        text += str(i + 1) + " " + emojis_dic[possibilities[i].category] + " - " + possibilities[i].name + '\n'
    return text

def find(update, context):
    """Cerca quins restaurants satisfan la cerca realitzada i n'escriu una llista numerada de 12 elements com a molt. També ofereix la possibilitat d'expandir fins a 6 possibilitats de més. ."""

    if len(context.args) != 1:
        queries = [entry for entry in context.args]
        possibilities = find_restaurants(queries, list_restaurants)
        context.user_data['found'] = possibilities # actualitzem i guardem les possibilitats associades a l'últim found realitzat.
        num_outputs  = min(len(possibilities), 12)
        if num_outputs == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text= "Oh no... 😢 No s'ha trobat cap restaurant amb aquesta entrada... Prova-ho amb una altra... 😊")       
        else:            
            context.bot.send_message(chat_id=update.effective_chat.id, text= _text_rest(0, num_outputs, possibilities))
            context.user_data["more"] = [False, ""] # encara no s'ha clicat al botó de more
            if len(possibilities) > 12:
                more = _text_rest(12, 12 + min(len(possibilities)-12, 6), possibilities) # guarda el text de les opcions de més
                context.user_data["more"] = [False, more] 
                keyboard = [[InlineKeyboardButton("Veure més opcions", callback_data="more")]]
                rm = InlineKeyboardMarkup(keyboard)
                update.message.reply_text("No estàs convençuda/ut? Si vols més opcions clica a Veure més opcions." , reply_markup=rm)
    
    elif len(context.args) == 0: 
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Ups, si no em dius què vols no podré trobar-te el millor per a tu. ;)")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= "Ai, ai, ai, quantes coses vols a la vegada!")



def info(update, context):
    """"Mostra la informació sobre el restaurant especificat pel seu número (triat de la darrera llista numerada obtinguda amb /find)."""

    if 'found' in context.user_data:
        possibilities = context.user_data['found']
        try:
            entry = int(context.args[0])
            # assegurar-se que l'entrada es troba entre el mínim i el màxim, que depèn de si s'han demanat més opcions o no
            if 0 < entry <= min(12 + (context.user_data["more"][0])*min(6, len(possibilities) - 12), len(possibilities)): 
                restaurant = possibilities[entry-1]
                context.bot.send_message(chat_id=update.effective_chat.id, text= _write_info_of_restaurant(restaurant))
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text= 'Ups. Prova amb un número dins el rang de possibilitats.')
        except Exception:
            context.bot.send_message(chat_id=update.effective_chat.id, text = 'Ups. L\'entrada no és vàlida...')
            
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'Ups. Prova a fer /find primer... Si vols saber què fa la comanda /info fes /help info.')

    

def guide(update, context):
    """Mostra un mapa amb el camí més curt per anar del punt actual on et trobes al restaurant especificat pel seu número
    (triat de la darrera llista numerada obtinguda amb /find) conjuntament amb una breu descripció del trajecte."""

    try:
        if 'found' in context.user_data:
            possibilities = context.user_data['found']
            entry = int(context.args[0])

            if 0 < entry <= min(12 + (context.user_data["more"][0])*min(6, len(possibilities) - 12), len(possibilities)):
                context.bot.send_message(chat_id=update.effective_chat.id, text="Això pot trigar uns segons...⌛\nAquí tens una broma per l'espera...")
                
                # trobar el camí més curt
                coordinate_restaurant = possibilities[entry - 1].position
                current_location = context.user_data["location"]
                path = find_path(street_graph, city_graph, current_location, coordinate_restaurant)

                # broma
                context.bot.send_message(chat_id=update.effective_chat.id, text= jokes.values[randint(0, 99999)%1623][1])

                # guardar camí a fitxer
                filename = "%d.png" % randint(0, 9999999)   # ho guardem a un fitxer de nom un enter aleatori perquè no hi hagi solapament amb diferents usuaris.
                plot_path(city_graph, path, filename)

                # mostrar els resultats obtinguts a l'usuari
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(filename, "rb"))    # imatge de recorregut
                context.bot.send_message(chat_id=update.effective_chat.id, text = get_path_description(city_graph, path))   # descripció recorregut
                context.bot.send_message(chat_id=update.effective_chat.id, text = "Temps aproximat de trajecte: " + str(get_time_path(city_graph,path)) + " min.\nBona sort nano! RUm RUm.") # temps de recorregut
                os.remove(filename)

            else:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                        text='Ups. Prova amb un número dins el rang de possibilitats...')

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                text='Ups. Prova a fer find primer.')
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sisplau, envia'm la teva ubicació 📍 perquè pugui guiar-te.")



def main() -> None:

    # declara una constant amb el access token que llegeix de token.txt
    TOKEN = open('token.txt').read().strip()

    # crea objectes per treballar amb Telegram
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # indica que quan el bot rebi una comanda s'executi la funció associada a aquesta
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('find', find))
    dispatcher.add_handler(CommandHandler('info', info))
    dispatcher.add_handler(CommandHandler('guide', guide))
    dispatcher.add_handler(CommandHandler('author', author))
    dispatcher.add_handler(MessageHandler(Filters.location, _where))
    dispatcher.add_handler(CallbackQueryHandler(_handler_more))

    # engega el bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    """Executar funció main"""

    main()
