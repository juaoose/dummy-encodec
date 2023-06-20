import io

import torch
import torchaudio
from encodec.compress import compress
from encodec.utils import convert_audio
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from encodec import EncodecModel

# HQ model
model = EncodecModel.encodec_model_48khz()
model.set_target_bandwidth(6.0)

# Check for GPU access
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = FastAPI()


@app.post("/")
def encode(file: UploadFile = File(...)):

    contents = file.file.read()

    # Load and pre-process the audio waveform
    wav, sr = torchaudio.load(io.BytesIO(contents))

    # Is this how you do it? https://github.com/mimbres/encodec/blob/main/encodec/compress.py#L168
    model.to(device)
    wav = wav.to(device)

    wav = convert_audio(wav, sr, model.sample_rate, model.channels)

    audio_bytes = compress(model, wav, False)

    with open("test.ecdc", 'wb') as f:
        f.write(audio_bytes)

    # TODO(juaoose): might want to use StreamingResponse
    # once we support chunked encoding
    return FileResponse("test.ecdc", media_type="application/octet-stream", filename="response.ecdc")
