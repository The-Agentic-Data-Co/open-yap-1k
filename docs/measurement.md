# How the figures are measured

Conformance schema version 2.

Every number we publish about this corpus is measured from the audio and the
transcripts, not estimated and not claimed. This page states each method and
each threshold, so you can reproduce any figure.

**What we publish is the method, not the code.** You can recompute any figure
from what is here, but you cannot rerun our exact implementation, so a value
you compute may differ in the last digit. Every constant that would explain
such a difference is stated below.

## Signal

### Effective bandwidth

Median 11.6 kHz, 5th to 95th percentile
6.9 to 22.3.

The highest frequency at which a track still carries real sound. A file header can say 48 kHz while the audio inside stops at 8 kHz.

We read the frequency spectrum of a track’s speech in one pass, up to 262,144 samples, or 5.5 seconds at 48 kHz. We smooth it over 100 Hz either side, then take the highest frequency within 60 dB of the loudest.

Telephone audio cliffs near 4 kHz. A Bluetooth headset in hands-free mode caps near 8 kHz. It ships as `effective_bandwidth_hz`.

### DNSMOS background noise

Median 3.97 BAK, 5th to 95th percentile
3.49 to 4.14.

Noise is the hardest thing here to measure, so we use DNSMOS BAK, a neural network from Microsoft. It predicts how a listener would rate the background, on ITU-T P.835’s scale of 1 to 5.

P.835 puts words on the numbers. At 3 you notice the background but it does not get in the way. At 4 you barely notice it. At 5 you do not notice it at all. The release page plays a 10 second clip from a real recording at each score, so you can hear each one for yourself: https://theagenticdatacompany.com/open-yap-1k.

BAK reads a 9.01 second window, the only length it is calibrated for. We slide that window every 3 seconds and take each track’s median. We drop windows under 25 percent speech, because the model only hears noise behind a voice.

## Conversational dynamics

### Overlap

Median 8.3 % of voiced time, 5th to 95th percentile
2.8 to 20.9.

The share of talking time where both people speak at once. Almost none usually means echo cancellation gated one microphone, which erases the very thing a full-duplex model needs to learn. Below 3 percent we flag the conversation.

We cut both tracks into 20 millisecond frames. A frame counts as speech when it passes three times that track’s own noise floor, or a fixed floor of 0.004, whichever is higher. The figure is the frames where both speak, divided by the frames where either does.

### Turn-taking gap

Median 580 ms, 5th to 95th percentile
280 to 1120.

The silence between one person finishing and the other starting. Get this wrong in a voice model and it either interrupts the user or leaves them hanging.

We merge the voiced stretches of both tracks onto one timeline. Every change of speaker gives one gap, and the figure is the median of them. Where the next speaker started early the two are talking at once, so that goes under Overlap instead.

CANDOR, a large public corpus of natural conversation, reports 380 milliseconds. It ships as `turn_taking_gap_ms`.

### Speech dominance

Median 0.56 share, 5th to 95th percentile
0.27 to 0.81.

Speaker A’s share of the talking, where 0.5 is an even split.

We count the 20 millisecond frames in which A is voiced, then divide by the frames in which either speaker is. Overlapping speech counts for both people, so the two shares add up to more than 1 when they talk at once.

The metadata field `speech_dominance` is a different number. That one is A’s share of the transcript words.

### Speaking rate

Median 186 words/min, 5th to 95th percentile
156 to 218.

How fast a person speaks, in words per minute of actual speaking time.

The denominator is the choice that matters, so we tested three across 28 channels of real conversation. Dividing by the whole recording gave 74 words per minute at the median. That measures how much of the call each person held, not how fast they talk. Voice activity detection gave 192, but it counts breaths, laughter and a partner’s bleed as talking, and it swung from 82 to 281 on the same audio.

So we sum each word’s own duration from the transcript and divide the word count by that. Only entries typed as words count, on both sides of the division. It ships as `avg_wpm`.

## Conformance

Pass rates against a stated threshold, over delivered tracks.

| Check | Threshold | Pass rate |
|---|---|--:|
| Track pairs sharing a common timeline anchor | Required | 100.00% |
| Conversations with word-level transcripts | Both speakers | 100.00% |
| Tracks whose background noise is not intrusive | Median BAK at least 3.0 (P.835) | 100.00% |
| Tracks with zero clipped samples | Under 0.1% of samples at full scale | 98.38% |
| Tracks above telephone bandwidth | Bandwidth at least 6.0 kHz | 96.44% |

**A failing track is still delivered.** This table reports the corpus, it does
not filter it. A buyer who wants to exclude flagged tracks has the per-track
numbers in `speaker_<a|b>_meta.json` to do it themselves.

## Constants

The flag thresholds, verbatim from the implementation:

| Constant | Value |
|---|--:|
| Band-limited below | 6,000 Hz |
| High gating above | 1% |
| Low overlap below | 3% |
| Clipping above | 0.1% |
| Dead-channel run | 2 s |
| Clean tier needs SNR | 20 dB |
| Negligible silence below | 1% |
| Dropout concentration | 0.35 |

The background-noise window, verbatim:

| Constant | Value |
|---|--:|
| Window | 9.01 s |
| Hop | 3 s |
| Minimum speech share in a window | 0.25 |

The window length is not a choice: DNSMOS P.835 sig_bak_ovr.onnx (microsoft/DNS-Challenge, CC BY 4.0) is calibrated
at that length and only at that length. Windows below the speech share are
dropped, because the model only hears a background behind a voice.

## Coverage

Each figure is only as true as the share of the corpus that carries the
underlying measurement. Every section reports its own denominator:

| Section | Measured | Of |
|---|--:|--:|
| population | 239 | 239 |
| conversationLength | 1,602 | 1,602 |
| relationship | 1,602 | 1,602 |
| wordsPerConversation | 1,602 | 1,602 |
| vocabulary | 3,204 | 3,204 |
| audio | 1,602 | 1,602 |
| speakingRate | 3,204 | 3,204 |
| noise | 3,204 | 3,204 |
