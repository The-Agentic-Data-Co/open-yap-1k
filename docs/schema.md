# Field schema

Layout revision 16. The number counts changes to the field list
below, not to the corpus. [`archive-layout.md`](archive-layout.md) names the
three version numbers a delivery carries.

Every field the delivered archive carries. JSON Schemas for the same files
are in [`../data/schema/`](../data/schema/), and the flat list is in
[`../data/fields.json`](../data/fields.json).

A `null` means the value was not measured or the speaker did not report it.
It never means zero.

## `manifest.json`

| Field | Description |
|---|---|
| `dataset_version` | version of this file's field list |
| `generated_at` | ISO 8601 timestamp |
| `archive_contents` | "full" or "incremental" |
| `audio_format` | audio codec (wav or flac) |
| `sample_rate` | sample rate of every delivered audio file, in Hz |
| `total_conversations` | number of conversations |
| `total_duration_seconds` | total duration in seconds |
| `languages` | BCP-47 language codes |
| `conversation_ids` | stable pseudonymous conversation IDs |
| `transcript_schema_version` | transcript schema version |
| `measurement_schema_version` | audio measurement method version |
| `loudness_normalization` | present only when the archive was built with a loudness normalization setting: { setting, scope ("conversation" or "track"), measure ("lufs", "rms" or "peak"), target, unit, method ("constant_gain"), version } |

## `conv_<id>/meta.json`

| Field | Description |
|---|---|
| `conversation_id` | stable pseudonymous conversation ID |
| `language` | BCP-47 language tag |
| `relationship` | self-reported relationship between speakers |
| `duration_seconds` | conversation length in seconds |
| `recorded_at` | recording date (YYYY-MM-DD) |
| `speaker_a_id` | pseudonymous ID for speaker A |
| `speaker_b_id` | pseudonymous ID for speaker B |
| `conversation_summary` | LLM summary of the conversation (2-3 sentences) |
| `topics[]` | topic tags discussed in the conversation |
| `speech_dominance` | speaker A's share of spoken words, 0..1 (0.5 = equal) |
| `turn_taking_gap_ms` | median turn-taking gap in milliseconds (conversational latency) |
| `turns_per_minute` | speaker handoffs per minute of complete aligned recording, excluding short overlapping backchannels |
| `is_segment` | true when this folder is one kept stretch of a longer recording |
| `source_conversation_id` | pseudonymous ID of the recording this stretch was cut from; null when not a segment |
| `segment_index` | 0-based position among the kept stretches of that recording; null when not a segment |
| `segment_count` | how many kept stretches that recording was cut into; null when not a segment |
| `segment_start_seconds` | where this stretch starts on the source recording's clock, in seconds; null when not a segment |
| `segment_end_seconds` | where this stretch ends on the source recording's clock, in seconds; null when not a segment |

## `conv_<id>/speaker_<a|b>_meta.json`

| Field | Description |
|---|---|
| `speaker_id` | pseudonymous speaker ID |
| `age_range` | bucketed age range |
| `gender` | self-reported gender |
| `country` | self-reported country (ISO-3166 alpha-2) |
| `education_level` | self-reported education level |
| `native_language` | self-reported native language (BCP-47) |
| `accent` | provenance-derived accent from self-reported demographics (not measured from audio): { origin_country (ISO-3166 childhood country where the accent forms), english_native (true if English is the first language, else false; null if unknown) } |
| `recording` | { sample_rate (delivered Hz), original_sample_rate (verified native capture Hz), duration_seconds, bit_depth: 16, channels: 1, integrated_lufs (measured LUFS, nullable), true_peak_dbtp (measured dBTP, nullable), loudness_normalization (present only on a normalized archive) } — audio is delivered at its recorded level unless the archive was built with a loudness normalization setting; loudness + true-peak are measured on the rendition shipped here, after any normalization, rather than on any other, so you can normalize to your own target |
| `transcript` | transcript JSON filename |
| `avg_wpm` | words per minute of SPEAKING time — transcript words divided by the time spent producing them, not by the length of the recording. A speaker silent while their partner talks does not read as a slow one |
| `echo_cancellation` | whether echo cancellation was applied at capture, as reported by the client (a capture setting, not measured from audio); null where the client reported nothing |
| `headphones` | whether the speaker used headphones (authoritative on mobile, heuristic on web) |
| `device` | capture device / audio-route label |
| `audio_metrics` | measured from THIS track, at the rate this archive ships. Conformance, DNSMOS, and physical time-series measurements land independently, so one can exist while another is null; the block itself is null only when none exists |
| `audio_metrics.noise_floor_dbfs` | the room in dBFS, lower = quieter. Null where the track has not been measured yet, which is most of the catalogue today; on a measured track, null means there is no room tone to measure at all |
| `audio_metrics.silence_profile` | what fills this track when the speaker is not talking, measured from the audio rather than from any capture flag. "room_tone" (the actual room), "noise_gated" (the capture chain wrote digital silence between turns), "dropout" (the microphone cut out mid-recording, audio either side), "no_signal" (nothing was ever voiced). Null is unmeasured rather than a fifth shape |
| `audio_metrics.silent_while_partner_spoke_pct` | share of the partner's speech during which this microphone carried no signal, the trailing pad excluded. Read it beside the silence_profile of BOTH tracks: 0 means the overlap survived only where this track is room_tone or noise_gated and the partner voiced something, and a high value means a gate erased that overlap. Two shapes force 0 with no overlap behind it — a no_signal track, whose whole file is the excluded pad, and any track whose PARTNER is no_signal, because the partner's speech is the denominator. A dropout forces neither, because its hole has audio either side of it and is counted. Gated tracks run the whole range, so this is what tells a lightly affected track from a gutted one. Null is unmeasured |
| `audio_metrics.effective_bandwidth_hz` | effective bandwidth in Hz. Measurement version 4 uses the 99.99% energy cutoff during detected speech. Null when unmeasured or unmeasurable |
| `audio_metrics.dnsmos_bak_median` | ITU-T P.835 background-noise median on the nominal 1-5 mean-opinion-score scale, 5 = not noticeable; calibrated predictions can fall outside this range |
| `audio_metrics.dnsmos_sig_median` | ITU-T P.835 speech-signal median, nominal 1-5: the voice itself; calibrated predictions can fall outside this range |
| `audio_metrics.dnsmos_ovr_median` | ITU-T P.835 overall median, nominal 1-5: voice and background together; calibrated predictions can fall outside this range |
| `audio_metrics.dnsmos_time_series` | names the file holding the same three scores over time |
| `audio_metrics.signal_metrics_time_series` | names the file holding SNR, noise floor, and clipping percentage over time |
| `recording.loudness_normalization.setting` | the setting as scope:measure:target, e.g. conversation:rms:-20 |
| `recording.loudness_normalization.scope` | "conversation" = one shared change for every speaker in the conversation; "track" = a separate change for each track |
| `recording.loudness_normalization.measure` | "lufs" = loudness (ITU-R BS.1770), "rms" = average level over the whole file including pauses, "peak" = the loudest sample |
| `recording.loudness_normalization.target` | the level the setting asks for, e.g. -20 |
| `recording.loudness_normalization.unit` | "LUFS" for lufs, "dBFS" for rms and peak |
| `recording.loudness_normalization.method` | "constant_gain": one volume change for the whole track, with no compression or limiting |
| `recording.loudness_normalization.gain_db` | the volume change applied to this track, in dB |
| `recording.loudness_normalization.target_reached` | true when the result is within 0.1 dB of the target |
| `recording.loudness_normalization.limited_by` | "clipping" = the change stopped just below full scale, so the result is below the target; "unmeasurable" = nothing to measure, so the track is unchanged; null when the target was reached |
| `recording.loudness_normalization.conversation_before` | the conversation level in the chosen measure before the change; null for per-track settings |
| `recording.loudness_normalization.conversation_after` | the conversation level in the chosen measure after the change; null for per-track settings |
| `recording.loudness_normalization.track_before` | { lufs, rms_dbfs, sample_peak_dbfs } of this track before the change |
| `recording.loudness_normalization.track_after` | { lufs, rms_dbfs, sample_peak_dbfs } of this track as delivered |

