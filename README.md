#Word Translate


##Description
This microservice takes a word from any given language, and translates it to another. For exact use, you can check the api Swagger documentation at: localhost:8000/docs/

##Improvements

There are three main improvement points for this project, first:

- The official Google API wasn't freely available, and web-scraping is not a good practice for these kind of tasks, so I used the googletrans free API package. With this, I could access the translations, but only provide a single example and definition, and no synonyms. If I had access to the paid API, this can easily be solved.
- Second, please kindly note that this was my first time ever using FastAPI. I mainly used Flask before, and while they are similar, and I tried to follow FastAPI best practices, they are not the same.
- Unit tests should still be added, but according to the time constraints I was given, I prioritized finishing the task first.


###Running it with docker compose:
I added a dummy_env.txt file, you should change that to .env (it's just a bad practice to include .env in the repo)

- Build the docker compose with:
    ```
    docker compose build
    ```
  
- Run the docker compose with:
    ```
    docker compose up
    ```
