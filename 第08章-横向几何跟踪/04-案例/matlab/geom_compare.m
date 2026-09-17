thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
p = vehicle_params();
path = make_path_local();
v = 12; dt = 0.02; T = 18; n = round(T/dt);
% Pure Pursuit
x = [0; 1.2; 0]; idx = 1;
traj1 = zeros(3,n+1); e1 = zeros(1,n+1); traj1(:,1)=x;
for k = 1:n
    [delta, idx] = pure_pursuit_local(x, path, p.L, 2+0.3*v, idx);
    x = bicycle_euler(x, v, delta, dt, p.L);
    traj1(:,k+1)=x;
    i = nearest_local(x(1:2), path, idx);
    e1(k+1) = signed_ey_local(x(1:2), path(:,i), path(3,i));
end
% Stanley
x = [0; 1.2; 0]; idx = 1;
traj2 = zeros(3,n+1); e2 = zeros(1,n+1); traj2(:,1)=x;
for k = 1:n
    [delta, idx] = stanley_local(x, path, p.L, 2.2, v, idx);
    x = bicycle_euler(x, v, delta, dt, p.L);
    traj2(:,k+1)=x;
    i = nearest_local(x(1:2), path, idx);
    e2(k+1) = signed_ey_local(x(1:2), path(:,i), path(3,i));
end
fprintf('PP RMSE=%.3f  Stanley RMSE=%.3f\n', rms(e1), rms(e2));
t = linspace(0,T,n+1);
figure;
subplot(1,2,1); plot(path(1,:),path(2,:),'k--', traj1(1,:),traj1(2,:),'k-', traj2(1,:),traj2(2,:),'Color',[0.5 0.5 0.5]);
axis equal; grid on; legend('path','PP','Stanley'); xlabel('X'); ylabel('Y');
subplot(1,2,2); plot(t,e1,'k-', t,e2,'Color',[0.5 0.5 0.5]); grid on; xlabel('t'); ylabel('ey');
sgtitle('Geometric tracking');

function path = make_path_local()
ds = 0.5; R = 40;
xs = 0:ds:59.5; ys = zeros(size(xs)); ps = zeros(size(xs));
n_arc = round(0.5*pi*R/ds);
ang = linspace(0, 0.5*pi, n_arc);
xa = 60 + R*sin(ang); ya = R*(1-cos(ang)); pa = ang;
ys2 = (ya(end)+ds):ds:(ya(end)+120);
xs2 = xa(end) * ones(size(ys2));
ps2 = (pi/2) * ones(size(ys2));
path = [xs xa xs2; ys ya ys2; ps pa ps2];
end

function i = nearest_local(p, path, start)
i0 = max(start,1); i1 = min(size(path,2), i0+80);
d = hypot(path(1,i0:i1)-p(1), path(2,i0:i1)-p(2));
[~,j] = min(d); i = i0+j-1;
end

function ey = signed_ey_local(p, ppath, psi)
n = [-sin(psi); cos(psi)];
ey = n' * (p(:) - ppath(1:2));
end

function [delta, idx] = pure_pursuit_local(x, path, L, ld, idx)
idx = nearest_local(x(1:2), path, idx);
acc = 0; j = idx;
while j < size(path,2) && acc < ld
    acc = acc + hypot(path(1,j+1)-path(1,j), path(2,j+1)-path(2,j));
    j = j+1;
end
look = path(1:2,j);
dx = look(1)-x(1); dy = look(2)-x(2);
eta = cos(x(3))*dx + sin(x(3))*dy;
zeta = -sin(x(3))*dx + cos(x(3))*dy;
alpha = atan2(zeta, eta);
delta = atan2(2*L*sin(alpha), ld);
delta = max(min(delta, deg2rad(35)), -deg2rad(35));
end

function [delta, idx] = stanley_local(x, path, L, k, v, idx)
lf = L*1.2/2.8;
pf = x(1:2) + [cos(x(3)); sin(x(3))]*lf;
idx = nearest_local(pf, path, idx);
psi_p = path(3,idx);
ey = signed_ey_local(pf, path(:,idx), psi_p);
epsi = mod(psi_p - x(3) + pi, 2*pi) - pi;
delta = epsi - atan(k*ey/(v+0.1));
delta = max(min(delta, deg2rad(35)), -deg2rad(35));
end
