# Convenient and easily tweakable Atom+Markdown+Pandoc+Jupyter experience (can export to ipynb)

# (R Markdown alternative)

Assume you want Jupyter notebook experience but in IDE like Atom/Visual Studio Code.

So you either write markdown document with insertions of python code blocks. You can run these code blocks via Atom's Hydrogen package and instantly see their results. 

Or you write Hydrogen .py file split by `# %%` separator into cells. You can run these cells via Hydrogen and instantly see results. You even can edit this file in PyCharm studio as it's a valid python (unless you use magics).

If you want to convert this document to some output format (html/pdf/ipynb) and send to other people then you use [Pandoctools](https://github.com/kiwi0fruit/pandoctools). It can convert both .md and .py files described above to valid mardown, or valid ipynb, or html,  or pdf (but default pandoc templates are not what I like).

And Pandoctools not just converts - it gives you ability to tweak and tune the process of conversion the way you like. Then save this conversion algorithm as profile and reuse it. It's really convenient to use Pandoc with it's filters for this task - or even use simple CLI pipe text filters.

And you write conversion algorithm in bash script - the best language for this task as it can easily glue and combine text filters written in any language (as long as they have command line interface).

So in the proposed tool chain you:

* Write Markdown in Atom (with all available packages that help much),
* Insert Jupyter code cells and deploy via Hydrogen,
* Apply any Pandoc or text filters via [Pandoctools](https://github.com/kiwi0fruit/pandoctools) to convert to markdown/html/pdf/ipynb,
    * Pandoctools lets you define text filters pipelines ("profiles") and apply them to any file by simply adding two lines to markdown metadata section and opening the file with Pandoctools. You define text conversion algorithm once and then just use it with few 'Open with' clicks (or even with one short key with Atom package).
    * Collecting Jupyter cells outputs is also a Pandoc filter,
    * There are even working cross-references in exported ipynb,
    * Can convert markdown to markdown in order to post-convert with existing tools,
    * Optionally write math in SugarTeX that is a more readable LaTeX language extension and a transpiler to LaTeX.

[**Example doc**](https://github.com/kiwi0fruit/pandoctools/blob/master/examples): from markdown with Jupyter python code blocks, SugarTeX math and cross-references to ipynb notebook.

See more about all mentioned tools in [Pandoctools repo](https://github.com/kiwi0fruit/pandoctools).

There are also recommendations of nice Atom packages and even good open-source font fallback chains for Unicode-rich markdown documents (monospace for editor, serif/sans for output).

**UPD**

Worth noting that there is another way of joining plain markdown documents with Jupyter notebooks: storing Jupyter notebooks in markdown format - you still use Jupyter but have another content manager (or something). [notedown, podoc and ipymd](https://gist.github.com/mrtns/da998d5fde666d6da26807e1f246246e) go this way.

Another way is to abandon writing code in Jupyter (I myself find it frustrating) and write it in Atom editor with Hydrogen package. But then the question of export to ipynb arises. And Pandoctools solves this problem.

And even more! It's shell pipelines allow you to add custom text transformations and leverage pandoc filters. So for example I added SugarTeX filter because I didn't liked how LaTeX insertions look alien in Markdown (I guess it's because of low readability of LaTeX - both Python and Markdown are very readable languages).


## [Some discussion on Reddit](https://www.reddit.com/r/IPython/comments/8mfx8o/convenient_and_easily_tweakable/)
