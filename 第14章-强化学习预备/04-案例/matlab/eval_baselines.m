thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
p = vehicle_params();
n_ep = 8;
stats = zeros(2,3); % return, steps, rmse
for kind = 1:2
    Gs = zeros(n_ep,1); Ns = Gs; Rs = Gs;
    for ep = 1:n_ep
        [G, n, rmse] = rollout_local(p, kind, 10+ep);
        Gs(ep)=G; Ns(ep)=n; Rs(ep)=rmse;
    end
    stats(kind,:) = [mean(Gs), mean(Ns), mean(Rs)];
end
fprintf('random return=%.2f steps=%.1f eyRMSE=%.3f\n', stats(1,:));
fprintf('PID    return=%.2f steps=%.1f eyRMSE=%.3f\n', stats(2,:));
figure; bar(stats(:,1)); set(gca,'XTickLabel', {'random','PID'});
ylabel('mean return'); title('Lane-keeping baselines'); grid on;

function [G, n, rmse] = rollout_local(p, kind, seed)
rng(seed);
dt = 0.05; v = 12; max_steps = 200;
ey0 = -0.5 + rand; epsi0 = -0.1 + 0.2*rand;
[Yp, psip] = path_at(0);
x = [0; Yp+ey0; psip+epsi0];
G = 0; eys = [];
for k = 1:max_steps
    [Yp, psip] = path_at(x(1));
    ey = x(2)-Yp;
    epsi = mod(x(3)-psip+pi,2*pi)-pi;
    if kind == 1
        delta = deg2rad(20)*(2*rand-1);
    else
        delta = -0.8*ey - 1.6*epsi;
    end
    delta = max(min(delta, deg2rad(35)), -deg2rad(35));
    x = bicycle_euler(x, v, delta, dt, p.L);
    r = -ey^2 - 0.5*epsi^2 - 0.05*delta^2 + 0.05;
    eys(end+1) = ey; %#ok<AGROW>
    if abs(ey) > 2.5
        r = r - 10; G = G + r; n = k; rmse = rms(eys); return;
    end
    G = G + r;
end
n = max_steps; rmse = rms(eys);
end

function [Y, psi] = path_at(X)
Y = 0.6*sin(2*pi*X/70);
dY = 0.6*(2*pi/70)*cos(2*pi*X/70);
psi = atan(dY);
end
