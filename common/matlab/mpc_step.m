function U = mpc_step(x, A, B, Q, R, N, umin, umax, dumax, u_prev)
n = size(A,1);
Phi = zeros(n*N, n);
Gamma = zeros(n*N, N);
Ap = eye(n);
for i = 1:N
    Ap = Ap * A;
    Phi((i-1)*n+1:i*n, :) = Ap;
    Acol = eye(n);
    for j = i:-1:1
        Gamma((i-1)*n+1:i*n, j) = Acol * B;
        Acol = Acol * A;
    end
end
Qb = kron(eye(N), Q);
H = Gamma' * Qb * Gamma + R * eye(N);
H = 0.5 * (H + H');
f = Gamma' * Qb * Phi * x(:);
lb = umin * ones(N,1);
ub = umax * ones(N,1);
% rate: |DU| <= dumax via linear inequalities
Aineq = zeros(2*N, N);
bineq = zeros(2*N, 1);
Aineq(1,1) = 1; bineq(1) = u_prev + dumax;
Aineq(2,1) = -1; bineq(2) = -u_prev + dumax;
for i = 2:N
    Aineq(2*i-1, i) = 1; Aineq(2*i-1, i-1) = -1; bineq(2*i-1) = dumax;
    Aineq(2*i, i) = -1; Aineq(2*i, i-1) = 1; bineq(2*i) = dumax;
end
opts = optimoptions('quadprog', 'Display', 'off');
try
    U = quadprog(H, f, Aineq, bineq, [], [], lb, ub, [], opts);
catch
    U = -H \ f;
    U = min(max(U, umin), umax);
end
if isempty(U)
    U = u_prev * ones(N,1);
end
end
