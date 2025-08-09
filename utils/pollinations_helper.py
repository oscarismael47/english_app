import requests
import urllib.parse
import os
import uuid
import json
import base64
from datetime import datetime
from PIL import Image
import time
import sseclient  # pip install sseclient-py

class PollinationsHandler:
    def __init__(self, image_save_dir="generated_images", audio_save_dir="generated_audio"):
        self.image_save_dir = image_save_dir
        self.audio_save_dir = audio_save_dir
        os.makedirs(self.image_save_dir, exist_ok=True)
        os.makedirs(self.audio_save_dir, exist_ok=True)

    def generate_audio(self, text, voice="echo", filename=None):
        encoded_text = urllib.parse.quote(text)
        url = f"https://text.pollinations.ai/{encoded_text}"
        params = {
            "model": "openai-audio",
            "voice": voice
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            if 'audio/mpeg' in response.headers.get('Content-Type', ''):
                if filename is None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"audio_{timestamp}.mp3"
                audio_path = os.path.join(self.audio_save_dir, filename)
                with open(audio_path, 'wb') as f:
                    f.write(response.content)
                print(f"Audio saved successfully as {audio_path}")
                return audio_path
            else:
                print("Unexpected content type received instead of audio.")
                print(f"Content-Type: {response.headers.get('Content-Type')}")
                print("Response preview:", response.text[:200])
                return None
        except requests.exceptions.RequestException as e:
            print(f"Audio generation failed: {e}")
            return None

    def generate_image(self, prompt, width=1280, height=720, seed=42, model="flux",
                       nologo=None, transparent=None, image=None, referrer=None):
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        params = {
            "width": width,
            "height": height,
            "seed": seed,
            "model": model,
        }
        if nologo:
            params["nologo"] = "true"
        if transparent:
            params["transparent"] = "true"
        if image:
            params["image"] = image
        if referrer:
            params["referrer"] = referrer

        try:
            response = requests.get(url, params=params, timeout=300)
            response.raise_for_status()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"img_{timestamp}.jpg"
            image_path = os.path.join(self.image_save_dir, filename)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Image saved as {image_path}")
            return image_path
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image: {e}")
            return None

    def generate_text(self, prompt, model="openai", seed=42, json_output=False, system=None, referrer=None):
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://text.pollinations.ai/{encoded_prompt}"
        params = {
            "model": model,
            "seed": seed,
        }
        if json_output:
            params["json"] = "true"
        if referrer:
            params["referrer"] = referrer
        if system:
            params["system"] = system
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            if json_output:
                try:
                    data = json.loads(response.text)
                    print("Response (JSON parsed):", data)
                    return data
                except json.JSONDecodeError:
                    print("Error: Invalid JSON received.")
                    print("Raw response:", response.text)
                    return None
            else:
                print("Response (Plain Text):")
                print(response.text)
                return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching text: {e}")
            return None

    def transcribe_audio(self, audio_path, question="Transcribe this audio"):
        url = "https://text.pollinations.ai/openai"
        headers = {"Content-Type": "application/json"}
        try:
            with open(audio_path, "rb") as audio_file:
                base64_audio = base64.b64encode(audio_file.read()).decode("utf-8")
        except FileNotFoundError:
            print(f"Error: Audio file not found at {audio_path}")
            return None

        audio_format = audio_path.split(".")[-1].lower()
        if audio_format not in ["mp3", "wav"]:
            print(f"Unsupported audio format '{audio_format}'. Only mp3 and wav are supported.")
            return None

        payload = {
            "model": "openai-audio",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": base64_audio,
                                "format": audio_format
                            }
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            transcription = result.get("choices", [{}])[0].get("message", {}).get("content")
            return transcription
        except requests.exceptions.RequestException as e:
            print(f"Error transcribing audio: {e}")
            return None

    def analyze_image(self, image_path=None, image_url=None, question="What's in this image?"):
        url_api = "https://text.pollinations.ai/openai"
        headers = {"Content-Type": "application/json"}

        if image_url:
            content = [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        elif image_path:
            try:
                with open(image_path, "rb") as img_file:
                    base64_image = base64.b64encode(img_file.read()).decode("utf-8")
            except FileNotFoundError:
                print(f"Error: Image not found at {image_path}")
                return None

            image_format = image_path.split(".")[-1].lower()
            if image_format not in ['jpeg', 'jpg', 'png', 'gif', 'webp']:
                print(f"Warning: Unsupported format '{image_format}'. Assuming jpeg.")
                image_format = "jpeg"

            content = [
                {"type": "text", "text": question},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{image_format};base64,{base64_image}"
                    }
                }
            ]
        else:
            print("Error: Either image_path or image_url must be provided.")
            return None

        payload = {
            "model": "openai",
            "messages": [{"role": "user", "content": content}],
            "max_tokens": 500
        }

        try:
            response = requests.post(url_api, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content")
        except requests.exceptions.RequestException as e:
            print(f"Error analyzing image: {e}")
            return None


# Dentro de la clase PollinationsHandler:
    def stream_text(self, prompt, model="openai", system=None):
        """
        Stream real-time text generation using Server-Sent Events (SSE).
        """
        url = "https://text.pollinations.ai/openai"
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }

        messages = [{"role": "user", "content": prompt}]
        if system:
            messages.insert(0, {"role": "system", "content": system})

        payload = {
            "model": model,
            "messages": messages,
            "stream": True
        }

        try:
            response = requests.post(url, headers=headers, json=payload, stream=True)
            response.raise_for_status()
            client = sseclient.SSEClient(response)

            full_response = ""
            print("Streaming response:\n")
            for event in client.events():
                if event.data:
                    if event.data.strip() == "[DONE]":
                        print("\nStream finished.")
                        break
                    try:
                        chunk = json.loads(event.data)
                        content = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
                        if content:
                            print(content, end="", flush=True)
                            full_response += content
                    except json.JSONDecodeError:
                        print(f"\nInvalid chunk: {event.data}")

            print("\n--- End of Stream ---")
            return full_response

        except requests.exceptions.RequestException as e:
            print(f"\nError during streaming request: {e}")
            return None
        except Exception as e:
            print(f"\nError processing stream: {e}")
            return None

