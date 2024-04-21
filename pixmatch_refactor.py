import streamlit as st
import os
import time as tm
import random
import base64
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh
# Configuracion de los atributos generales de la página
st.set_page_config(page_title = "PixMatch", page_icon="🕹️", layout = "wide", initial_sidebar_state = "expanded")

# Obtener la unidad de disco donde se encuentra el directorio actual
vDrive = os.path.splitdrive(os.getcwd())[0]

#if vDrive == "C:": vpth = "C:/Users/Shawn/dev/utils/pixmatch/"   # local developer's disc
#else:

#establecer la ruta del directorio local del desarrollador
vpth = "./"

# crea la plantilla para un estilo de texto grande
sbe = """<span style='font-size: 140px;
                      border-radius: 7px;
                      text-align: center;
                      display:inline;
                      padding-top: 3px;
                      padding-bottom: 3px;
                      padding-left: 0.4em;
                      padding-right: 0.4em;
                      '>
                      |fill_variable|
                      </span>"""

# crea la plantilla para un estilo para emojis
pressed_emoji = """<span style='font-size: 24px;
                                border-radius: 7px;
                                text-align: center;
                                display:inline;
                                padding-top: 3px;
                                padding-bottom: 3px;
                                padding-left: 0.2em;
                                padding-right: 0.2em;
                                '>
                                |fill_variable|
                                </span>"""

# Línea divisoria delgada
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"

