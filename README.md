<h1 align="center">Open Yap 1K</h1>

<p align="center"><strong>The world's largest open dataset of natural two-speaker English conversation.</strong><br>1,000 hours of channel-separated audio.</p>

<p align="center">
  <a href="https://theagenticdatacompany.com/open-yap-1k"><img src="docs/media/request-corpus.svg" alt="Request full corpus" height="36"></a>
  &nbsp;
  <a href="https://huggingface.co/datasets/TheAgenticDataCompany/open-yap-1k"><img src="docs/media/explore-sample.svg" alt="Explore free sample" height="36"></a>
</p>

<p align="center">
  <a href="https://theagenticdatacompany.com/">Website</a> ·
  <a href="DATASHEET.md">Datasheet</a> ·
  <a href="docs/schema.md">Schema</a>
</p>

---

## At a glance

| Audio | Conversations | Speakers | Capture |
|:---:|:---:|:---:|:---:|
| **1,000 hours** | **1,602** | **239** | **48 kHz, 16-bit PCM** |

## Hear it

[![Waveform of a sample conversation](docs/media/sample-openyap1k-01.svg)](https://huggingface.co/datasets/TheAgenticDataCompany/open-yap-1k)

The Hugging Face [dataset viewer](https://huggingface.co/datasets/TheAgenticDataCompany/open-yap-1k) plays every sample row. Download the sample with:

```bash
pip install -r tools/requirements.txt
python tools/download_sample.py
```

## Why natural conversation matters

Fisher and Switchboard paired strangers around assigned topics. Telephone networks also limited their audio to about 4 kHz. Newer corpora record wider bandwidth, but many still pair strangers.

Open Yap 1K assigns no partner or topic. Each participant invites someone they already know and talks freely.

Familiar speakers interrupt more, use more backchannels and leave shorter turn gaps. We publish overlap, turn-taking gaps and speaking rate for every conversation.

These 1,000 hours come from a larger licensed corpus built with voice AI labs and research teams. We released this part so researchers can train and test conversational systems with natural, commercially usable speech.

## Comparable datasets

| Dataset | Hours | Year | Band | Access | Source |
|---|--:|--:|---|---|---|
| Fisher English | 1,959 | 2004 | narrowband | paid | [LDC2004S13 + LDC2005S13](https://catalog.ldc.upenn.edu/LDC2004S13) |
| **Open Yap 1K** | **1,000** | 2026 | wideband | free | [this release](https://theagenticdatacompany.com/open-yap-1k) |
| Switchboard-2 | 898 | 1998 | narrowband | paid | [LDC98S75 + LDC99S79 + LDC2002S06](https://catalog.ldc.upenn.edu/LDC98S75) |
| otoSpeech full-duplex | 280 | 2026 | wideband | free | [otoearth/otoSpeech-full-duplex-280h](https://huggingface.co/datasets/otoearth/otoSpeech-full-duplex-280h) |
| Switchboard-1 | 260 | 1993 | narrowband | paid | [LDC97S62](https://catalog.ldc.upenn.edu/LDC97S62) |
| AMI Meeting Corpus | 100 | 2006 | wideband | free | [AMI corpus](https://groups.inf.ed.ac.uk/ami/corpus/) |
| CALLHOME English | 56 | 1996 | narrowband | paid | [LDC97S42](https://catalog.ldc.upenn.edu/LDC97S42) |
| CALLFRIEND English | 52 | 1996 | narrowband | paid | [LDC2019S21 + LDC2020S08](https://catalog.ldc.upenn.edu/LDC2019S21) |

Open Yap 1K is the largest publicly available dataset of natural two-speaker English conversation licensed for commercial use. This comparison excludes non-commercial releases, scripted corpora and corpora assembled by diarising recorded media.

## Documentation

| File | What it answers |
|---|---|
| [`DATASHEET.md`](DATASHEET.md) | Who made this, how, from whom and what it should not be used for |
| [`docs/schema.md`](docs/schema.md) | Every field in the delivered archive |
| [`docs/archive-layout.md`](docs/archive-layout.md) | What a delivered archive looks like on disk |
| [`docs/measurement.md`](docs/measurement.md) | How each published figure is measured |
| [`docs/provenance.md`](docs/provenance.md) | Collection, consent and quality assurance |
| [`docs/access.md`](docs/access.md) | How to request the corpus and what you may do with it |
| [`docs/data-use-agreement.txt`](docs/data-use-agreement.txt) | The full-corpus contract |

Machine-readable equivalents live in [`data/`](data/): `corpus-stats.json`, `fields.json` and the JSON Schemas in `data/schema/`.

## Citation

```bibtex
@misc{openyap1k,
  title     = {Open Yap 1K: Channel-Separated English Natural Two-Speaker Conversations},
  author    = {The Agentic Data Company},
  year      = {2026},
  version   = {1.0},
  publisher = {The Agentic Data Company},
  url       = {https://theagenticdatacompany.com/open-yap-1k},
}
```

## Acknowledgements

Background-noise scores come from DNSMOS P.835 `sig_bak_ovr.onnx` from [Microsoft's DNS Challenge](https://github.com/microsoft/DNS-Challenge), licensed under CC BY 4.0.

We thank the 239 people who recorded these conversations and agreed to their release. The corpus is their voices.

---

<p align="center">
  <a href="https://theagenticdatacompany.com/"><strong>The Agentic Data Company</strong></a><br>
  <a href="https://discord.gg/PBvuZQfgw9">Discord</a> ·
  <a href="https://github.com/The-Agentic-Data-Co">GitHub</a> ·
  <a href="https://huggingface.co/TheAgenticDataCompany">Hugging Face</a> ·
  <a href="https://www.linkedin.com/company/theagenticdataco/">LinkedIn</a>
</p>
