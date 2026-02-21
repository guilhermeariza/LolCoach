# LolCoach - AI Voice Coach para League of Legends

Assistente de coaching por voz que roda em background durante suas partidas. 100% hands-free, seguro para uso com Riot Vanguard (sem hooks de teclado, sem injeção de memória).

## Como Funciona

| Comando | Wake Word | Ação |
|---------|-----------|------|
| Dica rápida | "Computer" | Captura a tela → Gemini analisa → Resposta em áudio |
| Pergunta específica | "Jarvis" | Grava sua pergunta → Captura tela → Gemini responde em áudio |

## Pré-requisitos

- Python 3.10+
- Microfone funcional
- Fone de ouvido (para não criar feedback de áudio)
- Sistema operacional: Windows 10/11 ou Linux

### Dependência de sistema (PyAudio)

**Windows:**
```bash
pip install pyaudio
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

## Configuração

### 1. Clonar o repositório

```bash
git clone https://github.com/guilhermeariza/LolCoach.git
cd LolCoach
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Obter as chaves de API

Você precisa de 3 chaves de API (todas possuem tier gratuito):

#### Picovoice (Porcupine Wake Word)
1. Acesse [https://console.picovoice.ai/](https://console.picovoice.ai/)
2. Crie uma conta gratuita
3. Na dashboard, copie sua **AccessKey**
4. O plano gratuito permite até 3 wake words e uso ilimitado para desenvolvimento

#### Google Gemini
1. Acesse [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. O plano gratuito inclui 15 requisições por minuto no Gemini 1.5 Flash

#### OpenAI (Whisper + TTS)
1. Acesse [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Crie uma conta e adicione créditos (mínimo $5)
3. Gere uma nova API key
4. Whisper: ~$0.006/minuto | TTS: ~$0.015/1000 caracteres

### 5. Configurar o arquivo .env

```bash
cp .env.example .env
```

Edite o `.env` com suas chaves:

```
PICOVOICE_ACCESS_KEY=sua_chave_picovoice_aqui
GEMINI_API_KEY=sua_chave_gemini_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 6. Gerar os sons de feedback

```bash
python generate_beeps.py
```

## Uso

```bash
python main.py
```

### Durante a partida:

- **Diga "Computer"** → Você ouve um bip curto, a tela é capturada, e em poucos segundos o coach fala uma dica rápida sobre o que focar.

- **Diga "Jarvis"** → Você ouve um bip duplo, o microfone grava por 6 segundos. Faça sua pergunta (ex: "Devo fazer o Baron agora?"). A tela é capturada, e o coach responde sua pergunta específica.

- **Ctrl+C** para encerrar.

## Estrutura do Projeto

```
LolCoach/
├── main.py              # Ponto de entrada - orquestra tudo
├── config.py            # Configuração e variáveis de ambiente
├── wake_word.py         # Detecção de wake words (Porcupine)
├── screen_capture.py    # Captura de tela (mss)
├── audio_recorder.py    # Gravação de microfone (sounddevice)
├── stt.py               # Speech-to-Text (OpenAI Whisper)
├── ai_coach.py          # Análise de IA (Google Gemini)
├── tts.py               # Text-to-Speech + reprodução (OpenAI TTS + pygame)
├── generate_beeps.py    # Gerador de sons de feedback
├── sounds/              # Arquivos de beep gerados
├── requirements.txt     # Dependências Python
├── .env.example         # Template de configuração
└── .gitignore
```

## Segurança (Riot Vanguard)

Esta aplicação é segura para uso com o Riot Vanguard porque:

- **Não utiliza hooks de teclado** — sem `keyboard`, `pynput`, ou qualquer biblioteca que intercepte input do sistema
- **Não injeta memória** — não lê nem modifica a memória do processo do jogo
- **Não automatiza input** — não envia nenhum comando de teclado ou mouse para o jogo
- **Captura de tela via mss** — usa a API padrão do sistema operacional (mesma usada por OBS, Discord, etc.)
- **Apenas escuta o microfone** — a única interação com hardware é a leitura passiva do microfone

A aplicação funciona de forma completamente independente do cliente do jogo.
