# Archive layout

What a delivered corpus archive contains, once you have requested and
received it.

Layout revision 16. The number counts changes to the tree below: which
files exist, and what each one is named. A delivery carries two other
numbers, and they count different things:

- **Corpus version 1.0**, in the citation. The release itself.
- **`dataset_version`**, inside `manifest.json`. The fields of that one file.

```
conversations/conv_<id>/meta.json
conversations/conv_<id>/speaker_a.flac
conversations/conv_<id>/speaker_a_dnsmos.json
conversations/conv_<id>/speaker_a_meta.json
conversations/conv_<id>/speaker_a_signal_metrics.json
conversations/conv_<id>/speaker_a_transcript.json
conversations/conv_<id>/speaker_b.flac
conversations/conv_<id>/speaker_b_dnsmos.json
conversations/conv_<id>/speaker_b_meta.json
conversations/conv_<id>/speaker_b_signal_metrics.json
conversations/conv_<id>/speaker_b_transcript.json
conversations/manifest.json
conversations/verification.json
```

## What the names mean

- `conv_<12 hex>` — a stable pseudonymous conversation code. It is the first
  12 hex characters of a SHA-256, so it cannot be reversed, and it does not
  change between deliveries. Incremental downloads stack on it.
- `speaker_a` and `speaker_b` — the two sides, each an isolated mono file.
  There is no mixed track: the separation is the product.
- `*_dnsmos.json` — the background-noise time series. **Absent, not empty,**
  when a track was not scored. An absent file means no measurement exists.
- `*_signal_metrics.json` — one-second SNR, noise-floor, and clipping values.
  It is absent when matching measurements do not exist for the delivered audio.
- `verification.json` accompanies measurement-version-4 archives. It lists SHA-256 hashes
  for delivered files and decoded audio samples. The validator checks file hashes before schemas.

## Audio

48,000 Hz, 16-bit PCM, one channel per file, delivered
un-normalised. Loudness is measured and reported per track rather than
corrected, so the original dynamics survive.

Validate an archive you have received:

```bash
python tools/validate_archive.py /path/to/extracted/archive
```
