# Getting the corpus

## The free sample

Published on the Hugging Face Hub at [TheAgenticDataCompany/open-yap-1k](https://huggingface.co/datasets/TheAgenticDataCompany/open-yap-1k).
Accept the terms on the dataset page, then:

```bash
pip install -r tools/requirements.txt
python tools/download_sample.py
```

CC-BY-4.0, with a rider: you may not attempt to identify a speaker, and you
may not build voice clones identifiable as a speaker in the corpus. Training
a general model alongside other data is fine — the rider is about targeting
an individual. Full text in [`../LICENSE-SAMPLE.txt`](../LICENSE-SAMPLE.txt).

## The full corpus

Request it at https://theagenticdatacompany.com/open-yap-1k. Three steps:

1. **Request.** Tell us who you are and what you want it for.
2. **Review.** We read it and reply.
3. **Delivery.** Approved recipients get a portal account, and either a
   direct download or delivery into their own S3 bucket.

It is offered under the Open Yap 1K Data Use Agreement (v1), which is
a contract you accept when you request it. Accepting the sample's licence
does not grant this one, and vice versa.

### What it permits

- Commercial use, including in products you sell
- Research use, published or internal
- Training, fine-tuning and evaluating models, and deploying what you train
- Internal copies, and access for staff and contractors under the same terms
- Retaining the delivered dataset, and anything derived from it, after a speaker withdraws

### What it prohibits

- Redistributing, resharing, sublicensing or reselling the dataset or any part of it
- Attempting to identify a speaker, or link a recording to any external record
- Creating voice clones, replicas or generative reproductions identifiable as a speaker in the corpus
- Holding the dataset under weaker controls than your own confidential material
- Retaining any copy of the dataset after a breach of these terms, or after a written request from The Agentic Data Company

This summary is not the agreement. The agreement is
[`../LICENSE-CORPUS.txt`](../LICENSE-CORPUS.txt), in full, and it governs.
