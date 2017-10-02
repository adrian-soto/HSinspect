# HSinspect

Predictive model for health and safety inspections in the USA. It is based in data from the Occupational Health and Safety Administration, curated by Enigma public

  https://public.enigma.com/browse/occupational-safety-and-health-administration-osha/98fa73e5-f974-4c46-8419-8010543c3cd2
  
The model is based on the random forest algorithm and it predicts both the outcome of a violation and its probability.

## Getting Started

This Python code:
1) creates the SQL database
2) trains and validates the model, optimizing hyperparameters
3) evaluates its performance
4) creates maps of violations by US state

### Prerequisites

This code is Python 2.7 and relies on the following packages:
- numpy
- matplotlib
- pandas
- postgresql
- sqlalchemy
- psycopg2
- basemap

Please ensure these packages are installed before attempting to run this code


## Authors

* **Adrián Soto**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* OSHA for collecting the data
* Enigma Public for releasing the data
* The almighty Stack Overflow community since the code in map/ is a modification of
    https://stackoverflow.com/questions/39742305/how-to-use-basemap-python-to-plot-us-with-50-states

