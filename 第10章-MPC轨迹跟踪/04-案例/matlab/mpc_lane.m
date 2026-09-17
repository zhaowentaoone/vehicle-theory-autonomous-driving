thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
p = vehicle_params();
v = 15; dt = 0.05; N = 12;
Ac = [0 v; 0 0]; Bc = [0; v/p.L];
A = eye(2)+Ac*dt; B = Bc*dt;
Q = diag([6,10]); R = 1.5;
dmax = deg2rad(8); dumax = deg2rad(4);
x = [0; 1.5; 0]; T = 20; n = round(T/dt);
traj = zeros(3,n+1); eys = zeros(1,n+1); traj(:,1)=x; u_prev = 0; sat=0;
for k = 1:n
    [Yp, psip] = path_at(x(1));
    ey = x(2)-Yp;
    epsi = mod(x(3)-psip+pi,2*pi)-pi;
    U = mpc_step([ey;epsi], A, B, Q, R, N, -dmax, dmax, dumax, u_prev);
    delta = U(1);
    if abs(abs(delta)-dmax) < 1e-4, sat = sat+1; end
    u_prev = delta;
    x = bicycle_euler(x, v, delta, dt, p.L);
    traj(:,k+1)=x;
    eys(k+1)=x(2)-path_at(x(1));
end
fprintf('RMSE ey=%.3f sat_frac=%.2f\n', rms(eys), sat/n);
Xs = linspace(0, traj(1,end), 200);
Ys = zeros(size(Xs));
for i = 1:numel(Xs)
    Ys(i) = path_at(Xs(i));
end
figure;
subplot(1,2,1); plot(Xs,Ys,'k--', traj(1,:),traj(2,:),'k-'); axis equal; grid on;
subplot(1,2,2); plot(linspace(0,T,n+1), eys, 'k-'); grid on;
sgtitle('Linear MPC lane keeping');

function [Y, psi] = path_at(X)
Y = 0.8*sin(2*pi*X/80);
dY = 0.8*(2*pi/80)*cos(2*pi*X/80);
psi = atan(dY);
end
