# How the figures are measured

Conformance schema version 4.

Audio measurements describe the delivered tracks. Speaker demographics come from speaker reports.

## Effective bandwidth method

Conformance schema 4 averages power spectra from contiguous speech-active windows across the complete recording.
Speech detection uses 20 ms RMS frames and threshold max(3 × percentile20(RMS), 0.004). It fills gaps shorter than 160 ms and removes runs shorter than 160 ms.
The transform size is 2^floor(log2(sample_rate × 0.1)), with 50% overlap. At 48 kHz this is 4,096 samples.
A window contributes when its centre is speech-active. Subtract its mean and apply the periodic Hann window: 0.5 − 0.5 × cos(2πi/N).
Square the complex transform magnitudes. Double positive-frequency bins except Nyquist, then average across windows.
Effective bandwidth is the lowest frequency reaching 99.99% of cumulative power in this unsmoothed mean spectrum, rounded to the nearest hertz.
No usable speech-active spectrum produces null. The result includes noise during selected windows and is not a calibrated microphone response.

## Turn rate

Turn-metrics schema version 1.

Energy-based voice activity detection finds speech intervals on the aligned
48 kHz master speaker pair. Each speaker change after the first start is a reply
or an interruption. A segment at most one second long is a backchannel when
it overlaps the partner and has one second of that speaker's silence on each
side. Backchannels do not count as turns.

`turns_per_minute = (reply_count + interruption_count) × 60 ÷ duration_seconds`.
The duration covers the complete aligned recording, including silence.

## Signal time series

Signal-metrics schema version 1; method `yaproom_energy_vad_minstats_v1`.

Each array has one value per second on the delivered track's timeline.
Entry i starts at i × step_seconds; the final entry ends at duration_seconds.
Each array has measurement_count = ceil(duration_seconds ÷ step_seconds) entries.
Twenty-millisecond frames feed the same energy voice-activity detector as
the conformance report.

The noise floor is the median, within that second, of a centred 1.5-second
sliding-minimum power track. Voiced frames, frames that are at least half
exact zero, and frames at the 16-bit converter floor do not contribute.
A track needs at least 100 live non-speech frames before any noise-floor
or SNR value is reported.

SNR is the speech-frame RMS level in dBFS minus the local noise floor.
It is null where that second has no measured speech or no measured floor.
Clipping is the percentage of samples whose absolute level is at least 0.999.

## Signal

### Effective bandwidth

Median 10.3 kHz, 5th to 95th percentile
5.6 to 18.1.

Frequency below which 99.99% of the measured energy lies during detected speech.

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

Median 0.51 share, 5th to 95th percentile
0.24 to 0.77.

Speaker A’s share of spoken words, where 0.5 is an even split.

### Speaking rate

Median 188 words/min, 5th to 95th percentile
159 to 221.

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
| Tracks below the clipping threshold | Under 0.1% of samples at full scale | 99.13% |
| Tracks with effective bandwidth above 6 kHz | Effective bandwidth at least 6.0 kHz | 92.01% |

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

The physical signal series, verbatim:

| Constant | Value |
|---|--:|
| Frame | 0.02 s |
| Measurement | 1 s |
| Step | 1 s |
| Noise-floor context | 1.5 s |
| Exact-zero exclusion | 0.5 |
| Minimum live noise frames | 100 |
| Digital-silence floor | -90 dBFS |
| Clipping sample threshold | 0.999 |

## Coverage

Each figure is only as true as the share of the corpus that carries the
underlying measurement. Every section reports its own denominator:

| Section | Measured | Of |
|---|--:|--:|
| population | 239 | 239 |
| conversationLength | 1,602 | 1,602 |
| turnsPerMinute | 1,602 | 1,602 |
| wordsPerConversation | 1,602 | 1,602 |
| vocabulary | 3,204 | 3,204 |
| audio | 1,602 | 1,602 |
| speakingRate | 3,204 | 3,204 |
| noise | 3,204 | 3,204 |
