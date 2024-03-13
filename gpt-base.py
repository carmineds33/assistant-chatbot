import streamlit as st
import openai
from keysX import GPT_API_KEY, GPT_ASSISTANT_KEY
import time

# Configura il client OpenAI con la tua API key
openai.api_key = GPT_API_KEY

# Funzione per creare ed eseguire una richiesta all'assistente OpenAI
def submit_to_openai(query):
    client = openai.OpenAI(api_key=GPT_API_KEY)

    # Crea un assistente se non hai già un GPT_ASSISTANT_KEY specifico
    # Nel tuo caso, sembra che tu abbia già un assistente specifico, quindi lo recupero.
    my_assistant = client.beta.assistants.retrieve(GPT_ASSISTANT_KEY)

    # Crea un thread con un messaggio
    thread = client.beta.threads.create(
        messages=[
            {"role": "user", "content": query}
        ]
    )

    # Invia il thread all'assistente (come una nuova esecuzione)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=GPT_ASSISTANT_KEY)
    
    # Aspetta il completamento dell'esecuzione
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)  # Evita di fare polling troppo frequente

    # Ottieni l'ultimo messaggio dal thread
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    # Ritorna l'ultimo messaggio
    return messages[0].content[0].text.value  # Assicurati che questa parte corrisponda a come vuoi che venga estratto il messaggio

# Interfaccia Streamlit
st.title('Assistente GPT con documenti NAR')

# Campo di input per la query
user_query = st.text_input("Inserisci la tua richiesta:", "") #"Parlami del caso di nuova richiesta da LR a OMr"

# Bottone per inviare la richiesta
if st.button('Invia Richiesta a OpenAI'):
    with st.spinner('Invio in corso...'):
        response = submit_to_openai(user_query)
        st.success('Risposta ricevuta!')
        st.write(response)
