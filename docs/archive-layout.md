# Archive layout

What a delivered corpus archive contains, once you have requested and
received it.

Layout revision 9. The number counts changes to the tree below: which
files exist, and what each one is named. A delivery carries two other
numbers, and they count different things:

- **Corpus version 1.0**, in the citation. The release itself.
- **`dataset_version`**, inside `manifest.json`. The fields of that one file.

```
conversations/
  manifest.json
  conv_a1b2c3d4e5f6/
    speaker_a.flac   (or .wav)
    speaker_b.flac   (or .wav)
    meta.json
    speaker_a_meta.json
    speaker_b_meta.json
    speaker_a_transcript.json
    speaker_b_transcript.json
    speaker_a_dnsmos.json
    speaker_b_dnsmos.json
  conv_7f3e9d014a6c/
    ...
```

## What the names mean

- `conv_<12 hex>` — a stable pseudonymous conversation code. It is the first
  12 hex characters of a SHA-256, so it cannot be reversed, and it does not
  change between deliveries. Incremental downloads stack on it.
- `speaker_a` and `speaker_b` — the two sides, each an isolated mono file.
  There is no mixed track: the separation is the product.
- `*_dnsmos.json` — the background-noise time series. **Absent, not empty,**
  when a track was not scored. An absent file means no measurement exists.

## Audio

48,000 Hz, 16-bit PCM, one channel per file, delivered
un-normalised. Loudness is measured and reported per track rather than
corrected, so the original dynamics survive.

Validate an archive you have received:

```bash
python tools/validate_archive.py /path/to/extracted/archive
```
