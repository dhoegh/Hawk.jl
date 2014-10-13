module Hawk
using PyCall
@pyimport Hawk as h

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
	h.latexplot(args...; kws...)
end
end # module
