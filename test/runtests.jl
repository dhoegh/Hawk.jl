using Hawk
using Base.Test

@constants begin
    a=10
end

@test isconst(:a)
