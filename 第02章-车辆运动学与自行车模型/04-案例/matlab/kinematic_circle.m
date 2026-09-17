thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
p = vehicle_params();

dt = 0.01; T = 12; v = 8; delta = deg2rad(15);
n = round(T/dt);
x = [0; 0; 0];
traj = zeros(3, n+1);
traj(:,1) = x;
for k = 1:n
    x = bicycle_euler(x, v, delta, dt, p.L);
    traj(:,k+1) = x;
end

R_th = p.L / tan(delta);
cx = 0; cy = R_th;
radii = hypot(traj(1,:) - cx, traj(2,:) - cy);
fprintf('theoretical R = %.3f m\n', R_th);
fprintf('simulated R mean = %.3f m, std = %.4f m\n', mean(radii), std(radii));
fprintf('relative radius error = %.2f %%\n', abs(mean(radii)-R_th)/R_th*100);

t = linspace(0, T, n+1);
figure;
subplot(1,2,1);
plot(traj(1,:), traj(2,:), 'k-'); hold on;
rectangle('Position', [cx-R_th, cy-R_th, 2*R_th, 2*R_th], 'Curvature', [1 1], 'LineStyle', '--');
axis equal; grid on;
xlabel('X (m)'); ylabel('Y (m)');
title('Open-loop kinematic bicycle');

subplot(1,2,2);
plot(t, rad2deg(unwrap(traj(3,:))), 'k-');
xlabel('t (s)'); ylabel('yaw (deg)'); grid on;
title('Yaw grows linearly at constant delta');