if __name__ == "__main__":
    handler = PollinationsHandler()

    print("\n📸 Generando imagen...")
    image_path = handler.generate_image("A futuristic city with flying cars in 60's", model="flux")
    print(f"Ruta imagen: {image_path}")

    print("\n🔊 Generando audio...")
    audio_path = handler.generate_audio("Hello, this is a test of audio generation.", voice="echo")
    print(f"Ruta audio: {audio_path}")

    print("\n📖 Generando texto...")
    text_response = handler.generate_text(
        prompt="What is quantum computing?",
        system="Explain in simple terms.",
        json_output=False
    )
    print(f"Texto generado:\n{text_response}")

    print("\n📝 Transcribiendo audio...")
    audio_path = r"generated_audio\audio_20250808_114623.mp3"
    if audio_path:
        transcript = handler.transcribe_audio(audio_path)
        print(f"Transcripción:\n{transcript}")

    print("\n🔍 Analizando imagen local...")
    if image_path:
        analysis_local = handler.analyze_image(image_path=image_path, question="What do you see in this image?")
        print(f"Análisis de imagen local:\n{analysis_local}")

    print("\n🌐 Analizando imagen por URL...")
    url_img = "https://html.com/wp-content/uploads/flamingo.jpg"
    analysis_url = handler.analyze_image(image_url=url_img, question="What animal is this?")
    print(f"Análisis de imagen por URL:\n{analysis_url}")

    print("\n💬 Texto en streaming (SSE)...")
    streamed_text = handler.stream_text("Tell me a story about a robot who learns emotions.")
    print(f"\nTexto completo (streamed):\n{streamed_text}")
