# Datasheet — Open Yap 1K

Following Gebru et al., *Datasheets for Datasets* (2018).

## Motivation

**Why was it created?** Conversational AI needs recordings of people talking
the way they actually talk. The large conversational corpora are telephone
recordings from the 1990s and 2000s, band-limited near 4 kHz, with assigned
partners and assigned topics. We wanted natural conversation at full
bandwidth, with each speaker on their own channel.

**Who created and funded it?** The Agentic Data Company, from its own funds.
It is released free because progress in conversational AI is slower than it
needs to be, and open data is the fastest way to change that.

## Composition

**What does it contain?** 1,602 conversations, 1,000
hours, 239 speakers. Each conversation is two people who already know
each other, talking freely. Both sides are recorded separately and shipped as
separate files on one timeline.

**Sampling.** Each speaker invites someone they know. Nothing is assigned —
not the partner, not the topic. So it is not a random sample of any
population, and the relationship distribution reflects who people chose to
call.

**Is anything missing?** Yes. Where a measurement does not exist, the field is
`null` rather than a filled-in guess. Coverage per section is published in
[`docs/measurement.md`](docs/measurement.md).

**Does it contain confidential or offensive content?** It is unscripted human
conversation, so it contains whatever people said. Every transcript is passed
through a screen for personally identifying information and content-policy
violations, and flagged conversations are excluded. The screen is automated
and is not perfect.

## Collection

All audio was recorded on our own platform.

- Speakers register, give explicit consent before their first recording, and are paid for their time.
- Demographics are self-reported at registration, before any recording, and are never inferred from audio.
- Speaker identifiers are pseudonymous and stable within the release. Names, contact details and account identifiers are excluded.

**Were people paid?** Yes, for their time.

**Consent.** Speakers consent before their first recording. The sample
published openly required a second, narrower consent, given per conversation
by both speakers, which is irreversible — so that set may only ever shrink.

## Preprocessing

Audio is captured locally as uncompressed PCM and resampled once. It is
delivered un-normalised, so the original dynamics survive. Transcripts are
produced by automatic speech recognition with word-level timings.

## Uses

- **Speech-to-speech and full-duplex.** Both sides as independent signals on one timeline. Overlap and turn-taking intact.
- **Expressive TTS.** Spontaneous prosody on clean, isolated 48 kHz tracks. Laughter, fillers, and hesitation.
- **Audio understanding.** Unprompted speech with word-level transcripts and speaker metadata.

## Limitations

- **Transcripts are not human-verified.** They come from automatic speech
  recognition. Expect errors, especially on overlapping speech and names.
- **Conversations are not independent samples.** A speaker appears in more
  than one conversation. Split by `speaker_id`, not by conversation, or your
  evaluation set will share voices with your training set and your numbers
  will be optimistic.
- **English only**, and the speaker population is not a census of anywhere.
  Read the demographic distributions before generalising from them.
- **Country is self-reported** at registration and is not verified.
- **Speakers know each other.** That is the point, and it is also a bias: this
  is not a corpus of strangers, task-oriented dialogue, or meetings.
- **The published sample is hand-picked**, so nothing about its distribution
  generalises to the corpus. Use `corpus-stats.json` for the corpus.

## Distribution

The sample is on the Hugging Face Hub under CC-BY-4.0 with a rider. The full
corpus is by request at https://theagenticdatacompany.com/open-yap-1k, under the Open Yap 1K Data Use Agreement.
See [`docs/access.md`](docs/access.md).

## Maintenance

Maintained by The Agentic Data Company. Errors in the data can be reported as
an issue on [The-Agentic-Data-Co/open-yap-1k](https://github.com/The-Agentic-Data-Co/open-yap-1k/issues)
using the data-issue template, which asks for the `conv_` code.

A speaker may withdraw consent at any time. Recordings we have already paid
for are retained and remain distributable as a licensed asset, but the
withdrawing speaker's identity is erased. Their demographics and audio survive
so that datasets already delivered stay valid.
