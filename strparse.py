import re
from argparse import ArgumentParser

def demacro(text: str) -> str:
    replacements: dict[str, str] = {
        r"\ii ": r"\item ",
        r"\ii[": r"\item[",
        r"\wh": r"\widehat",
        r"\wt": r"\widetilde",
        r"\ol": r"\overline",
        r"\epsilon": r"\varepsilon",
        r"\eps": r"\varepsilon",
        r"\dang": r"\measuredangle",
        r"\dg": r"^{\circ}",
        r"\inv": r"^{-1}",
        r"\half": r"\frac{1}{2}",
        r"\GL": r"\operatorname{GL}",
        r"\SL": r"\operatorname{SL}",
        r"\NN": r"{\mathbb N}",
        r"\ZZ": r"{\mathbb Z}",
        r"\CC": r"{\mathbb C}",
        r"\RR": r"{\mathbb R}",
        r"\QQ": r"{\mathbb Q}",
        r"\FF": r"{\mathbb F}",
        r"\ts": r"\textsuperscript",
        r"\opname": r"\operatorname",
        r"\defeq": r"\overset{\text{def}}{=}",
        r"\id": r"\operatorname{id}",
        r"\ord": r"\operatorname{ord}",
        r"\sign": r"\operatorname{sign}",
        r"\injto": r"\hookrightarrow",
        r"\vdotswithin=": r"\vdots",
    }
    
    keys = sorted(replacements, key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(key) for key in keys))

    text = pattern.sub(lambda m: replacements[m.group()], text)

    text = text.replace("``", '"')

    return text

def remove_soft_newlines(text: str) -> str:
    return re.sub(
        r"[a-zA-Z]\n[a-zA-Z]",
        lambda m: m.group(0).replace("\n", " "),
        text,
    )

def toAOPS(text: str) -> str:
    DIVIDER = "\n" + r"-------------------" + "\n\n"

    text = demacro(text)

    text = re.sub(r"(?m)(?<!\\)%.*$", "", text)
    text = text.replace(r"\%", "%")

    text = text.replace(r"\qedhere", "")

    text = text.replace(r"\begin{asy}", "\n[asy]\n")
    text = text.replace(r"\end{asy}", "\n[/asy]")

    text = text.replace(r"\begin{center}", "")
    text = text.replace(r"\end{center}", "")

    text = text.replace(r"\par ", "\n")

    text = text.replace(r"\item ", "[*]")
    text = text.replace(r"\begin{enumerate}", "[list=1]")
    text = text.replace(r"\end{enumerate}", "[/list]")
    text = text.replace(r"\begin{itemize}", "[list]")
    text = text.replace(r"\end{itemize}", "[/list]")
    text = text.replace(r"\begin{description}", "[list]")
    text = text.replace(r"\end{description}", "[/list]")

    for env in [
        "theorem",
        "claim",
        "lemma",
        "proposition",
        "corollary",
        "definition",
        "remark",
    ]:
        label = env.title()

        text = re.sub(
            rf"\\begin\{{{env}\*?\}}(?:\[([^\]]*)\])?",
            lambda m: (
                "\n\n"
                + "[b][color=red]"
                + label
                + (f": {m.group(1)}" if m.group(1) else ":")
                + "[/color][/b] "
            ),
            text,
        )

        text = text.replace(rf"\end{{{env}*}}", "")
        text = text.replace(rf"\end{{{env}}}", "")
    text = text.replace(r"\begin{proof}", "[i]Proof.[/i] ")
    text = text.replace(r"\end{proof}", r"$\blacksquare$" + "\n")

    text = text.replace(r"\bigskip", DIVIDER)
    text = text.replace(r"\medskip", DIVIDER)

    text = text.replace(r"\#", "#")

    text = re.sub(
        r"opacity\(0\.[0-9]+\)+([^,]+), ",
        "invisible, ",
        text,
    )

    text = re.sub(
        r"\\emph{([^}]*)}",
        r"[i]\1[/i]",
        text,
    )
    text = re.sub(
        r"\\textit{([^}]*)}",
        r"[i]\1[/i]",
        text,
    )
    text = re.sub(
        r"\\textbf{([^}]*)}",
        r"[b]\1[/b]",
        text,
    )

    text = re.sub(
        r"\\paragraph{([^}]*)}",
        DIVIDER + r"[color=blue][b]\1[/b][/color]",
        text,
    )
    text = re.sub(
        r"\\subparagraph{([^}]*)}",
        DIVIDER + r"[b]\1[/b]",
        text,
    )

    text = re.sub(
        r"\\url{([^}]*)}",
        r"[url]\1[/url]",
        text,
    )
    text = re.sub(
        r"\\href{([^}]*)}{([^}]*)}",
        r"[url=\1]\2[/url]",
        text,
    )

    text = re.sub(
        r"\\item\[([^\]]*)\]",
        r"[*] [b]\1[/b]",
        text,
    )

    text = text.replace(r"\arc", r"\widehat")

    text = re.sub(
        r"\\oveq{([^}]*)}",
        r"\\overset{\1}{=}",
        text,
    )

    return remove_soft_newlines(text)


def main() -> None:
    parser = ArgumentParser(
        description="Convert LaTeX to AoPS."
    )

    parser.add_argument(
        "input_file",
        help="Path to the input file to be processed.",
    )

    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as f:
        data = f.read()

    output = toAOPS(data)
    print(output, end="")


if __name__ == "__main__":
    main()
