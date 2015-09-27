# Hawk
This is a personal repository for small tools. It provides a `latexplot` function that changes the settings for PyPlot 
plots to fit Latex layout.

`latexplot` changes the setting for a plot to fit latex layout
The functions first argument is the size given as a ration of page width.
An optional keyword argument aspect_ratio ratio can be given.
```
#settings applies to all plots after this command
latexplot(ratio, aspect_ratio=(sqrt(5)-1.0)/2)

#setting only apply to the plot before the end
latexplot(ratio, aspect_ratio=(sqrt(5)-1.0)/2) do
	plot(1:10)
end
```

[![Build Status](https://travis-ci.org/dhoegh/Hawk.jl.svg?branch=master)](https://travis-ci.org/dhoegh/Hawk.jl)
