function [x, P] = kf_predict(x, P, A, Q)
x = A * x;
P = A * P * A' + Q;
P = 0.5 * (P + P');
end
