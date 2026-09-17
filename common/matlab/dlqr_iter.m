function K = dlqr_iter(A, B, Q, R)
P = Q;
for i = 1:400
    K = (R + B' * P * B) \ (B' * P * A);
    Pnew = A' * P * A - A' * P * B * K + Q;
    if norm(Pnew - P, 'fro') < 1e-10
        P = Pnew; break;
    end
    P = 0.5 * (Pnew + Pnew');
end
K = (R + B' * P * B) \ (B' * P * A);
end
