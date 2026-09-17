thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
p = vehicle_params();
full = simulate_local(p, true, true);
nolka = simulate_local(p, true, false);
noacc = simulate_local(p, false, true);
print_m('full', full); print_m('no_LKA', nolka); print_m('no_ACC', noacc);
figure;
subplot(3,1,1); plot(full(:,1), full(:,5), 'k-', full(:,1), full(:,6), 'k--'); grid on; legend('ego','lead');
subplot(3,1,2); plot(full(:,1), full(:,4), 'k-'); grid on; ylabel('spacing');
subplot(3,1,3); plot(full(:,1), full(:,3), 'k-', nolka(:,1), nolka(:,3), 'Color',[0.5 0.5 0.5]); grid on;
legend('full','no LKA'); xlabel('t'); ylabel('ey');
sgtitle('Project A: ACC + LKA');

function print_m(name, rec)
fprintf('%s s_min=%.2f eyRMSE=%.3f\n', name, min(rec(:,4)), rms(rec(:,3)));
end

function rec = simulate_local(p, use_acc, use_lka)
dt = 0.02; T = 25; n = round(T/dt);
[Y0, ~] = path_at(0);
x = [0; Y0+0.4; 0]; v = 12; vp = 13; xp = 28; Lveh = 4.5;
rec = zeros(n,6);
for k = 1:n
    t = (k-1)*dt;
    if t < 10, ap = 0; elseif vp > 6, ap = -2.5; else, ap = 0; end
    s = xp - x(1) - Lveh;
    if use_acc
        sdes = 6 + 1.4*v;
        a = 0.25*(s-sdes) + 0.9*(vp-v);
        a = max(min(a,2),-5);
    else
        a = 0;
    end
    if use_lka
        [Yp, psip] = path_at(x(1));
        ey = x(2)-Yp;
        epsi = mod(psip - x(3) + pi, 2*pi) - pi;
        delta = epsi - atan(2.0*ey/(v+0.1));
        delta = max(min(delta, deg2rad(35)), -deg2rad(35));
    else
        delta = 0;
    end
    v = max(v + dt*a, 0.5);
    vp = max(vp + dt*ap, 0);
    xp = xp + dt*vp;
    x = bicycle_euler(x, v, delta, dt, p.L);
    rec(k,:) = [t, x(1), x(2)-path_at(x(1)), s, v, vp];
end
end

function [Y, psi] = path_at(X)
Y = 0.7*sin(2*pi*X/90);
dY = 0.7*(2*pi/90)*cos(2*pi*X/90);
psi = atan(dY);
end
