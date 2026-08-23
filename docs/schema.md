# Field schema

Archive shape version 9.

Every field the delivered archive carries. JSON Schemas for the same files
are in [`../data/schema/`](../data/schema/), and the flat list is in
[`../data/fields.json`](../data/fields.json).

A `null` means the value was not measured or the speaker did not report it.
It never means zero.

## `manifest.json`

| Field | Description |
|---|---|
| `dataset_version` | dataset schema version |
| `generated_at` | ISO 8601 timestamp |
| `archive_contents` | "full" or "incremental" |
| `audio_format` | audio codec (wav or flac) |
| `total_conversations` | number of conversations |
| `total_duration_seconds` | total duration in seconds |
| `languages` | BCP-47 language codes |
| `conversation_ids` | stable pseudonymous conversation IDs |
| `transcript_schema_version` | transcript schema version |

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
| `recording` | { sample_rate (Hz — the rate THIS archive ships; per-archive, not fixed), duration_seconds, bit_depth: 16, channels: 1, integrated_lufs (measured LUFS, nullable), true_peak_dbtp (measured dBTP, nullable) } — audio is delivered un-normalized; loudness + true-peak are measured and reported so you can normalize to your own target, and both are measured on the rendition shipped here rather than on any other |
| `transcript` | transcript JSON filename |
| `avg_wpm` | words per minute of SPEAKING time — transcript words divided by the time spent producing them, not by the length of the recording. A speaker silent while their partner talks does not read as a slow one |
| `echo_cancellation` | whether echo cancellation was applied at capture, as reported by the client (a capture setting, not measured from audio); null where the client reported nothing |
| `headphones` | whether the speaker used headphones (authoritative on mobile, heuristic on web) |
| `device` | capture device / audio-route label |
| `audio_metrics` | measured from THIS track, at the rate this archive ships. The conformance half (noise floor, silence, bandwidth) and the DNSMOS half land independently, so either can be null while the other carries values; the block itself is null only when neither has been measured |
| `audio_metrics.noise_floor_dbfs` | the room in dBFS, lower = quieter. Null where the track has not been measured yet, which is most of the catalogue today; on a measured track, null means there is no room tone to measure at all |
| `audio_metrics.silence_profile` | what fills this track when the speaker is not talking, measured from the audio rather than from any capture flag. "room_tone" (the actual room), "noise_gated" (the capture chain wrote digital silence between turns), "dropout" (the microphone cut out mid-recording, audio either side), "no_signal" (nothing was ever voiced). Null is unmeasured rather than a fifth shape |
| `audio_metrics.silent_while_partner_spoke_pct` | share of the partner's speech during which this microphone carried no signal, the trailing pad excluded. Read it beside the silence_profile of BOTH tracks: 0 means the overlap survived only where this track is room_tone or noise_gated and the partner voiced something, and a high value means a gate erased that overlap. Two shapes force 0 with no overlap behind it — a no_signal track, whose whole file is the excluded pad, and any track whose PARTNER is no_signal, because the partner's speech is the denominator. A dropout forces neither, because its hole has audio either side of it and is counted. Gated tracks run the whole range, so this is what tells a lightly affected track from a gutted one. Null is unmeasured |
| `audio_metrics.effective_bandwidth_hz` | the highest frequency carrying real energy: the microphone's limit, not the container's. Null where the track is unmeasured, or carried nothing voiced |
| `audio_metrics.dnsmos_bak_median` | ITU-T P.835 background-noise median on the 1-5 mean-opinion-score scale, 5 = not noticeable |
| `audio_metrics.dnsmos_sig_median` | ITU-T P.835 speech-signal median, 1-5: the voice itself |
| `audio_metrics.dnsmos_ovr_median` | ITU-T P.835 overall median, 1-5: voice and background together |
| `audio_metrics.dnsmos_time_series` | names the file holding the same three scores over time |

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
| `bak[]` | background-noise score per measurement, 1-5 (5 = not noticeable). Entry i covers [i\*step_seconds, i\*step_seconds+measurement_seconds) on the delivered timeline; null where the audio held too little speech to score |
| `sig[]` | speech-signal score per measurement, 1-5; null on the same entries as bak |
| `ovr[]` | overall score per measurement, 1-5; null on the same entries as bak |
