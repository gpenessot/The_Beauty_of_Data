# ERA5 Temperature Visualization Project

This project visualizes global temperature trends using ERA5 climate data. It creates a compelling lollipop plot to illustrate maximum daily temperatures from 1940 to the present.

## Project Structure

```
.
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   ├── preprocess_data.py
│   └── lollipop.py
├── img/
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```
   git clone git@github.com:gpenessot/The_Beauty_of_Data.git
   cd The_Beauty_of_Data
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the preprocessing script:
   ```
   python scripts/preprocess_data.py
   ```
   This will download the ERA5 data and process it.

2. Generate the visualization:
   ```
   python scripts/lollipop.py
   ```
   The resulting plot will be saved in the `img/` directory.

## Data

The raw ERA5 data is downloaded from the Copernicus Climate Change Service (C3S). Processed data is stored in the `data/processed/` directory.

## Visualization

The project uses Matplotlib to create a lollipop plot, showcasing temperature trends over time. Custom libraries (drawarrow, pyfonts, pypalettes) are used to enhance the visual appeal.

## Credits

This project draws inspiration from the work of Joseph Barbier. We gratefully acknowledge the use of his libraries:
- drawarrow
- pyfonts
- pypalettes

## License

[Include your chosen license here]

## Contact

[Your Name] - [Your Email]

Project Link: [https://github.com/your-username/era5-temperature-visualization](https://github.com/your-username/era5-temperature-visualization)