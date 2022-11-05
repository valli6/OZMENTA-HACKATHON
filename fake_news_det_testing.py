import pandas as pd
import pyttsx3
import speech_recognition as sr
engine=pyttsx3.init('sapi5')
def speaking(news_audio):
    engine.say(news_audio)
    engine.runAndWait()
engine.runAndWait()
dataframe = pd.read_csv('news.csv')
x = dataframe['text']
y = dataframe['label']
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=0)
tfvect = TfidfVectorizer(stop_words='english',max_df=0.7)
tfid_x_train = tfvect.fit_transform(x_train)
tfid_x_test = tfvect.transform(x_test)
classifier = PassiveAggressiveClassifier(max_iter=50)
classifier.fit(tfid_x_train,y_train)
y_pred = classifier.predict(tfid_x_test)
score = accuracy_score(y_test,y_pred)
#print(f'Accuracy: {round(score*100,2)}%')
cf = confusion_matrix(y_test,y_pred, labels=['FAKE','REAL'])
def fake_news_det(news):
    input_data = [news]
    vectorized_input_data = tfvect.transform(input_data)
    prediction = classifier.predict(vectorized_input_data)
    print(prediction)
    beat_list=['beat','bet']
    if news in beat_list:
        print('FAKE')
        speaking("It is fake")
    if prediction[0]=='FAKE':
        print("Sorry your news is fake")
        speaking(" Sorry  your  news  is  fake")
    else:
        speaking("Your news is true")
        print("your news is true and it's accuracy is  ",round(score*100,2))
import pickle
#pickle.dump(classifier,open('model.pkl', 'wb'))
loaded_model = pickle.load(open('model.pkl', 'rb'))
def fake_news_det1(news):
    input_data = [news]
    vectorized_input_data = tfvect.transform(input_data)
    prediction = loaded_model.predict(vectorized_input_data)
    print(prediction)
speaking("How would you want your input type speech or text: ")
typing_or_sr_condition=input("How would you want your input type (speech/text): ")
speech_word_match_list=['speech','SPEECH','spee','spe','sp','speach']
type_word_match_list=['text',"TEXT",'tex','te']
if typing_or_sr_condition in speech_word_match_list:
    speaking("How many news do you want to find the news is real or fake")
    counts = int(input("How many news do you want to find the news is real or fake:"))
    r=sr.Recognizer()
    with sr.Microphone() as source:
        speaking("Say your news to find that news is fake or not ")
        audio=r.listen(source)
        try:
            news=r.recognize_google(audio)
            fake_news_det(news)
        except sr.UnknownValueError:
            speaking("Could not understand audio say that again please")
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
elif typing_or_sr_condition in type_word_match_list:
    try:
        speaking("How many news do you want to find the news is real or fake ")
        counts = int(input("How many news do you want to find the news is real or fake:"))
        for i in range(counts):
            speaking("Enter your news to find it is fake or real ")
            news_ = str(input("Enter your news to find it is fake or real:"))
            fake_news_det(news_)
    except :
        speaking("Sorry enter the valid input ")
        print("Sorry enter the valid input")
else:
    speaking("please text the exact input")
    print("please text the exact input")