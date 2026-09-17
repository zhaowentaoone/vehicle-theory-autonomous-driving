thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
p = vehicle_params();

dt = 0.01;
Fx_max = 4000;
Fx_min = -p.m * 0.7 * p.g;
v = 0; x = 0; t = 0;
ts = t; vs = v; xs = x;
phase = 'accel';
t_100 = NaN; s_brake = NaN;
while t < 40
    if strcmp(phase, 'accel')
        Fx = Fx_max;
        if v >= 28
            phase = 'brake';
            s_brake = x;
        end
    else
        Fx = Fx_min;
    end
    Froll = p.m * p.g * p.fr;
    Faero = 0.5 * p.rho * p.Cd * p.Af * v * abs(v);
    ax = (Fx - Froll - Faero) / p.m;
    v = max(v + dt * ax, 0);
    x = x + dt * v;
    t = t + dt;
    ts(end+1) = t; vs(end+1) = v; xs(end+1) = x; %#ok<SAGROW>
    if isnan(t_100) && v >= 100/3.6
        t_100 = t;
    end
    if strcmp(phase, 'brake') && v <= 0.05
        break;
    end
end
fprintf('0-100 km/h time ≈ %.2f s\n', t_100);
fprintf('brake distance = %.1f m\n', xs(end) - s_brake);
figure;
subplot(2,1,1); plot(ts, vs*3.6, 'k-'); ylabel('km/h'); grid on;
subplot(2,1,2); plot(ts, xs, 'k-'); xlabel('t (s)'); ylabel('m'); grid on;
sgtitle('Longitudinal accel then brake');
