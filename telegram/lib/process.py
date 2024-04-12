import os
import requests
from openai import OpenAI
import soundfile as sf
import numpy as np
from dotenv import load_dotenv
import os

client = OpenAI(api_key = os.getenv("OPENAI_API"))
modelo = "gpt-4-turbo"
prompt = 'Genera únicamente una lista con tres puntos clave de la información sobre '
audio_format = "mp3"
final_folder = "audios"

def generate_list(topic):
    response = client.chat.completions.create(
    model= modelo,
    messages=[
        {"role": "system", "content": prompt + topic},
    ]
    )
    resultado = response.choices[0].message.content.split("\n")
    bullet_list = [valor for valor in resultado if valor != ""]
    print(bullet_list)
    return bullet_list

def sub_summary(sentence):
    response = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": f"Genera un resumen extenso basado en este tema en forma de conversación de dos personas de nombre Juan y María: {sentence}"},
        ]
        )
    subtext = f'\n{response.choices[0].message.content}'
    print(subtext)
    return subtext

def create_meta_summary(bullet_list):
    meta_summary = ''
    for sentence in bullet_list:
        subtext = sub_summary(sentence)
        meta_summary += subtext
    return meta_summary

def texto_a_voz_openai(text_input, output_filename, voice, output_folder="audios", model="tts-1"):
    # Crear la solicitud para la síntesis de voz
    try:
        response = client.audio.speech.create(model=model, input=text_input, voice=voice)
    except Exception as e:
        raise Exception(f"Error al comunicarse con la API de OpenAI: {e}")

    file_path = os.path.join(output_folder, output_filename)
    # Escribir el archivo de salida
    try:
        with open(file_path, "wb") as f:
            response.write_to_file(file_path)
    except IOError as e:
        raise IOError(f"No se pudo escribir el archivo de salida: {e}")

def separar_por_orador(texto, user_id):
    texto =  texto.split("\n")
    for i in range(len(texto)):
        frase = texto[i].split(":")
        # check if folder exists, if not create
        if not os.path.exists(final_folder + "/" + user_id):
            os.makedirs(final_folder + "/" + user_id)
        filename = f"{user_id}/audio{'0'*(5-len(str(i)))}{i}.{audio_format}"
        if "María" in frase[0]:
            texto_a_voz_openai(text_input=frase[1], voice="nova",
                               output_filename=filename)
        elif "Juan" in frase[0]:
            texto_a_voz_openai(text_input=frase[1], voice="echo",
                                output_filename=filename)

def combinar_audios(carpeta_entrada, archivo_salida):
    try:
        archivos_audio = [archivo for archivo in os.listdir(carpeta_entrada) if archivo.endswith(f".{audio_format}")]
        if not archivos_audio:
            print("No se encontraron archivos de audio en la carpeta.")
            return
        # Ordenar los archivos de audio por nombre
        archivos_audio.sort()

        # Leer y combinar los archivos de audio
        audio_combinado = np.array([])
        for archivo in archivos_audio:
            ruta_archivo = os.path.join(carpeta_entrada, archivo)
            audio, samplerate = sf.read(ruta_archivo)
            if audio_combinado.size == 0:
                audio_combinado = audio
            else:
                audio_combinado = np.concatenate((audio_combinado, audio))

        # Escribir el archivo de audio combinado
        sf.write(archivo_salida, audio_combinado, samplerate)
        print(f"Se ha combinado correctamente {len(archivos_audio)} archivos de audio en '{archivo_salida}'.")
    except Exception as e:
        print("Error al combinar los archivos de audio:", e)

def limpiar_carpetas(carpeta_1):
    try:
        # Limpiar la primera carpeta
        for archivo in os.listdir(carpeta_1):
            ruta_archivo = os.path.join(carpeta_1, archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
        print("Carpetas limpiadas exitosamente.")
    except Exception as e:
        print("Error al limpiar carpetas:", e)

def run(topic, user_id):
    if not os.path.exists(final_folder):
            os.makedirs(final_folder)
    audio_dir = f'{topic}.{audio_format}'
    bullet_list = generate_list(topic)
    script = create_meta_summary(bullet_list)
    separar_por_orador(script, user_id)
    combinar_audios(os.path.join(final_folder + "/" + user_id), audio_dir)
    limpiar_carpetas(final_folder)
    return audio_dir