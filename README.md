# Language Workbench Competition 2025 - textX Solution

This solution implements the [LWC2025
assignment](https://github.com/judithmichael/lwb25) using
[textX](https://github.com/textX/textX/).

To run this solution follow these steps:

1. This solution uses Nix for reproducible dev. environments. Install
   [Nix](https://nixos.org/download/) and enable flake feature by adding
   `experimental-features = nix-command flakes` to `~/.config/nix/nix.conf`. See
   more [here](https://nixos.wiki/wiki/flakes)

1. Clone the repository:

   ``` sh
   git clone git@github.com:igordejanovic/lwc2025.git
   cd lwc2025
   ```

1. Create dev environment with nix:

   ``` sh
   nix develop
   ```

   After nix finishes you will be in a bash shell with everything installed and setup.
   
   Tip: you can automate this step using [direnv tool](https://direnv.net/).

1. Generate questionnaire for the tax example:

   ``` sh
   textx generate --target web examples/tax.ql -o tax --overwrite
   ```
   This will run textX generator registered for QL language and web target.
   The app will be generated in the `tax` folder.

1. Install runtime dependencies for the app and run it:

   ``` sh
   cd tax
   npm install
   npm run dev
   ```
   The app will be available at the displayed URL with hot-reloading.

1. Go to displayed address in your browser and play with the example. Open
   `examples/tax.ql` file in your editor and change it, regenerate code (step
   4). The app hot-reloads automatically in the browser as long as you kept vite
   running in the background (`npm run dev` command).

# Questionnaire language

See examples in the `examples` folder.

What is implemented currently:

- Language:
  - [x] Each question can be either a field with declared type (types are
        `boolean`, `integer`, `money`, `string`, `date`) or an expression where
        the type will be inferred.
  - [x] Optional ranges for types where it makes sense with type checking.
  - [x] Optional default values with type check.
  - [x] Questions can be nested inside if blocks of the form (`if <condition> {
        ... }`) with semantics that nested questions are shown to the user only
        if condition is satisfied.
  - [x] Expressions support usual logical/math operation as well as if/then/else
        expressions (`if <cond> then <expression> else <expression>`).
  - [x] Type checking: all operations are type checked and errors are reported
        if operation doesn't make sense for the operand types.
  - [x] Topological sorting and calculating dependent expressions in the correct order.
  - [x] Cycle check: question expressions can reference other questions. If the loop
        is formed it will be reported as error.
  - [ ] Determinism: support for same question in multiple if branches and check
        that the question will show only once in each possible run.
  - [ ] Styling language

- Generator/runtime:
  - [x] textX generator which transforms .ql files to React implementation
  - [x] Hiding/showing elements of the form when dependent questions are not
        defined (not answered or not visible)
  - [x] Auto-calculation of dependent expression fields on each change.
  - [x] Save form data to JSON including only fields/questions which are
        answered.
  - [ ] Ranges checking
  - [ ] Default values support


# Key parts of implementation

textX fosters modular architecture where each language/generator can be
developed as a separate Python project and installed separately. textX will
dynamically discover languages and generators installed in the Python
environment. Languages and generators can be listed in CLI by `textx
list-languages` and `textx list-generators` commands.

textX project [textx-lang-ql](./textx-lang-ql/) implements the QL language. If
installed in the environment it will be visible by textX:

``` sh
> textx list-languages
txcl (*.txcl)                 textx-gen-coloring[0.2.0]               A language for syntax highlight definition.
questlang (*.ql)              textx-lang-ql[0.1.0]                    Questionnaire Language in textX - LWC 2025
textX (*.tx)                  textX[4.2.1]                            A meta-language for language definition
```

The key part of the implementation is [the textX grammar of the
language](./textx-lang-ql/questlang/questlang.tx)

Topological sorting and cycle detection is implemented in [kahn
module](./textx-lang-ql/questlang/kahn.py). Type checking is done in [types
module](./textx-lang-ql/questlang/types.py) and general form processing/checking
is done in [form](./textx-lang-ql/questlang/form.py) module.

Generator is implemented in [textx-gen-ql-web project](./textx-gen-ql-web) using
textx-jinja package which is support for Jinja2 template engine based generation
for textX generator projects. When installed in the environment it will be
visible by textX:

``` sh
> textx list-generators
questlang -> web              textx-gen-ql-web[0.1.0]       Generator for generating web from questlang descriptions
textX -> vscode               textx-gen-vscode[0.2.1]       Generating VS Code extension for installed textX projects.
textX -> textmate             textx-gen-coloring[0.2.0]     Generating textmate syntax highlighting from textX grammars
textX -> dot                  textX[4.2.1]                  Generating dot visualizations from textX grammars
textX -> PlantUML             textX[4.2.1]                  Generating PlantUML visualizations from textX grammars
any -> dot                    textX[4.2.1]                  Generating dot visualizations from arbitrary models
```

Any registered generator can be called through `textx generate` command like
shown in the first section above.


# Editor

Although any editor can be used you can use textX VS Code extension which
provides editor services for all textX based languages (syntax highlight, inline
error reporting and basic folding and completion).

To run the editor follow these steps:

1. Install textX extension (soon this version will also be available at the VS Code marketplace).

   ``` sh
   # From the project root
   code --extensions-dir vscode-extensions --install-extension textX-0.3.0.vsix
   ```

1. Run VS Code withing the project folder.

   ``` sh
   code --extensions-dir vscode-extensions .
   ```

1. Right-click `pyproject.toml` in `textx-lang-ql` folder and select "Install textX project".
1. Open any example from the `examples` folder. It should be highlighted and
   errors should be reported. Also, basic generic VS Code folding and completion
   is available.
   
**Note:** textX uses PEG parsing without error recovery so only the first syntax
error is reported until it is fixed after which next error is reported if exists
and so on.
   
**Tip:** Editor highlighting and error reporting refreshes dynamically on grammar
change. Try to change `questlang.tx` grammar and observe `tax.ql` editor
changes. This can be of great help during a new language prototyping.
   

# Metrics

Implementation LOC calculated using [cloc tool](https://github.com/AlDanial/cloc).

- QL language:
  ```
   $ cloc --read-lang-def=textx-cloc-defs.txt ./textx-lang-ql/questlang
   -------------------------------------------------------------------------------
   Language                     files          blank        comment           code
   -------------------------------------------------------------------------------
   Python                           5             76             47            265
   textX grammar                    1             23              4             79
   -------------------------------------------------------------------------------
   SUM:                             6             99             51            344
   -------------------------------------------------------------------------------
  ```

- QL Web (React) generator:

  ```
  $ cloc ./textx-gen-ql-web/qlweb --include-lang=python,jsx,"jinja template",javascript,typescript,html   -------------------------------------------------------------------------------
   -------------------------------------------------------------------------------
   Language                     files          blank        comment           code
   -------------------------------------------------------------------------------
   Jinja Template                   2             24              0            219
   JSX                              5             13              0            156
   Python                           2             34             23            144
   JavaScript                       2              3              1             37
   TypeScript                       1              2              0             23
   HTML                             1              0              0             13
   -------------------------------------------------------------------------------
   SUM:                            13             76             24            592
   -------------------------------------------------------------------------------
  ```

## Key Technologies

- [textX](https://github.com/textX/textX/) - Language engineering framework
- [textX-LS](https://github.com/textX/textX-LS/) - Language Server Protocol and
  VS Code extension for textX
- [React](https://reactjs.org/) + [MUI](https://mui.com/) - Web runtime - generated code target
