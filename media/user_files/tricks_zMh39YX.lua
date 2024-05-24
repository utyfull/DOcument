conf = {
   N="A84.J9542.J92.76",    -- fix N hand
   num=1000                  -- finish after accepting 100 deals
}

-- accept only the deals in which S has 1NT opening:
function filter()
    --S:nt(15, 15)
    --S:spades()==4
    return S:clubs() >= 5 and S:hcp_in_range(18,20) and S:spades() == 4
	   and S:hearts() == 3
end

-- for each accepted deal, calculate number of tricks in NT by S:
function stats()
    local t = tricks(N, "H")
    count("N by N, number of tricks", t)
    count("chance to win 4H by S", t >= 10)
end
