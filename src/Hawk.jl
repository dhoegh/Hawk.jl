module Hawk
using PyCall

filename = abspath(joinpath(dirname(@__FILE__),"Hawk.py"))

if PyCall.pyversion < v"3"
	@pyimport imp
	(path, name) = dirname(filename), basename(filename)
    (name, ext) = rsplit(name, '.', limit=2)

    (file, filename, data) = imp.find_module(name, [path])
    Hawkpy = imp.load_module(name, file, filename, data)
else
	@pyimport importlib.machinery as machinery
	#The pyimport is not used due to Hawk.py is not in path
	loader = machinery.SourceFileLoader("test",filename)
	Hawkpy = loader[:load_module]("test")
end


export @constants, latexplot

macro constants(exprs)
    for (i,exp) in enumerate(exprs.args)
        if exp.head==:(=)
            exprs.args[i] = Expr(:const,exp)
        end
    end
    return esc(exprs)
end

"`latexplot` changes the setting for a plot to fit latex layout
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
"
function latexplot(args...; kws...)
	Hawkpy[:latexplot](args...; kws...)
end

function latexplot(f::Function, args...; kws...)
	Hawkpy[:latexplot](args...; kws...)
    try
        f()
    finally
        latexplot_reset()
    end
end

function latexplot_reset()
    Hawkpy[:latexplot_reset]()
end

end # module
