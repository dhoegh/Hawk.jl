module Hawk

export @constants
macro constants(exprs)
    for (i,exp) in enumerate(exprs.args)
        if exp.head==:(=)
            exprs.args[i] = Expr(:const,exp)
        end
    end
    return esc(exprs)
end

end # module