## `conv_<id>/speaker_<a|b>_transcript.json`

| Field | Description |
|---|---|
| `conversation_id` | stable pseudonymous conversation ID |
| `speaker_index` | which speaker stem ("a" or "b") |
| `language` | BCP-47 language tag |
| `text` | full transcript text |
| `words[]` | array of { word, start, end, type } |
| `corrections_applied` | true if a reviewer corrected the ASR output |

## `conv_<id>/speaker_<a|b>_dnsmos.json`

| Field | Description |
|---|---|
| `conversation_id` | stable pseudonymous conversation ID |
| `speaker_index` | which speaker stem ("a" or "b") |
| `metric` | always "dnsmos_p835" — ITU-T P.835 scores predicted by Microsoft DNSMOS |
| `model` | model file and licence the scores came from |
| `measurement_seconds` | seconds of audio each score describes (fixed by the model) |
| `step_seconds` | seconds between consecutive measurements; measurements overlap |
| `measurement_count` | number of entries in each of the arrays below |
| `bak[]` | background-noise score per measurement, nominal 1-5 (5 = not noticeable); calibrated predictions can fall outside this range. Entry i covers [i\*step_seconds, i\*step_seconds+measurement_seconds) on the delivered timeline; null where the audio held too little speech to score |
| `sig[]` | speech-signal score per measurement, nominal 1-5; calibrated predictions can fall outside this range; null on the same entries as bak |
| `ovr[]` | overall score per measurement, nominal 1-5; calibrated predictions can fall outside this range; null on the same entries as bak |

## `conv_<id>/speaker_<a|b>_signal_metrics.json`

| Field | Description |
|---|---|
| `conversation_id` | stable pseudonymous conversation ID |
| `speaker_index` | which speaker stem (seat or scripted role) |
| `schema_version` | version of this signal-metrics file shape |
| `method` | versioned measurement method |
| `sample_rate_hz` | sample rate of the measured delivered audio |
| `duration_seconds` | duration of the measured track |
| `measurement_seconds` | seconds of audio each value describes |
| `step_seconds` | seconds between consecutive values |
| `measurement_count` | number of entries in each metric array |
| `frame_seconds` | analysis-frame duration used for speech and floor measurements |
| `noise_floor_context_seconds` | local context used to estimate the noise floor |
| `max_zero_fraction` | frames at or above this exact-zero share are excluded from level measurements |
| `min_live_noise_frames` | minimum live non-speech evidence required before SNR and noise floor are measurable |
| `min_real_noise_floor_dbfs` | levels at or below this converter floor count as digital silence |
| `clipping_threshold` | absolute normalized sample level counted as clipped |
| `snr_db[]` | signal-to-noise ratio in dB per measurement; null without measurable speech or room tone |
| `noise_floor_dbfs[]` | local noise floor in dBFS per measurement; null where no real room tone is measurable |
| `clipping_pct[]` | percentage of samples at or above clipping_threshold per measurement |
