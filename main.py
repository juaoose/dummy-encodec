import torchaudio
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from encodec import EncodecModel
from encodec.compress import compress
from encodec.utils import convert_audio

model = EncodecModel.encodec_model_48khz()
model.set_target_bandwidth(6.0)

app = FastAPI()


@app.post("/")
def encode(file: UploadFile = File(...)):

    # Load and pre-process the audio waveform
    wav, sr = torchaudio.load(file.filename)
    wav = convert_audio(wav, sr, model.sample_rate, model.channels)

    # Do not use large model
    audio_bytes = compress(model, wav, False)

    with open("test.ecdc", 'wb') as f:
        f.write(audio_bytes)

    return FileResponse("test.ecdc")
