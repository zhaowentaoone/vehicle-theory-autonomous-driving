function x = bicycle_exact(x, v, delta, dt, L, delta_max)
if nargin < 6
    delta_max = deg2rad(35);
end
delta = max(min(delta, delta_max), -delta_max);
if abs(delta) < 1e-6
    x = bicycle_euler(x, v, 0, dt, L, delta_max);
    return;
end
X = x(1); Y = x(2); psi = x(3);
R = L / tan(delta);
dpsi = v * dt / R;
X = X + R * (sin(psi + dpsi) - sin(psi));
Y = Y + R * (-cos(psi + dpsi) + cos(psi));
psi = mod(psi + dpsi + pi, 2*pi) - pi;
x = [X; Y; psi];
end
