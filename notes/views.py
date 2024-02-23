from django.shortcuts import render
from youtube_transcript_api import YouTubeTranscriptApi
import os
from pytube import extract
import openai

def about(request):
    return render(request, 'notes/about.html')

def contact(request):
    return render(request, 'notes/contact.html')

def index(request):
    if request.method == 'POST':
        try:
            link = request.POST.get('link')
            print(link) 
            url=extract.video_id(str(link))
            srt = YouTubeTranscriptApi.get_transcript(url)
            
            prompt = "start by giving a heading of the notes after that explain context of the youtube video from the given text in less than 15 points also highlight important points as bold text and if text is too small then return less points  ,in case theres no propper information then return that provide link of the video which has more info there's info is too short but dont mention text insted call it link , or length of information is too long the return small amount of data and return small info but answer should be in points and also bold the important text"
            for i in srt:
                prompt += i["text"] + " "
            print(len(prompt))
            if len(prompt)>5000: 
                prompt = prompt[:5000]
            print(len(prompt))
            openai.api_key = 'YOUR_API_KEY'

            def generate_response(prompt):
                model_engine = "text-davinci-003"
                prompt = (f"{prompt}")

                completions = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )

                message = completions.choices[0].text
                print(message.strip())
                return message.strip()

            response = generate_response(prompt)
            return render(request, 'notes/index.html',{'link': response})
       
        except Exception as e:
            return render(request, 'notes/index.html', {'link': ' Oh no! Error. The API key has expired😞'})

    return render(request, 'notes/index.html')
