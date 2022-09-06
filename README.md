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
```pip install git+https://github.com/adafruit/Adafruit_Python_ADS1x15.git```


# How to run

```python app.py run-app```

```python app.py run-video --video_path=test.mp4```