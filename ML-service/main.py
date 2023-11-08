import nemo.collections.asr as nemo_asr
golos_model = nemo_asr.models.EncDecCTCModel.restore_from(restore_path="QuartzNet15x5_golos.nemo.gz", map_location="cpu")
audio_dir = "1.wav"

transcription = golos_model.transcribe([audio_dir])
print(transcription)