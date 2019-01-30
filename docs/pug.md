# Pug 

First install:

```bash
conda install -c defaults -c conda-forge pypugjs
```
or
```bash
pip install pypugjs
```

See more: [pypugjs](https://github.com/kakulukia/pypugjs) and [pugjs](https://github.com/pugjs/pug).

Here is a simple example showing how to use Pug in Pandoctools via Knitty:  
(the code would be highlighted in the VSCode with language of the file set to pug - thanks to the space after <code>src = """ </code>)

```py
from pypugjs import simple_convert as pug
from IPython.display import HTML, Markdown


# %%
src = """ 

doctype html
html(lang="en")
  head
    title= pageTitle
    script(type='text/javascript').
      if (foo) bar(1 + 5)
  body
    h1 Pug - node template engine
    #container.col
      if youAreUsingPug
        p You are amazing
      else
        p Get on it!
      p.
        Pug is a terse and simple templating language with a
        strong focus on performance and powerful features.
"""
HTML(pug(src))
```
Output before `HTML()`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Pug</title>
    <script type="text/javascript">
      if (foo) bar(1 + 5)
    </script>
  </head>
  <body>
    <h1>Pug - node template engine</h1>
    <div id="container" class="col">
      <p>You are amazing</p>
      <p>Pug is a terse and simple templating language with a strong focus on performance and powerful features.</p>
    </div>
  </body>
</html>
```

Example where you can mix Pug with Markdown:

```py
Markdown(f"""
Some text with an icon: {pug('i.icon.checkmark')}
""")
```
Output before `Markdown()`:
```html
Some text with an icon: <i class="icon checkmark"></i>
```