#Estilo para el color del boton purpura
purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """

#Estado de la sesion
mystate = st.session_state
# Si no existen las siguientes claves en el estado de la sesión, se inicializan con valores predeterminados
if "expired_cells" not in mystate: mystate.expired_cells = []
if "myscore" not in mystate: mystate.myscore = 0
if "plyrbtns" not in mystate: mystate.plyrbtns = {}
if "sidebar_emoji" not in mystate: mystate.sidebar_emoji = ''
if "emoji_bank" not in mystate: mystate.emoji_bank = []
if "GameDetails" not in mystate: mystate.GameDetails = ['Medium', 6, 7, '']  # Nivel de dificultad, intervalo de segundos para autogeneración, celdas totales por fila o columna, nombre del jugador

# common functions
def ReduceGapFromPageTop(wch_section='main page'):
    """
    Reduce el espacio desde la parte superior de la página ajustando el relleno de la sección especificada.
    """
    if wch_section == 'main page':
        # área principal
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
    elif wch_section == 'sidebar':
        # barra lateral
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)
    elif wch_section == 'all':
        # área principal
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
        # barra lateral
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)


def Leaderboard(what_to_do):
    """
    Gestiona la creación, escritura y lectura del marcador.
    Parametros:
        what_to_do el string representa la accion a realizar ('create' para crear, 'write' para escribir, 'read' para leer).
    """
    if what_to_do == 'create':
        # Crea un archivo de marcador si no existe y el nombre del jugador está disponible
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json') == False:
                tmpdict = {}
                json.dump(tmpdict, open(vpth + 'leaderboard.json', 'w'))  # write file

    elif what_to_do == 'write':
        # Escribe en el marcador si el nombre del jugador está disponible
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))  # lee un archivo
                leaderboard_dict_lngth = len(leaderboard)

                leaderboard[str(leaderboard_dict_lngth + 1)] = {'NameCountry': mystate.GameDetails[3],'HighestScore': mystate.myscore}
                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # ordena decendentemente

                if len(leaderboard) > 4:
                    for i in range(len(leaderboard) - 4):
                        leaderboard.popitem()

                json.dump(leaderboard, open(vpth + 'leaderboard.json', 'w'))  # escribe en el archivo

    elif what_to_do == 'read':
        # Lee el marcador si el nombre del jugador está disponible
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))  # lee el archivo

                leaderboard = dict(
                    sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # ordena decendente

                sc0, sc1, sc2, sc3, sc4 = st.columns((2, 3, 3, 3, 3))
                rknt = 0
                for vkey in leaderboard.keys():
                    if leaderboard[vkey]['NameCountry'] != '':
                        rknt += 1
                        if rknt == 1:
                            sc0.write('🏆 Past Winners:')
                            sc1.write(f"🥇 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 2:
                            sc2.write(f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 3: sc3.write(f"🥉 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 4:
                            sc4.write(f"🥉 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")

def InitialPage():
    """
       Define la página inicial del juego Pix Match.
    """
    with st.sidebar:
        st.subheader("🖼️ Pix Match:")
        st.markdown(horizontal_bar, True)

        # sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 420))
        sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 390))
        st.image(sidebarlogo, use_column_width='auto')

    # ViewHelp
    hlp_dtl = f"""<span style="font-size: 26px;">
    <ol>
    <li style="font-size:15px";>Game play opens with (a) a sidebar picture and (b) a N x N grid of picture buttons, where N=6:Easy, N=7:Medium, N=8:Hard.</li>
    <li style="font-size:15px";>You need to match the sidebar picture with a grid picture button, by pressing the (matching) button (as quickly as possible).</li>
    <li style="font-size:15px";>Each correct picture match will earn you <strong>+N</strong> points (where N=5:Easy, N=3:Medium, N=1:Hard); each incorrect picture match will earn you <strong>-1</strong> point.</li>
    <li style="font-size:15px";>The sidebar picture and the grid pictures will dynamically regenerate after a fixed seconds interval (Easy=8, Medium=6, Hard=5). Each regeneration will have a penalty of <strong>-1</strong> point</li>
    <li style="font-size:15px";>Each of the grid buttons can only be pressed once during the entire game.</li>
    <li style="font-size:15px";>The game completes when all the grid buttons are pressed.</li>
    <li style="font-size:15px";>At the end of the game, if you have a positive score, you will have <strong>won</strong>; otherwise, you will have <strong>lost</strong>.</li>
    </ol></span>""" 

    sc1, sc2 = st.columns(2)
    random.seed()
    GameHelpImg = vpth + random.choice(["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    GameHelpImg = Image.open(GameHelpImg).resize((550, 550))
    sc2.image(GameHelpImg, use_column_width='auto')

    sc1.subheader('Rules | Playing Instructions:')
    sc1.markdown(horizontal_bar, True)
    sc1.markdown(hlp_dtl, unsafe_allow_html=True)
    st.markdown(horizontal_bar, True)

    author_dtl = "<strong>Happy Playing: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
    st.markdown(author_dtl, unsafe_allow_html=True)

def ReadPictureFile(wch_fl):
    """
    Lee un archivo de imagen y devuelve su representacion en base64.
    """
    try:
        pxfl = f"{vpth}{wch_fl}"  # Obtiene la ruta completa del archivo de imagen.
        return base64.b64encode(open(pxfl, 'rb').read()).decode()  # Lee el archivo de imagen, lo codifica en base64 y lo devuelve como una cadena.

    except:
        return ""  # Devuelve una cadena vacía si hay algún error durante la lectura del archivo de imagen.


def PressedCheck(vcell):
    """
    Verifica si un botón de celda ha sido presionado y realiza las acciones correspondientes.

    """
    if mystate.plyrbtns[vcell]['isPressed'] == False:  # Verifica si el botón de la celda aún no ha sido presionado.
        mystate.plyrbtns[vcell]['isPressed'] = True  # Marca el botón de la celda como presionado.
        mystate.expired_cells.append(vcell)  # Agrega el índice de la celda a la lista de celdas expiradas.

        if mystate.plyrbtns[vcell][
            'eMoji'] == mystate.sidebar_emoji:  # Verifica si el emoji del botón coincide con el emoji de la barra lateral.
            mystate.plyrbtns[vcell]['isTrueFalse'] = True  # Marca el resultado como verdadero.
            mystate.myscore += 5  # Aumenta la puntuación en 5 puntos.

            # Ajusta la puntuación según la dificultad del juego.
            if mystate.GameDetails[0] == 'Easy':
                mystate.myscore += 5
            elif mystate.GameDetails[0] == 'Medium':
                mystate.myscore += 3
            elif mystate.GameDetails[0] == 'Hard':
                mystate.myscore += 1

        else:  # Si el emoji del botón no coincide con el emoji de la barra lateral.
            mystate.plyrbtns[vcell]['isTrueFalse'] = False  # Marca el resultado como falso.
            mystate.myscore -= 1  # Reduce la puntuación en 1 punto.


def ResetBoard():
    """
    Reinicia el tablero del juego.

    """
    total_cells_per_row_or_col = mystate.GameDetails[2]  # Obtiene el número total de celdas por fila o columna.

    # Selecciona un emoji aleatorio para la barra lateral.
    sidebar_emoji_no = random.randint(1, len(mystate.emoji_bank)) - 1
    mystate.sidebar_emoji = mystate.emoji_bank[sidebar_emoji_no]

    sidebar_emoji_in_list = False  # Bandera para verificar si el emoji de la barra lateral esta en la lista de emojis de los botones.

    # Asigna emojis aleatorios a los botones que no han sido presionados.
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        rndm_no = random.randint(1, len(mystate.emoji_bank)) - 1
        if mystate.plyrbtns[vcell]['isPressed'] == False:
            vemoji = mystate.emoji_bank[rndm_no]
            mystate.plyrbtns[vcell]['eMoji'] = vemoji
            if vemoji == mystate.sidebar_emoji:
                sidebar_emoji_in_list = True

    # Si el emoji de la barra lateral no esta en la lista de emojis de los botones, se agrega aleatoriamente a un boton.
    if sidebar_emoji_in_list == False:
        tlst = [x for x in range(1, ((total_cells_per_row_or_col ** 2) + 1))]
        flst = [x for x in tlst if x not in mystate.expired_cells]
        if len(flst) > 0:
            lptr = random.randint(0, (len(flst) - 1))
            lptr = flst[lptr]
            mystate.plyrbtns[lptr]['eMoji'] = mystate.sidebar_emoji


def PreNewGame():
    """
        Prepara el juego para una nueva partida.

        """
    total_cells_per_row_or_col = mystate.GameDetails[2] # Obtiene el número total de celdas por fila o columna.
    # Reinicia la lista de celdas expiradas y la puntuación del jugador.
    mystate.expired_cells = []
    mystate.myscore = 0
    # Define listas de emojis para cada nivel de dificultad.
    foxes = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    emojis = ['😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😠', '😳', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤒']
    humans = ['👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '👨‍🦱', '👩‍🦰', '‍👨', '👱', '👩', '👱', '👩‍', '👨‍🦳', '👩‍🦲', '👵', '🧓', '👴', '👲', '👳'] 
    foods = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬', '🥒', '🌽', '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗', '🍖', '🦴', '🌭', '🍔', '🍟', '🍕']
    clocks = ['🕓', '🕒', '🕑', '🕘', '🕛', '🕚', '🕖', '🕙', '🕔', '🕤', '🕠', '🕕', '🕣', '🕞', '🕟', '🕜', '🕢', '🕦']
    hands = ['🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊', '🤛', '🤜', '👏', '🙌', '🤲', '🤝', '🤚🏻', '🖐🏻', '✋🏻', '🖖🏻', '👌🏻', '🤏🏻', '✌🏻', '🤞🏻', '🤟🏻', '🤘🏻', '🤙🏻', '👈🏻', '👉🏻', '👆🏻', '🖕🏻', '👇🏻', '☝🏻', '👍🏻', '👎🏻', '✊🏻', '👊🏻', '🤛🏻', '🤜🏻', '👏🏻', '🙌🏻', '🤚🏽', '🖐🏽', '✋🏽', '🖖🏽', '👌🏽', '🤏🏽', '✌🏽', '🤞🏽', '🤟🏽', '🤘🏽', '🤙🏽', '👈🏽', '👉🏽', '👆🏽', '🖕🏽', '👇🏽', '☝🏽', '👍🏽', '👎🏽', '✊🏽', '👊🏽', '🤛🏽', '🤜🏽', '👏🏽', '🙌🏽']
    animals = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔', '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗', '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆', '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕', '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔']
    vehicles = ['🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼', '🛴', '🚲', '🛵', '🛺', '🚔', '🚍', '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬', '💺', '🚀', '🛸', '🚁', '🛶', '⛵️', '🚤', '🛳', '⛴', '🚢']
    houses = ['🏠', '🏡', '🏘', '🏚', '🏗', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪️', '🕌', '🕍', '🛕']
    purple_signs = ['☮️', '✝️', '☪️', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️', '♌️', '♍️', '♎️', '♏️', '♐️', '♑️', '♒️', '♓️', '🆔', '🈳']
    red_signs = ['🈶', '🈚️', '🈸', '🈺', '🈷️', '✴️', '🉐', '㊙️', '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘', '🚼', '🛑', '⛔️', '📛', '🚫', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭']
    blue_signs = ['🚾', '♿️', '🅿️', '🈂️', '🛂', '🛃', '🛄', '🛅', '🚹', '🚺', '🚻', '🚮', '🎦', '📶', '🈁', '🔣', '🔤', '🔡', '🔠', '🆖', '🆗', '🆙', '🆒', '🆕', '🆓', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '🔢', '⏏️', '▶️', '⏸', '⏯', '⏹', '⏺', '⏭', '⏮', '⏩', '⏪', '⏫', '⏬', '◀️', '🔼', '🔽', '➡️', '⬅️', '⬆️', '⬇️', '↗️', '↘️', '↙️', '↖️', '↪️', '↩️', '⤴️', '⤵️', '🔀', '🔁', '🔂', '🔄', '🔃', '➿', '🔚', '🔙', '🔛', '🔝', '🔜']
    moon = ['🌕', '🌔', '🌓', '🌗', '🌒', '🌖', '🌑', '🌜', '🌛', '🌙']

    random.seed()
    # Selecciona una lista de emojis aleatoria dependiendo del nivel de dificultad.
    if mystate.GameDetails[0] == 'Easy':
        wch_bank = random.choice(['foods', 'moon', 'animals'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Medium':
        wch_bank = random.choice(['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Hard':
        wch_bank = random.choice(['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs', 'red_signs', 'blue_signs', 'moon'])
        mystate.emoji_bank = locals()[wch_bank]
    # Reinicia el diccionario de botones del jugador.
    mystate.plyrbtns = {}
    for vcell in range(1, ((total_cells_per_row_or_col ** 2)+1)): mystate.plyrbtns[vcell] = {'isPressed': False, 'isTrueFalse': False, 'eMoji': ''}

def ScoreEmoji():
    """
    Asigna un emoji basado en la puntuación del jugador.

    """
    if mystate.myscore == 0:  # Si la puntuación es igual a cero.
        return '😐'  # Devuelve el emoji de expresión neutral.
    elif -5 <= mystate.myscore <= -1:  # Si la puntuación está entre -5 y -1.
        return '😏'  # Devuelve el emoji de expresión ligeramente negativa.
    elif -10 <= mystate.myscore <= -6:  # Si la puntuación está entre -10 y -6.
        return '☹️'  # Devuelve el emoji de expresión negativa.
    elif mystate.myscore <= -11:  # Si la puntuación es igual o inferior a -11.
        return '😖'  # Devuelve el emoji de expresión muy negativa.
    elif 1 <= mystate.myscore <= 5:  # Si la puntuación está entre 1 y 5.
        return '🙂'  # Devuelve el emoji de expresión ligeramente positiva.
    elif 6 <= mystate.myscore <= 10:  # Si la puntuación está entre 6 y 10.
        return '😊'  # Devuelve el emoji de expresión positiva.
    elif mystate.myscore > 10:  # Si la puntuación es mayor que 10.
        return '😁'  # Devuelve el emoji de expresión muy positiva.


def NewGame():
    ResetBoard()# Reinicia el tablero del juego
    total_cells_per_row_or_col = mystate.GameDetails[2]# Obtiene el número total de celdas por fila o columna

    ReduceGapFromPageTop('sidebar')  # Reducción del espacio desde la parte superior de la página
    with st.sidebar:
        st.subheader(f"🖼️ Pix Match: {mystate.GameDetails[0]}")# Encabezado de la barra lateral con el nivel de dificultad seleccionado
        st.markdown(horizontal_bar, True)# Línea horizontal decorativa

        st.markdown(sbe.replace('|fill_variable|', mystate.sidebar_emoji), True) # Muestra el emoji de la barra lateral

        aftimer = st_autorefresh(interval=(mystate.GameDetails[1] * 1000), key="aftmr")# Actualiza automáticamente el temporizador en la barra lateral
        if aftimer > 0: mystate.myscore -= 1 # Reduce el puntaje si el temporizador está en funcionamiento

        st.info(f"{ScoreEmoji()} Score: {mystate.myscore} | Pending: {(total_cells_per_row_or_col ** 2) - len(mystate.expired_cells)}")

        st.markdown(horizontal_bar, True)
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            mystate.runpage = Main
            st.rerun()

    Leaderboard('read')
    st.subheader("Picture Positions:")
    st.markdown(horizontal_bar, True)

    # Set Board Dafaults
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ", unsafe_allow_html=True)  # make button face big
    errores = 0
    for i in range(1, (total_cells_per_row_or_col+1)):
        tlst = ([1] * total_cells_per_row_or_col) + [2] # 2 = rt side padding
        globals()['cols' + str(i)] = st.columns(tlst)

    for vcell in range(1, (total_cells_per_row_or_col ** 2)+1):
        if errores == (total_cells_per_row_or_col ** 1)+1:
            mystate.runpage = Main
            st.rerun()
            break
        if 1 <= vcell <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0

        elif ((total_cells_per_row_or_col * 1)+1) <= vcell <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)

        elif ((total_cells_per_row_or_col * 2)+1) <= vcell <= (total_cells_per_row_or_col * 3):
            arr_ref = '3'
            mval = (total_cells_per_row_or_col * 2)

        elif ((total_cells_per_row_or_col * 3)+1) <= vcell <= (total_cells_per_row_or_col * 4):
            arr_ref = '4'
            mval = (total_cells_per_row_or_col * 3)

        elif ((total_cells_per_row_or_col * 4)+1) <= vcell <= (total_cells_per_row_or_col * 5):
            arr_ref = '5'
            mval = (total_cells_per_row_or_col * 4)

        elif ((total_cells_per_row_or_col * 5)+1) <= vcell <= (total_cells_per_row_or_col * 6):
            arr_ref = '6'
            mval = (total_cells_per_row_or_col * 5)

        elif ((total_cells_per_row_or_col * 6)+1) <= vcell <= (total_cells_per_row_or_col * 7):
            arr_ref = '7'
            mval = (total_cells_per_row_or_col * 6)

        elif ((total_cells_per_row_or_col * 7)+1) <= vcell <= (total_cells_per_row_or_col * 8):
            arr_ref = '8'
            mval = (total_cells_per_row_or_col * 7)

        elif ((total_cells_per_row_or_col * 8)+1) <= vcell <= (total_cells_per_row_or_col * 9):
            arr_ref = '9'
            mval = (total_cells_per_row_or_col * 8)

        elif ((total_cells_per_row_or_col * 9)+1) <= vcell <= (total_cells_per_row_or_col * 10):
            arr_ref = '10'
            mval = (total_cells_per_row_or_col * 9)

        globals()['cols' + arr_ref][vcell-mval] = globals()['cols' + arr_ref][vcell-mval].empty()
        if mystate.plyrbtns[vcell]['isPressed'] == True:
            if mystate.plyrbtns[vcell]['isTrueFalse'] == True:
                globals()['cols' + arr_ref][vcell-mval].markdown(pressed_emoji.replace('|fill_variable|', '✅️'), True)

            elif mystate.plyrbtns[vcell]['isTrueFalse'] == False:
                globals()['cols' + arr_ref][vcell-mval].markdown(pressed_emoji.replace('|fill_variable|', '❌'), True)
                errores+=1

        else:
            vemoji = mystate.plyrbtns[vcell]['eMoji']
            globals()['cols' + arr_ref][vcell-mval].button(vemoji, on_click=PressedCheck, args=(vcell, ), key=f"B{vcell}")

    st.caption('') # vertical filler
    st.markdown(horizontal_bar, True)

    if len(mystate.expired_cells) == (total_cells_per_row_or_col ** 2) :
        Leaderboard('write')

        if mystate.myscore > 0: st.balloons()
        elif mystate.myscore <= 0: st.snow()

        tm.sleep(5)
        mystate.runpage = Main
        st.rerun()


def Main():
    """
    Funcion principal que configura la interfaz de usuario y maneja las acciones del juego.
    Esta establece la apariencia de la interfaz de usuario, incluido el ancho de la barra lateral y el color de los botones.
    También presenta la página inicial y proporciona opciones para seleccionar el nivel de dificultad del juego y el nombre del jugador.
    Además, permite iniciar un nuevo juego y actualiza la interfaz de usuario en consecuencia.
    """

    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>', unsafe_allow_html=True)  # Reduce el ancho de la barra lateral
    st.markdown(purple_btn_colour, unsafe_allow_html=True)  # Establece el color de los botones en púrpura

    InitialPage()  # Muestra la página inicial

    with st.sidebar:
        # Permite al usuario seleccionar el nivel de dificultad y proporcionar el nombre del jugador
        mystate.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1,horizontal=True, )
        mystate.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India',help='Optional input only for Leaderboard')


        # Botón para iniciar un nuevo juego
        if st.button(f"🕹️ New Game", use_container_width=True):
            # Configura los detalles del juego según el nivel de dificultad seleccionado
            if mystate.GameDetails[0] == 'Easy':
                mystate.GameDetails[1] = 8  # Intervalo de tiempo en segundos
                mystate.GameDetails[2] = 6  # Celdas totales por fila o columna

            elif mystate.GameDetails[0] == 'Medium':
                mystate.GameDetails[1] = 6  # Intervalo de tiempo en segundos
                mystate.GameDetails[2] = 7  # Celdas totales por fila o columna

            elif mystate.GameDetails[0] == 'Hard':
                mystate.GameDetails[1] = 5  # Intervalo de tiempo en segundos
                mystate.GameDetails[2] = 8  # Celdas totales por fila o columna

            Leaderboard('create')  # Crea la tabla de clasificación

            PreNewGame()  # Prepara el nuevo juego
            mystate.runpage = NewGame  # Establece la página de juego
            st.rerun()  # Reinicia la interfaz de usuario para iniciar el nuevo juego

        st.markdown(horizontal_bar, True)  # Línea divisoria en la barra lateral


if 'runpage' not in mystate:
    mystate.runpage = Main  # Establece la pagina principal como la pagina de inicio por defecto
mystate.runpage()  # Ejecuta la página activa puede ser Main o NewGame