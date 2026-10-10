# Contributing

Contributions are welcome, especially:

- **Language review.** Native-speaker review of Kazakh and Arabic outputs. Open an issue with the
  *Language quality* template, quote the prompt and the answer, and suggest a correction.
- **Factual errors.** Wrong Azure permissions, limits or behaviours. Use the *Factual error* template
  and link the relevant Microsoft Learn page.
- **Pipeline improvements.** Filters, evaluation, new Azure topics.

## Development

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install ruff
ruff check .
bash -n pipeline/*.sh publish/*.sh
```

CI runs the same checks on every pull request.

## Rules

- Never commit tokens, keys or `kaggle.json`. CI runs a secret scan.
- Do not add real Microsoft certification exam questions.
- Derivative models must not use the QAZTECH name; see [TRADEMARK.md](TRADEMARK.md).
- By contributing you agree that your contribution is licensed under Apache-2.0.

Please follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
