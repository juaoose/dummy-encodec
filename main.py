import requests
import torch
import torchaudio

from encodec import EncodecModel
from encodec.utils import convert_audio
from encodec.compress import compress

# Instantiate a pretrained EnCodec model
model = EncodecModel.encodec_model_48khz()
# The number of codebooks used will be determined bythe bandwidth selected.
# E.g. for a bandwidth of 6kbps, `n_q = 8` codebooks are used.
# Supported bandwidths are 1.5kbps (n_q = 2), 3 kbps (n_q = 4), 6 kbps (n_q = 8) and 12 kbps (n_q =16) and 24kbps (n_q=32).
# For the 48 kHz model, only 3, 6, 12, and 24 kbps are supported. The number
# of codebooks for each is half that of the 24 kHz model as the frame rate is twice as much.
model.set_target_bandwidth(6.0)

# Load and pre-process the audio waveform
wav, sr = torchaudio.load("sample.wav")
wav = convert_audio(wav, sr, model.sample_rate, model.channels)

# Do not use large model
audio_bytes = compress(model, wav, False)

with open("test.ecdc", 'wb') as f:
    f.write(audio_bytes)