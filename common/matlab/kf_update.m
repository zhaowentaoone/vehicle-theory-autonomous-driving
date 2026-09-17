function [x, P, K] = kf_update(x, P, y, C, R)
K = (P * C') / (C * P * C' + R);
x = x + K * (y - C * x);
P = (eye(size(P)) - K * C) * P;
P = 0.5 * (P + P');
end
