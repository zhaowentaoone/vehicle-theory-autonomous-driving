thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
p = vehicle_params();
rng(2);
dt = 0.05; T = 20; n = round(T/dt);
x_true = [0;0;0]; v = 12;
x_hat = [0.5;-0.5;0.1]; P = diag([9,9,0.2]);
Q = diag([0.05,0.05,0.002])*dt; R = diag([4,4]);
C = [1 0 0; 0 1 0];
traj_t = zeros(2,n); traj_g = traj_t; traj_e = traj_t;
for k = 1:n
    delta = deg2rad(4)*sin(2*pi*(k-1)*dt/12);
    x_true = bicycle_euler(x_true, v, delta, dt, p.L);
    r_meas = v/p.L*tan(delta) + 0.02*randn;
    psi = x_hat(3);
    A = [1 0 -v*dt*sin(psi); 0 1 v*dt*cos(psi); 0 0 1];
    x_hat = x_hat + [v*dt*cos(psi); v*dt*sin(psi); r_meas*dt];
    P = A*P*A' + Q;
    y = x_true(1:2) + 2*randn(2,1);
    [x_hat, P] = kf_update(x_hat, P, y, C, R);
    traj_t(:,k)=x_true(1:2); traj_g(:,k)=y; traj_e(:,k)=x_hat(1:2);
end
fprintf('GNSS RMSE=%.3f  EKF RMSE=%.3f\n', ...
    sqrt(mean(sum((traj_g-traj_t).^2,1))), sqrt(mean(sum((traj_e-traj_t).^2,1))));
figure; plot(traj_t(1,:),traj_t(2,:),'k-', traj_g(1,:),traj_g(2,:),'.', traj_e(1,:),traj_e(2,:),'k--');
axis equal; grid on; legend('true','GNSS','EKF'); title('GNSS + yaw-rate EKF');
