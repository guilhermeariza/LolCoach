# LolCoach — AI Voice Coach para League of Legends

Um assistente de coaching por voz que roda em background durante suas partidas de League of Legends. Totalmente **hands-free**: você fala, ele analisa sua tela e responde no seu fone de ouvido.

100% seguro para uso com **Riot Vanguard** — sem hooks de teclado, sem injeção de memória, sem automação de input.

---

## Sumário

- [Como Funciona](#como-funciona)
- [Demonstração de Uso](#demonstração-de-uso)
- [Pré-requisitos](#pré-requisitos)
- [Instalação Passo a Passo](#instalação-passo-a-passo)
- [Obtendo as Chaves de API](#obtendo-as-chaves-de-api)
- [Configuração do .env](#configuração-do-env)
- [Executando](#executando)
- [Exemplos de Uso em Partida](#exemplos-de-uso-em-partida)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Arquitetura e Fluxos](#arquitetura-e-fluxos)
- [Estimativa de Custo](#estimativa-de-custo)
- [Resolução de Problemas](#resolução-de-problemas)
- [Segurança — Riot Vanguard](#segurança--riot-vanguard)

---

## Como Funciona

O LolCoach escuta seu microfone continuamente usando detecção de **wake words** offline (Porcupine). Quando você diz uma das palavras de ativação, ele executa um dos dois fluxos:

| Wake Word | Função | O que acontece |
|-----------|--------|----------------|
| **"Computer"** | Dica rápida | Captura a tela → Gemini analisa o estado do jogo → Resposta em áudio no fone |
| **"Jarvis"** | Pergunta específica | Grava sua pergunta (6s) → Captura a tela → Transcreve via Whisper → Gemini responde → Áudio no fone |

---

## Demonstração de Uso

```
=======================================================
  LolCoach - AI Voice Coach para League of Legends
=======================================================

  Diga "Computer" para uma dica rápida.
  Diga "Jarvis" + sua pergunta para análise específica.
  Pressione Ctrl+C para sair.

[WAKE] Escutando wake words... (Diga 'Computer' ou 'Jarvis')
[WAKE] Detectado: "computer"
[FLOW] Capturando tela...
[FLOW] Enviando para Gemini...
[GEMINI] Dica: Foca no farm, você tá 20 CS atrás. Não troque agora.
[FLOW] Gerando áudio...
[FLOW] Dica reproduzida com sucesso.
```

---

## Pré-requisitos

- **Python 3.10** ou superior
- **Microfone** funcional (headset, webcam ou microfone USB)
- **Fone de ouvido** (obrigatório — evita feedback de áudio entre o TTS e o microfone)
- **Conexão com a internet** (para as APIs do Gemini, OpenAI Whisper e TTS)
- **Sistema operacional:** Windows 10/11 ou Linux (Ubuntu 20.04+)

---

## Instalação Passo a Passo

### 1. Clonar o repositório

```bash
git clone https://github.com/guilhermeariza/LolCoach.git
cd LolCoach
```

### 2. Instalar dependência de sistema (PortAudio)

O PyAudio requer a biblioteca PortAudio instalada no sistema operacional.

**Windows** — nenhuma ação necessária, o pip instala automaticamente:
```bash
pip install pyaudio
```

**Linux (Debian / Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-pyaudio
```

**macOS:**
```bash
brew install portaudio
```

### 3. Criar e ativar um ambiente virtual

```bash
python -m venv venv
```

**Windows (CMD):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Instalar as dependências Python

```bash
pip install -r requirements.txt
```

Isso instalará:

| Pacote | Versão | Função |
|--------|--------|--------|
| `pvporcupine` | >= 3.0.0 | Detecção de wake words offline |
| `pyaudio` | >= 0.2.14 | Stream de áudio para o Porcupine |
| `mss` | >= 9.0.0 | Captura de tela rápida |
| `sounddevice` | >= 0.4.6 | Gravação de microfone |
| `scipy` | >= 1.11.0 | Escrita de WAV em memória |
| `openai` | >= 1.0.0 | Whisper (STT) + TTS |
| `google-generativeai` | >= 0.5.0 | Google Gemini (visão + texto) |
| `pygame` | >= 2.5.0 | Reprodução de áudio |
| `python-dotenv` | >= 1.0.0 | Carregamento do arquivo .env |

### 5. Gerar os sons de feedback

O programa emite beeps curtos quando detecta uma wake word. Execute uma vez para gerá-los:

```bash
python generate_beeps.py
```

Isso cria dois arquivos na pasta `sounds/`:
- `beep_general.wav` — bip curto agudo (wake word "Computer")
- `beep_question.wav` — bip duplo grave-agudo (wake word "Jarvis")

---

## Obtendo as Chaves de API

Você precisa de **3 chaves de API**. As três possuem planos gratuitos ou de baixo custo.

### Picovoice (Porcupine — detecção de wake word)

1. Acesse **[https://console.picovoice.ai/](https://console.picovoice.ai/)**
2. Clique em **"Sign Up"** e crie uma conta gratuita
3. Após o login, na página principal da dashboard, você verá sua **AccessKey**
4. Copie a chave (é uma string longa começando com letras e números)

> **Plano gratuito:** uso ilimitado para desenvolvimento, até 3 wake words simultâneas. As palavras "Computer" e "Jarvis" são keywords built-in gratuitas — não é necessário treinar um modelo customizado.

### Google Gemini (análise de imagem + texto)

1. Acesse **[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. Faça login com sua conta Google
3. Clique em **"Create API Key"**
4. Selecione um projeto do Google Cloud (ou crie um novo) e confirme
5. Copie a chave gerada

> **Plano gratuito:** 15 requisições por minuto e 1.500 por dia no modelo Gemini 1.5 Flash. Mais do que suficiente para partidas — você faria no máximo ~2 requisições por minuto em uso intenso.

### OpenAI (Whisper STT + Text-to-Speech)

1. Acesse **[https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)**
2. Crie uma conta (se ainda não tem)
3. Adicione créditos na seção **Billing** (mínimo de $5, recomendado)
4. Vá em **API Keys** e clique em **"Create new secret key"**
5. Dê um nome (ex: "LolCoach") e copie a chave gerada

> **Custos estimados:**
> - Whisper (transcrição): ~$0.006 por minuto de áudio
> - TTS (geração de voz): ~$0.015 por 1.000 caracteres
> - Uma sessão típica de 40 min de jogo com ~20 comandos custa menos de **$0.05**

---

## Configuração do .env

Copie o arquivo de exemplo e edite com suas chaves:

```bash
cp .env.example .env
```

Abra o arquivo `.env` em qualquer editor de texto e preencha:

```env
# Picovoice (Porcupine Wake Word)
PICOVOICE_ACCESS_KEY=COLE_SUA_CHAVE_PICOVOICE_AQUI

# Google Gemini
GEMINI_API_KEY=COLE_SUA_CHAVE_GEMINI_AQUI

# OpenAI (Whisper STT + TTS)
OPENAI_API_KEY=COLE_SUA_CHAVE_OPENAI_AQUI
```

> **Importante:** O arquivo `.env` está no `.gitignore` e nunca será commitado. Suas chaves ficam apenas na sua máquina.

---

## Executando

Com o ambiente virtual ativo e o `.env` configurado:

```bash
python main.py
```

Você verá:

```
=======================================================
  LolCoach - AI Voice Coach para League of Legends
=======================================================

  Diga "Computer" para uma dica rápida.
  Diga "Jarvis" + sua pergunta para análise específica.
  Pressione Ctrl+C para sair.

[WAKE] Escutando wake words... (Diga 'Computer' ou 'Jarvis')
```

A partir daqui, abra o League of Legends e jogue normalmente. O LolCoach fica rodando em background.

Para encerrar, volte ao terminal e pressione **Ctrl+C**.

---

## Exemplos de Uso em Partida

### Exemplo 1 — Dica rápida (fase de rotas)

> Você está no mid lane, minuto 8, e não sabe se deve ficar farmando ou roaming.

**Você diz:** "Computer"

**LolCoach responde (no fone):** *"Empurra a wave e roama pra bot. O support inimigo tá sem flash."*

### Exemplo 2 — Pergunta sobre objetivo

> O Baron está vivo, metade do time inimigo morreu, e você não sabe se é hora.

**Você diz:** "Jarvis, a gente faz Baron agora?"

**LolCoach responde:** *"Sim, vai Baron. São 3 mortos do inimigo e o jungler deles tá sem smite."*

### Exemplo 3 — Dúvida de build

> Você está na loja e não sabe qual item comprar.

**Você diz:** "Jarvis, qual item eu faço agora?"

**LolCoach responde:** *"Fecha o Zhonya. Eles têm muito burst de AD e você tá morrendo rápido."*

### Exemplo 4 — Teamfight

> Uma teamfight está prestes a acontecer no dragão.

**Você diz:** "Computer"

**LolCoach responde:** *"Não force o fight. Espera o engage deles e foca o ADC que tá posicionado na frente."*

---

## Estrutura do Projeto

```
LolCoach/
│
├── main.py                # Ponto de entrada — orquestra todos os módulos
├── config.py              # Carrega .env, valida chaves, define constantes
├── wake_word.py           # Loop de escuta com Porcupine (detecção offline)
├── screen_capture.py      # Captura de tela via mss (em memória, sem disco)
├── audio_recorder.py      # Grava microfone via sounddevice (retorna WAV bytes)
├── stt.py                 # Transcrição de áudio via OpenAI Whisper API
├── ai_coach.py            # Envia screenshot + texto ao Google Gemini
├── tts.py                 # Converte texto em fala (OpenAI TTS) + reproduz (pygame)
├── generate_beeps.py      # Script utilitário para gerar sons de feedback
│
├── sounds/                # Sons de feedback gerados
│   ├── beep_general.wav   # Bip curto — wake word "Computer"
│   └── beep_question.wav  # Bip duplo — wake word "Jarvis"
│
├── requirements.txt       # Dependências Python
├── .env.example           # Template das chaves de API
├── .gitignore             # Ignora .env, __pycache__, venv, etc.
└── README.md              # Este arquivo
```

---

## Arquitetura e Fluxos

### Fluxo 1 — Dica Geral ("Computer")

```
Microfone (contínuo)
    │
    ▼
Porcupine detecta "Computer"
    │
    ▼
Toca beep_general.wav ──► Feedback imediato pro jogador
    │
    ▼
mss captura a tela (PNG em memória)
    │
    ▼
Gemini 1.5 Flash analisa a imagem
    │  prompt: "Me dê uma dica rápida do que focar agora (máximo 2 frases)"
    ▼
OpenAI TTS converte a resposta em áudio
    │
    ▼
pygame reproduz no fone de ouvido
```

### Fluxo 2 — Pergunta Específica ("Jarvis")

```
Microfone (contínuo)
    │
    ▼
Porcupine detecta "Jarvis"
    │
    ▼
Toca beep_question.wav ──► Feedback: "pode falar"
    │
    ▼
sounddevice grava o microfone por 6 segundos
    │
    ├──► mss captura a tela (PNG em memória)
    │
    ▼
OpenAI Whisper transcreve o áudio em texto
    │
    ▼
Gemini 1.5 Flash recebe imagem + pergunta transcrita
    │
    ▼
OpenAI TTS converte a resposta em áudio
    │
    ▼
pygame reproduz no fone de ouvido
```

### Diagrama de Módulos

```
┌──────────────────────────────────────────────────┐
│                    main.py                       │
│         (orquestra fluxos em threads)            │
├──────────┬───────────┬───────────┬───────────────┤
│          │           │           │               │
▼          ▼           ▼           ▼               ▼
wake_word  screen_     audio_      ai_coach       tts
  .py      capture     recorder      .py          .py
           .py         .py        (Gemini)     (OpenAI TTS
(Porcupine) (mss)    (sounddevice)              + pygame)
                        │
                        ▼
                      stt.py
                    (Whisper)
│                                                  │
├──────────────────────────────────────────────────┤
│                   config.py                      │
│            (.env + constantes globais)           │
└──────────────────────────────────────────────────┘
```

> Todas as chamadas de API rodam em **threads separadas** (via `threading.Thread`), garantindo que o loop de escuta do microfone nunca seja bloqueado.

---

## Estimativa de Custo

| Serviço | Custo por uso | Custo por partida (~20 comandos) |
|---------|---------------|----------------------------------|
| Picovoice (Porcupine) | Gratuito (plano dev) | $0.00 |
| Google Gemini 1.5 Flash | Gratuito (até 1.500 req/dia) | $0.00 |
| OpenAI Whisper | ~$0.006 / minuto de áudio | ~$0.01 |
| OpenAI TTS | ~$0.015 / 1.000 caracteres | ~$0.03 |
| **Total por partida** | | **~$0.04** |

> Com $5 de créditos na OpenAI, você tem aproximadamente **125 partidas** de coaching.

---

## Resolução de Problemas

### "Chaves de API faltando no .env"

Certifique-se de que:
1. O arquivo se chama `.env` (com o ponto na frente), não `env` ou `.env.example`
2. Não há espaços ao redor do `=` (ex: `GEMINI_API_KEY=abc123`, não `GEMINI_API_KEY = abc123`)
3. As chaves não estão entre aspas

### "Erro de PyAudio / PortAudio"

O PyAudio depende do PortAudio nativo do sistema. Veja a seção [Instalar dependência de sistema](#2-instalar-dependência-de-sistema-portaudio).

No Linux, se o erro persistir:
```bash
sudo apt-get install -y libasound2-dev portaudio19-dev
pip install --force-reinstall pyaudio
```

### "pvporcupine: Invalid AccessKey"

- Verifique se a `PICOVOICE_ACCESS_KEY` no `.env` está correta (sem espaços extras)
- Confirme que a chave não expirou no [console do Picovoice](https://console.picovoice.ai/)

### "Nenhum áudio é reproduzido"

- Verifique se o fone de ouvido está definido como dispositivo de saída padrão do sistema
- No Linux, pode ser necessário instalar o PulseAudio: `sudo apt-get install pulseaudio`
- Teste a saída de áudio com: `python -c "import pygame; pygame.mixer.init(); print('OK')"`

### "Wake word não é detectada"

- Fale claramente e em volume normal — "Computer" (com pronúncia em inglês) ou "Jarvis"
- O microfone deve ser o dispositivo de entrada padrão do sistema
- Verifique se outro programa não está usando o microfone exclusivamente
- A sensibilidade padrão é 0.6 (de 0 a 1). Pode ser ajustada em `wake_word.py` na linha `sensitivities=[0.6, 0.6]` — aumente para 0.8 se estiver em ambiente barulhento

### "Resposta do Gemini demora muito"

- O Gemini 1.5 Flash normalmente responde em 2-4 segundos
- Se sua conexão for lenta, o gargalo está no upload da imagem (~200-500KB por screenshot)
- Verifique sua conexão com a internet

---

## Segurança — Riot Vanguard

O Riot Vanguard é o anti-cheat a nível de kernel usado pelo League of Legends. O LolCoach foi projetado para ser **totalmente compatível**:

| O que o LolCoach faz | Risco para Vanguard |
|-----------------------|---------------------|
| Escuta o microfone via PyAudio/sounddevice | **Nenhum** — leitura passiva de áudio, igual a Discord/OBS |
| Captura de tela via `mss` | **Nenhum** — usa a API padrão do OS, igual a OBS/GeForce/Discord |
| Chama APIs externas (Gemini, OpenAI) | **Nenhum** — requisições HTTP normais |
| Reproduz áudio via pygame | **Nenhum** — saída de áudio padrão |

O que o LolCoach **NÃO** faz:

- **Não intercepta teclado/mouse** — nenhuma biblioteca como `keyboard`, `pynput` ou hooks de baixo nível
- **Não lê memória do processo** — nenhum acesso a memória do cliente do LoL
- **Não injeta código** — nenhuma DLL injection ou modificação de arquivos do jogo
- **Não automatiza input** — nenhum comando é enviado ao jogo (nenhum clique, nenhuma tecla)
- **Não modifica pacotes de rede** — nenhuma interceptação de tráfego

A aplicação funciona de forma completamente independente e externa ao cliente do jogo, assim como qualquer outro programa comum (Spotify, Chrome, Discord, etc.).

---

## Tecnologias Utilizadas

| Tecnologia | Uso no projeto |
|------------|----------------|
| [Picovoice Porcupine](https://picovoice.ai/platform/porcupine/) | Detecção de wake words offline (ultraleve, ~1% CPU) |
| [mss](https://github.com/BoboTiG/python-mss) | Captura de tela rápida sem queda de FPS |
| [sounddevice](https://python-sounddevice.readthedocs.io/) | Gravação de microfone |
| [OpenAI Whisper](https://platform.openai.com/docs/guides/speech-to-text) | Transcrição de áudio para texto (STT) |
| [Google Gemini 1.5 Flash](https://ai.google.dev/gemini-api/docs) | Análise de imagem + geração de resposta |
| [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech) | Conversão de texto em fala |
| [pygame](https://www.pygame.org/) | Reprodução de áudio |
