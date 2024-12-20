# FunPlotter - A web app for plotting univariate functions

#### Video Demo: <https://youtu.be/R-DCsLx2c0w>

#### URL: <https://funplotter.pythonanywhere.com>

#### GitHub repo: <https://github.com/af0liveira/funplotter>

#### Description:

_FunPlotter_ is a single-page web app for plotting univariate functions on a
canvas.

The program is implemented in Python using Flask.
The interface is divided in 3 main parts:

1. A section with the forms for functions already included in the graph;
2. A form for inserting new functions;
3. A canvas for displaying the function curves.

In order to plot a new curve, the user needs for input a valid univariate
function and the lower an higher bounds of the function domain.
Function expressions are case insensitive and will only accept _x_ as variable.
Differentiation and integration can be used as well; e.g. 'integrate(x)' will
evaluate to 'x**2 / 2'.
Mathematical expressions can be used to define domain limits, e.g. 'pi *
exp(1)', as long as the expressions evaluate to unique values.

The input information is validated in the frontend and further processed in the
backed before being parsed using SymPy, which is also used in combination
with NumPy to generate the data for plotting the functions.

After processing the input, the plots are displayed with
[Chart.js](https://www.chartjs.org/) with an HTML canvas.

The app has been deployed on PythonAnywhere and is publicly accessible at
<https://funplotter.pythonanywhere.com>.

_FunPlotter_ has been developed as my final project for
[Harvard's CS50x 2024](https://cs50.harvard.edu/x/2024/).

#### Project structure

The project is organized as follows:

```txt
./
|-- README.md               : This file
|-- requirements.txt        : List for requirements, compatible with pip
|-- .env                    : Environment variables
|-- funplotter.py           : Main application file
`-- app/
    |-- __init__.py         : Definitions for running the app
    |-- config.py           : App configuratin file
    |-- forms.py            : Classes/functions for rendering input forms
    |-- parsers.py          : Routines for parsing user input data
    |-- routes.py           : Endpoints end logic for HTTP GET/POST methods
    |-- static/
    |   |-- chart.js        : Settings for Chart.js re graph properties
    |   `-- styles.css      : CSS custom definitions for app layout
    `-- templates/
        |-- index.html      : Main HTML file for (app interface)
        `-- partials/               : Specialized sections for the HTML
            |-- flash_msgs.html     : Layout for notification sections
            |-- functions.html      : Defines the form for adding new functions
            `-- new_function.html   : Defines the layout for plotted functions
```

Note that the `SECRET_KEY` -- and any other environment variables that might be
added in the future -- is defined in `.env` and loaded into the code using
'dotenv'.

#### Running the project locally

Assuming that you have a copy of the [GitHub
repo](https://github.com/af0liveira/funplotter), you should be able to run the
code locally as follows (make sure to run the command from the project's base
directory):

> Note:
> * The procedure below is meant for bash/zsh; other command shells might be
>   different.
> * This is not the only way to run the app; but it's the one I used. `;)`

1. (Optional, but recommended) Create a virtual environment using 'venv'

```console
$ python3.12 -m venv .venv      # create the virtual environment
$ source .venv/bin/activate     # activate the virtual environment 
```

2. Install the dependencies listed in `requirements.txt`

```console
$ pip install -r requirements.txt
[ output not shown here ]
```

3. Start the development server with 'flask'

```console
$ flask run
 * Serving Flask app 'funplotter.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

4. If all went well, the app can be opened in a webbrowser via
   <http://127.0.0.1:5000>.

---

