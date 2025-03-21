import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import random

# Funzione per caricare il DataFrame dal CSV
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path, sep=';', encoding='utf-8')
    return df
df = load_data(r'patente_nautica_domande.csv') # Carica il DataFrame dal file CSV

# Funzione per selezionare una domanda casuale
def select_random_question(df):
    random_index = random.randint(0, len(df) - 1)
    question_row = df.iloc[random_index]
    return question_row

# Inizializza lo stato della sessione se non esiste
if 'question_row' not in st.session_state:
    st.session_state['question_row'] = select_random_question(df)
if 'score' not in st.session_state:
    st.session_state['score'] = {
        'TEORIA DELLO SCAFO': 12,
        'MOTORI': 7,
        'SICUREZZA DELLA\rNAVIGAZIONE': 19,
        'MANOVRA E CONDOTTA': 22,
        'COLREG E SEGNALAMENTO\rMARITTIMO': 34,
        'METEOROLOGIA': 26,
        'NAVIGAZIONE\rCARTOGRAFICA ED\rELETTRONICA': 14,
        'NORMATIVA DIPORTISTICA E\rAMBIENTALE': 35,
        'TEORIA': 29,
        'ATTREZZATURA': 30,
        'MANOVRE': 9
    }
if 'question_number' not in st.session_state:
    st.session_state['question_number'] = {
        'TEORIA DELLO SCAFO': 19,
        'MOTORI': 15,
        'SICUREZZA DELLA\rNAVIGAZIONE': 22,
        'MANOVRA E CONDOTTA': 29,
        'COLREG E SEGNALAMENTO\rMARITTIMO': 50,
        'METEOROLOGIA': 29,
        'NAVIGAZIONE\rCARTOGRAFICA ED\rELETTRONICA': 35,
        'NORMATIVA DIPORTISTICA E\rAMBIENTALE': 42,
        'TEORIA': 39,
        'ATTREZZATURA': 34,
        'MANOVRE': 37
    }

# SideBar
st.sidebar.header("Usefull utilities")
st.sidebar.image("https://brandlogos.net/wp-content/uploads/2012/12/rosa-dei-venti-vector-logo.png")
st.sidebar.image("https://www.tiberyacht.com/images/sailingboat-lightning-num_941a4hjh.png")

# Header
right_col, center_col, left_col = st.columns([1, 3, 1])
with right_col:
    st.image('https://png.pngtree.com/png-clipart/20200224/original/pngtree-blue-sailing-boat-logo-icon-abstract-vector-template-sailboat-on-the-png-image_5221280.jpg', width=100)
with center_col:
    st.title('Patente Nautica')
with left_col:
    # https://echarts.streamlit.app/?ref=streamlit-io-component-charts
    liquidfill_option = {
        "series": [{"type": "liquidFill", "data": [sum(st.session_state['score'].values())/sum(st.session_state['question_number'].values())],
        'label': {'fontSize': 16}, 'outline': {'borderDistance': 0}}]
    }
    # st.write("I tuoi risultati")
    st_echarts(options=liquidfill_option, height='100px')

main_tab, test_tab, results_tab = st.tabs(["Project Overview", "Test", "Results"]) # Creates 3 tabs

# Pagina principale (Project Overview)
with main_tab:
    st.header("Benvenuto al Quiz per la Patente Nautica!")
    st.write("Questa applicazione è stata creata per aiutarti a prepararti per l'esame teorico della patente nautica.")
    st.write("Nella sezione 'Test', potrai rispondere a domande casuali estratte da un database di quesiti ufficiali.")
    st.write("Il tuo punteggio verrà visualizzato in tempo reale nella barra laterale e potrai tenere traccia dei tuoi progressi.")
    st.subheader("Come funziona:")
    st.markdown("- Naviga alla tab 'Test' per iniziare a rispondere alle domande.")
    st.markdown("- Seleziona una risposta e clicca su 'Invia risposta'.")
    st.markdown("- Riceverai un feedback immediato sulla correttezza della tua risposta.")
    st.markdown("- Clicca su 'Prossima domanda' per passare alla domanda successiva.")
    st.markdown("- Nella tab 'Results', potrai visualizzare un riepilogo completo dei tuoi risultati per argomento.")
    st.write("Speriamo che questa applicazione ti sia utile per ottenere la tua patente nautica!")
    st.subheader("Improvements:")
    st.markdown("- Estrarre le domande in base alla percentuale di sbagliate.")
    st.markdown("- Salvare i dati anche se si chiude la sessione.")

# Pagina Test
with test_tab:
    _, _, left_col_inside_tab = st.columns([1, 4, 1])
    with left_col_inside_tab:
        if st.button('Prossima domanda'): # Pulsante per passare alla domanda successiva
            st.empty()  # Rimuovi il messaggio di successo/errore prima aver caricato una nuova domanda
            st.session_state['question_row'] = select_random_question(df)
    # Estrazione dei dati della domanda corrente dallo stato della sessione
    question_row = st.session_state['question_row']
    question = question_row['DOMANDA']
    topic = question_row['VOCE']
    tema = question_row['TEMA']
    if str(question_row['RISPOSTA 3']) == 'Only two answer, this is not valid': # domande vela hanno solo due risposte
        answers = [question_row['RISPOSTA 1'], question_row['RISPOSTA 2']]
        correct_flags = [question_row['V/F 1'], question_row['V/F 2']]
    else:
        answers = [question_row['RISPOSTA 1'], question_row['RISPOSTA 2'], question_row['RISPOSTA 3']]
        correct_flags = [question_row['V/F 1'], question_row['V/F 2'], question_row['V/F 3']]

    st.subheader(topic)
    st.write(f"**{question}**") # Scrivere in grossetto con **
    selected_answer = st.radio('Seleziona una risposta:', answers, key=f"radio_{st.session_state['question_number']}") # radio button only one correct

    if st.button('Invia risposta'): # Pulsante di invio
        # Verifica della correttezza della risposta
        correct_index = correct_flags.index('V')  # Trova l'indice della risposta corretta
        if selected_answer == answers[correct_index]:
            st.success('Risposta corretta!')
            st.session_state['score'][tema] += 1
            st.session_state['question_number'][tema] += 1
        else:
            st.error('Risposta errata.')
            st.session_state['question_number'][tema] += 1
            st.write(f'La risposta corretta è: {answers[correct_index]}')
    st.write(f"Punteggio attuale: {sum(st.session_state['score'].values())} su {sum(st.session_state['question_number'].values())}")

# Pagine Grafici risultati
with results_tab:
    scores = st.session_state['score']
    totals = st.session_state['question_number']
    chart_data = [] # Prepara i dati per il grafico
    for category, score in scores.items():
        total = totals.get(category, 0)
        chart_data.append({'Categoria': category, 'Successi': score, 'Totale': total})
    df = pd.DataFrame(chart_data)
    # Crea il grafico a barre con st.bar_chart https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart
    st.bar_chart(df, x="Categoria", y=["Successi", "Totale"], horizontal=True, stack=False, x_label='results')