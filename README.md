# instruments

[![DOI](https://zenodo.org/badge/119964879.svg)](https://doi.org/10.5281/zenodo.19185605)

A database and plotting tool for tracking detector counts over time across far-infrared, sub-mm, and mm astronomy instruments.

![instruments.png](https://raw.githubusercontent.com/sr-cdf/instruments/master/instruments.png)

## Repository Contents

- **`instruments.csv`** — The database of instrument details, including detector types, counts, and references.
- **`instruments.py`** — A Python script that reads the CSV and generates the plot.
- **`instruments.png`** — The output plot, showing detector counts over time.

## Usage

To regenerate the plot after updating the database:

```bash
python instruments.py
```

## Data Accuracy

Some entries in the database are based on best estimates where conflicting values exist in the literature or where precise figures were not readily available. Corrections are very welcome — if you spot an error or have a more authoritative source, please open an issue or submit a pull request.

## Contributing

Contributions and corrections to the instrument database are welcome. To add or update an entry, modify `instruments.csv` and submit a pull request.

### Required fields

- `Instrument` — Name of the instrument.
- `Date` — Year of first light or deployment.
- `Detector_Type` — Must be either `Bolometer` or `KID`.
- `Detector_Subtype` — e.g. `TES`, `LEKID`, `MKID`, or another concise label.
- `Total_Detectors` — Total number of detectors.

### Recommended fields

Please fill in as many of the remaining columns as possible, and include a reference to the paper describing the instrument.

## Citation

If you use this software or the data contained in this repository, please see [`CITATION.cff`](CITATION.cff) for citation information.
