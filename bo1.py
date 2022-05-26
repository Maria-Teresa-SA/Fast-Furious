from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import city
import metro
import restaurants
from random import randint
import os


street_graph = city.load_osmnx_graph("barcelona.grf")
metro_graph = metro.get_metro_graph()
graph_city = city.build_city_graph(street_graph, metro_graph)
list_restaurants = restaurants.read()


diccionari_ajuda = {
    "start" : "Inicia la conversa amb el bot.",
    "help" : "Ofereix ajuda sobre les comandes disponibles. Si necessites informació addicional d'alguna d'aquestes comandes pots fer-ho fent help <comand>. Per exemple, /help help.",
    "author" : "Mostra el nom de les autores del projecte.",
    "find" : """Cerca quins restaurants satisfan la cerca realitzada i n'escriu una llista numerada (12 elements com a molt). Quan s'ha realitzat una demanda, es pot requerir més informació 
    sobre un restaurant concret utilitzant la comanda info (veure abaix). Per exemple: /find pizza.""",
    "info" : "Mostra la informació sobre el restaurant especificat pel seu número (triat de la darrera llista numerada obtinguda amb /find).",
    "guide" : """Mostra un mapa amb el camí més curt per anar del punt actual on et trobes al restaurant especificat pel seu número (triat de la darrera llista numerada obtinguda amb /find). Agafa la targeta de metro i a degustar!"""
}

diccionari_emojis = {
    'Restaurants' : "🍽️",
    'Tablaos flamencs' : "💃",
    'Cocteleries' : "🍸",
    'Xampanyeries' : "🍾",
    'Bars i pubs musicals' : "🍺" ,
    'Discoteques' : "🌐",
    'Karaokes': "🎤",
    'Teatres' : "🎭"
}

def start(update, context):
    """Funció que saluda i que s'executa quan el bot reb el missatge /start."""

    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Què passa tronco! Benvingut a Fast and Furious. Si necessites ajuda, utilitza la comanda /help.")
    username = update.effective_chat.username
    fullname =  update.effective_chat.first_name + ' ' + update.effective_chat.last_name



def help(update, context):
    """Ofereix ajuda a l'usuari i especificacions de les diferents accions que pot realitzar el bot."""

    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text = 
        """Hola, soc el Bot i soc aquí per ajudar! Aquest bot implementa les següents comandes:
                1. start
                2. find
                3. info
                4. guide
                5. help
                6. author
        Si necessites informació addicional d'alguna d'aquestes comandes pots fer-ho fent help <comand>.
        Molta sort navegant-me. ;)
        """)
        
    elif context.args[0] in diccionari_ajuda:
        context.bot.send_message(chat_id=update.effective_chat.id, text = diccionari_ajuda[context.args[0]])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "No reconec aquesta comanda.")

def where(update, context):
    lat = update.effective_message.location.latitude
    lon = update.effective_message.location.longitude
    context.user_data["location"] = metro.Coord(lon, lat)

def author(update, context):
    """Escriu pel xat el nom de les autores del projecte."""

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hola! Aquest bot l'han creat les millors programadores del món (pista: Sílvia Fàbregas i Laura Solà)")

def text_twelve(begin: int, end: int, possibilities):
    _text = ""
    for i in range(begin, end):
        _text += str(i + 1) + " " + diccionari_emojis[possibilities[i].category] + " - " + possibilities[i].name + '\n'
    return _text

# POSEM LO DE ASYNC???? PERGUNTAR A LEMMA
def find(update, context):
    """Troba els restaurants que compleixen les condicions requerides per l'usuari i imprimeix les opcions disponibles per pantalla (màxim 12 opcions)."""

    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Ups, si no em dius què vols no podré trobar-te el millor per tu. ;)")
    
    else:
        queries = []
        for entry in context.args: 
            queries.append(str(entry))
        possibilities = restaurants.find(queries, list_restaurants)
        # actualitzem i guardem les possibilitats associades a l'últim found realitzat.
        context.user_data['found'] = possibilities
        num_outputs  = min(len(possibilities), 12)
        if num_outputs == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text= "Oh no... 😢 No s'ha trobat cap restaurant amb aquesta entrada... Prova-ho amb una altra... 😊")       
        else:            
            context.bot.send_message(chat_id=update.effective_chat.id, text= text_twelve(0, num_outputs, possibilities))
            # if(len(possibilities) > 12):
            #     keyboard = [
            #         [
            #             InlineKeyboardButton("Veure més opcions", callback_data= text_twelve(12, 12 + min(len(possibilitats)-12, 12))),
            #             InlineKeyboardButton("Ja m'agraden aquestes", callback_data=None),
            #         ]
            #     ]
            #     rm = InlineKeyboardMarkup(keyboard)
            #     update.message.reply_text("No estàs convençuda? Si vole veure més opcions clica a More." , reply_markup=rm)

                    
    


def write_info_of_restaurant(restaurant):
    nom = "Nom del restaurant: " + restaurant.name + "\n"
    categoria = "Categoria: " + restaurant.category + " " + diccionari_emojis[restaurant.category] + "\n"
    districte = "Districte: " + restaurant.address.district + "\n"
    barri = "Barri: " + restaurant.address.neighbourhood + "\n"
    adressa = "Addressa: Carrer " + restaurant.address.address_name + " número " + restaurant.address.address_num + "\n"
    return nom+categoria+districte+barri+adressa


# altres errors a considerar: primer argument d'entrada no és un enter
def info(update, context):
    if 'found' in context.user_data:
        possibilities = context.user_data['found']
        try:
            entrada = int(context.args[0])
            if entrada <= len(possibilities):
                restaurant = possibilities[entrada - 1]
                _text = write_info_of_restaurant(restaurant)
                context.bot.send_message(chat_id=update.effective_chat.id, text= _text)

            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text= 'Prova amb un número dins el rang de possibilitats.')
        except Exception as e:
            print(e)
            context.bot.send_message(chat_id=update.effective_chat.id, text = '💣')
            
    else:
        # print(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'Ups. Prova a fer find primer... Si vols saber què fa la comanda info fes /help info.')

    

# recordar checkejar que l'entrada és un enter
def guide(update, context):
    if 'found' in context.user_data:
        possibilities = context.user_data['found']
        entrada = int(context.args[0])
        if entrada <= len(possibilities):

            filename = "%d.png" % randint(0, 9999999)
            coordinate_restaurant = possibilities[entrada - 1].position
            current_location = context.user_data["location"]
            # falta afegir les coordenades del retaurant, agafar les coordenades de la persona amb qui ens comuniquem, fer les funcions plot(city i path) i show a city.py
            path = city.find_path(street_graph, graph_city, coordinate_restaurant, current_location)
            city.plot_path(graph_city, path, filename)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(filename, "rb"))
            os.remove(filename)
        # else:
        #     context.bot.send_message(chat_id=update.effective_chat.id,
        #                              text='Prova amb un número dins el rang de possibilitats.')

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='ups. Prova a fer find primer.')


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
    dispatcher.add_handler(MessageHandler(Filters.location, where))


    # engega el bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    """Executar funció main"""

    main()