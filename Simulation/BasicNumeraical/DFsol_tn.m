function uxt = DFsol_tn(x,terms,U0,k,L)
%diffustion ���ѪR��(u(x,0)���`�ƨ�Ʈ�)
%u = 0 when n = even integer
uxt = @SolForT;
    function sol = SolForT(t)
        u = zeros(1,length(x));
        n = 1;
        for i = 1:terms
            lambda = n*pi/L;
            un = (4*U0/pi)*(exp(-(lambda)^2*k*t)*sin(lambda*x))/n;
            u = u + un;
            n = n + 2;
            sol = u;
        end
    end
end
