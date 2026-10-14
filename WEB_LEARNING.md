# CalBuddy web learning journal

## Milestone 1: a browser request and a Python response

A virtual environment keeps this project's packages separate from other projects.
Use `.venv-web` for the web app; the older `.venv` references a macOS installation.

From the project directory in PowerShell:

```powershell
python -m venv .venv-web
.\.venv-web\Scripts\python.exe -m pip install -r requirements-web.txt
.\.venv-web\Scripts\python.exe -m flask --app app:create_app run --debug
```

`-m` runs a module using the specified Python interpreter. `pip` installs the
packages listed in the requirements file. The Flask command imports `app.py`,
calls `create_app`, and starts a local development server. Debug mode reloads
changed code during local development.

Visit http://127.0.0.1:5000/ in your browser. Stop the server with Ctrl+C.

You can also run `app.py` with PyCharm's Run button using the `.venv-web`
interpreter, or run `.\.venv-web\Scripts\python.exe app.py` in PowerShell.
The `if __name__ == "__main__":` block starts the server when Python executes
this file directly. When the Flask command imports the file, that block does
not run; the command calls the factory and starts the server instead.
Keep the server running while using the page in your browser.

### Follow the request

1. The browser sends an HTTP GET request for `/`.
2. Flask finds the function registered with `@app.get("/")`.
3. The `home` function returns HTML, the language describing the page content.
4. Flask sends that HTML as a response and the browser displays it.

`Flask(__name__)` constructs the application. `__name__` identifies the Python
module so Flask can locate resources such as templates later. `create_app` is
an application factory: a function that creates an app. This will let us add
configuration and feature modules as CalBuddy grows.

The first version used HTML inside a Python string so the request cycle was
easy to follow. Milestone 2 moves that HTML to a Jinja template.
The existing terminal application still starts with `main.py`.

### Try it yourself

Change the paragraph in `templates/home.html` to a message of your own, save, and refresh.
Before trying `/meals` in the browser, predict the result: we have only
registered `/`. What does Flask send when no route matches?

## Milestone 2: templates and Python values

A template is page content with places for supplied values. Flask uses Jinja,
a template engine, to produce HTML from templates. By default, Flask looks
for these files in a `templates` folder beside the application module.

Our route now calls:

```python
return render_template("home.html", greeting="Welcome to CalBuddy!")
```

`render_template` is a function imported from Flask. The first argument chooses
the template. The keyword argument supplies a value named `greeting` to that
template; it is not a setting or a special Flask keyword.

In `templates/home.html`, `<h1>{{ greeting }}</h1>` inserts that supplied value
inside a heading. Jinja runs on the server. The browser receives the completed
HTML, such as `<h1>Welcome to CalBuddy!</h1>`, rather than the Jinja expression.
For HTML templates, Jinja escapes ordinary string values by default so they are
displayed as text rather than interpreted as HTML markup.

This keeps the route's request-handling work separate from page structure.
Other Flask projects can use the same folder and rendering pattern.

### Follow the new request

Browser requests `/` → Flask calls `home()` → `render_template` loads
`home.html` → Jinja substitutes `greeting` → Flask sends HTML → browser displays it.

### Try it yourself

1. Change the `greeting` value in `app.py`, save, and refresh the browser.
2. Change the paragraph text in `templates/home.html`, save, and refresh.
3. Explain which change affected a Python-supplied value and which affected the
   page's HTML directly. Bootstrap styling comes after this distinction is clear.

## Milestone 3: viewing real meals

`meal_routes.py` groups meal routes using a Flask Blueprint. A blueprint records
related routes; `create_app` attaches them with `app.register_blueprint(meals_bp)`.
The blueprint name `meals` prefixes endpoint names, so `list_meals` is known to
Flask as `meals.list_meals`. An endpoint is a route's internal name, not its URL.

When the browser requests `/meals`, the `list_meals` function retrieves active
meals through `crud.get_active_meals` and passes the returned list to the template:

```python
return render_template("meals.html", meals=meals, error=None)
```

The left `meals` names the template variable; the right `meals` refers to the
local Python variable holding the database results. Each list element is a
dictionary with keys such as `name`, `calories`, and `protein_g`.

In the template, `{% for meal in meals %}` repeats its contents for each meal.
`{{ meal['name'] }}` inserts a dictionary value. `{% endfor %}` ends the loop.
Use `{{ ... }}` to output a value and `{% ... %}` for instructions such as loops
and conditions. Jinja executes these instructions on the server.

HTML `table` contains a header (`thead`) and body (`tbody`). `tr` is a row, `th`
is a header cell, and `td` is a data cell. The loop creates one body row per meal.
Bootstrap's `table` and `table-striped` classes style the table, while a
`table-responsive` wrapper allows horizontal scrolling on narrow screens.

`{% if error %}`, `{% elif meals %}`, and `{% else %}` select the error, populated,
or empty state. `raise_on_error=True` asks the existing CRUD function to signal
failures with a Python exception; its default behavior for the terminal app is
unchanged. The route catches that exception and returns a friendly message with
HTTP status 503 (service unavailable), rather than reporting an empty database.
`current_app` provides access to the application handling the request so we can
log technical details to its console. HTTP status 200 means a successful response.

`url_for('meals.list_meals')` builds a URL using an endpoint name. In templates,
Flask makes `url_for` available automatically. The HTML `a` element is a link;
its `href` identifies the destination. Styling a link as a Bootstrap button
does not turn it into a form submission.

### Try it yourself

Visit `/meals` or click View meals from the home page. Find the Jinja loop and
trace one meal from the Python list to the corresponding HTML row. Add a second
meal in the terminal app and refresh the page. Explain why no extra HTML row
needs to be written by hand.
