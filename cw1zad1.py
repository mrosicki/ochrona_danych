from flask import Flask, render_template, request

app = Flask(__name__, template_folder='.')

polish_chars_by_freq = 'aioeznrwstcykdpmujlbghfqvx'

correct_key = 'aeioznlscrywtkmdpjubghf'


def letters_by_freq(message):
    message = message.replace('\n','').replace(' ', '')
    letters_dict = dict.fromkeys(message, 0)
    for letter in message:
        letters_dict[letter]+=1
    
    if ' ' in letters_dict:
        letters_dict.pop(' ')

    letters_dict_sorted = {k: v for k, v in sorted(letters_dict.items(), key=lambda item: item[1], reverse=True)}

    letters_freq = ''
    for key in letters_dict_sorted.keys():
        letters_freq+=key
    return letters_freq

def digrams_by_freq(message):
    message = message.replace('\n','')
    digram_dict = {}
    for i in range(len(message)-1):
        digram = message[i] + message[i+1]
        if ' ' in digram:
            continue
        if digram in digram_dict:
            digram_dict[digram] +=1
        else:
            digram_dict[digram] = 0
    digram_dict_sorted = {k: v for k, v in sorted(digram_dict.items(), key=lambda item: item[1], reverse=True)}

    digram_freq = ''
    for key in digram_dict_sorted.keys():
        digram_freq+=key
    return digram_freq

def decode_message(from_key, to_key, message):
    zipped = zip(from_key, to_key)
    switch_dict = dict(zipped)
    decoded_message = ''
    for letter in message:
        if letter in switch_dict:
            decoded_message+=switch_dict[letter]
        else:
            decoded_message+=letter
    return decoded_message

@app.route('/',  methods=['post', 'get'])
def main():
    if request.method == 'POST':
        from_value = request.form.get('from_key')
        to_value = request.form.get('to_key')
        message_chars_by_freq = request.form.get('message_chars_by_freq')  
        coded_message = request.form.get('coded_message')
        decoded_message = request.form.get('decoded_message')
        from_set = set(from_value)
        to_set = set(to_value)

        if 'decode' in request.form:
            decoded_message = decode_message(from_value, to_value, coded_message)
        else:
            message_chars_by_freq = letters_by_freq(coded_message)
        errors = []

        if len(from_set) != len(from_value) or len(to_set) != len(to_value):
            errors.append("Klucze dekodujące nie mogą posiadać duplikatów.")
        if len(from_value) != len(to_value):
            errors.append("Klucze dekodujące są różnych długości.")

        return render_template(
            'cw1zad1.html',
            coded_message=coded_message,
            decoded_message=decoded_message,
            from_key=from_value,
            to_key=to_value,
            polish_chars_by_freq=polish_chars_by_freq,
            message_chars_by_freq=message_chars_by_freq,
            errors=errors
        )
    return render_template(
        'cw1zad1.html',
        coded_message='',
        decoded_message='',
        from_key='',
        to_key='',
        polish_chars_by_freq=polish_chars_by_freq,
        message_chars_by_freq=''
    )

app.run(debug=True)