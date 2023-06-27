from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

engini = pyttsx3.init()
voices = engini.getProperty('voices')
engini.setProperty('voices', voices[0].id)
activationWord = 'computer'

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome"
webbrowser.register(chrome_path, None, webbrowser.BackgroundBrowser(chrome_path))

appId = '5R49J7-J888YX9J2V'
wolframClient = wolframalpha.Client(appId)


def speak(text, rate = 120):
    engini.setProperty('rate', rate)
    engini.say(text)
    engini.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print('Listener a command')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('Recognizer speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print('The input speech was: {query}')

    except Exception as exception:
        print('I did not quit catch that')
        speak('I did not quit catch that')
        print(exception)
        return 'None'
    return query

def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No wikipedia result')
        return 'No wikipedia recevid'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikkiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def ListorDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    
    else:
        return var['plaintext']

def search_wolframlApha(query = ''):
    response = wolframClient.query(query)

    if response['@success'] == 'false':
        return 'Cold not computer'
    
    else:
        result = ''
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]

        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ("definition" in pod1['@title'].lower()):
            result = ListorDict(pod1['subpod'])
            return result.split('(')[0]
        
        else:
            question = ListorDict(pod0['subpod'])
            return question.split('(')

            speak('Computetion fieled. Querying the universal databank.')
            return search_wikipedia(question)

if __name__ == '__main__':
    speak('All system normal')

    while True:
        query = parseCommand().lower().split()
        
        if query[0] == activationWord:
            query.pop(0)

        if query[0] == 'say':
            if 'hello' in query:
                speak('Greetings all.')
            else:
                query.pop(0)
                speech = ' '.join(query)
                speak(speech)

        if query[0] == 'go' and query[1] == 'to':
            speak('Opening..')
            query = ' '.join(query[2:])
            webbrowser.get('chrome').open_new(query)
        
        if query[0] == "wikipedia":
            query = ' '.join(query[1:])
            speak('Querying the universal databank.')
            speak(search_wikipedia(query))

        if query[0] == 'compute' or query[0] == 'computer':
            query = ' '.join(query[1:])
            speak('Computing.')
            try:
                result = search_wolframlApha(query)
                speak(result)
            except:
                speak('Unable to compute')


        if query[0] == 'log':
            speak('Ready to record your note')
            newNote = parseCommand().lower()
            now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            with open('note_%s.txt' % now, 'w') as newFile:
                newFile.write(newNote)
            speak('Now written')

        if query[0] == 'exit':
            speak('Goodbye')
            break