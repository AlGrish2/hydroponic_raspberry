# hydroponic_raspberry

# Build

1. Create `.env` file
2. Create environment variables

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- VIDEOS_BUCKET - bucket name with raw videos created by VideoMaker
- PROCESSED_VIDEOS_BUCKET - bucket name with videos processed by the VideoRecognizer

3. Installing libraries

```pip install -r requirements.txt```


# How to run

```python3 app.py run-app```

```python app.py run-video --video_path=test.mp4```

# Scheduling
1. ```crontab -e```
2. insert the following line, change the word interval  to intended interval between runs
- */interval * * * * cd /home/algrish/hydroponic_raspberry && python3 app.py run-app >> /home/algrish/hydroponic_raspberry/log.txt 2>&1