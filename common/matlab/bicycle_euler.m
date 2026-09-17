function x = bicycle_euler(x, v, delta, dt, L, delta_max)
if nargin < 6
    delta_max = deg2rad(35);
end
delta = max(min(delta, delta_max), -delta_max);
X = x(1); Y = x(2); psi = x(3);
X = X + dt * v * cos(psi);
Y = Y + dt * v * sin(psi);
psi = wrapToPi_local(psi + dt * v / L * tan(delta));
x = [X; Y; psi];
end

function a = wrapToPi_local(a)
a = mod(a + pi, 2*pi) - pi;
end
