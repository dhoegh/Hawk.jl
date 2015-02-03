module Hawk
using PyCall
@pyimport importlib.machinery as machinery

#The pyimport is not used due to Hawk.py is not in path
loader = machinery.SourceFileLoader("test",abspath(joinpath(dirname(@__FILE__),"Hawk.py")))
Hawkpy = loader[:load_module]("test")


export @constants, latexplot
macro constants(exprs)
    for (i,exp) in enumerate(exprs.args)
        if exp.head==:(=)
            exprs.args[i] = Expr(:const,exp)
        end
    end
    return esc(exprs)
end

function latexplot(args...; kws...)
	Hawkpy[:latexplot](args...; kws...)
end

function latexplot(f::Function, args...; kws...)
	Hawkpy[:latexplot](args...; kws...)
    f()
    Hawkpy[:latexplot_reset]()
end

end # module
