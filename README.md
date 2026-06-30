# Journal submission figure package

This folder contains source-data tables and plotting scripts for the selected
human gut and musDD figures.

Structure:

- `figures/`: PNG and PDF outputs generated from the packaged CSV files.
- `source_data/`: one CSV source table per figure.
- `code/plot_scripts/`: one plotting script per figure plus the shared helper
  module `common.py`.
- `MANIFEST.csv`: mapping between each figure, source table and plotting script.
- `requirements.txt`: pinned plotting dependencies.

To regenerate all figures:

```bash
cd journal_submission_final
python code/plot_scripts/run_all.py
```

The plotting scripts use the CSV files in `source_data/` and write PNG/PDF
outputs to `figures/`.
