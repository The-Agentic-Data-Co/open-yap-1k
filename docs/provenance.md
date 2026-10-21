# Collection method

We collect the audio with our own app, which works like a phone call. A speaker invites someone they know, and the two of them simply talk. This gives us natural conversation and a straightforward way to scale collection. The trade-off is less control over the recording environment, so real-world noise appears more often. We keep the subtle noise, because it teaches a model robustness. However, we remove the long tail of noisy recordings with several ML models combined into one pipeline.

| | Other datasets | Open Yap 1K |
|---|---|---|
| Speakers | Strangers, paired by the collector | Friends and family, self-paired |
| Setting | A treated room | Real rooms, on their own devices |
| Conversation | An assigned topic | Free talk, any topic |
| What you hear | Clean turns, little overlap | Overlap, quick turns, backchannel, laughter |
| Background | Pristine | Slightly noisier, kept on purpose |

## Consent and privacy

All audio was recorded on our own platform.

- Speakers register, give explicit consent before their first recording, and are paid for their time.
- Demographics are self-reported at registration, before any recording, and are never inferred from audio.
- Speaker identifiers are pseudonymous and stable within the release. Names, contact details and account identifiers are excluded.

## Quality assurance

### Human linguistic QA

A human reviews each conversation for language proficiency, accent classification, and ratings for naturalness and expressivity.

### Transcript screening

Every transcript is passed through an LLM screen for personally identifying information and for content-policy violations. Flagged conversations are excluded.

## Intended use

### Speech-to-speech and full-duplex

Both sides as independent signals on one timeline. Overlap and turn-taking intact.

### Expressive TTS

Spontaneous prosody on clean, isolated 48 kHz tracks. Laughter, fillers, and hesitation.

### Audio understanding

Unprompted speech with word-level transcripts and speaker metadata.
