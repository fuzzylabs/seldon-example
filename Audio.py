import io
import pickle
import numpy as np
import librosa
import soundfile
import base64


def spectrogram_from_samples(samples):
    X = librosa.stft(samples)
    return librosa.amplitude_to_db(abs(X))


def wav_bytes_to_spectrogram(input_bytes: bytes):
    samples, _ = librosa.load(soundfile.SoundFile(io.BytesIO(input_bytes)))
    return spectrogram_from_samples(samples)


def prep_spectrogram(spectrogram: np.array, new_timesteps: int = None) -> np.array:
    # Pad the values of X with 0s up to the given time steps
    if new_timesteps is None:
        return spectrogram
    return np.pad(spectrogram, [(0, 0), (0, new_timesteps - spectrogram.shape[1])], constant_values=(0,)).T


class Model:
    def __init__(self):
        with open("model.pickle", "rb") as file:
            self._model = pickle.loads(file.read())

    def predict(self, X: str):
        return self._model(prep_spectrogram(wav_bytes_to_spectrogram(base64.b64decode(X)), 200))
