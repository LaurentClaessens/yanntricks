pseudo_caption="<+Type your caption here+>"

to_be_checked_general_latex=r"""
\documentclass[a4paper,12pt]{article}

\usepackage{latexsym}
\usepackage{amsfonts}
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{bbm}		
\usepackage[cdot,thinqspace,amssymb]{SIunits}
\usepackage{pdfsync}

\usepackage{eso-pic}
\usepackage{pstricks}
\usepackage{pst-node}
\usepackage{pst-eucl}
\usepackage{pst-plot}
\usepackage{pst-math}
\usepackage{pst-func}
\usepackage{pstricks-add}
\usepackage{calc}
\usepackage{subfigure}
\usepackage{catchfile}
\usepackage{graphicx}


\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue}

\usepackage{textcomp}


\def\eA{\mathbbm{A}}
\def\eC{\mathbbm{C}}
\def\eH{\mathbbm{H}}
\def\eK{\mathbbm{K}} 
\def\eN{\mathbbm{N}}
\def\eQ{\mathbbm{Q}}
\def\eR{\mathbbm{R}}
\def\eZ{\mathbbm{Z}}
\newcommand{\mtu}{\mathbbm{1}}
\DeclareMathOperator{\SO}{SO}
\DeclareMathOperator{\pr}{\texttt{proj}}


\begin{document}

% Remember that launching the phystricks script with --tests do not create the .pstricks file.

Here are the figures to be manually checked.


XXXXXX

\end{document}
"""
