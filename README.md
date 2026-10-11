```text
 ┌──────────────────────────────────────────────
 │
 │   u w u n y a
 │   a soft, playful friend for your Discord server
 │
 │   discord.py  ·  NVIDIA-hosted models  ·  Python
 │
 └──────────────────────────────────────────────
```

uwunya is a Discord bot built to be there when someone needs a kind word. She chats like a gentle, cheerful friend, keeps replies short, and knows when to drop the playfulness and just listen. The conversations are powered by free, open models served through NVIDIA's OpenAI-compatible API.

> uwunya is a friendly companion, not a therapist. She encourages people to lean on real friends, family and professionals, and she is not a replacement for them.

---

## At a glance

```text
 language ........ Python 3.10+
 library ......... discord.py (async)
 ai provider ..... NVIDIA build API (OpenAI-compatible endpoint)
 model ........... z-ai/glm-5.3-flash   (swap in one line)
 triggers ........ $commands  and  @mentions
 status .......... working, memory feature in progress
```

---

## Features

1. **Supportive chat.** Ask a question with `$ask` or just mention her, and she replies in a warm, natural voice.
2. **Her own personality.** Everything about how she talks lives in one editable `SYSTEM_PROMPT`: tone, length, formatting rules and a safety section for serious moments.
3. **Never freezes.** AI calls are fully async, so she keeps responding to everyone else while one answer is being written.
4. **Fails gently.** If the AI is down or rate-limited, users see a friendly message and the real error goes to your terminal.
5. **Little extras.** `$hello` for a greeting and `$quote` for a random quote.

---

## How it works

```text
   a message arrives in Discord
              │
              ▼
        on_message()
              │
     ┌────────┼─────────────┬─────────────┐
     ▼        ▼             ▼             ▼
  $hello    $quote      $ask <text>    @uwunya <text>
              │             └──────┬──────┘
              ▼                    ▼
        ZenQuotes API          ask_ai()
                                   │
                  SYSTEM_PROMPT + the user's message
                                   │
                                   ▼
                       NVIDIA API  ──►  model reply
                                   │
                                   ▼
                       channel.send(reply)
```

---

## Commands

| Trigger | What it does |
| --- | --- |
| `$hello` | uwunya says hi |
| `$quote` | Fetches a random quote from ZenQuotes |
| `$ask <message>` | Sends your message to the AI and replies in her voice |
| `@uwunya <message>` | Same as `$ask`, without the prefix |

---

## Getting started

### Before you begin

1. Python 3.10 or newer.
2. A Discord application with a bot user, created in the [Discord Developer Portal](https://discord.com/developers/applications).
3. An NVIDIA API key (starts with `nvapi-`) from [build.nvidia.com](https://build.nvidia.com).

### Install

```bash
git clone <your-repo-url>
cd uwunya

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Configure

Create a file named `.env` in the project root:

```text
MY_BOT_TOKEN=your_discord_bot_token
MY_NVIDIA_KEY=nvapi-your_nvidia_key
```

No quotes, and no spaces around `=`.

### Enable the Message Content intent

In the Developer Portal, open your application, go to **Bot**, scroll to **Privileged Gateway Intents**, switch on **Message Content Intent**, and click **Save Changes**. Without this the bot connects but cannot read messages, and fails with `PrivilegedIntentsRequired`.

### Run

```bash
python code/main.py
```

When the terminal prints `Hello! I am ... and I am now online!`, try `$hello` in your server.

---

## Configuration

| Setting | Where | Purpose |
| --- | --- | --- |
| `MY_BOT_TOKEN` | `.env` | Your Discord bot token |
| `MY_NVIDIA_KEY` | `.env` | Your NVIDIA API key |
| `model` | `ask_ai()` in `main.py` | Which hosted model answers. Copy the exact ID from the model's page on build.nvidia.com |
| `SYSTEM_PROMPT` | top of `main.py` | uwunya's personality, tone and rules |
| `temperature` | `ask_ai()` | Lower is steadier, higher is more varied |
| `max_tokens` | `ask_ai()` | Reply length cap. Reasoning models need some headroom, or replies can come back empty |

---

## Project layout

```text
uwunya/
├── .env                 secrets, never commit this
├── .gitignore           should list .env and .venv/
├── requirements.txt
└── code/
    ├── main.py          the bot itself
    └── mind.py          scratch file for testing the AI on its own
```

`requirements.txt`:

```text
discord.py
python-dotenv
requests
openai
```

The `openai` package is used only as a client library. Requests are sent to NVIDIA's endpoint (`https://integrate.api.nvidia.com/v1`), not to OpenAI.

---

## Her personality

uwunya's voice is defined entirely by `SYSTEM_PROMPT`. The current version asks her to:

1. Sound like a friend texting, not customer support.
2. Acknowledge feelings first and avoid rushing to advice.
3. Keep replies short and ask at most one gentle question at a time.
4. Use cute touches rarely, and drop them completely when someone is hurting.
5. Write in plain sentences, with no bullet lists or heading-style formatting.
6. Respond to talk of self-harm with calm, serious care and point toward a trusted person or local emergency or crisis service.

Edit the prompt, restart the bot, and her voice changes. Small, specific instructions work better than long ones.

---

## Privacy and responsible use

1. Anything sent through `$ask` or a mention is passed to NVIDIA's servers to generate a reply. Do not share passwords or private details with her.
2. Messages in a server channel are visible to everyone in that channel. For personal topics, a direct message is kinder to the person talking.
3. AI replies are generated text and can be wrong. She does not diagnose or give medical advice, and she should never be the only support someone has.
4. Free API tiers are rate-limited. If replies stop or errors appear, check the terminal first.

---

## Roadmap

- [x] Connect to NVIDIA's hosted models
- [x] Custom personality through a system prompt
- [x] Mentions as well as `$ask`
- [ ] Short per-user memory: about five lines on how to chat with each person, saved in a free Postgres database (Neon)
- [ ] `$mynotes` to view saved notes and `$forget` to delete them
- [ ] One-time notice the first time someone chats with her
- [ ] Short-term conversation memory for follow-up questions
- [ ] Per-user cooldown and splitting of long replies
- [ ] 24/7 hosting

When the memory feature lands, notes will describe communication style and light interests only, never sensitive details, and anyone will be able to read or delete theirs.

---

<details>
<summary><b>Troubleshooting</b></summary>

<br>

**`Missing credentials` on startup.** The NVIDIA key came back empty. Check that `.env` contains `MY_NVIDIA_KEY=...`, that the name matches exactly, and that the file is saved.

**`PrivilegedIntentsRequired`.** Turn on Message Content Intent in the Developer Portal and save.

**Bot is online but ignores messages.** Same cause as above, or the code is missing `intents.message_content = True`.

**`IndentationError`.** Python needs consistent indentation. Check that function and `if` bodies are indented.

**Nothing happens after `client.run(...)`.** Everything below that line never executes. Keep it as the very last line of the file.

**Replies are empty or cut off.** Raise `max_tokens`. Reasoning models can spend the whole budget thinking.

**`404` or model not found.** The model ID changed. Copy the current one from the model's page.

**`429` errors.** You hit the free-tier rate limit. Wait a moment and try again.

</details>

---

```text
 built by Breezy, one small step at a time.
 if she made someone's day a little softer, that was the point.
```