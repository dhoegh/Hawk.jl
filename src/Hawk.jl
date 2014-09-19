module Hawk

export @constants
macro constants(exprs)
    con=symbol("const")
    for (i,exp) in enumerate(exprs.args)
        if exp.head==:(=)
            out = Expr(con)
            push!(out.args,:($exp))
            exprs.args[i] = out
        end
    end
    return esc(exprs)
end

end # module
