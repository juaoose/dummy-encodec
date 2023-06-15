import io
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

    contents = file.file.read()

    # Load and pre-process the audio waveform
    wav, sr = torchaudio.load(io.BytesIO(contents))
    wav = convert_audio(wav, sr, model.sample_rate, model.channels)

    # We should be able to use lm, if we run on GPU
    audio_bytes = compress(model, wav, True)

    with open("test.ecdc", 'wb') as f:
        f.write(audio_bytes)

    # TODO(juaoose): might want to use StreamingResponse
    # once we support chunked encoding
    return FileResponse("test.ecdc")
